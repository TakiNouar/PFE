"""Block A single-cell protocol (architecture/07), for either level.

Usage (from Simulations/BLA/simulation):
    python -m bla_sim.single_cell --level full
    python -m bla_sim.single_cell --level onepiece
Writes outputs/blockA/single_cells_<level>.json and .png.
"""
import argparse
import json
import time

import numpy as np

from . import cells as C
from .nrn import OUTPUT_DIR, load_config, setup
from .provenance import run_metadata


def _run(h, t_end):
    h.finitialize(h.v_init)
    h.continuerun(t_end)


def _clamp(h, cell, delay, dur, amp):
    stim = h.IClamp(cell.soma(0.5))
    setattr(stim, "del", delay)          # "del" is a Python keyword
    stim.dur = dur
    stim.amp = amp
    return stim


def passive(h, kind, level, p):
    cell = C.make_cell(h, kind, level)
    stim = _clamp(h, cell, p["settle_ms"], p["passive_step_ms"], p["passive_step_nA"])
    tv = h.Vector().record(h._ref_t)
    vv = h.Vector().record(cell.soma(0.5)._ref_v)
    t_on = p["settle_ms"]
    _run(h, t_on + p["passive_step_ms"] + 50)
    t, v = np.array(tv), np.array(vv)
    vrest = v[(t >= t_on - 100) & (t < t_on)].mean()
    v_ss = v[(t >= t_on + p["passive_step_ms"] - 50) & (t < t_on + p["passive_step_ms"])].mean()
    dv = v_ss - vrest
    step = (t >= t_on) & (t < t_on + p["passive_step_ms"])
    reached = np.nonzero((v[step] - vrest) <= 0.632 * dv)[0]
    tau = float(t[step][reached[0]] - t_on) if len(reached) else float("nan")
    peak = (v[step] - vrest).min()
    del stim
    return {"vrest_mV": float(vrest), "rin_MOhm": float(dv / p["passive_step_nA"]),
            "tau_ms": tau, "sag_ratio": float(dv / peak) if peak else float("nan")}


def step_response(h, kind, level, amp, dur, p, keep_trace=False):
    cell = C.make_cell(h, kind, level)
    t_on = p["settle_ms"]
    stim = _clamp(h, cell, t_on, dur, amp)
    nc, spk = C.spike_detector(h, cell)
    rec = None
    if keep_trace:
        rec = h.Vector().record(cell.soma(0.5)._ref_v, p["trace_interval_ms"])
    _run(h, t_on + dur + 100)
    st = [s - t_on for s in spk if t_on <= s < t_on + dur]
    isi = np.diff(st)
    out = {"amp_nA": amp, "dur_ms": dur, "count": len(st),
           "spike_times_ms": [round(s, 3) for s in st],
           "latency_ms": st[0] if st else None,
           "adaptation_ratio": float(isi[-1] / isi[0]) if len(isi) >= 2 else None}
    if keep_trace:
        out["_trace"] = np.array(rec)
    del stim, nc
    return out


def noise_only(h, kind, level, cfg, p):
    cell = C.make_cell(h, kind, level)
    h.Random().Random123_globalindex(p["noise_seed"])
    keep = C.attach_noise(h, cell, kind, gid=0, n_total=1, cfg=cfg)
    nc, spk = C.spike_detector(h, cell)
    rec = h.Vector().record(cell.soma(0.5)._ref_v, p["trace_interval_ms"])
    t0 = p["noise_settle_ms"]
    _run(h, t0 + p["noise_only_ms"])
    st = np.array([s for s in spk if s >= t0])
    isi = np.diff(st)
    out = {"duration_s": p["noise_only_ms"] / 1000, "count": int(len(st)),
           "rate_Hz": float(len(st) / (p["noise_only_ms"] / 1000)),
           "isi_cv": float(isi.std() / isi.mean()) if len(isi) >= 2 else None,
           "seed": p["noise_seed"]}
    v = np.array(rec)
    i0 = int(t0 / p["trace_interval_ms"])
    out["_trace"] = v[i0:i0 + int(5000 / p["trace_interval_ms"])]
    del keep, nc
    return out


