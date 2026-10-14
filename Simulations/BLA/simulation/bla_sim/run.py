"""Run one network simulation (architecture/07): build, schedule, advance in chunks, save.

Usage (from Simulations/BLA/simulation):
    python -m bla_sim.run --block B --level full --n 200 --seed 1
    python -m bla_sim.run --block C_main --level reduced --n 1000 --seed 1
Blocks:
    B        settle, rest, 3 threat trials at x4                (Block B, Gate R2)
    C_main   settle, rest, 5 trials at each of x2, x4, x8        (C1-C3)
    C_rest   settle, rest                                        (C4 size check, C7 reproducibility)
    C_inhoff settle, rest, 5 trials at x4, FSI->PN weights at 0  (C5)
    C_nmda   settle, rest, PN->PN AMPA off                       (C6 diagnostic)
    C_noff   settle, rest, PN->PN connections removed            (C6 diagnostic)
    bench    0.2 s warm-up, then 1 s timed                        (Phase 0)
    demo     0.2 s settle, 0.8 s rest, one x8 trial (0.5 s before, 1 s threat, 1 s after);
             a few minutes at 100 cells, to see the live viewer working (no gate uses it)
Writes outputs/<block>_<level>_n<N>/seed<seed>/: spikes.npz, run.json (parameters,
network summary, schedule, timing).
--broadcast writes live snapshots for the viewer (architecture/13, display only; off by default,
and must stay off for the C7 reproducibility run).
Benchmark-only options (Phase 0, never for gate runs): --no-synapses (cells and noise
only: no internal connections, gap junctions or afferents) and --dt <ms>.
"""
import argparse
import copy
import json
import time

import numpy as np

from .inputs import build_trains, connect_afferents
from .network import Network
from .nrn import OUTPUT_DIR, load_config, setup
from .provenance import run_metadata

BLOCKS = {
    "B": {"trials": [4, 4, 4]},
    "C_main": {"trials": "doses"},
    "C_rest": {"trials": []},
    "C_inhoff": {"trials": [4] * 5, "inhibition_off": True},
    "C_nmda": {"trials": [], "pnpn_ampa_off": True},
    "C_noff": {"trials": [], "pnpn_off": True},
    "bench": {"trials": [], "bench": True},
    "demo": {"trials": [8], "demo": True},
}


def schedule(block, cfg):
    p, th = cfg["protocol"], cfg["threat"]
    spec = BLOCKS[block]
    if spec.get("bench"):
        return {"settle_ms": 200.0, "rest_ms": 1000.0, "trials": [], "t_end_ms": 1200.0}
    if spec.get("demo"):
        return {"settle_ms": 200.0, "rest_ms": 800.0, "t_end_ms": 3500.0,
                "trials": [{"dose": 8, "start_ms": 1000.0, "threat_on_ms": 1500.0, "threat_off_ms": 2500.0,
                            "end_ms": 3500.0}]}
    doses = spec["trials"]
    if doses == "doses":
        doses = [d for d in th["doses"] for _ in range(th["trials_per_dose"])]
    t = p["settle_ms"] + p["rest_ms"]
    trials = []
    for dose in doses:
        trials.append({"dose": dose, "start_ms": t, "threat_on_ms": t + th["pre_ms"],
                       "threat_off_ms": t + th["pre_ms"] + th["threat_ms"],
                       "end_ms": t + th["pre_ms"] + th["threat_ms"] + th["post_ms"]})
        t = trials[-1]["end_ms"]
    return {"settle_ms": p["settle_ms"], "rest_ms": p["rest_ms"], "trials": trials, "t_end_ms": t}


