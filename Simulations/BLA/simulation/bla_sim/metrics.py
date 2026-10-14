"""Network metrics (architecture/08). Pure functions of spikes, cell types and schedule."""
import numpy as np

from .network import stream


def _counts(spikes, t0, t1, n):
    t, g = spikes["t_ms"], spikes["gid"]
    sel = (t >= t0) & (t < t1)
    return np.bincount(g[sel], minlength=n)


def rest_rates(spikes, sched):
    types = spikes["types"]
    n = len(types)
    t0 = sched["settle_ms"]
    t1 = t0 + sched["rest_ms"]
    rate = _counts(spikes, t0, t1, n) / ((t1 - t0) / 1000.0)
    out = {}
    for name, mask in (("PN_A", types == "PN_A"), ("PN_C", types == "PN_C"),
                       ("PN", types != "FSI"), ("FSI", types == "FSI")):
        r = rate[mask]
        out[name] = {"mean_Hz": float(r.mean()), "sd_Hz": float(r.std()),
                     "silent_fraction": float((r == 0).mean())}
    return out, rate


def rest_windows(spikes, sched, width_ms=2000.0):
    """PN population rate in consecutive windows of the rest epoch (for the rest range)."""
    types = spikes["types"]
    pn = types != "FSI"
    t0 = sched["settle_ms"]
    edges = np.arange(t0, t0 + sched["rest_ms"] + 1e-9, width_ms)
    vals = []
    for a, b in zip(edges[:-1], edges[1:]):
        c = _counts(spikes, a, b, len(types))
        vals.append(c[pn].mean() / (width_ms / 1000.0))
    return np.array(vals)


def synchrony(spikes, sched, seed, n_pairs=100, bin_ms=5.0, min_spikes=5):
    types = spikes["types"]
    t0, t1 = sched["settle_ms"], sched["settle_ms"] + sched["rest_ms"]
    t, g = spikes["t_ms"], spikes["gid"]
    sel = (t >= t0) & (t < t1)
    counts = np.bincount(g[sel], minlength=len(types))
    cand = np.nonzero((types != "FSI") & (counts >= min_spikes))[0]
    if len(cand) < 2:
        return {"index": None, "pairs": 0, "eligible_PNs": int(len(cand))}
    rng = stream(seed, "metrics")
    edges = np.arange(t0, t1 + bin_ms, bin_ms)
    binned = {}

    def b(i):
        if i not in binned:
            binned[i] = np.histogram(t[sel][g[sel] == i], bins=edges)[0].astype(float)
        return binned[i]

    cc = []
    for _ in range(n_pairs):
        i, j = rng.choice(cand, 2, replace=False)
        x, y = b(i), b(j)
        if x.std() > 0 and y.std() > 0:
            cc.append(np.corrcoef(x, y)[0, 1])
    return {"index": float(np.mean(cc)) if cc else None, "pairs": len(cc), "eligible_PNs": int(len(cand))}


def isi_cv(spikes, sched, min_spikes=5):
    types = spikes["types"]
    t0, t1 = sched["settle_ms"], sched["settle_ms"] + sched["rest_ms"]
    t, g = spikes["t_ms"], spikes["gid"]
    cvs = []
    for i in np.nonzero(types != "FSI")[0]:
        s = np.sort(t[(g == i) & (t >= t0) & (t < t1)])
        if len(s) >= min_spikes:
            d = np.diff(s)
            cvs.append(d.std() / d.mean())
    return {"mean": float(np.mean(cvs)) if cvs else None, "cells": len(cvs)}


def threat_response(spikes, sched):
    types = spikes["types"]
    n = len(types)
    out = {}
    for tr in sched["trials"]:
        pre = _counts(spikes, tr["threat_on_ms"] - 2000, tr["threat_on_ms"], n) / 2.0
        dur = _counts(spikes, tr["threat_on_ms"], tr["threat_off_ms"], n) / ((tr["threat_off_ms"] - tr["threat_on_ms"]) / 1000.0)
        late = _counts(spikes, tr["end_ms"] - 2000, tr["end_ms"], n) / 2.0
        d = out.setdefault(str(tr["dose"]), {"PN_pre": [], "PN_threat": [], "PN_late_post": [],
                                              "FSI_pre": [], "FSI_threat": []})
        for k, arr in (("pre", pre), ("threat", dur)):
            d[f"PN_{k}"].append(float(arr[types != "FSI"].mean()))
            d[f"FSI_{k}"].append(float(arr[types == "FSI"].mean()))
        d["PN_late_post"].append(float(late[types != "FSI"].mean()))
    summary = {}
    for dose, d in out.items():
        summary[dose] = {k: float(np.mean(v)) for k, v in d.items()}
        summary[dose]["PN_response_Hz"] = summary[dose]["PN_threat"] - summary[dose]["PN_pre"]
        summary[dose]["FSI_response_Hz"] = summary[dose]["FSI_threat"] - summary[dose]["FSI_pre"]
        summary[dose]["trials"] = len(d["PN_pre"])
    return summary


def all_metrics(spikes, sched, seed):
    rates, _ = rest_rates(spikes, sched)
    w = rest_windows(spikes, sched)
    return {"rest": rates,
            "rest_range_PN_Hz": {"mean": float(w.mean()), "sd": float(w.std()),
                                 "low": float(w.mean() - 2 * w.std()), "high": float(w.mean() + 2 * w.std())},
            "synchrony": synchrony(spikes, sched, seed),
            "isi_cv": isi_cv(spikes, sched),
            "threat": threat_response(spikes, sched)}
