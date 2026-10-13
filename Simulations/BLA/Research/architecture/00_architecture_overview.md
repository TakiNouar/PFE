# BLA Simulation Architecture — Overview

**Location:** `Simulations/BLA/Research/architecture/`  
**Purpose:** The binding specification for isolated BLA **Run 1**. No code: structure, numbers, rules, module map.  
**Revised:** October 2026 (Run 1 redesign). Why it changed: `Simulations/BLA/reports/04_run1_redesign_oct2026.md`.

This series is the authoritative design for Run 1. It supersedes the archived failed tests in `reports/test_run_1/`.

The Design Blueprint is a living outline only. When this architecture and the literature disagree with older blueprint numbers, **architecture + literature win**, and the blueprint is updated afterward.

---

## Run 1 in one paragraph

Run 1 is an **offline test campaign**, not the live emotion engine. It rebuilds Feng et al. 2019's basolateral amygdala at Feng's own reduced size of **1,000 cells**. It uses Feng's NEURON files (cell templates, channels, synapses, noise) **unchanged** from ModelDB 247968. The only things we write ourselves are the wiring, the inputs and the measurements. Run 1 passes when the network fires like a real rat BLA at rest, responds to a "threat" input, and settles back afterwards (`10_validation_gates.md`). The simulator and cell detail for the **live** engine are decided later, from the Phase 0 speed benchmark (`07_simulation_protocol.md`).

## Decisions locked for Run 1

| Decision | Choice | File |
|---|---|---|
| Simulator | NEURON 9.0.2 + ModelDB 247968 files, unchanged | `03`, `09` |
| Cell types | PN-A, PN-C, FSI (Feng's three). **No SOM** | `02`, `03` |
| Cell detail | Feng's full templates: 16 segments per PN, 2 per FSI | `03` |
| Size | 1,000 cells (640 / 260 / 100); scale check at 500 | `02` |
| Wiring | Keep Feng's **inputs per cell** (in-degree), not his distance probabilities | `05` |
| Replication target | Feng's **code** where it differs from the paper; every difference logged | `04`, `12` |
| Inputs | Feng's background noise + Feng's afferent spike trains; threat = afferents turned up ×2, ×4, ×8 | `06` |
| Live viewer | Live broadcast of the running test (microscope, oscilloscope, status); display only | `13` |

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
| `03_neuron_models.md` | Feng's cell templates and what they contain |
| `04_synaptic_models.md` | Feng's synapse files: kinetics, weights, depression, gap junctions |
| `05_connectivity.md` | In-degree wiring rule, delays |
| `06_noise_and_drive.md` | Background noise, afferent trains, threat input |
| `07_simulation_protocol.md` | Phase 0 benchmark, run sequence, durations, seeds |
| `08_metrics_and_outputs.md` | Metrics and output files |
| `09_code_module_map.md` | Package layout (no code) |
| `10_validation_gates.md` | Pass/fail gates |
| `11_anti_patterns.md` | Failures that must not recur |
| **`12_sources_map.md`** | **Parameter ↔ source table** |
| `13_live_viewer.md` | Live broadcast of the running test (display only) |

---

## Scope

**In scope:** PN-A + PN-C + FSI; local recurrent circuit; Feng background noise and afferent input; a threat input with three strengths; inhibition check; reproducibility; speed benchmark; a display-only live viewer.

**Out of scope:** SOM, VIP, CCK cells; long after-discharge; LTP/LTD; neuromodulation; LFP calculation; other regions; the live real-time engine; gamma as a pass/fail gate (diagnostic only).
