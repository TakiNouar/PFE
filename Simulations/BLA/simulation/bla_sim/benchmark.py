"""Phase 0 speed benchmark (architecture/07): one row = one or more `run --block bench` processes.

Usage (from Simulations/BLA/simulation):
    python -m bla_sim.benchmark                 # every row, in order (~1 h on the laptop)
    python -m bla_sim.benchmark --rows R200 R500
    python -m bla_sim.benchmark --list
Each row runs in fresh processes (0.2 s warm-up, then 1 s timed). Rows run one after the
other, so they do not slow each other down; only the parallel row starts several at once.
Writes outputs/benchmark/: benchmark.csv, benchmark.json (rows, machine state, Block B/C
estimates) and logs/<row>.log. Results are rewritten after every row.
"""
import argparse
import csv
import json
import subprocess
import sys
import time
from datetime import datetime

import numpy as np

from .metrics import rest_rates
from .nrn import OUTPUT_DIR, SIM_DIR, load_config
from .run import schedule

BENCH_DIR = OUTPUT_DIR / "benchmark"

# id, purpose, level, n, extra run.py arguments, parallel processes (seeds 1..k)
ROWS = [
    ("R200", "Main level, 200 cells (Block B, reduced half)", "reduced", 200, [], 1),
    ("R500", "Main level, 500 cells (C4 size check)", "reduced", 500, [], 1),
    ("R1000", "Main level, 1,000 cells (Block C)", "reduced", 1000, [], 1),
    ("R1000_nosyn", "Main level, 1,000 cells, cells and noise only: cost of synapses (U26)",
     "reduced", 1000, ["--no-synapses"], 1),
    ("R1000_dt01", "Main level, 1,000 cells, dt 0.1 ms (information only)", "reduced", 1000, ["--dt", "0.1"], 1),
    ("F200", "Reference level, 200 cells (Block B, full half)", "full", 200, [], 1),
    ("R1000_par5", "Main level, 1,000 cells, 5 processes at once (seeds 1-5): parallel throughput",
     "reduced", 1000, [], 5),
    ("R1000_live", "Main level, 1,000 cells, live broadcast on: the viewer's overhead",
     "reduced", 1000, ["--broadcast"], 1),
]
PENDING = []


def tag_of(row_id):
    return "phase0_" + row_id


def machine_state():
    import psutil
    st = {"logical_cpus": psutil.cpu_count(), "physical_cores": psutil.cpu_count(logical=False),
          "ram_GB": round(psutil.virtual_memory().total / 1e9, 1)}
    bat = psutil.sensors_battery()
    st["power_plugged"] = None if bat is None else bool(bat.power_plugged)
    st["battery_percent"] = None if bat is None else bat.percent
    try:
        st["power_scheme"] = subprocess.run(["powercfg", "/getactivescheme"], capture_output=True,
                                            text=True, timeout=10).stdout.strip()
    except Exception as e:          # information only
        st["power_scheme"] = f"unknown ({e})"
    return st


def run_row(row):
    row_id, purpose, level, n, extra, k = row
    logs = BENCH_DIR / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    started = datetime.now().isoformat(timespec="seconds")
    state = machine_state()
    procs = []
    t0 = time.perf_counter()
    for seed in range(1, k + 1):
        cmd = [sys.executable, "-m", "bla_sim.run", "--block", "bench", "--level", level, "--n", str(n),
               "--seed", str(seed), "--tag", tag_of(row_id)] + extra
        log = open(logs / f"{row_id}_seed{seed}.log", "w", encoding="utf-8")
        procs.append((subprocess.Popen(cmd, cwd=SIM_DIR, stdout=log, stderr=subprocess.STDOUT), log))
    codes = []
    for p, log in procs:
        codes.append(p.wait())
        log.close()
    wall = time.perf_counter() - t0
    if any(codes):
        return {"row": row_id, "purpose": purpose, "status": f"FAILED (exit codes {codes}); see logs/",
                "started": started, **state}

    runs = []
    for seed in range(1, k + 1):
        d = OUTPUT_DIR / f"bench_{level}_n{n}_{tag_of(row_id)}" / f"seed{seed}"
        r = json.loads((d / "run.json").read_text(encoding="utf-8"))
        sp = dict(np.load(d / "spikes.npz", allow_pickle=True))
        rates, _ = rest_rates(sp, r["schedule"])
        runs.append((r, rates))
    rtf = np.array([r["timing"]["real_time_factor"] for r, _ in runs])
    r0, rates0 = runs[0]
    return {"row": row_id, "purpose": purpose, "status": "ok", "level": level,
            "cell_level": r0["network"]["cell_level"], "n": n, "processes": k,
            "variant": " ".join(extra) or "-", "dt_ms": r0["config"]["simulation"]["dt_ms"],
            "real_time_factor": float(rtf.mean()), "rtf_min": float(rtf.min()), "rtf_max": float(rtf.max()),
            "build_s": float(np.mean([r["timing"]["build_s"] for r, _ in runs])),
            "peak_memory_MB": float(max(r["timing"].get("peak_memory_MB", r["timing"]["memory_MB"])
                                        for r, _ in runs)),
            "row_wall_s": wall,
            "seed1_PN_A_Hz": rates0["PN_A"]["mean_Hz"], "seed1_PN_C_Hz": rates0["PN_C"]["mean_Hz"],
            "seed1_FSI_Hz": rates0["FSI"]["mean_Hz"],
            "started": started, **state}


