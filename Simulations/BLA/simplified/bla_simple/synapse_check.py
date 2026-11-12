"""Gate S2 (spec 14): the GeNN synapses against Feng's synapse files, all protocols.

Runs the fitted rise-and-decay synapses with per-spike depression in GeNN (exact CPU backend,
double precision, dt 0.1 ms) on targets clamped at -70 mV, with the same spike trains and
weights as the reference (synapse_reference.npz, Feng's files in NEURON). Compares, per
pathway, receptor and protocol, the largest conductance and the charge (time integral).

Pass rule (spec 14 S2): peak and charge within +-5 % for isolated spikes, 5 Hz trains and
Poisson 20 Hz (the per-connection rates of the network). 20 Hz, 50 Hz and 1 ms doublets are
reported: there Feng's file saturates and rescales the active conductance (S-DEV-3).

Usage (from Simulations/BLA/simplified, in with_gpu_env.cmd):
    <venv python> -m bla_simple.synapse_check
Writes outputs/S2_synapses.json and S2_synapses.png.
"""
import json
import os

import numpy as np

from .fit_synapses import DELAY_MS, load_reference
from .paths import BUILD_DIR, CONFIG_DIR, OUTPUT_DIR
from .synapses import PRE_INIT, models, psm_params, wu_params

DT = 0.1
GATED = ("isolated (1 s apart)", "5 Hz x10", "Poisson 20 Hz")
E_REV = {"AMPA": 0.0, "NMDA": 0.0, "GABA": -75.0}


def pathway_key(p):                    # "PN_to_FSI" -> "PN_FSI"
    return p.replace("_to_", "_")


