"""Start and supervise the parallel runs of Block B or Block C (architecture/07, 09).

Usage (from Simulations/BLA/simulation):
    python -m bla_sim.launcher B --dry-run      # list the jobs with time estimates, start nothing
    python -m bla_sim.launcher B                # Block B: 3 seeds x full and reduced, 200 cells
    python -m bla_sim.launcher C                # Block C: C1-C7
Options: --max-procs K (default: physical cores - 1), --force (rerun finished jobs).

One `python -m bla_sim.run` process per job, at most K at once, longest jobs first; never
pc.nthread > 1. Every job broadcasts to the live viewer except C7 (C_rest, 1,000 cells, seed 1),
the reproducibility re-run that must run with the broadcast off (architecture/07, 13). A job whose run.json already exists is skipped, so an interrupted block resumes
where it stopped. While the launcher runs it asks Windows not to sleep (SetThreadExecutionState;
released when it exits, no setting is changed). Writes outputs/launcher/<block>_status.json
(updated at every start and finish) and outputs/launcher/logs/<job>.log.
"""
import argparse
import json
import subprocess
import sys
import time
from datetime import datetime

from .nrn import OUTPUT_DIR, SIM_DIR, load_config
from .run import schedule

LAUNCH_DIR = OUTPUT_DIR / "launcher"


def plan(block):
    """Jobs (block, level, n, seed) from architecture/07."""
    if block == "B":
        return [("B", lvl, 200, s) for lvl in ("full", "reduced") for s in (1, 2, 3)]
    seeds = load_config()["protocol"]["seeds"]
    return ([("C_main", "reduced", 1000, s) for s in seeds] +          # C1-C3
            [("C_inhoff", "reduced", 1000, s) for s in seeds] +        # C5
            [("C_rest", "reduced", 500, s) for s in seeds] +           # C4
            [("C_nmda", "reduced", 1000, 1), ("C_noff", "reduced", 1000, 1),   # C6
             ("C_rest", "reduced", 1000, 1)])                          # C7 (broadcast off)


def broadcasts(j):
    return not (j[0] == "C_rest" and j[2] == 1000)        # C7 runs with the broadcast off


def job_name(j):
    return f"{j[0]}_{j[1]}_n{j[2]}_seed{j[3]}"


def run_dir(j):
    return OUTPUT_DIR / f"{j[0]}_{j[1]}_n{j[2]}" / f"seed{j[3]}"


def estimate_h(j, cfg, bench):
    """Wall-clock hours from the Phase 0 benchmark (None if it has not been run)."""
    rows = {r["row"]: r for r in bench.get("rows", []) if r.get("status") == "ok"}
    key = ("F" if j[1] == "full" else "R") + str(j[2])
    if key not in rows:
        return None
    slow = bench.get("estimates", {}).get("parallel_slowdown", 1.0)
    return rows[key]["real_time_factor"] * slow * schedule(j[0], cfg)["t_end_ms"] / 1000.0 / 3600.0


def keep_awake(on):
    if sys.platform != "win32":
        return
    import ctypes
    ES_CONTINUOUS, ES_SYSTEM_REQUIRED = 0x80000000, 0x00000001
    ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | (ES_SYSTEM_REQUIRED if on else 0))


def main():
    import psutil
    ap = argparse.ArgumentParser()
    ap.add_argument("block", choices=("B", "C"))
    ap.add_argument("--max-procs", type=int, default=max(1, (psutil.cpu_count(logical=False) or 2) - 1))
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    cfg = load_config()
    bp = OUTPUT_DIR / "benchmark" / "benchmark.json"
    bench = json.loads(bp.read_text(encoding="utf-8")) if bp.exists() else {}
    jobs = plan(args.block)
    est = {job_name(j): estimate_h(j, cfg, bench) for j in jobs}
    jobs.sort(key=lambda j: -(est[job_name(j)] or schedule(j[0], cfg)["t_end_ms"] * j[2]))
    todo = [j for j in jobs if args.force or not (run_dir(j) / "run.json").exists()]

    print(f"Block {args.block}: {len(jobs)} jobs, {len(jobs) - len(todo)} already done, "
          f"up to {args.max_procs} at once")
    for j in jobs:
        e = est[job_name(j)]
        state = "todo" if j in todo else "done"
        print(f"  {job_name(j):32s} {schedule(j[0], cfg)['t_end_ms'] / 1000:5.0f} s simulated  "
              f"{'~%.1f h' % e if e else '(no benchmark)':>10s}  {state}")
    if args.dry_run or not todo:
        return

    LAUNCH_DIR.mkdir(parents=True, exist_ok=True)
    (LAUNCH_DIR / "logs").mkdir(exist_ok=True)
    status_path = LAUNCH_DIR / f"{args.block}_status.json"
    status = {job_name(j): {"state": "queued" if j in todo else "done (earlier)", "estimate_h": est[job_name(j)]}
              for j in jobs}

    def save():
        status_path.write_text(json.dumps({"block": args.block, "updated": datetime.now().isoformat(timespec="seconds"),
                                           "max_procs": args.max_procs, "jobs": status}, indent=1), encoding="utf-8")

    keep_awake(True)
    running = {}
    queue = list(todo)
    try:
        while queue or running:
            while queue and len(running) < args.max_procs:
                j = queue.pop(0)
                name = job_name(j)
                cmd = [sys.executable, "-u", "-m", "bla_sim.run", "--block", j[0], "--level", j[1],
                       "--n", str(j[2]), "--seed", str(j[3])] + (["--broadcast"] if broadcasts(j) else [])
                log = open(LAUNCH_DIR / "logs" / f"{name}.log", "w", encoding="utf-8")
                running[name] = (subprocess.Popen(cmd, cwd=SIM_DIR, stdout=log, stderr=subprocess.STDOUT), log)
                status[name].update(state="running", started=datetime.now().isoformat(timespec="seconds"),
                                    cmd=" ".join(cmd[1:]))
                print(f"[{datetime.now():%H:%M:%S}] start  {name}", flush=True)
                save()
            time.sleep(5)
            for name, (p, log) in list(running.items()):
                if p.poll() is not None:
                    log.close()
                    del running[name]
                    ok = p.returncode == 0
                    status[name].update(state="done" if ok else f"FAILED (exit {p.returncode})",
                                        finished=datetime.now().isoformat(timespec="seconds"))
                    print(f"[{datetime.now():%H:%M:%S}] {'done  ' if ok else 'FAILED'} {name}", flush=True)
                    save()
    except KeyboardInterrupt:
        # Stop the children too: a restart would otherwise launch duplicates of unfinished jobs.
        for name, (p, log) in running.items():
            p.terminate()
            log.close()
            status[name].update(state="stopped by user", finished=datetime.now().isoformat(timespec="seconds"))
        save()
        print("Stopped; unfinished jobs will run again at the next launch.")
        return
    finally:
        keep_awake(False)
    failed = [n for n, s in status.items() if s["state"].startswith("FAILED")]
    print(f"Block {args.block} finished; {len(failed)} failed{': ' + ', '.join(failed) if failed else ''}")


if __name__ == "__main__":
    main()
