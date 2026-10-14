"""Afferent spike trains and the threat input (architecture/06).

Feng's 1,800 surrogate trains (recorded cortical cells, Headley et al. 2015) come from
ModelDB 247968 input/spikesmatrix_op and input/spikes_ind; Run 1 uses the first M.
The threat (DEV-005) adds Poisson spikes to every train during a threat window so that
its rate is multiplied by the dose D.
"""
import numpy as np

from .network import lognormal_params, stream
from .nrn import FENG_DIR


def load_feng_trains(n_trains):
    ind = np.array((FENG_DIR / "input" / "spikes_ind").read_text().split(), dtype=float).reshape(-1, 2)
    times = np.array((FENG_DIR / "input" / "spikesmatrix_op").read_text().split(), dtype=float)
    if n_trains > len(ind):
        raise ValueError(f"only {len(ind)} trains in Feng's file")
    return [times[int(a):int(b) + 1] if a <= b else np.array([]) for a, b in ind[:n_trains]]


def train_layout(types, cfg):
    a = cfg["afferents"]
    n_pn = int((types != "FSI").sum())
    n_fsi = int((types == "FSI").sum())
    m = max(1, round(a["trains_per_PN"] * n_pn / a["PNs_per_train"]))
    k_fsi = round(a["trains_per_FSI"] * n_fsi / m)
    return m, min(a["PNs_per_train"], n_pn), min(k_fsi, n_fsi)


def build_trains(types, cfg, seed, t_end, threat_windows):
    """Spike times per train for the whole run: Feng's train (looped if needed) + threat spikes.

    threat_windows: list of (start_ms, stop_ms, dose).
    """
    a = cfg["afferents"]
    m, _, _ = train_layout(types, cfg)
    base = load_feng_trains(m)
    rng = stream(seed, "threat")
    L = a["train_length_ms"]
    out, rates = [], []
    for tr in base:
        rate_per_ms = len(tr) / L
        rates.append(rate_per_ms * 1000.0)
        reps = int(np.ceil(t_end / L))
        times = np.concatenate([tr + k * L for k in range(reps)]) if len(tr) else np.array([])
        extra = []
        for start, stop, dose in threat_windows:
            n_extra = rng.poisson((dose - 1) * rate_per_ms * (stop - start))
            extra.append(rng.uniform(start, stop, size=n_extra))
        times = np.sort(np.concatenate([times] + extra)) if extra else times
        out.append(times[times < t_end])
    return out, np.array(rates)


def connect_afferents(net, trains):
    """Feng's afferent wiring at our size: each train -> 40 PNs and k FSIs (architecture/06)."""
    h, cfg, types = net.h, net.cfg, net.types
    a = cfg["afferents"]
    m, n_pn_per, k_fsi = train_layout(types, cfg)
    pn = np.nonzero(types != "FSI")[0]
    fsi = np.nonzero(types == "FSI")[0]
    r_t, r_w = stream(net.seed, "aff_targets"), stream(net.seed, "aff_weights")
    mu_p, s_p = lognormal_params(*a["weight_mean_var_PN"])
    mu_f, s_f = lognormal_params(*a["weight_mean_var_FSI"])
    lo, hi = a["delay_uniform_ms"]
    keep, n_conn = [], 0
    for times in trains:
        vec = h.Vector(times)
        vs = h.VecStim()
        vs.play(vec)
        keep += [vec, vs]
        targets = [(int(g), "PN") for g in r_t.choice(pn, n_pn_per, replace=False)]
        if k_fsi > 0:
            targets += [(int(g), "FSI") for g in r_t.choice(fsi, k_fsi, replace=False)]
        for gid, kind in targets:
            w = r_w.lognormal(mu_p, s_p) if kind == "PN" else r_w.lognormal(mu_f, s_f)
            d = r_w.uniform(lo, hi)
            if net.level == "full":
                syn = getattr(h, "pyrD2pyrD_STFD" if kind == "PN" else "pyrD2interD_STFD")(net.cells[gid].dend(0.9))
                syn.initW = float(w)
                nc = h.NetCon(vs, syn)
                nc.weight[0] = 1.0
                keep.append(syn)
            else:
                nc = h.NetCon(vs, net.exc_target(gid, "aff"))
                nc.weight[0] = float(w)
            nc.delay = float(d)
            keep.append(nc)
            n_conn += 1
    net._keep += keep
    return {"trains": m, "PNs_per_train": n_pn_per, "FSIs_per_train": k_fsi, "connections": n_conn}
