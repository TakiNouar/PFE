"""Block A3: Feng's synapse files vs the event-driven synapses (architecture/04, DEV-007).

Each receiving compartment is voltage-clamped at -70 mV, so both versions see the
same voltage and the conductances can be compared directly.

Usage (from Simulations/BLA/simulation):
    python -m bla_sim.synapse_test
Writes outputs/blockA/synapse_test.json and synapse_test.png.
"""
import json

import numpy as np

from .nrn import OUTPUT_DIR, load_config, setup
from .provenance import run_metadata

# Event-driven parameters copied from Feng's files (defaults of the .mod files are
# PN->PN for ExcEv and FSI->PN for InhEv).
PATHWAYS = {
    "PN_to_PN": {"feng": "pyrD2pyrD_STFD", "ours": "ExcEv", "set": {},
                 "receptors": [("AMPA", "g_ampa", "g_a"), ("NMDA", "g_nmda", "g_n")], "W": [2.0, 1.5, 3.0]},
    "PN_to_FSI": {"feng": "pyrD2interD_STFD", "ours": "ExcEv",
                  "set": {"Cdur_a": 0.713, "AlphaTmax_a": 10.1571, "Beta_a": 0.4167, "fac_floor": 0.7},
                  "receptors": [("AMPA", "g_ampa", "g_a"), ("NMDA", "g_nmda", "g_n")], "W": [7.0, 5.0, 9.0]},
    "FSI_to_PN": {"feng": "interD2pyrD_STFD", "ours": "InhEv", "set": {},
                  "receptors": [("GABA", "g_gaba", "g")], "W": [12.0, 10.0, 14.0]},
    "FSI_to_FSI": {"feng": "interD2interD_STFD", "ours": "InhEv",
                   "set": {"AlphaTmax": 1.853, "Beta": 0.147, "gbar": 0.2e-3},
                   "receptors": [("GABA", "g_gaba", "g")], "W": [20.0, 15.0, 25.0]},
}


def spike_trains(rng):
    def regular(rate, n, start=100.0):
        return list(start + np.arange(n) * 1000.0 / rate)
    poisson = list(100 + np.cumsum(rng.exponential(1000 / 20, size=60)))
    doublets = [x for k in range(10) for x in (100 + 200 * k, 101 + 200 * k)]
    return {
        "isolated (1 s apart)": [100.0, 1100.0, 2100.0],
        "5 Hz x10": regular(5, 10),
        "20 Hz x10": regular(20, 10),
        "50 Hz x10": regular(50, 10),
        "doublets 1 ms apart": doublets,
        "Poisson 20 Hz": [t for t in poisson if t < 3000],
    }


def _compartment(h, name):
    sec = h.Section(name=name)
    sec.L = sec.diam = 20
    sec.insert("pas")
    clamp = h.SEClamp(sec(0.5))
    clamp.dur1 = 1e9
    clamp.amp1 = -70
    clamp.rs = 0.001
    return sec, clamp


def compare(h, pw, trains_by_conn, t_end):
    """Feng: one synapse object per connection. Ours: one object for all connections."""
    keep = []
    sec_f, cl_f = _compartment(h, "feng_target")
    sec_o, cl_o = _compartment(h, "ours_target")
    ours = getattr(h, pw["ours"])(sec_o(0.5))
    for k, v in pw["set"].items():
        setattr(ours, k, v)
    fengs = []
    for times, W in trains_by_conn:
        vs = h.VecStim()
        tv = h.Vector(times)
        vs.play(tv)
        f = getattr(h, pw["feng"])(sec_f(0.5))
        f.initW = W
        ncf = h.NetCon(vs, f, 0, 1.0, 1.0)
        nco = h.NetCon(vs, ours, 0, 1.0, W)
        fengs.append(f)
        keep += [vs, tv, ncf, nco]
    rec = {}
    for name, gf, go in pw["receptors"]:
        rec[name] = ([h.Vector().record(getattr(f, f"_ref_{gf}")) for f in fengs],
                     h.Vector().record(getattr(ours, f"_ref_{go}")))
    h.finitialize(-70)
    h.continuerun(t_end)
    out = {}
    for name, (feng_vecs, ours_vec) in rec.items():
        W = np.array([W for _, W in trains_by_conn])[:, None]
        feng = (np.array([np.array(v) for v in feng_vecs]) * W).sum(axis=0)   # Feng: current = W * g
        o = np.array(ours_vec)
        peak = np.abs(feng).max()
        out[name] = {"peak_uS": float(peak), "max_abs_diff_uS": float(np.abs(o - feng).max()),
                     "max_diff_rel_peak": float(np.abs(o - feng).max() / peak) if peak else 0.0,
                     "_feng": feng, "_ours": o}
    for s in (sec_f, sec_o):
        h.delete_section(sec=s)
    del keep, fengs, ours, cl_f, cl_o
    return out


