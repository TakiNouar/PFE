# 09 — Code Module Map (no source code)

Python drives NEURON. Feng's files do the biophysics; our code only builds, runs and measures. Names are suggestions; the separation of concerns is what matters.

```
Simulations/BLA/simulation/
├── mechanisms/                 # ModelDB 247968 files, unchanged, NOT committed (no licence):
│                               # *.mod, cell templates (.hoc), input/ train files
│   └── HASHES.txt              # SHA-256 of every file (Gate 0) — the only committed file here
├── mechanisms_run1/            # OUR files, committed: reduced_pn.json (two-piece PN, 03),
│                               # exc_ev.mod / inh_ev.mod (event-driven synapses, 04);
│                               # compiled to their own nrnmech.dll (not committed)
├── bla_sim/
│   ├── config/
│   │   └── run1.json           # every value we set + source keys (12_sources_map)
│   ├── cells.py                # load templates; make PN-A / PN-C / FSI by ID, at either level
│   ├── reduce_pn.py            # builds and checks the reduced PNs from Feng's full cell (Gate R1)
│   ├── synapse_test.py         # Feng vs event-driven synapse unit test (step A3)
│   ├── placement.py            # cube, density, 25 µm minimum distance
│   ├── wiring.py               # in-degree rule, weights, delays, gap-junction pairs
│   ├── inputs.py               # Gfluct noise, Feng afferent trains, threat spikes
│   ├── run.py                  # settle → rest → trials; pc.psolve in chunks
│   ├── benchmark.py            # Phase 0 timing table
│   ├── single_cell.py          # step-1 current steps + gap coupling
│   ├── metrics.py              # pure functions of spike/voltage data
│   ├── report.py               # writes metrics.json / metrics.txt / summary.txt
│   ├── broadcast.py            # writes live/ snapshots between chunks (13_live_viewer)
│   └── viewer_server.py        # small local web server for the viewer, run separately
├── viewer/                     # live viewer page: index.html + JS (canvas), no internet needed
├── outputs/<run_id>/           # see 08_metrics_and_outputs.md (live/ = viewer snapshots only)
├── deviations.md
└── main.py                     # one entry point: reads config, runs the requested steps
```

Keep `Simulations/BLA/simulation/` free of spaces in its path (`nrnivmodl` breaks on spaces).

**Loading both mechanism sets:** NEURON loads Feng's `nrnmech.dll` and ours separately; our mechanisms use new names, so they never clash with Feng's. Run scripts from outside the `mechanisms` folders: NEURON auto-loads an `nrnmech.dll` found in the current directory, and loading it again fails.

**Parallel runs:** `main.py` starts one process per seed or condition (at most one per physical core) and never uses `pc.nthread` above 1.

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