def simulate(block, level, n, seed, cfg=None, on_chunk=None, log=print, variant=None, on_start=None):
    """variant (benchmark only): {"no_synapses": bool, "dt_ms": float}.
    on_start(net, tvec, idvec, sched) runs once before finitialize; on_chunk(net, t, tvec, idvec,
    sched) after every chunk (live viewer hooks; display only)."""
    cfg = copy.deepcopy(cfg or load_config())
    variant = variant or {}
    if variant.get("dt_ms"):
        cfg["simulation"]["dt_ms"] = float(variant["dt_ms"])
    synapses = not variant.get("no_synapses", False)
    h = setup(cfg)
    meta = run_metadata(h)
    sched = schedule(block, cfg)
    t0 = time.perf_counter()
    net = Network(h, cfg, n, level, seed).build(synapses=synapses)
    windows = [(tr["threat_on_ms"], tr["threat_off_ms"], tr["dose"]) for tr in sched["trials"]]
    trains, rates = build_trains(net.types, cfg, seed, sched["t_end_ms"], windows)
    aff = connect_afferents(net, trains) if synapses else {"trains": 0, "connections": 0}
    spec = BLOCKS[block]
    if spec.get("inhibition_off"):
        net.set_pathway_weight_factor("FSI_PN", 0.0)
    if spec.get("pnpn_off"):
        net.set_pathway_weight_factor("PN_PN", 0.0)
    if spec.get("pnpn_ampa_off"):
        net.set_pnpn_ampa(False)
    tvec, idvec = h.Vector(), h.Vector()
    net.pc.spike_record(-1, tvec, idvec)
    build_s = time.perf_counter() - t0
    wiring = (f"{net.summary()['connections']} connections, {aff['trains']} afferent trains, "
              f"{len(net.gaps)} gap pairs" if synapses else "no synapses (noise only)")
    log(f"[{block} {level} n={n} seed={seed}{' ' + str(variant) if variant else ''}] built in {build_s:.1f} s: "
        f"{wiring}; simulating {sched['t_end_ms'] / 1000:g} s")

    if on_start is not None:
        on_start(net, tvec, idvec, sched)
    h.finitialize(cfg["simulation"]["v_init_mV"])
    chunk = cfg["protocol"]["chunk_ms"]
    t_end = sched["t_end_ms"]
    t_start = time.perf_counter()
    timed_from = sched["settle_ms"] if spec.get("bench") else 0.0
    t_timed = None
    t = 0.0
    next_log = time.perf_counter() + 60
    while t < t_end - 1e-9:
        t = min(t + chunk, t_end)
        net.pc.psolve(t)
        if t_timed is None and t >= timed_from:
            t_timed = time.perf_counter()
        if on_chunk is not None:
            on_chunk(net, t, tvec, idvec, sched)
        if time.perf_counter() > next_log:
            el = time.perf_counter() - t_start
            log(f"  t = {t / 1000:.2f} s simulated, {el / 60:.1f} min elapsed, "
                f"~{el / t * (t_end - t) / 60:.0f} min left")
            next_log = time.perf_counter() + 300
    wall = time.perf_counter() - t_start
    timed_wall = time.perf_counter() - (t_timed or t_start)
    timed_sim_s = (t_end - timed_from) / 1000.0
    rtf = timed_wall / timed_sim_s
    import psutil
    mi = psutil.Process().memory_info()
    mem_mb = mi.rss / 1e6
    peak_mb = getattr(mi, "peak_wset", mi.rss) / 1e6      # Windows: peak working set

    out = {"meta": meta, "block": block, "level": level, "n": n, "seed": seed,
           "schedule": sched, "network": net.summary(), "afferents": aff,
           "afferent_train_rates_Hz": {"mean": float(rates.mean()), "min": float(rates.min()), "max": float(rates.max())},
           "conditions": {k: v for k, v in spec.items() if k != "trials"}, "variant": variant,
           "broadcast": on_start is not None,
           "timing": {"build_s": build_s, "simulate_wall_s": wall, "real_time_factor": rtf,
                      "memory_MB": mem_mb, "peak_memory_MB": peak_mb},
           "config": cfg}
    spikes = {"t_ms": np.array(tvec), "gid": np.array(idvec).astype(np.int32), "types": net.types}
    return out, spikes, net


def save(out, spikes, run_dir):
    run_dir.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(run_dir / "spikes.npz", **spikes)
    (run_dir / "run.json").write_text(json.dumps(out, indent=1, default=str), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--block", choices=list(BLOCKS), required=True)
    ap.add_argument("--level", choices=("full", "reduced"), required=True)
    ap.add_argument("--n", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--tag", default="")
    ap.add_argument("--no-synapses", action="store_true", help="benchmark only: cells and noise only")
    ap.add_argument("--dt", type=float, default=None, help="benchmark only: time step in ms")
    ap.add_argument("--broadcast", action="store_true", help="write live/ snapshots for the viewer")
    args = ap.parse_args()
    variant = {}
    if args.no_synapses or args.dt:
        if args.block != "bench":
            ap.error("--no-synapses and --dt are for --block bench only")
        variant = {"no_synapses": args.no_synapses, "dt_ms": args.dt}
    name = f"{args.block}_{args.level}_n{args.n}" + (f"_{args.tag}" if args.tag else "")
    run_dir = OUTPUT_DIR / name / f"seed{args.seed}"
    hooks = {}
    if args.broadcast:
        from .broadcast import Broadcaster
        b = Broadcaster(run_dir, args.block, args.level, args.n, args.seed)
        hooks = {"on_start": b.start, "on_chunk": b.on_chunk}
    out, spikes, _ = simulate(args.block, args.level, args.n, args.seed, variant=variant, **hooks)
    save(out, spikes, run_dir)
    n_spk = len(spikes["t_ms"])
    print(f"done: {n_spk} spikes, real-time factor {out['timing']['real_time_factor']:.1f}, "
          f"{out['timing']['memory_MB']:.0f} MB -> {run_dir}")


if __name__ == "__main__":
    main()
