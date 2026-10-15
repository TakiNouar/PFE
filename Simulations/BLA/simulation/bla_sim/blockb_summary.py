"""Block B summary: the reference behaviour of Feng's network for the simplified model.

Usage (from Simulations/BLA/simulation): python -m bla_sim.blockb_summary
Reads outputs/B_full_n200/seed*/ and writes outputs/blockB/reference_summary.json:
mean and SD across seeds of the rest rates, rest range, synchrony, ISI CV and, per dose,
the PN and FSI rates before, during and after the threat, plus FSI depolarization-block
episodes (all FSIs silent in a 250 ms bin while firing before the threat).
"""
import json

import numpy as np

from .metrics import all_metrics
from .nrn import OUTPUT_DIR


def fsi_block_episodes(sp, sched):
    ty, t, g = sp["types"], sp["t_ms"], sp["gid"]
    f = ty[g] == "FSI"
    out = []
    for tr in sched["trials"]:
        e = np.arange(tr["threat_on_ms"], tr["end_ms"] + 1e-9, 250.0)
        h = np.histogram(t[f], e)[0]
        silent = [float(e[i]) for i in np.nonzero(h == 0)[0]]
        if silent:
            out.append({"dose": tr["dose"], "silent_bins_start_ms": silent})
    return out


def main():
    d = OUTPUT_DIR / "B_full_n200"
    seeds, per = [], {}
    for p in sorted(d.glob("seed*")):
        r = json.loads((p / "run.json").read_text(encoding="utf-8"))
        sp = dict(np.load(p / "spikes.npz", allow_pickle=True))
        s = int(p.name[4:])
        m = all_metrics(sp, r["schedule"], s)
        m["fsi_block"] = fsi_block_episodes(sp, r["schedule"])
        m["recovered"] = {k: bool(m["rest_range_PN_Hz"]["low"] <= v["PN_late_post"] <= m["rest_range_PN_Hz"]["high"])
                          for k, v in m["threat"].items()}
        per[s] = m
        seeds.append(s)

    def stat(f):
        v = np.array([f(per[s]) for s in seeds], float)
        return {"mean": float(v.mean()), "sd": float(v.std(ddof=1)) if len(v) > 1 else 0.0, "per_seed": v.tolist()}

    summary = {
        "source": "Feng et al. 2019 cells and synapses unchanged (ModelDB 247968), 200 cells, in-degree wiring "
                  "(DEV-001), Feng's noise and afferent trains; settle 3 s, rest 30 s, one trial each at x2, x4, x8",
        "seeds": seeds,
        "rest_Hz": {k: stat(lambda m, k=k: m["rest"][k]["mean_Hz"]) for k in ("PN_A", "PN_C", "PN", "FSI")},
        "rest_range_PN_Hz": {k: stat(lambda m, k=k: m["rest_range_PN_Hz"][k]) for k in ("low", "high")},
        "synchrony_index": stat(lambda m: m["synchrony"]["index"]),
        "isi_cv_PN": stat(lambda m: m["isi_cv"]["mean"]),
        "threat": {dose: {k: stat(lambda m, dose=dose, k=k: m["threat"][dose][k])
                          for k in ("PN_pre", "PN_threat", "PN_late_post", "PN_response_Hz",
                                    "FSI_pre", "FSI_threat", "FSI_response_Hz")}
                   for dose in ("2", "4", "8")},
        "recovered": {s: per[s]["recovered"] for s in seeds},
        "fsi_depolarization_block": {s: per[s]["fsi_block"] for s in seeds},
    }
    out = OUTPUT_DIR / "blockB"
    out.mkdir(parents=True, exist_ok=True)
    (out / "reference_summary.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    r = summary["rest_Hz"]
    print("rest: " + ", ".join(f"{k} {v['mean']:.2f} ± {v['sd']:.2f} Hz" for k, v in r.items()))
    for dose, t in summary["threat"].items():
        print(f"x{dose}: PN {t['PN_pre']['mean']:.2f} -> {t['PN_threat']['mean']:.2f} ± {t['PN_threat']['sd']:.2f} Hz, "
              f"FSI {t['FSI_pre']['mean']:.1f} -> {t['FSI_threat']['mean']:.1f} ± {t['FSI_threat']['sd']:.1f} Hz")
    print("FSI block episodes:", summary["fsi_depolarization_block"])
    print(f"-> {out / 'reference_summary.json'}")


if __name__ == "__main__":
    main()