def estimates(rows, cfg):
    """Block B and C wall-clock estimates from the measured rows (architecture/07 run lists)."""
    by = {r["row"]: r for r in rows if r.get("status") == "ok"}
    if not {"R200", "R500", "R1000", "F200", "R1000_par5"} <= set(by):
        return {"note": "needs rows R200, R500, R1000, F200 and R1000_par5"}
    slow = by["R1000_par5"]["real_time_factor"] / by["R1000"]["real_time_factor"]
    sim_s = {b: schedule(b, cfg)["t_end_ms"] / 1000.0 for b in ("B", "C_main", "C_rest", "C_inhoff")}

    def hours(row, block, s=slow):
        return by[row]["real_time_factor"] * s * sim_s[block] / 3600.0

    b_full, b_red = hours("F200", "B"), hours("R200", "B")
    waves = [("C_main x5 seeds (C1-C3)", hours("R1000", "C_main"), 5),
             ("C_inhoff x5 seeds (C5)", hours("R1000", "C_inhoff"), 5),
             ("C_rest n500 x5 seeds (C4)", hours("R500", "C_rest"), 5),
             ("C_nmda, C_noff, C_rest seed 1 (C6, C7)", hours("R1000", "C_rest"), 3)]
    return {
        "parallel_slowdown": slow,
        "simulated_s": sim_s,
        "assumption": "all runs of a wave in parallel (one per core), each slowed by the measured "
                      "5-process factor; waves one after the other",
        "block_B": {"full_h_per_seed": b_full, "reduced_h_per_seed": b_red,
                    "wall_h_all_6_in_parallel": max(b_full, b_red)},
        "block_C": {"waves_h": {name: h for name, h, _ in waves},
                    "wall_h": sum(h for _, h, _ in waves),
                    "cpu_h": sum(h * k for _, h, k in waves)},
    }


def write(rows, cfg):
    BENCH_DIR.mkdir(parents=True, exist_ok=True)
    keys = []
    for r in rows:
        keys += [k for k in r if k not in keys]
    with open(BENCH_DIR / "benchmark.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)
    out = {"date": datetime.now().isoformat(timespec="seconds"), "rows": rows,
           "pending": [{"row": i, "purpose": p, "reason": why} for i, p, why in PENDING],
           "estimates": estimates(rows, cfg)}
    (BENCH_DIR / "benchmark.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", nargs="+", choices=[r[0] for r in ROWS])
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()
    if args.list:
        for r in ROWS:
            print(f"{r[0]:12s} {r[1]}")
        for i, p, why in PENDING:
            print(f"{i:12s} {p} [pending: {why}]")
        return
    cfg = load_config()
    chosen = [r for r in ROWS if not args.rows or r[0] in args.rows]
    old = {}
    if (BENCH_DIR / "benchmark.json").exists():
        old = {r["row"]: r for r in json.loads((BENCH_DIR / "benchmark.json").read_text(encoding="utf-8"))["rows"]}
    for row in chosen:
        print(f"[{datetime.now():%H:%M:%S}] {row[0]}: {row[1]} ...", flush=True)
        res = run_row(row)
        old[row[0]] = res
        if res["status"] == "ok":
            print(f"    real-time factor {res['real_time_factor']:.1f} (x{res['processes']} processes), "
                  f"peak {res['peak_memory_MB']:.0f} MB, PN-A {res['seed1_PN_A_Hz']:.2f} Hz, "
                  f"PN-C {res['seed1_PN_C_Hz']:.2f} Hz, FSI {res['seed1_FSI_Hz']:.1f} Hz, "
                  f"row took {res['row_wall_s'] / 60:.1f} min", flush=True)
        else:
            print("    " + res["status"], flush=True)
        rows = [old[r[0]] for r in ROWS if r[0] in old]
        out = write(rows, cfg)
    est = out["estimates"]
    if "block_C" in est:
        print(f"Parallel slowdown (5 processes): x{est['parallel_slowdown']:.2f}")
        print(f"Block B: full {est['block_B']['full_h_per_seed']:.1f} h, reduced "
              f"{est['block_B']['reduced_h_per_seed']:.1f} h per seed (all in parallel)")
        print(f"Block C: about {est['block_C']['wall_h']:.1f} h wall clock, {est['block_C']['cpu_h']:.0f} CPU-hours")
    print(f"-> {BENCH_DIR}")


if __name__ == "__main__":
    main()
