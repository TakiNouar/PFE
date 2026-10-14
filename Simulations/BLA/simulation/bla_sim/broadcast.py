"""Live broadcast for the viewer (architecture/13): display-only snapshots written between chunks.

run.py (with --broadcast) calls start() once before finitialize and on_chunk() after every
chunk of simulated time. Nothing here is read back by the simulation, metrics or reports.
Files in outputs/<block>_<level>_n<N>/seed<k>/live/ (gitignored):
    cells.json       once: positions, types, probe cells, schedule
    status.json      every chunk: step, simulated clock, speed, time left
    chunk_<n>.json   every chunk: spikes [gid, t_ms] and the probe voltages every 0.5 ms
Each file is written to a temporary name and renamed, so the viewer never reads half a file.
Only the last 60 s of simulated activity is kept. Any error here is reported once and
ignored: the simulation never waits for, or fails because of, the broadcast.
"""
import json
import os
import time

import numpy as np

from .network import stream

V_DT_MS = 0.5
KEEP_S = 60.0
TYPES = ("PN_A", "PN_C", "FSI")
BLOCK_LABEL = {"B": "Block B: reference comparison", "C_main": "Block C: main run (C1-C3)",
               "C_rest": "Block C: rest only", "C_inhoff": "Block C: inhibition off (C5)",
               "C_nmda": "Block C: PN->PN NMDA only (C6)", "C_noff": "Block C: PN->PN removed (C6)",
               "bench": "Phase 0 benchmark", "demo": "Viewer demo (no gate)"}


def _write(path, obj):
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(obj, separators=(",", ":")), encoding="utf-8")
    for _ in range(3):                      # Windows: the server may be reading the old file
        try:
            os.replace(tmp, path)
            return
        except PermissionError:
            time.sleep(0.01)


class Broadcaster:
    def __init__(self, run_dir, block, level, n, seed):
        self.dir = run_dir / "live"
        self.block, self.level, self.n, self.seed = block, level, n, seed
        self.run_id = f"{run_dir.parent.name}/{run_dir.name}"
        self.ok = True

    def _guard(self, fn, *a):
        if not self.ok:
            return
        try:
            fn(*a)
        except Exception as e:              # display only: never stop the simulation
            print(f"  [broadcast off after error: {e!r}; the simulation continues]", flush=True)
            self.ok = False

    # -- hooks called by run.simulate -------------------------------------------
    def start(self, net, tvec, idvec, sched):
        self._guard(self._start, net, tvec, idvec, sched)

    def on_chunk(self, net, t, tvec, idvec, sched):
        self._guard(self._chunk, t)

    # -- implementation ---------------------------------------------------------
    def _start(self, net, tvec, idvec, sched):
        h = net.h
        self.dir.mkdir(parents=True, exist_ok=True)
        for f in self.dir.glob("chunk_*.json"):
            f.unlink()
        self.sched, self.tvec, self.idvec = sched, tvec, idvec
        self.chunk_ms = net.cfg["protocol"]["chunk_ms"]
        rng = stream(self.seed, "probes")
        self.probes = {k: int(rng.choice(np.nonzero(net.types == k)[0])) for k in TYPES}
        self.vecs = {g: h.Vector().record(net.cells[g].soma(0.5)._ref_v, V_DT_MS) for g in self.probes.values()}
        self.i_spk, self.i_v, self.k = 0, 0, 0
        self.t_prev, self.ema = 0.0, None
        self.t_wall0 = self.t_last = time.perf_counter()
        code = {k: i for i, k in enumerate(TYPES)}
        cells = [[round(float(x) * 1000, 1), round(float(y) * 1000, 1), round(float(z) * 1000, 1), code[k]]
                 for (x, y, z), k in zip(net.pos, net.types)]
        _write(self.dir / "cells.json", {
            "run": self.run_id, "block": self.block, "label": BLOCK_LABEL.get(self.block, self.block),
            "level": self.level, "cell_level": net.cell_level, "n": self.n, "seed": self.seed,
            "side_um": net.side_mm * 1000, "types": TYPES, "cells": cells, "probes": self.probes,
            "schedule": sched, "chunk_ms": self.chunk_ms, "v_dt_ms": V_DT_MS})
        self._status(0.0, time.perf_counter())

    def _step(self, t):
        s = self.sched
        if t <= s["settle_ms"]:
            return {"phase": "settle"}
        if t <= s["settle_ms"] + s["rest_ms"] or not s["trials"]:
            return {"phase": "rest"}
        for i, tr in enumerate(s["trials"]):
            if t <= tr["end_ms"] + 1e-9:
                same = [x for x in s["trials"] if x["dose"] == tr["dose"]]
                k = sum(1 for x in s["trials"][:i] if x["dose"] == tr["dose"]) + 1
                ph = ("before threat" if t <= tr["threat_on_ms"] else
                      "THREAT" if t <= tr["threat_off_ms"] else "after threat")
                return {"phase": ph, "trial": k, "trials_at_dose": len(same), "dose": tr["dose"],
                        "trial_index": i + 1, "trials_total": len(s["trials"])}
        return {"phase": "end"}

    def _status(self, t, now):
        t_end = self.sched["t_end_ms"]
        per = self.ema
        _write(self.dir / "status.json", {
            "run": self.run_id, "block": self.block, "label": BLOCK_LABEL.get(self.block, self.block),
            "level": self.level, "n": self.n, "seed": self.seed, "pid": os.getpid(),
            "chunk": self.k, "chunk_ms": self.chunk_ms, "t_ms": t, "t_end_ms": t_end,
            "progress": t / t_end, "step": self._step(t),
            "wall_per_chunk_s": per, "slower_than_real_time": per / (self.chunk_ms / 1000.0) if per else None,
            "elapsed_s": now - self.t_wall0,
            "eta_s": per * (t_end - t) / self.chunk_ms if per else None,
            "updated": time.time(), "done": t >= t_end - 1e-9})

    def _chunk(self, t):
        now = time.perf_counter()
        dt_wall = now - self.t_last
        self.t_last = now
        self.ema = dt_wall if self.ema is None else 0.8 * self.ema + 0.2 * dt_wall
        self.k += 1
        ts, gs = self.tvec.as_numpy()[self.i_spk:], self.idvec.as_numpy()[self.i_spk:]
        self.i_spk += len(ts)
        v, v_t0 = {}, self.i_v * V_DT_MS
        for g, vec in self.vecs.items():
            a = vec.as_numpy()[self.i_v:]
            v[str(g)] = np.round(a, 2).tolist()
            n_new = len(a)
        self.i_v += n_new
        _write(self.dir / f"chunk_{self.k}.json", {
            "chunk": self.k, "t0": self.t_prev, "t1": t,
            "spikes": [[int(g), round(float(x), 2)] for g, x in zip(gs, ts)],
            "v_t0": v_t0, "v": v})
        self.t_prev = t
        self._status(t, now)
        old = self.dir / f"chunk_{self.k - int(KEEP_S * 1000 / self.chunk_ms)}.json"
        try:
            old.unlink(missing_ok=True)
        except PermissionError:
            pass
