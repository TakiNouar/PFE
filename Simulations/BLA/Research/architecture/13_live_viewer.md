# 13 — Live Viewer (display only)

**Purpose:** watch Run 1 while it runs, like a live broadcast of what the network is doing.
**Status:** part of Run 1, built with the simulation code. **Display only:** no metric, gate or result is ever read from it.

---

## What you see

| Panel | Shows |
|---|---|
| **Microscope** | All cells at their real positions in the cube, each flashing when it fires; colour by type (PN-A, PN-C, FSI); can be rotated |
| **Oscilloscope** | Membrane voltage of three probe cells (one PN-A, one PN-C, one FSI), ringed in the microscope view |
| **Activity strip** | PN and FSI population rate over the last 10 s of simulated time, with threat windows shaded |
| **Status** | Current step (settle / rest / threat trial k of 5 at ×D / size check / …), seed n of 5, simulated clock, speed (how many times slower than real time), estimated time left, and a progress bar for the whole protocol |

## How "live" works

The simulation runs slower than real time (estimated 10–60×; measured in Phase 0). A live broadcast is therefore **slow motion**: what you see is what the computer is calculating at that moment.

1. The run advances in **50 ms chunks** of simulated time (`pc.psolve`).
2. After each chunk it writes one small snapshot: the spikes in that chunk (cell, time), the three probe voltages sampled every 0.5 ms, and the status.
3. The viewer plays each chunk stretched over the time the next one takes to compute, so the picture moves continuously rather than in jumps.
4. Optional **catch-up replay** button: loops the last 10 s of simulated activity at real speed.

## Rules (so it cannot change results)

1. **Display only.** Metrics come from the run's own spike files (`08`), never from `live/`.
2. **The simulation never waits for the viewer.** It writes each snapshot to a temporary file and renames it (so the viewer never reads half a file), then continues. If the viewer is closed or crashes, the run is unaffected.
3. **No per-time-step Python.** Snapshots are written between chunks only.
4. **No effect on the dynamics.** Recording spikes and three voltages does not change the simulation, and with a fixed time step the chunk length does not change spike times. Gate 1's reproducibility re-run (`07` step 8) is done **with the broadcast switched off** and must give an identical spike file. That proves it.
5. **Probe cells** are chosen once per seed from the seeded stream and listed in `cells.json`.

## Files

Under `Simulations/BLA/simulation/outputs/<run_id>/live/` (rolling, not an output, gitignored):

| File | Written | Content |
|---|---|---|
| `cells.json` | once per seed | cell id, type, x / y / z (mm), probe ids |
| `status.json` | every chunk | latest chunk number, step, seed, trial, dose, simulated time, measured speed, time left |
| `chunk_<n>.json` | every chunk | spikes in the chunk, three probe voltage traces |

Only the last ~60 s of simulated activity is kept; older chunk files are deleted.

## Serving

- A small local web server (Python standard library), started **separately** from the simulation, serves the viewer page and the `live/` folder at `http://localhost:8765`.
- By default only this laptop can open it. Optional: allow other devices on your home network (phone, desktop); Windows Firewall will ask once.
- The page is plain HTML + canvas and needs no internet connection.

## Speed check

Phase 0 includes one row with the broadcast **on** at 1,000 cells, to measure its overhead. The expected overhead is negligible: one small file per chunk, roughly every second or more of computing.