def main():
    cfg = load_config()
    h = setup(cfg)
    meta = run_metadata(h)
    rng = np.random.default_rng(1)
    trains = spike_trains(rng)
    results, examples = {}, {}
    for pname, pw in PATHWAYS.items():
        results[pname] = {}
        for tname, times in trains.items():
            r = compare(h, pw, [(times, pw["W"][0])], t_end=max(times) + 400)
            results[pname][tname] = {k: {a: b for a, b in v.items() if not a.startswith("_")} for k, v in r.items()}
            if tname == "20 Hz x10":
                examples[pname] = r
        multi = [(sorted(rng.uniform(100, 2500, size=25)), W) for W in pw["W"]]
        r = compare(h, pw, multi, t_end=2900)
        results[pname]["3 connections, Poisson, one shared object"] = {
            k: {a: b for a, b in v.items() if not a.startswith("_")} for k, v in r.items()}

    worst_isolated = max(v["max_diff_rel_peak"] for p in results.values()
                         for v in p["isolated (1 s apart)"].values())
    worst_any = max(v["max_diff_rel_peak"] for p in results.values() for t in p.values() for v in t.values())
    summary = {"isolated_spikes_worst_rel_diff": worst_isolated, "isolated_pass_1pct": worst_isolated <= 0.01,
               "all_trains_worst_rel_diff": worst_any}
    d = OUTPUT_DIR / "blockA"
    d.mkdir(parents=True, exist_ok=True)
    (d / "synapse_test.json").write_text(json.dumps({"meta": meta, "summary": summary, "results": results},
                                                    indent=1), encoding="utf-8")
    for pname, p in results.items():
        for tname, t in p.items():
            print(f"{pname:10s} {tname:42s} " + "  ".join(
                f"{k}: {100 * v['max_diff_rel_peak']:.3f}%" for k, v in t.items()))
    print(f"isolated spikes worst difference {100 * worst_isolated:.3f}% of peak "
          f"({'PASS' if summary['isolated_pass_1pct'] else 'FAIL'} at 1%); all trains worst {100 * worst_any:.3f}%")

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(len(examples), 1, figsize=(9, 2.3 * len(examples)), squeeze=False)
    dt = h.dt
    for ax, (pname, r) in zip(axes[:, 0], examples.items()):
        for name, v in r.items():
            t = np.arange(len(v["_feng"])) * dt
            ax.plot(t, v["_feng"] * 1000, color="0.6", lw=3, label=f"{name} Feng")
            ax.plot(t, v["_ours"] * 1000, lw=1, label=f"{name} event-driven")
        ax.set_title(f"{pname.replace('_', ' ')} · 20 Hz train", fontsize=10)
        ax.set_ylabel("nS")
        ax.legend(fontsize=7, loc="upper right")
    axes[-1, 0].set_xlabel("ms")
    fig.tight_layout()
    fig.savefig(d / "synapse_test.png", dpi=120)
    plt.close(fig)


if __name__ == "__main__":
    main()