def main():
    import pygenn as G
    idx, data = load_reference()
    fits = json.loads((CONFIG_DIR / "synapses_fitted.json").read_text(encoding="utf-8"))["fits"]
    protocols = list(dict.fromkeys(e["protocol"] for e in idx["entries"]))
    combos = list(dict.fromkeys((e["pathway"], e["receptor"]) for e in idx["entries"]))
    spikes = {p: data[next(e["key"] for e in idx["entries"] if e["protocol"] == p) + "|spikes"] for p in protocols}
    t_end = max(s.max() for s in spikes.values()) + 600.0

    mods = models()
    clamp = G.create_neuron_model("clamped", vars=[("V", "scalar", G.VarAccess.READ_ONLY)])
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    cwd = os.getcwd()
    os.chdir(BUILD_DIR)
    try:
        m = G.GeNNModel("double", "s2_synapses", backend="single_threaded_cpu")
        m.dt = DT
        times = np.concatenate([spikes[p] for p in protocols])
        ends = np.cumsum([len(spikes[p]) for p in protocols])
        src = m.add_neuron_population("src", len(protocols), "SpikeSourceArray", {},
                                      {"startSpike": np.concatenate([[0], ends[:-1]]), "endSpike": ends})
        src.extra_global_params["spikeTimes"].set_init_values(times)
        groups = {}
        for k, (pw, rec) in enumerate(combos):
            tgt = m.add_neuron_population(f"tgt{k}", len(protocols), clamp, {}, {"V": -70.0})
            W = next(e["W"] for e in idx["entries"] if e["pathway"] == pw)
            psm = G.init_postsynaptic(mods["psm_nmda" if rec == "NMDA" else "psm"],
                                      psm_params(fits[f"{pw}|{rec}"], E_REV[rec]), {"x": 0.0, "g": 0.0},
                                      var_refs={"V": G.create_var_ref(tgt, "V")})
            wu = G.init_weight_update(mods["wu"], wu_params(pathway_key(pw), rec, fits[f"{pw}|{rec}"]),
                                      {"W": W, "delay": 0}, pre_vars=dict(PRE_INIT))
            sg = m.add_synapse_population(f"syn{k}", "SPARSE", src, tgt, wu, psm,
                                          G.init_sparse_connectivity("OneToOne"))
            sg.axonal_delay_steps = int(round(DELAY_MS / DT))
            sg.max_dendritic_delay_timesteps = 1
            groups[(pw, rec)] = sg
        m.build()
        m.load()
        n_steps = int(round(t_end / DT))
        rec_g = {c: np.zeros((n_steps, len(protocols))) for c in combos}
        for i in range(n_steps):
            m.step_time()
            for c, sg in groups.items():
                sg.psm_vars["g"].pull_from_device()
                rec_g[c][i] = sg.psm_vars["g"].values
        m.unload()
    finally:
        os.chdir(cwd)

    results, worst_gated = {}, 0.0
    for (pw, rec) in combos:
        for j, p in enumerate(protocols):
            e = next(e for e in idx["entries"] if e["pathway"] == pw and e["receptor"] == rec and e["protocol"] == p)
            ref = data[e["key"] + "|g"]
            ref = ref[::int(round(DT / idx["dt_ms"]))][:n_steps]            # Feng's trace on the 0.1 ms grid
            ours = rec_g[(pw, rec)][:len(ref), j]
            peak_rel = ours.max() / ref.max() - 1
            charge_rel = ours.sum() / ref.sum() - 1
            gated = p in GATED
            ok = abs(peak_rel) <= 0.05 and abs(charge_rel) <= 0.05
            if gated:
                worst_gated = max(worst_gated, abs(peak_rel), abs(charge_rel))
            results[f"{pw}|{rec}|{p}"] = {"peak_rel": float(peak_rel), "charge_rel": float(charge_rel),
                                          "gated": gated, "pass": bool(ok) if gated else None}
            print(f"{pw:10s} {rec:5s} {p:22s} peak {100*peak_rel:+6.1f}%  charge {100*charge_rel:+6.1f}%  "
                  f"{('PASS' if ok else 'FAIL') if gated else '(reported)'}")
    exc_path = CONFIG_DIR / "gate_exceptions.json"
    approved = {e["key"]: e for e in json.loads(exc_path.read_text(encoding="utf-8")).get("S2", [])} if exc_path.exists() else {}
    failed = [k for k, r in results.items() if r["gated"] and not r["pass"]]
    unapproved = [k for k in failed if k not in approved]
    for k in failed:
        results[k]["approved_exception"] = approved.get(k)
    status = ("FAIL" if unapproved else
              f"PASS with {len(failed)} approved exception{'s' if len(failed) != 1 else ''}" if failed else "PASS")
    out = {"gate": "S2", "status": status, "worst_gated_rel": worst_gated, "dt_ms": DT, "backend": "single_threaded_cpu",
           "precision": "double", "rule": "peak and charge within 5 % for " + ", ".join(GATED), "results": results}
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "S2_synapses.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    figure(idx, data, protocols, combos, rec_g)
    print(f"Gate S2: {status} (worst gated difference {100*worst_gated:.1f} %)")


def figure(idx, data, protocols, combos, rec_g):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    show = ["isolated (1 s apart)", "20 Hz x10", "Poisson 20 Hz"]
    fig, ax = plt.subplots(len(combos), len(show), figsize=(14, 2.2 * len(combos)), squeeze=False)
    for i, (pw, rec) in enumerate(combos):
        for j, p in enumerate(show):
            e = next(e for e in idx["entries"] if e["pathway"] == pw and e["receptor"] == rec and e["protocol"] == p)
            ref = data[e["key"] + "|g"]
            t_ref = np.arange(len(ref)) * idx["dt_ms"]
            ours = rec_g[(pw, rec)][:, protocols.index(p)]
            t_o = (np.arange(len(ours)) + 1) * DT
            a = ax[i][j]
            a.plot(t_ref, ref * 1000, color="0.3", lw=1, label="Feng (NEURON)")
            a.plot(t_o, ours * 1000, color="tab:orange", lw=1, ls="--", label="simplified (GeNN)")
            a.set_xlim(90, 650 if p != "Poisson 20 Hz" else 1600)
            a.set_title(f"{pw} {rec}: {p}", fontsize=8)
            a.tick_params(labelsize=7)
            if j == 0:
                a.set_ylabel("g (nS)", fontsize=8)
    ax[0][0].legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "S2_synapses.png", dpi=110)
    plt.close(fig)


if __name__ == "__main__":
    main()
