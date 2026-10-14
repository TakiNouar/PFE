"""Gate R2 (architecture/10): the reduced 200-cell network matches the full-detail one (Block B).

Usage (from Simulations/BLA/simulation), after Block B:
    python -m bla_sim.gate_r2
    python -m bla_sim.gate_r2 --full outputs/B_full_n200 --reduced outputs/B_reduced_n200
Reads <dir>/seed<k>/{run.json, spikes.npz} for the seeds present at both levels, and
outputs/blockA/synapse_test.json. Writes outputs/blockB/reduction_R2.json and .png.

Rules (architecture/10); SD = sample SD across the full-detail seeds:
  rest       reduced mean resting rate of PN-A, PN-C and FSI within full mean +- 2 SD
  threat     reduced PN and FSI rate increase during the x4 threat within full mean +- 2 SD
  recovery   a level "recovers" when, in every seed, the PN rate in the last 2 s of the trials
             (mean over trials) lies inside that seed's rest range; both levels must agree
  synchrony  index < 0.5 at both levels, and |full - reduced| < 0.1 (seed means)
  synapses   step A3 reported (largest relative difference over all trains)
Also checks that both levels were built from the same network (same connection count,
gap pairs and afferent wiring per seed), which the shared random streams guarantee.
"""
import argparse
import json

import numpy as np

from .metrics import all_metrics
from .nrn import OUTPUT_DIR

THREAT_DOSE = "4"
PSTH_BIN_MS = 100.0


def load(d):
    runs = {}
    for p in sorted(d.glob("seed*")):
        if (p / "run.json").exists() and (p / "spikes.npz").exists():
            runs[int(p.name[4:])] = (json.loads((p / "run.json").read_text(encoding="utf-8")),
                                     dict(np.load(p / "spikes.npz", allow_pickle=True)))
    return runs


def per_seed(run, spikes, seed):
    m = all_metrics(spikes, run["schedule"], seed)
    rr = m["rest_range_PN_Hz"]
    m["recovered"] = {dose: bool(rr["low"] <= v["PN_late_post"] <= rr["high"])
                      for dose, v in m["threat"].items()}
    return m


def within_2sd(full_vals, red_vals):
    f, r = np.asarray(full_vals, float), np.asarray(red_vals, float)
    if len(f) < 2:
        return {"status": "not evaluable (fewer than 2 full-detail seeds)"}
    mf, sd, mr = float(f.mean()), float(f.std(ddof=1)), float(r.mean())
    return {"full_mean": mf, "full_sd": sd, "reduced_mean": mr, "diff": mr - mf,
            "limit": 2 * sd, "pass": bool(abs(mr - mf) <= 2 * sd),
            "full_per_seed": f.tolist(), "reduced_per_seed": r.tolist()}


def psth(run, spikes):
    """Population PN rate (Hz per cell) around the threat, mean over trials."""
    types, t, g = spikes["types"], spikes["t_ms"], spikes["gid"]
    pn_t = t[types[g] != "FSI"]
    n_pn = int((types != "FSI").sum())
    edges = np.arange(-2000.0, 6000.0 + 1e-9, PSTH_BIN_MS)
    rows = [np.histogram(pn_t - tr["threat_on_ms"], bins=edges)[0] / n_pn / (PSTH_BIN_MS / 1000.0)
            for tr in run["schedule"]["trials"] if str(tr["dose"]) == THREAT_DOSE]
    return edges[:-1] + PSTH_BIN_MS / 2, (np.mean(rows, axis=0) if rows else None)


def same_network(rf, rr):
    keys = (("network", "connections"), ("network", "gap_pairs"), ("afferents", "connections"))
    return all(rf[a][b] == rr[a][b] for a, b in keys)


