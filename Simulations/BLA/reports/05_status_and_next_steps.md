# BLA Run 1 — Status and Next Steps

**Date:** 2026-10-14
**Purpose:** a self-contained starting point for the next working session.
**Branch:** `run1-redesign`. Binding spec: `Simulations/BLA/Research/architecture/` (00–13). Decision history: `04_run1_redesign_oct2026.md`. Deviations: `Simulations/BLA/simulation/deviations.md` (DEV-001 to DEV-007).

---

## 1. Where things stand

| Part | Status |
|---|---|
| Spec (architecture 00–13) | Up to date with every decision below |
| Phase 0 setup | **Done.** Python 3.12.10, NEURON 9.0.2 (`C:\nrn`), Feng's ModelDB 247968 files byte-exact and hashed, both mechanism sets compiled |
| Phase 0 benchmark | **Done** (`outputs/benchmark/`, table in `architecture/07`). Block B about 12 h, Block C about 2 days |
| Block A (single cells, reductions, synapses) | **Done.** Gate 2 passed (time constant explained, U29). Gate R1 passed for the chosen cell with one approved exception; event-driven synapses identical to Feng's |
| Network code | **Written** (`network.py`, `inputs.py`, `run.py`, `metrics.py`) and benchmarked at 200–1,000 cells |
| Run tools | **Written and tested**: `launcher.py` (ran two demo seeds in parallel), `gate_r2.py` (tested on synthetic spikes: passes when matched, fails on the right lines when not) |
| Block B (200-cell reference comparison, Gate R2) | **Ready to start** (`python -m bla_sim.launcher B`). About 12 h. Ask M. T. Nouar first |
| Block C (main run, 1,000 cells, 5 seeds) | Not started. About 237 CPU-hours, about 2 days on 5 parallel processes |
| Live viewer | **Built and tested** (`architecture/13`): microscope, oscilloscope, activity strip, status, replay. The broadcast leaves spike files identical (checked at 100 and 1,000 cells) and costs ≤ 2 % |

## 2. Decisions in force (all by M. T. Nouar)

