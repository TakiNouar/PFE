# BLA Simulation Architecture — Overview

**Location:** `Simulations/BLA/Research/architecture/`  
**Purpose:** The binding specification for isolated BLA **Run 1**. No code: structure, numbers, rules, module map.  
**Revised:** October 2026 (Run 1 redesign), updated 2026-10-14 (option D: two levels). Why: `Simulations/BLA/reports/04_run1_redesign_oct2026.md`.

This series is the authoritative design for Run 1. It supersedes the archived failed tests in `reports/test_run_1/`.

The Design Blueprint is a living outline only. When this architecture and the literature disagree with older blueprint numbers, **architecture + literature win**, and the blueprint is updated afterward.

---

## Run 1 in one paragraph

Run 1 is an **offline test campaign**, not the live emotion engine. It rebuilds Feng et al. 2019's basolateral amygdala in **two levels**:

- **Reference level:** Feng's NEURON files (cells, synapses, noise) **unchanged** from ModelDB 247968, kept small (single cells and a 200-cell network) because it is slow: about 1 hour of computing per simulated second at 1,000 cells on the project laptop (measured 2026-10-14).
- **Main level:** the full 1,000-cell network and full protocol, built with two speed reductions: a **two-piece principal cell** (Feng's exact soma plus one lumped dendrite), and **event-driven synapses** that reproduce Feng's synapses exactly. It must reproduce the reference level's behaviour before its results count.

We write the wiring, the inputs, the measurements, and the two reductions. Run 1 passes when the reductions match Feng's originals and the main network fires like a real rat BLA at rest, responds to a "threat" input, and settles back afterwards (`10_validation_gates.md`). The live engine's design is decided later, from the measured speeds (U26).

## Decisions locked for Run 1

| Decision | Choice | File |
|---|---|---|
| Simulator | NEURON 9.0.2 + ModelDB 247968 files, unchanged (our new files sit beside them, never replace them) | `03`, `09` |
| Cell types | PN-A, PN-C, FSI (Feng's three). **No SOM** | `02`, `03` |
| Cell detail | **Reference:** Feng's full templates (16 segments per PN). **Main:** two-piece PN (Feng's exact soma + one lumped dendrite, no fitted values); Feng's FSI template unchanged | `03` |
| Synapses | **Reference:** Feng's four synapse files. **Main:** event-driven equivalents (Destexhe, Mainen & Sejnowski 1994 method), identical to Feng's to floating-point precision and ~400× faster | `04` |
| Size | **Main:** 1,000 cells (640 / 260 / 100), size check at 500. **Reference:** 200 cells (128 / 52 / 20) | `02` |
| Wiring | Keep Feng's **inputs per cell** (in-degree), not his distance probabilities | `05` |
| Replication target | Feng's **code** where it differs from the paper; every difference logged | `04`, `12` |
| Inputs | Feng's background noise + Feng's afferent spike trains; threat = afferents turned up ×2, ×4, ×8 | `06` |
| Parallelism | Feng's files are not thread safe, so each run uses one core; separate seeds run as parallel processes | `07` |
| Live viewer | Live broadcast of a running process (microscope, oscilloscope, status); display only | `13` |

---

## Literature authority (reading order)

1. **`Research/Sources/01_primary_bla_references.md`**: Feng Tables 3–7, the ModelDB code values, and the upstream citations.
2. **`architecture/12_sources_map.md`**: every number in this architecture mapped to its source.
3. ModelDB **247968** (Feng). ModelDB 150288 (Kim 2013) is **not** used for cell parameters: Feng revised Kim's PN model.

If a required value is missing from Sources, **stop** and report the gap. No guesses.

---

## Document index

| File | Content |
|------|---------|
| `00_architecture_overview.md` | This file |
| `01_goals_and_constraints.md` | Goals, non-goals, hard rules |
| `02_population_structure.md` | Cell counts, sizes, placement |
| `03_neuron_models.md` | Feng's cell templates; the two-piece PN |
| `04_synaptic_models.md` | Feng's synapse files; the event-driven synapses |
| `05_connectivity.md` | In-degree wiring rule, delays |
| `06_noise_and_drive.md` | Background noise, afferent trains, threat input |
| `07_simulation_protocol.md` | Phase 0 benchmark, reference and main run sequences, durations, seeds |
| `08_metrics_and_outputs.md` | Metrics and output files |
| `09_code_module_map.md` | Package layout (no code) |
| `10_validation_gates.md` | Pass/fail gates, including the reduction gate |
| `11_anti_patterns.md` | Failures that must not recur |
| **`12_sources_map.md`** | **Parameter ↔ source table** |
| `13_live_viewer.md` | Live broadcast of the running test (display only) |

---

## Scope

**In scope:** PN-A + PN-C + FSI; local recurrent circuit; Feng background noise and afferent input; a threat input with three strengths; inhibition check; reproducibility; speed benchmark; the two reductions and their validation against Feng's originals; a display-only live viewer.

**Out of scope:** SOM, VIP, CCK cells; long after-discharge; LTP/LTD; neuromodulation; LFP calculation; other regions; the live real-time engine; gamma as a pass/fail gate (diagnostic only).