def evaluate(full, red):
    seeds = sorted(set(full) & set(red))
    mf = {s: per_seed(*full[s], s) for s in seeds}
    mr = {s: per_seed(*red[s], s) for s in seeds}
    checks = {}
    checks["same_network"] = {"pass": all(same_network(full[s][0], red[s][0]) for s in seeds),
                              "seeds": seeds}
    checks["rest"] = {k: within_2sd([mf[s]["rest"][k]["mean_Hz"] for s in seeds],
                                    [mr[s]["rest"][k]["mean_Hz"] for s in seeds])
                      for k in ("PN_A", "PN_C", "FSI")}
    if all(THREAT_DOSE in mf[s]["threat"] for s in seeds):
        checks["threat_x4"] = {k: within_2sd([mf[s]["threat"][THREAT_DOSE][f"{k}_response_Hz"] for s in seeds],
                                             [mr[s]["threat"][THREAT_DOSE][f"{k}_response_Hz"] for s in seeds])
                               for k in ("PN", "FSI")}
        rec_f = all(mf[s]["recovered"][THREAT_DOSE] for s in seeds)
        rec_r = all(mr[s]["recovered"][THREAT_DOSE] for s in seeds)
        checks["recovery"] = {"full_recovers": rec_f, "reduced_recovers": rec_r, "pass": rec_f == rec_r,
                              "full_per_seed": [mf[s]["recovered"][THREAT_DOSE] for s in seeds],
                              "reduced_per_seed": [mr[s]["recovered"][THREAT_DOSE] for s in seeds]}
    else:
        checks["threat_x4"] = {"status": "not evaluable (no x4 trials)"}
        checks["recovery"] = {"status": "not evaluable (no x4 trials)"}
    sync = {}
    for name, m in (("full", mf), ("reduced", mr)):
        vals = [m[s]["synchrony"]["index"] for s in seeds]
        sync[name] = None if any(v is None for v in vals) else float(np.mean(vals))
    if None in sync.values():
        checks["synchrony"] = {"status": "not evaluable (too few PNs with >= 5 spikes)", **sync}
    else:
        checks["synchrony"] = {**sync, "diff": sync["reduced"] - sync["full"],
                               "pass": bool(sync["full"] < 0.5 and sync["reduced"] < 0.5
                                            and abs(sync["reduced"] - sync["full"]) < 0.1)}
    syn_path = OUTPUT_DIR / "blockA" / "synapse_test.json"
    if syn_path.exists():
        st = json.loads(syn_path.read_text(encoding="utf-8"))["summary"]
        checks["synapse_test"] = {"reported": True, "all_trains_worst_rel_diff": st["all_trains_worst_rel_diff"],
                                  "pass": True}
    else:
        checks["synapse_test"] = {"status": "not evaluable (run python -m bla_sim.synapse_test)"}

    flat = []
    for k, v in checks.items():
        subs = v.values() if k in ("rest", "threat_x4") and "status" not in v else [v]
        flat += [x.get("pass") for x in subs]
    status = "FAIL" if False in flat else ("INCOMPLETE" if None in flat else "PASS")
    return {"status": status, "seeds": seeds, "checks": checks,
            "per_seed": {"full": mf, "reduced": mr}}


def figure(res, full, red, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 3, figsize=(14, 4))
    c = res["checks"]
    names = ["PN_A", "PN_C", "FSI"]
    for a, keys, title, src in ((ax[0], names, "Resting rates (Hz)", c["rest"]),
                                (ax[1], ["PN", "FSI"], f"Rate increase during x{THREAT_DOSE} threat (Hz)",
                                 c.get("threat_x4", {}))):
        if "status" in src:
            a.set_title(title + "\n" + src["status"], fontsize=9)
            continue
        x = np.arange(len(keys))
        a.bar(x, [src[k]["full_mean"] for k in keys], 0.5, yerr=[src[k]["limit"] for k in keys],
              color="0.8", capsize=4, label="full (mean, +-2 SD)")
        for i, k in enumerate(keys):
            a.plot(np.full(len(src[k]["reduced_per_seed"]), i), src[k]["reduced_per_seed"], "o",
                   color="tab:blue", ms=4, label="reduced seeds" if i == 0 else None)
            a.plot(i, src[k]["reduced_mean"], "D", color="tab:red", ms=6, label="reduced mean" if i == 0 else None)
        a.set(xticks=x, xticklabels=keys, title=title)
        if a is ax[0]:
            a.set_yscale("log")             # PN rates ~1 Hz next to FSI rates ~20 Hz
        a.legend(fontsize=7)
    for runs, name, col in ((full, "full", "0.3"), (red, "reduced", "tab:blue")):
        curves = [psth(*runs[s]) for s in res["seeds"]]
        curves = [(t, y) for t, y in curves if y is not None]
        if curves:
            ax[2].plot(curves[0][0] / 1000.0, np.mean([y for _, y in curves], axis=0), color=col, label=name)
    ax[2].axvspan(0, 2, color="tab:red", alpha=0.1, label="threat")
    ax[2].set(xlabel="s from threat onset", ylabel="PN rate (Hz per cell)", title="PN rate around the threat")
    ax[2].legend(fontsize=7)
    fig.suptitle(f"Gate R2: {res['status']} (seeds {res['seeds']})")
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--full", default=str(OUTPUT_DIR / "B_full_n200"))
    ap.add_argument("--reduced", default=str(OUTPUT_DIR / "B_reduced_n200"))
    ap.add_argument("--out", default=str(OUTPUT_DIR / "blockB"))
    args = ap.parse_args()
    from pathlib import Path
    full, red = load(Path(args.full)), load(Path(args.reduced))
    if not set(full) & set(red):
        raise SystemExit(f"no seed present at both levels ({args.full}: {sorted(full)}, {args.reduced}: {sorted(red)})")
    res = evaluate(full, red)
    res["inputs"] = {"full": args.full, "reduced": args.reduced}
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "reduction_R2.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
    figure(res, full, red, out / "reduction_R2.png")
    for k, v in res["checks"].items():
        if k in ("rest", "threat_x4") and "status" not in v:
            for kk, vv in v.items():
                print(f"  {k:10s} {kk:5s} full {vv['full_mean']:7.2f} +- {vv['limit']:.2f}, "
                      f"reduced {vv['reduced_mean']:7.2f}: {'pass' if vv['pass'] else 'FAIL'}")
        else:
            print(f"  {k:10s} " + ", ".join(f"{a}={b}" for a, b in v.items() if not isinstance(b, (list, dict))))
    print(f"Gate R2: {res['status']} (seeds {res['seeds']}) -> {out / 'reduction_R2.json'}")


if __name__ == "__main__":
    main()
