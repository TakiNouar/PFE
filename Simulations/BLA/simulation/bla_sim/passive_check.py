"""Gate 2 / U29: the principal cell's membrane time constant, measured several standard ways.

Feng et al. 2019 state "tau_m ~30 ms" without the method. Block A's 63 %-rise time gives
34.9 ms for Feng's PN-A. Here the same cells get a small hyperpolarizing step (1 s, after
1 s of settling, then 1 s of recovery) and tau is estimated by:
  t63      time to 63.2 % of the steady-state response (Block A method)
  fit_on   single exponential fitted to the charging curve (first 300 ms of the step)
  fit_off  single exponential fitted to the recovery after the step (first 300 ms)
  tau0     slowest time constant: straight-line fit to ln|dV| over the late recovery,
           from 40 % down to 10 % of the response (Rall's "peeling")
Variants: step size, PN-C, Ih removed (diagnostic copy, Feng's files untouched), and the
main-level coarse cell. Leak-only values Cm / g_leak are reported for reference.

Usage (from Simulations/BLA/simulation):  python -m bla_sim.passive_check
Writes outputs/blockA/passive_tau.json and passive_tau.png.
"""
import json

import numpy as np

from . import cells as C
from .nrn import OUTPUT_DIR, load_config, setup
from .provenance import run_metadata
from .single_cell import _clamp, _run

SETTLE, STEP, AFTER = 1000.0, 1000.0, 1000.0
FIT_MS = 300.0
VARIANTS = [  # kind, level, amp (nA), Ih on
    ("PN_A", "full", -0.05, True),
    ("PN_A", "full", -0.01, True),
    ("PN_A", "full", -0.10, True),
    ("PN_C", "full", -0.05, True),
    ("PN_A", "full", -0.05, False),
    ("PN_A", "coarse_d2_p3", -0.05, True),
    ("PN_C", "coarse_d2_p3", -0.05, True),
]
PAPER_RM_KOHM_CM2, PAPER_CM = 55.0, 2.4      # Feng 2019 text (DEV-002)


def fit_exp(t, v):
    """Least-squares v = a + b exp(-t / tau); grid over tau, linear in a and b."""
    best = (np.inf, None)
    for tau in np.arange(1.0, 300.0, 0.05):
        X = np.column_stack([np.ones_like(t), np.exp(-t / tau)])
        coef = np.linalg.lstsq(X, v, rcond=None)[0]
        sse = float(np.sum((X @ coef - v) ** 2))
        if sse < best[0]:
            best = (sse, tau)
    return float(best[1])


def leak_only(cell, h):
    out = {}
    for name, sec in (("soma", cell.soma), ("dend", cell.dend)):
        seg = sec(0.5)
        g = next(getattr(seg, a) for a in ("glbar_leak", "glbar_leakDA") if hasattr(seg, a))
        out[name] = sec.cm * 1e-6 / g * 1e3        # (uF/cm2 -> F/cm2) / (S/cm2) -> s -> ms
    return out


def measure(h, kind, level, amp, ih_on, reduced):
    cell = C.make_cell(h, kind, level, reduced)
    if not ih_on:
        for sec in h.allsec():
            if sec.cell() == cell and h.ismembrane("hd", sec=sec):
                for seg in sec:
                    seg.ghdbar_hd = 0.0
    stim = _clamp(h, cell, SETTLE, STEP, amp)
    tv = h.Vector().record(h._ref_t)
    vv = h.Vector().record(cell.soma(0.5)._ref_v)
    _run(h, SETTLE + STEP + AFTER)
    t, v = np.array(tv), np.array(vv)
    t_on, t_off = SETTLE, SETTLE + STEP
    vrest = v[(t >= t_on - 100) & (t < t_on)].mean()
    v_ss = v[(t >= t_off - 50) & (t < t_off)].mean()
    dv = v_ss - vrest

    on = (t >= t_on) & (t < t_off)
    reached = np.nonzero((v[on] - vrest) <= 0.632 * dv)[0]
    t63 = float(t[on][reached[0]] - t_on)

    win_on = (t >= t_on) & (t < t_on + FIT_MS)
    fit_on = fit_exp(t[win_on][::10] - t_on, v[win_on][::10])
    win_off = (t >= t_off) & (t < t_off + FIT_MS)
    fit_off = fit_exp(t[win_off][::10] - t_off, v[win_off][::10])

    after = t >= t_off
    rel = (v[after] - vrest) / dv                 # 1 at step end, decays to 0
    first_below = lambda x: np.nonzero(rel <= x)[0][0]
    i0, i1 = first_below(0.4), first_below(0.1)
    slope = np.polyfit(t[after][i0:i1], np.log(rel[i0:i1]), 1)[0]
    tau0 = float(-1.0 / slope)

    norm_on = (v[on] - vrest) / dv
    out = {"kind": kind, "level": level, "amp_nA": amp, "Ih": ih_on,
           "vrest_mV": float(vrest), "rin_MOhm": float(dv / amp),
           "sag_ratio": float(dv / (v[on] - vrest).min()),
           "tau_ms": {"t63": t63, "fit_on": fit_on, "fit_off": fit_off, "tau0": tau0}}
    if level == "full":
        out["leak_only_ms"] = leak_only(cell, h)
    trace = (t[on][::20] - t_on, norm_on[::20])
    del stim, cell
    return out, trace


