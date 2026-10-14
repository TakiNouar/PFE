# 09 — Code Module Map (no source code)

Python drives NEURON. Feng's files do the biophysics; our code only builds, runs and measures. ✔ = written (2026-10-14); ☐ = still to write.

```
Simulations/BLA/simulation/
├── mechanisms/                 # ModelDB 247968 files, unchanged, NOT committed (no licence):
│                               # *.mod, cell templates (.hoc), input/ train files
│   └── HASHES.txt              # SHA-256 of every file (Gate 0) — the only committed file here
├── mechanisms_run1/            # OUR files, committed: reduced_pn.json (all reduced PNs, 03),
│                               # exc_ev.mod / inh_ev.mod (event-driven synapses, 04);
│                               # compiled to their own nrnmech.dll (not committed)
├── bla_sim/
│   ├── config/run1.json        ✔ every value we set + source keys (12_sources_map)
│   ├── nrn.py                  ✔ loads NEURON, both mechanism sets, Feng's templates and settings
│   ├── provenance.py           ✔ Gate 0 hash check, run metadata
│   ├── cells.py                ✔ Feng's cells, reduced PNs, Feng-style noise
│   ├── single_cell.py          ✔ Block A1/A2 protocol, gap coupling
│   ├── passive_check.py        ✔ Gate 2 / U29: membrane time constant by four methods
│   ├── reduce_pn.py            ✔ builds every reduced PN from Feng's cell; Gate R1
│   ├── drive_test.py           ✔ Block A2b, dendritic synaptic input (Gate R1)
│   ├── synapse_test.py         ✔ Block A3, Feng vs event-driven synapses
│   ├── plots.py                ✔ Block A figures
│   ├── network.py              ✔ placement, in-degree wiring, weights, delays, gap junctions, both levels
│   ├── inputs.py               ✔ Feng's afferent trains, threat spikes, afferent wiring
│   ├── run.py                  ✔ one simulation: blocks B, C_*, bench; pc.psolve in chunks; on_start / on_chunk
│   │                             hooks; --broadcast (viewer); benchmark-only --no-synapses, --dt
│   ├── metrics.py              ✔ rest rates, rest range, synchrony, ISI CV, threat response
│   ├── gate_r2.py              ✔ compares B_full and B_reduced outputs (Gate R2); tested on synthetic spikes
│   ├── benchmark.py            ✔ Phase 0 table (rows in 07), parallel-process throughput, Block B/C estimates
│   ├── launcher.py             ✔ starts the parallel processes for Blocks B and C; resumes; keeps Windows awake
│   ├── report.py               ☐ metrics.json / metrics.txt / summary.txt, gates 3–6
│   ├── broadcast.py            ✔ writes live/ snapshots from run.py's hooks (13)
│   └── viewer_server.py        ✔ small local web server for the viewer, run separately
├── viewer/                     ✔ live viewer page: index.html (canvas, no libraries), no internet needed
├── outputs/<run_id>/seed<k>/   # see 08_metrics_and_outputs.md (live/ = viewer snapshots only)
└── deviations.md
```

Keep `Simulations/BLA/simulation/` free of spaces in its path (`nrnivmodl` breaks on spaces).

**Loading both mechanism sets:** NEURON loads Feng's `nrnmech.dll` and ours separately; our mechanisms use new names, so they never clash with Feng's. Run scripts from outside the `mechanisms` folders: NEURON auto-loads an `nrnmech.dll` found in the current directory, and loading it again fails.

**Parallel runs:** `launcher.py` starts one `python -m bla_sim.run ...` process per seed or condition (default: physical cores − 1 at once, longest first) and skips jobs whose `run.json` exists, so an interrupted block resumes. Runs never use `pc.nthread` above 1. Every launched job broadcasts to the viewer except C7.

**Environment for every command** (shells opened before the installs need it set by hand): `NEURONHOME=C:\nrn`, `PYTHONPATH=C:\nrn\lib\python`, `PATH` including `C:\nrn\bin` and `C:\nrn\mingw\usr\bin`; Python at `%LOCALAPPDATA%\Programs\Python\Python312\python.exe`. Compile our mechanisms after any change with `C:\nrn\bin\nrnivmodl.bat` inside `mechanisms_run1/`.

## Responsibilities

- **config:** the only place numbers live. Nothing is hard-coded elsewhere.
- **cells:** templates only. No wiring.
- **wiring:** returns the connection list. Never touches inputs.
- **inputs:** noise, afferents, threat. Never touches wiring.
- **run:** orchestration only.
- **metrics:** pure functions, no side effects.
- **report:** reads `metrics.json` only.
- **broadcast / viewer:** read-only copies for display. Nothing in `metrics` or `report` may read `live/`.

## Forbidden

- Editing any file in `mechanisms/` (Gate 0 checks the hashes). Changes go in new files in `mechanisms_run1/`.
- Python callbacks that run every time step.
- Random numbers outside the named, seeded streams.
- Summary text that is not computed from `metrics.json`.
