"""Engine benchmark: how many simplified neurons run in real time, CPU (Brian2) vs GPU (GeNN).

Usage (from Simulations/BLA/simplified, in a shell with the MSVC + CUDA environment):
    <brian2 venv python> -m engine_benchmark.run_bench gpu          # GeNN, float, 1k-100k neurons
    <brian2 venv python> -m engine_benchmark.run_bench gpu-double   # GeNN, double precision
    <brian2 venv python> -m engine_benchmark.run_bench cpu --threads 1 3 6
Each configuration runs in its own process (fresh engine state); results are appended to
outputs/engine_benchmark/results.jsonl (one JSON object per line) with the machine state.
The real-time factor is wall-clock seconds per simulated second: below 1 = faster than real time.
"""
import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "engine_benchmark"
SIZES = {"gpu": [1000, 2000, 5000, 10000, 20000, 50000, 100000],
         "gpu-double": [1000, 10000],
         "cpu": [1000, 2000, 5000, 10000, 20000]}
SIM_MS = 2000.0


def one(kind, n, threads):
    """Run one configuration in this process and print its result as JSON."""
    import logging
    logging.disable(logging.WARNING)
    if kind.startswith("gpu"):
        from .genn_net import run_genn
        r = run_genn(n, SIM_MS, "double" if kind == "gpu-double" else "float",
                     build_root=str(OUT / "build_genn"))
    else:
        from .brian2_net import run_brian2
        r = run_brian2(n, SIM_MS, target="cpp_standalone", threads=threads,
                       build_dir=str(OUT / "build_brian2" / f"n{n}_t{threads}"))
    print("RESULT " + json.dumps({k: (float(v) if hasattr(v, "dtype") else v) for k, v in r.items()}), flush=True)


def machine():
    import psutil
    bat = psutil.sensors_battery()
    busy = [p.info["cmdline"] for p in psutil.process_iter(["cmdline"])
            if p.info["cmdline"] and any("bla_sim.run" in c for c in p.info["cmdline"])]
    return {"power_plugged": None if bat is None else bool(bat.power_plugged),
            "other_simulations_running": len(busy)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kind", choices=list(SIZES))
    ap.add_argument("--threads", type=int, nargs="+", default=[1])
    ap.add_argument("--sizes", type=int, nargs="+")
    ap.add_argument("--one", nargs=2, type=int, metavar=("N", "THREADS"), help=argparse.SUPPRESS)
    args = ap.parse_args()
    if args.one:
        return one(args.kind, *args.one)
    OUT.mkdir(parents=True, exist_ok=True)
    for threads in (args.threads if args.kind == "cpu" else [1]):
        for n in args.sizes or SIZES[args.kind]:
            cmd = [sys.executable, "-m", "engine_benchmark.run_bench", args.kind, "--one", str(n), str(threads)]
            p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
            line = next((l for l in p.stdout.splitlines() if l.startswith("RESULT ")), None)
            if line is None:
                print(f"{args.kind} n={n} threads={threads}: FAILED\n{p.stdout[-1500:]}\n{p.stderr[-3000:]}", flush=True)
                break
            r = json.loads(line[7:])
            r.update(date=datetime.now().isoformat(timespec="seconds"), **machine())
            with open(OUT / "results.jsonl", "a", encoding="utf-8") as f:
                f.write(json.dumps(r) + "\n")
            print(f"{r['engine']:22s} threads {threads}  n={n:6d}  {r['synapses']:9d} synapses  "
                  f"x{r['real_time_factor']:.2f} real time  PN {r['rate_PN_Hz']:.2f} Hz  FSI {r['rate_FSI_Hz']:.1f} Hz",
                  flush=True)
            if r["real_time_factor"] > 20:          # far from real time: larger sizes only take longer
                break


if __name__ == "__main__":
    main()
