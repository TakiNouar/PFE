"""Gate S1 (spec 14): the fitted simplified cells against Feng's cells, measured by simulation.

Runs on GeNN's exact CPU backend in double precision (the checking mode, spec 14 section 2), with
Block A's protocols and measurement methods:
  passive    -0.05 nA for 1 s after 1 s, then 1 s of recovery: resting potential, input resistance,
             63 % rise time and slowest time constant (Rall's peeling, 40 % -> 10 % of the recovery)
  ladder     1 s steps at 0.1 ... 1.5 nA: spike counts and first-spike latencies
  long       4 s steps at 0.4 and 1.0 nA: counts; PN-A gaps between spikes
  noise      Feng's background noise only, 60 s after 2 s: rates and ISI CV (20 cells per type)
  drive      Feng's afferent trains on the PN dendrite + noise, 20 s after 2 s (16 cells x 3 noise
             draws), the same trains, weights and delays as Feng's run (drive_test_inputs.npz)
Targets: Block A (single_cells_full.json, passive_tau.json) and the sharper Feng reference for noise
and drive (stage2_reference.json). Tolerances: spec 14 S1; the 63 % rise time is reported only
(a passive two-compartment cell is always faster there than Feng's, whose Ih slows it).

Usage (from Simulations/BLA/simplified, in with_gpu_env.cmd): <venv python> -m bla_simple.cell_check
Writes outputs/S1_cells.json and S1_cells.png.
"""
import json

import numpy as np

from .fit_cells import (DT, LADDER_MS, LONG_MS, SETTLE, Harness, Stage2Harness, block_a, pn_protocols,
                        pn_values, spikes_by_cell, stage2_measures)
from .paths import CONFIG_DIR, OUTPUT_DIR

BACKEND = "single_threaded_cpu"
TOL = {"vrest_mV": 1.0, "rin": 0.10, "tau": 0.10, "count": 0.10, "count_abs_below_10": 1, "latency": 0.10,
       "pn_a_gap": 0.15, "rate": 0.15, "cv": 0.10}


def load_params():
    p = json.loads((CONFIG_DIR / "cells_fitted.json").read_text(encoding="utf-8"))
    pn = dict(p["PN"]["params"]["shared"])
    pn.update({f"{k}_A": v for k, v in p["PN"]["params"]["PN_A"].items()})
    return pn, dict(p["FSI"]["params"])


def passive_measures(t, v, t_on, t_off, amp):
    vrest = v[(t >= t_on - 100) & (t < t_on)].mean()
    v_ss = v[(t >= t_off - 50) & (t < t_off)].mean()
    dv = v_ss - vrest
    on = (t >= t_on) & (t < t_off)
    t63 = float(t[on][np.argmax((v[on] - vrest) <= 0.632 * dv)] - t_on)
    after = t >= t_off
    rel = (v[after] - vrest) / dv
    i0, i1 = np.argmax(rel <= 0.4), np.argmax(rel <= 0.1)
    tau0 = float(-1.0 / np.polyfit(t[after][i0:i1], np.log(rel[i0:i1]), 1)[0])
    return {"vrest_mV": float(vrest), "rin_MOhm": float(dv / amp), "t63_ms": t63, "tau_slow_ms": tau0}


def run_passive(kind, values, n):
    """Simulate the passive protocol and record the soma voltage of every cell."""
    h = Harness(kind, n, 3000.0, backend=BACKEND, name=f"s1_passive_{kind}")
    vals = dict(values, Iamp=np.full(n, -0.05), Ton=np.full(n, 1000.0), Toff=np.full(n, 2000.0),
                noise_on=np.zeros(n))
    m = h.model
    m.load(num_recording_timesteps=h.steps)
    h.loaded = True
    from .cells import initial_state
    st = initial_state(kind, 0.0)
    for name in list(vals) + list(st):
        arr = (np.asarray(vals[name], float) if name in vals else
               np.asarray(vals.get("ELd", vals["EL"]), float) if name in ("V", "Vd") else np.full(n, st[name]))
        h.pop.vars[name].view[:] = arr
        h.pop.vars[name].push_to_device()
    trace = np.zeros((h.steps, n))
    for i in range(h.steps):
        m.step_time()
        h.pop.vars["V"].pull_from_device()
        trace[i] = h.pop.vars["V"].view
    h.close()
    return (np.arange(h.steps) + 1) * DT, trace


def count_ok(n, n_t):
    return abs(n - n_t) <= (TOL["count_abs_below_10"] if n_t < 10 else TOL["count"] * n_t)