def figure(results, traces, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    for r, (t, y) in zip(results, traces):
        lab = f"{r['kind']} {r['level']} {r['amp_nA']} nA{'' if r['Ih'] else ' Ih off'}"
        ax[0].plot(t, y, lw=1, label=lab)
    ax[0].axhline(0.632, color="k", lw=0.5, ls=":")
    for x, c in ((30, "tab:green"),):
        ax[0].axvline(x, color=c, lw=0.8, ls="--", label="Feng text ~30 ms")
    ax[0].set(xlim=(0, 200), xlabel="ms after step onset", ylabel="response / steady state",
              title="Charging curves")
    ax[0].legend(fontsize=7)
    names = ["t63", "fit_on", "fit_off", "tau0"]
    x = np.arange(len(names))
    w = 0.8 / len(results)
    for i, r in enumerate(results):
        ax[1].bar(x + i * w, [r["tau_ms"][k] for k in names], w)
    ax[1].axhline(30, color="tab:green", ls="--", lw=0.8)
    ax[1].set(xticks=x + 0.4 - w / 2, xticklabels=names, ylabel="tau (ms)", title="Estimates per variant")
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def main():
    cfg = load_config()
    h = setup(cfg)
    reduced = C.load_reduced_params()
    results, traces = [], []
    for kind, level, amp, ih in VARIANTS:
        r, tr = measure(h, kind, level, amp, ih, reduced)
        results.append(r)
        traces.append(tr)
        t = r["tau_ms"]
        print(f"{kind} {level:13s} {amp:+.2f} nA{'' if ih else ' Ih off'}: Vrest {r['vrest_mV']:.1f} mV, "
              f"Rin {r['rin_MOhm']:.0f} MOhm, tau t63 {t['t63']:.1f} | fit_on {t['fit_on']:.1f} | "
              f"fit_off {t['fit_off']:.1f} | tau0 {t['tau0']:.1f} ms")
    paper = PAPER_RM_KOHM_CM2 * 1e3 * PAPER_CM * 1e-6 * 1e3
    out = {"meta": run_metadata(h), "protocol": {"settle_ms": SETTLE, "step_ms": STEP, "after_ms": AFTER,
                                                 "fit_window_ms": FIT_MS, "tau0_window": "40 % to 10 %"},
           "feng_text": {"tau_m_ms": 30, "Rm_kOhm_cm2": PAPER_RM_KOHM_CM2, "Cm_uF_cm2": PAPER_CM,
                         "Rm_times_Cm_ms": paper},
           "results": results}
    d = OUTPUT_DIR / "blockA"
    (d / "passive_tau.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    figure(results, traces, d / "passive_tau.png")
    print(f"Feng text: tau ~30 ms; text Rm x Cm = {paper:.0f} ms; "
          f"code leak only (soma / dend): {results[0]['leak_only_ms']['soma']:.0f} / "
          f"{results[0]['leak_only_ms']['dend']:.0f} ms")
    print(f"-> {d / 'passive_tau.json'}")


if __name__ == "__main__":
    main()
