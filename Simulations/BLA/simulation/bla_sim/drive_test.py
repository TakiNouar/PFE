"""Single principal cells driven by Feng's afferent spike trains on the dendrite (Gate R1, synaptic part).

Each cell gets Feng's background noise at the soma plus three of Feng's afferent trains
through Feng's afferent synapse (pyrD2pyrD_STFD at dend(0.9), weight lognormal(9, 0.05))
or, for reduced cells, the event-driven ExcEv at the same place. Every level receives the
same trains, weights, delays and noise streams, so only the cell differs.

Usage (from Simulations/BLA/simulation):
    python -m bla_sim.drive_test --levels full twopiece coarse2 coarse4
Writes outputs/blockA/drive_test.json.
"""
import argparse
import json
import time

import numpy as np

from . import cells as C
from .inputs import load_feng_trains
from .network import lognormal_params, stream
from .nrn import OUTPUT_DIR, load_config, setup
from .provenance import run_metadata

N_PER_KIND = 8
SETTLE_MS, RUN_MS = 2000.0, 20000.0
TRAINS_PER_CELL = 3


def run_level(h, cfg, level):
    trains = load_feng_trains(TRAINS_PER_CELL * 2 * N_PER_KIND)
    a = cfg["afferents"]
    mu, sigma = lognormal_params(*a["weight_mean_var_PN"])
    rng = stream(1, "aff_weights")
    keep, spk, cells = [], [], []
    h.Random().Random123_globalindex(1)
    kinds = ["PN_A"] * N_PER_KIND + ["PN_C"] * N_PER_KIND
    for j, kind in enumerate(kinds):
        cell = C.make_cell(h, kind, level)
        keep += C.attach_noise(h, cell, kind, gid=j, n_total=1000, cfg=cfg)
        ev = None if level == "full" else h.ExcEv(cell.dend(0.9))
        for k in range(TRAINS_PER_CELL):
            times = trains[TRAINS_PER_CELL * j + k]
            vec = h.Vector(times[times < SETTLE_MS + RUN_MS])
            vs = h.VecStim()
            vs.play(vec)
            w, d = rng.lognormal(mu, sigma), rng.uniform(*a["delay_uniform_ms"])
            if level == "full":
                syn = h.pyrD2pyrD_STFD(cell.dend(0.9))
                syn.initW = float(w)
                nc = h.NetCon(vs, syn)
                nc.weight[0] = 1.0
                keep.append(syn)
            else:
                nc = h.NetCon(vs, ev)
                nc.weight[0] = float(w)
            nc.delay = float(d)
            keep += [vec, vs, nc]
        if ev is not None:
            keep.append(ev)
        nc_s, vec_s = C.spike_detector(h, cell)
        keep.append(nc_s)
        spk.append(vec_s)
        cells.append(cell)
    h.finitialize(cfg["simulation"]["v_init_mV"])
    t0 = time.perf_counter()
    h.continuerun(SETTLE_MS + RUN_MS)
    wall = time.perf_counter() - t0
    rates = [sum(1 for s in v if s >= SETTLE_MS) / (RUN_MS / 1000.0) for v in spk]
    del keep, cells
    return kinds, rates, wall


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--levels", nargs="+", default=["full"] + list(C.REDUCED_LEVELS))
    args = ap.parse_args()
    cfg = load_config()
    h = setup(cfg)
    meta = run_metadata(h)
    path = OUTPUT_DIR / "blockA" / "drive_test.json"
    out = {"meta": meta, "settle_ms": SETTLE_MS, "run_ms": RUN_MS, "cells_per_kind": N_PER_KIND,
           "trains_per_cell": TRAINS_PER_CELL, "levels": {}}
    if path.exists():   # keep earlier levels (the full-detail run takes ~10 min)
        out["levels"] = json.loads(path.read_text(encoding="utf-8"))["levels"]
    for level in args.levels:
        kinds, rates, wall = run_level(h, cfg, level)
        r = np.array(rates)
        k = np.array(kinds)
        out["levels"][level] = {"rates_Hz": rates, "wall_s": wall,
                                "PN_A_mean_Hz": float(r[k == "PN_A"].mean()),
                                "PN_C_mean_Hz": float(r[k == "PN_C"].mean())}
        print(f"{level:9s}: PN-A {r[k == 'PN_A'].mean():.2f} Hz, PN-C {r[k == 'PN_C'].mean():.2f} Hz "
              f"(per cell: {np.round(r, 2).tolist()}) [{wall:.0f} s]")
    if "full" in out["levels"]:
        f = np.array(out["levels"]["full"]["rates_Hz"])
        for level, v in out["levels"].items():
            rr = np.array(v["rates_Hz"])
            v["mean_rate_ratio_vs_full"] = float(rr.mean() / f.mean()) if f.mean() else None
    for stale in [k for k in out["levels"] if k not in ("full",) + C.REDUCED_LEVELS]:
        out["levels"].pop(stale)
    path.write_text(json.dumps(out, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