def main():
    t = block_a()
    pn, fsi = load_params()
    checks, report = [], {}

    def check(name, value, target, ok, rule):
        checks.append({"check": name, "value": value, "target": target, "pass": bool(ok), "rule": rule})

    # ---- passive (PN-A and PN-C share passive parameters; FSI)
    P1 = {k: np.array([v]) for k, v in pn.items()}
    pn_vals = {k: v for k, v in pn_values(P1, [("PN_C", 0.0, 0.0, 0.0), ("PN_A", 0.0, 0.0, 0.0)], 1).items()
               if k not in ("Iamp", "Ton", "Toff", "noise_on")}
    tt, tr = run_passive("PN", pn_vals, 2)
    fsi_vals = {k: np.full(1, v) for k, v in fsi.items()}
    tf, trf = run_passive("FSI", fsi_vals, 1)
    pas = {"PN_C": passive_measures(tt, tr[:, 0], 1000.0, 2000.0, -0.05),
           "PN_A": passive_measures(tt, tr[:, 1], 1000.0, 2000.0, -0.05),
           "FSI": passive_measures(tf, trf[:, 0], 1000.0, 2000.0, -0.05)}
    report["passive"] = pas
    for kind in ("PN_A", "PN_C", "FSI"):
        m, T = pas[kind], t[kind]
        check(f"{kind} resting potential", m["vrest_mV"], T["vrest"], abs(m["vrest_mV"] - T["vrest"]) <= TOL["vrest_mV"], "+-1 mV")
        check(f"{kind} input resistance", m["rin_MOhm"], T["rin"], abs(m["rin_MOhm"] / T["rin"] - 1) <= TOL["rin"], "+-10 %")
        tau_t = T["tau_slow"] if kind != "FSI" else T["tau63"]
        tau_m = m["tau_slow_ms"] if kind != "FSI" else m["t63_ms"]
        check(f"{kind} membrane time constant ({'slowest' if kind != 'FSI' else '63 % rise'})", tau_m, tau_t,
              abs(tau_m / tau_t - 1) <= TOL["tau"], "+-10 %")

    # ---- PN: ladder, long steps, noise, drive (one model)
    h = Stage2Harness(t, 1, backend=BACKEND, noise_cells=20, drive_reps=3, noise_ms=60000.0, name="s1_check_PN")
    sp = h.run(pn_values(P1, h.prot, 1, h.noise_kinds + h.drive_kinds))
    meas = stage2_measures(sp, h)
    h.close()
    rows = []
    for (kind, amp, on, off), s in zip(h.prot, sp[:len(h.prot)]):
        s = s[(s >= on) & (s < off)] - on
        if off - on == LADDER_MS:
            _, n_t, lat_t = next(x for x in t[kind]["ladder"] if x[0] == amp)
            lat = float(s[0]) if len(s) else None
            rows.append({"type": kind, "amp_nA": amp, "count": len(s), "count_target": n_t, "latency_ms": lat,
                         "latency_target_ms": lat_t})
            if kind == "PN_A":
                check(f"PN_A one spike per 1 s step, {amp} nA", len(s), 1, len(s) == 1, "exactly 1")
            else:
                check(f"PN_C spike count, {amp} nA", len(s), n_t, count_ok(len(s), n_t), "+-10 % (+-1 below 10)")
            check(f"{kind} first-spike latency, {amp} nA", lat, lat_t,
                  lat is not None and abs(lat / lat_t - 1) <= TOL["latency"], "+-10 %")
        else:
            _, n_t, times_t = next(x for x in t[kind]["long"] if x[0] == amp)
            rows.append({"type": kind, "amp_nA": amp, "dur_ms": LONG_MS, "count": len(s), "count_target": n_t,
                         "spike_times_ms": [round(float(x), 1) for x in s[:4]], "target_times_ms": times_t[:4]})
            if kind == "PN_C":
                check(f"PN_C 4 s count, {amp} nA", len(s), n_t, count_ok(len(s), n_t), "+-10 %")
            else:
                check(f"PN_A 4 s count, {amp} nA", len(s), n_t, len(s) == n_t, "exact")
                for i, (g, g_t) in enumerate(zip(np.diff(s), np.diff(times_t))):
                    check(f"PN_A 4 s gap {i + 1}, {amp} nA", float(g), float(g_t), abs(g / g_t - 1) <= TOL["pn_a_gap"], "+-15 %")
    ref = h.ref
    for kind in ("PN_A", "PN_C"):
        r_t, cv_t = ref["noise_only"][kind]["mean_Hz"], ref["noise_only"][kind]["isi_cv_mean"]
        r, cv = meas[f"noise_{kind}_Hz"], meas[f"noise_{kind}_cv"]
        check(f"{kind} noise-only rate", r, r_t, abs(r / r_t - 1) <= TOL["rate"], "+-15 %")
        check(f"{kind} noise-only ISI CV", cv, cv_t, abs(cv - cv_t) <= TOL["cv"], "+-0.1")
        d, d_t = meas[f"drive_{kind}_Hz"], ref["drive_summary"][kind]["mean_Hz"]
        check(f"{kind} dendritic-input rate", d, d_t, abs(d / d_t - 1) <= TOL["rate"], "+-15 %")

    # ---- FSI: ladder, long steps, noise only
    lad, longs = t["FSI"]["ladder"], t["FSI"]["long"]
    n_f = len(lad) + len(longs) + 20
    hf = Harness("FSI", n_f, 62000.0, backend=BACKEND, noise=True, name="s1_check_FSI")
    vals = {k: np.full(n_f, v) for k, v in fsi.items()}
    amp = [a for a, _, _ in lad] + [a for a, _, _ in longs] + [0.0] * 20
    toff = [SETTLE + LADDER_MS] * len(lad) + [SETTLE + LONG_MS] * len(longs) + [0.0] * 20
    vals.update(Iamp=np.array(amp), Ton=np.full(n_f, SETTLE), Toff=np.array(toff),
                noise_on=np.array([0.0] * (len(lad) + len(longs)) + [1.0] * 20))
    spf = spikes_by_cell(*hf.run(vals), n_f)
    hf.close()
    for (a, n_t, lat_t), s in zip(lad, spf[:len(lad)]):
        s = s[(s >= SETTLE) & (s < SETTLE + LADDER_MS)] - SETTLE
        lat = float(s[0]) if len(s) else None
        rows.append({"type": "FSI", "amp_nA": a, "count": len(s), "count_target": n_t, "latency_ms": lat,
                     "latency_target_ms": lat_t})
        check(f"FSI spike count, {a} nA", len(s), n_t, count_ok(len(s), n_t), "+-10 %")
        check(f"FSI first-spike latency, {a} nA", lat, lat_t, lat is not None and abs(lat / lat_t - 1) <= TOL["latency"], "+-10 %")
    for (a, n_t, _), s in zip(longs, spf[len(lad):len(lad) + len(longs)]):
        n = int(((s >= SETTLE) & (s < SETTLE + LONG_MS)).sum())
        check(f"FSI 4 s count, {a} nA", n, n_t, count_ok(n, n_t), "+-10 %")
    noise_rates = [((s >= 2000.0) & (s < 62000.0)).sum() / 60.0 for s in spf[-20:]]
    fr = float(np.mean(noise_rates))
    check("FSI noise-only rate", fr, 0.0, fr < 0.05, "silent (< 0.05 Hz), as Feng's FSIs")

    n_fail = sum(1 for c in checks if not c["pass"])
    status = "PASS" if n_fail == 0 else f"FAIL ({n_fail} of {len(checks)} checks)"
    report.update(rows=rows, stage2=meas, checks=checks, status=status,
                  backend=BACKEND, precision="double", dt_ms=DT,
                  reported_only={k: {"t63_ms": v["t63_ms"]} for k, v in pas.items()})
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "S1_cells.json").write_text(json.dumps(report, indent=1, default=float), encoding="utf-8")
    figure(t, rows, tt, tr, tf, trf)
    for c in checks:
        if not c["pass"]:
            print(f"  FAIL {c['check']}: {c['value']} (Feng {c['target']}, {c['rule']})")
    print(f"Gate S1: {status}; passive " + "; ".join(
        f"{k} {v['vrest_mV']:.1f} mV / {v['rin_MOhm']:.0f} MOhm / tau {v['tau_slow_ms']:.1f} (t63 {v['t63_ms']:.1f}) ms"
        for k, v in pas.items()))
    print("  noise and drive:", {k: round(v, 2) for k, v in meas.items()})