def gap_coupling(h, cfg, p):
    """Coupling coefficient of one HalfGap pair between two FSIs (Feng's wiring)."""
    a, b = C.make_cell(h, "FSI"), C.make_cell(h, "FSI")
    pc = h.ParallelContext()
    gaps = []
    for me, other, my_id, other_id in ((a, b, 900001, 900002), (b, a, 900002, 900001)):
        g = h.HalfGap(me.soma(0.5))
        pc.target_var(g, g._ref_vgap, other_id)
        pc.source_var(me.soma(0.5)._ref_v, my_id, sec=me.soma)
        g.r = cfg["gap_junction"]["r_megohm"]
        gaps.append(g)
    pc.setup_transfer()
    stim = _clamp(h, a, p["settle_ms"], p["gap_step_ms"], p["gap_step_nA"])
    tv = h.Vector().record(h._ref_t)
    va = h.Vector().record(a.soma(0.5)._ref_v)
    vb = h.Vector().record(b.soma(0.5)._ref_v)
    _run(h, p["settle_ms"] + p["gap_step_ms"])
    t, va, vb = np.array(tv), np.array(va), np.array(vb)
    t_on, t_end = p["settle_ms"], p["settle_ms"] + p["gap_step_ms"]
    base = (t >= t_on - 100) & (t < t_on)
    ss = (t >= t_end - 50) & (t < t_end)
    dva = va[ss].mean() - va[base].mean()
    dvb = vb[ss].mean() - vb[base].mean()
    del stim, gaps
    return {"r_megohm": cfg["gap_junction"]["r_megohm"], "dV_injected_mV": float(dva),
            "dV_partner_mV": float(dvb), "coupling_coefficient": float(dvb / dva)}


def run_protocol(h, level, cfg, kinds=C.KINDS, log=print):
    p = cfg["single_cell_protocol"]
    results, traces = {}, {}
    for kind in kinds:
        t0 = time.perf_counter()
        r = {"passive": passive(h, kind, level, p)}
        r["ladder"] = [step_response(h, kind, level, a, p["ladder_step_ms"], p,
                                     keep_trace=a in (0.4, 1.0)) for a in p["ladder_nA"]]
        r["long_steps"] = [step_response(h, kind, level, a, p["long_step_ms"], p, keep_trace=True)
                           for a in p["long_steps_nA"]]
        r["noise_only"] = noise_only(h, kind, level, cfg, p)
        traces[kind] = {
            "ladder": {s["amp_nA"]: s.pop("_trace") for s in r["ladder"] if "_trace" in s},
            "long": {s["amp_nA"]: s.pop("_trace") for s in r["long_steps"]},
            "noise": r["noise_only"].pop("_trace"),
        }
        r["wall_s"] = round(time.perf_counter() - t0, 1)
        n_sec = sum(1 for _ in h.allsec())
        if n_sec > 40:   # old cells must be freed, or every later run also simulates them
            log(f"WARNING: {n_sec} sections still exist after {kind}; cells are not being freed")
        results[kind] = r
        log(f"{level:8s} {kind:5s} done in {r['wall_s']} s: Vrest {r['passive']['vrest_mV']:.1f} mV, "
            f"Rin {r['passive']['rin_MOhm']:.0f} MOhm, tau {r['passive']['tau_ms']:.1f} ms, "
            f"ladder counts {[s['count'] for s in r['ladder']]}, "
            f"noise {r['noise_only']['rate_Hz']:.2f} Hz")
    return results, traces


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--level", choices=("full",) + C.REDUCED_LEVELS, default="full")
    args = ap.parse_args()
    cfg = load_config()
    h = setup(cfg)
    meta = run_metadata(h)
    kinds = C.KINDS if args.level == "full" else ("PN_A", "PN_C")
    results, traces = run_protocol(h, args.level, cfg, kinds)
    out = {"meta": meta, "level": args.level, "protocol": cfg["single_cell_protocol"], "cells": results}
    if args.level == "full":
        out["gap"] = gap_coupling(h, cfg, cfg["single_cell_protocol"])
        print(f"gap coupling coefficient {out['gap']['coupling_coefficient']:.3f}")
    d = OUTPUT_DIR / "blockA"
    d.mkdir(parents=True, exist_ok=True)
    (d / f"single_cells_{args.level}.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    np.savez_compressed(d / f"traces_{args.level}.npz",
                        **{f"{k}|{part}|{a}": v for k, tr in traces.items()
                           for part in ("ladder", "long") for a, v in tr[part].items()},
                        **{f"{k}|noise|0": tr["noise"] for k, tr in traces.items()})
    from .plots import single_cell_figure
    single_cell_figure(out, traces, d / f"single_cells_{args.level}.png",
                       cfg["single_cell_protocol"]["trace_interval_ms"])
    print(f"wrote {d / f'single_cells_{args.level}.json'}")


if __name__ == "__main__":
    main()