| Decision | Choice |
|---|---|
| Simulator | NEURON 9.0.2; Feng's files unchanged; one core per run, parallel processes for seeds (Feng's files are not thread safe) |
| Machine | The laptop (Ryzen 5 4600H, 6 cores) during Erasmus; the RTX 3060 desktop is not in use for now |
| Cells | PN-A, PN-C, FSI; no SOM |
| Reference level | Feng's full cells and synapses (single cells; 200-cell network) |
| Main-level principal cell | **`coarse_d2_p3`**: Feng's cell rebuilt on 6 segments (soma 1, apical 2, basal 3). One approved exception: PN-C fires 6 instead of 9 spikes before depolarization block at 1.5 nA |
| Main-level synapses | Event-driven `ExcEv` / `InhEv` (identical to Feng's, ~400× faster) |
| Size | 1,000 cells (640 / 260 / 100) main; 500 size check; 200 reference |
| Wiring | Feng's realised inputs per cell (25 / 43 / 215 / 22), distance-independent |
| Inputs | Feng's noise and afferent trains; threat = afferent rate ×2, ×4, ×8 for 2 s |
| Seeds | 5 (1–5) |
| Live viewer | Part of Run 1: a live, slow-motion broadcast, display only |

## 3. Next steps, in order

Done on 2026-10-14 (second session): coarse-cell smoke test and Gate R1 regeneration; Phase 0 benchmark; Gate 2 / U29; `gate_r2.py`; `launcher.py`; live viewer (`broadcast.py`, `viewer_server.py`, `viewer/index.html`) with a `demo` block.

1. **Block B** (about 12 h; ask before starting): `python -m bla_sim.launcher B`, and in a second terminal `python -m bla_sim.viewer_server` to watch. Then `python -m bla_sim.gate_r2` → Gate R2.
2. **U30 check** from Block B's 30 s rest: FSI rate at both levels. If it stays above 30 Hz, find the difference from Feng before Block C (see U30).
3. **`report.py`** (can be written while Block B runs): `metrics.json`, `metrics.txt`, `summary.txt`; Gates 3–6 per `architecture/10`, and the C7 reproducibility comparison (C_main seed 1 rest vs C_rest seed 1).
4. **Block C** (about 2 days): `python -m bla_sim.launcher C` → Gates 3–6 → report.

## 4. How to run things

Every command runs from `Simulations/BLA/simulation` (never from a `mechanisms` folder: NEURON auto-loads an `nrnmech.dll` found in the current directory). New terminals already have the NEURON settings; terminals opened before 2026-10-14 need them set by hand:

```
NEURONHOME=C:\nrn
PYTHONPATH=C:\nrn\lib\python
PATH = C:\nrn\bin;C:\nrn\mingw\usr\bin;...
python = %LOCALAPPDATA%\Programs\Python\Python312\python.exe
```

| Task | Command |
|---|---|
| Recompile our mechanisms (after editing `exc_ev.mod` / `inh_ev.mod`) | `C:\nrn\bin\nrnivmodl.bat` inside `mechanisms_run1/` |
| Block A1, Feng's single cells (~6 min) | `python -m bla_sim.single_cell --level full` |
| Block A2, reduced cells + Gate R1 (~5 min) | `python -m bla_sim.reduce_pn` |
| Block A2b, dendritic-input test (full level ~10 min) | `python -m bla_sim.drive_test --levels full coarse_d2_p3` |
| Block A3, synapse test (~1 min) | `python -m bla_sim.synapse_test` |
| Gate 2 time constant check (~1 min) | `python -m bla_sim.passive_check` |
| Phase 0 benchmark (~1 h; `--list` shows rows, `--rows` picks some) | `python -m bla_sim.benchmark` |
| One network run | `python -m bla_sim.run --block <B|C_main|C_rest|C_inhoff|C_nmda|C_noff|bench|demo> --level <full|reduced> --n <N> --seed <k> [--broadcast]` |
| Block B or C, all runs in parallel (`--dry-run` lists jobs and hours) | `python -m bla_sim.launcher B` / `C` |
| Gate R2 after Block B | `python -m bla_sim.gate_r2` |
| Live viewer (separate terminal; open http://localhost:8765) | `python -m bla_sim.viewer_server` (`--lan` for phone or desktop) |
| See the viewer working in ~3 min (100 cells, one ×8 threat) | `python -m bla_sim.run --block demo --level reduced --n 100 --broadcast` |

Outputs go to `outputs/<block>_<level>_n<N>/seed<k>/` (`run.json` committed; `spikes.npz` git-ignored).

## 5. Key measured numbers (laptop, 2026-10-14)

| Item | Value |
|---|---|
| Feng's full PN | 83 µs per cell per 0.05 ms step |
| Main-level coarse PN | 25 µs |
| Feng's FSI | 4.3 µs |
| Feng synapse / event-driven synapse | 1.32 / 0.003 µs per connection per step |
| Feng's PN, noise only | PN-A 0.35 Hz, PN-C 1.65 Hz (rat BLA 0.21 / 1.55 Hz) |
| 100-cell network, full detail | real-time factor 280; PN-A 0.62 Hz, PN-C 1.65 Hz, FSI 52.8 Hz (1 s, one seed) |
| 100-cell network, two-piece (rejected) | real-time factor 22.6; PN-A 0.36 Hz, PN-C 0.58 Hz, FSI 23.0 Hz |
| 100-cell network, coarse (chosen) | real-time factor 53.3 (5.3× faster than full); PN-A 0.61 Hz, PN-C 1.38 Hz, FSI 49.3 Hz |
| Phase 0, main level, 200 / 500 / 1,000 cells | real-time factor 112 / 279 / 565 (about 0.56 per cell) |
| Phase 0, reference level (Feng's files), 200 cells | real-time factor 656; PN-A 0.60, PN-C 1.10, FSI 42.8 Hz (main level at 200: 0.55 / 1.12 / 42.7) |
| Phase 0, 1,000 cells without synapses | 516 (synapses are ~9 % of the cost) |
| Phase 0, 5 runs at once | 650 each (×1.15 slower than one alone) |
| Phase 0, 1,000 cells, broadcast on | 578 (≤ 2 % cost); spikes identical to the run without it (5,821 spikes) |
| Membrane time constant (Feng's PN-A) | 30.9 ms slowest time constant (Feng ~30); 34.9 ms 63 % rise; 53–55 ms without Ih |

The 100-cell runs and the Phase 0 rows are 1 s samples (one seed), so they are speed measurements, not results. The reference and main levels agree at 200 cells, but FSIs fire ~42 Hz at every size, above the 10–30 Hz of Gate 3 (U30).

## 6. Open items

| ID | Item |
|---|---|
| U26 | Live engine: Phase 0 shows cells (not synapses) are ~91 % of the cost; a live engine needs far cheaper cells and several cores, or fewer neurons |
| U30 | FSIs ~42 Hz in all 1 s benchmark runs (Gate 3 wants 10–30); FSI depolarization block seen in the 100-cell ×8 demo. Check over Block B's 30 s rest |
| U27 | Threat pathway: later, a dedicated thalamic input |
| U28 | PN-A fires once per ~2 s under steady current: consistent with its sAHP and with rat data under noise; still check Feng's and Kim's description |
| — | `reports/` and `research_notes/` at the repo root (the October verification report and its notes) are not committed; decide whether to move them to `Research/reports/` |

## 7. Practical notes

- Feng's files must never be edited; Gate 0 hashes them on every run (`provenance.check_feng_hashes`).
- `pc.nthread(n > 1)` fails with Feng's files and then hangs the process. Use one core per run.
- PowerShell 5.1 strips quotes inside `python -c "..."`; put scripts in files.
- A stuck test process (PID 33984, 0 CPU) from 2026-10-14 lingers in the process list until the next reboot. It is harmless.