def figure(t, rows, tt, tr, tf, trf):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 3, figsize=(15, 4))
    for kind, col in (("PN_C", "tab:orange"), ("FSI", "tab:blue"), ("PN_A", "tab:red")):
        r = [x for x in rows if x["type"] == kind and "latency_ms" in x]
        ax[0].plot([x["amp_nA"] for x in r], [x["count_target"] for x in r], "o-", color=col, alpha=0.4, label=f"{kind} Feng")
        ax[0].plot([x["amp_nA"] for x in r], [x["count"] for x in r], "s--", color=col, label=f"{kind} simplified")
        ax[1].plot([x["amp_nA"] for x in r], [x["latency_target_ms"] for x in r], "o-", color=col, alpha=0.4)
        ax[1].plot([x["amp_nA"] for x in r], [x["latency_ms"] or np.nan for x in r], "s--", color=col)
    ax[0].set(xlabel="current (nA)", ylabel="spikes in 1 s", title="Firing curve (Feng: circles)")
    ax[0].legend(fontsize=7)
    ax[1].set(xlabel="current (nA)", ylabel="first-spike latency (ms)", yscale="log", title="Latency")
    ax[2].plot(tt - 1000, tr[:, 0], color="tab:orange", label="PN (simplified)")
    ax[2].plot(tf - 1000, trf[:, 0], color="tab:blue", label="FSI (simplified)")
    ax[2].set(xlim=(-100, 1600), xlabel="ms from step onset", ylabel="soma V (mV)", title="-0.05 nA step")
    ax[2].legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "S1_cells.png", dpi=110)
    plt.close(fig)


if __name__ == "__main__":
    main()
