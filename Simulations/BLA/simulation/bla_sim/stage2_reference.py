"""Stage-2 reference for the simplified cells (spec 14, gate S1): Feng's full cells under noise.

Block A measured the noise-only rates on one cell per type (60 s) and the dendritic-input test
on 8 cells per type with one noise seed. With ~20-100 spikes per measure, the sampling error
(~10-20 %) is as large as the S1 tolerance. This script repeats both with more samples:
  noise only:      10 cells per type (PN-A, PN-C, FSI), each 60 s after 2 s, own noise streams;
  dendritic input: the Block A setup (8 + 8 cells, 3 of Feng's afferent trains each on the
                   dendrite, weights lognormal(9, 0.05), delays U(0.5, 1) ms) with noise seeds 1-3.
It also exports the afferent trains, weights and delays used, so the simplified cells get
exactly the same input.

Usage (from Simulations/BLA/simulation): python -m bla_sim.stage2_reference
Writes outputs/blockA/stage2_reference.json and drive_test_inputs.npz.
"""
import json
import time

import numpy as np

from . import cells as C
from .drive_test import N_PER_KIND, RUN_MS, SETTLE_MS, TRAINS_PER_CELL
from .inputs import load_feng_trains
from .network import lognormal_params, stream
from .nrn import OUTPUT_DIR, load_config, setup
from .provenance import run_metadata

NOISE_CELLS, NOISE_MS, NOISE_SETTLE = 10, 60000.0, 2000.0
DRIVE_SEEDS = (1, 2, 3)


def isi_cv(t):
    d = np.diff(t)
    return float(d.std() / d.mean()) if len(d) >= 2 else None


def noise_only(h, cfg):
    out = {}
    keep, spk, kinds = [], [], []
    h.Random().Random123_globalindex(1)
    for k_i, kind in enumerate(("PN_A", "PN_C", "FSI")):
        for j in range(NOISE_CELLS):
            gid = 100 * k_i + j
            cell = C.make_cell(h, kind, "full")
            keep += C.attach_noise(h, cell, kind, gid=gid, n_total=1000, cfg=cfg)
            nc, vec = C.spike_detector(h, cell)
            keep += [cell, nc]
            spk.append(vec)
            kinds.append(kind)
    h.finitialize(cfg["simulation"]["v_init_mV"])
    h.continuerun(NOISE_SETTLE + NOISE_MS)
    for kind in ("PN_A", "PN_C", "FSI"):
        rates, cvs = [], []
        for v, k in zip(spk, kinds):
            if k != kind:
                continue
            t = np.array(v)
            t = t[t >= NOISE_SETTLE]
            rates.append(len(t) / (NOISE_MS / 1000.0))
            cvs.append(isi_cv(t))
        c = [x for x in cvs if x is not None]
        out[kind] = {"rates_Hz": rates, "mean_Hz": float(np.mean(rates)),
                     "sem_Hz": float(np.std(rates, ddof=1) / np.sqrt(len(rates))),
                     "isi_cv_mean": float(np.mean(c)) if c else None}
    del keep
    return out


def drive(h, cfg, seed, export):
    trains = load_feng_trains(TRAINS_PER_CELL * 2 * N_PER_KIND)
    a = cfg["afferents"]
    mu, sigma = lognormal_params(*a["weight_mean_var_PN"])
    rng = stream(1, "aff_weights")
    keep, spk = [], []
    h.Random().Random123_globalindex(seed)
    kinds = ["PN_A"] * N_PER_KIND + ["PN_C"] * N_PER_KIND
    for j, kind in enumerate(kinds):
        cell = C.make_cell(h, kind, "full")
        keep += C.attach_noise(h, cell, kind, gid=j, n_total=1000, cfg=cfg)
        for k in range(TRAINS_PER_CELL):
            times = trains[TRAINS_PER_CELL * j + k]
            times = times[times < SETTLE_MS + RUN_MS]
            vec = h.Vector(times)
            vs = h.VecStim()
            vs.play(vec)
            w, d = rng.lognormal(mu, sigma), rng.uniform(*a["delay_uniform_ms"])
            syn = h.pyrD2pyrD_STFD(cell.dend(0.9))
            syn.initW = float(w)
            nc = h.NetCon(vs, syn)
            nc.weight[0] = 1.0
            nc.delay = float(d)
            keep += [vec, vs, nc, syn]
            if export is not None:
                export["cell"].append(j)
                export["weight"].append(float(w))
                export["delay_ms"].append(float(d))
                export["times"].append(np.asarray(times, float))
        nc_s, vec_s = C.spike_detector(h, cell)
        keep += [cell, nc_s]
        spk.append(vec_s)
    h.finitialize(cfg["simulation"]["v_init_mV"])
    h.continuerun(SETTLE_MS + RUN_MS)
    rates = [sum(1 for s in v if s >= SETTLE_MS) / (RUN_MS / 1000.0) for v in spk]
    del keep
    return kinds, rates


def main():
    cfg = load_config()
    h = setup(cfg)
    out = {"meta": run_metadata(h), "noise_only": None, "drive": {}}
    t0 = time.perf_counter()
    out["noise_only"] = noise_only(h, cfg)
    print("noise only:", {k: round(v["mean_Hz"], 3) for k, v in out["noise_only"].items()},
          f"[{time.perf_counter() - t0:.0f} s]", flush=True)
    export = {"cell": [], "weight": [], "delay_ms": [], "times": []}
    for seed in DRIVE_SEEDS:
        kinds, rates = drive(h, cfg, seed, export if seed == DRIVE_SEEDS[0] else None)
        r, k = np.array(rates), np.array(kinds)
        out["drive"][str(seed)] = {"rates_Hz": rates, "PN_A_mean_Hz": float(r[k == "PN_A"].mean()),
                                   "PN_C_mean_Hz": float(r[k == "PN_C"].mean())}
        print(f"drive seed {seed}: PN-A {r[k == 'PN_A'].mean():.2f} Hz, PN-C {r[k == 'PN_C'].mean():.2f} Hz "
              f"[{time.perf_counter() - t0:.0f} s]", flush=True)
    allr = {kind: np.concatenate([np.array(v["rates_Hz"])[np.array(kinds) == kind] for v in out["drive"].values()])
            for kind in ("PN_A", "PN_C")}
    out["drive_summary"] = {kind: {"mean_Hz": float(v.mean()), "sem_Hz": float(v.std(ddof=1) / np.sqrt(len(v)))}
                            for kind, v in allr.items()}
    d = OUTPUT_DIR / "blockA"
    (d / "stage2_reference.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    lens = np.array([len(x) for x in export["times"]])
    np.savez_compressed(d / "drive_test_inputs.npz", kinds=np.array(kinds), cell=np.array(export["cell"]),
                        weight=np.array(export["weight"]), delay_ms=np.array(export["delay_ms"]),
                        times=np.concatenate(export["times"]), offsets=np.concatenate([[0], np.cumsum(lens)]),
                        settle_ms=SETTLE_MS, run_ms=RUN_MS)
    print("drive summary:", {k: (round(v["mean_Hz"], 2), round(v["sem_Hz"], 2)) for k, v in out["drive_summary"].items()})


if __name__ == "__main__":
    main()
