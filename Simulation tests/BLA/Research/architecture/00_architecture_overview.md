# BLA Simulation Architecture — Overview

**Location:** `Simulation tests/BLA/Research/architecture/`  
**Purpose:** Literature-constrained specification of how isolated BLA **Run 1** must be built. No code — structure, numbers, rules, module map.

This series is the authoritative design for Run 1 (clean restart). It supersedes guessed parameters from archived failed tests in `reports/test_run_1/`.

The Design Blueprint is a living outline only. When this architecture and the literature disagree with older blueprint numbers, **architecture + literature win**, and the blueprint is updated afterward.

---

## Literature authority (required reading order)

1. **`Research/Sources/01_primary_bla_references.md`** — Feng Table 3/4/7, upstream citations (Mahanty 1998, Guzman 2016, Galarreta 1997, Woodruff 2007, Silberberg 2004, Destexhe 2001, Zador 1990).
2. **`Research/Sources/05_computational_neuroscience.md`** — Destexhe 2001 vs 2003 distinction, HH, dual-exp synapses.
3. **`Research/Sources/02_supporting_biological.md`** — Abatis/distance bands, Zador Mg block.
4. **`architecture/12_sources_map.md`** — every architecture number mapped to the Sources entry above.
5. ModelDB **247968** (Feng) and **150288** (Kim) for mechanisms.

If a required value is missing from Sources, **stop** and report the gap. No cortical defaults presented as BLA fact, no “reasonable” guesses.

Full audit: `Research/reports/literature_provenance_audit_sep2026.md`.

---

## Document index

| File | Content |
|------|---------|
| `00_architecture_overview.md` | This file |
| `01_goals_and_constraints.md` | Success criteria, non-goals, hard rules |
| `02_population_structure.md` | Cell counts, layout (default 50/12/8) |
| `03_neuron_models.md` | Compartments, currents, heterogeneity |
| `04_synaptic_models.md` | Kinetics, Mg block, STP + upstream sources |
| `05_connectivity.md` | Distance-dependent + Woodruff probabilities |
| `06_noise_and_drive.md` | OU noise (Destexhe 2001 / Feng Table 7), drive |
| `07_simulation_protocol.md` | Time base, seeds, diagnostics |
| `08_metrics_and_outputs.md` | Metrics, outputs, reproducibility |
| `09_code_module_map.md` | Package layout (no code) |
| `10_validation_gates.md` | Pass/fail gates |
| `11_anti_patterns.md` | Archived failures — must not recur |
| **`12_sources_map.md`** | **Parameter ↔ Sources citation table** |

---

## Scope (isolated BLA Run 1)

**In scope:** PN + PV-like + SOM-like; local recurrent circuit; graded desynchronized activity; functional inhibition; reproducible metrics.

**Out of scope:** long after-discharge; LTP/LTD rules; dynamic neuromodulation; projection-defined ensembles; full 10-region wiring; intermittent gamma as a hard gate (diagnostic only).
