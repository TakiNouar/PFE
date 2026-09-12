# BLA Simulation Architecture — Overview

**Location:** `Simulation tests/BLA/Research/architecture/`  
**Purpose:** Complete, literature-constrained specification of how the isolated BLA simulation must be built. No code — only structure, numbers, rules, and module mapping.

This series is the authoritative design for **Run 1** (clean restart). It supersedes all guessed parameters from the archived failed tests in `reports/test_run_1/`.

The Design Blueprint is a living project outline only; when this architecture and the literature disagree with older blueprint numbers, **this architecture and the literature win**, and the blueprint should be updated afterward.

---

## Document index

| File | Content |
|------|---------|
| `00_architecture_overview.md` | This file — goals, constraints, reading order |
| `01_goals_and_constraints.md` | Success criteria, non-goals, hard rules |
| `02_population_structure.md` | Cell counts, types, spatial layout, density |
| `03_neuron_models.md` | Compartments, currents, passive properties, heterogeneity |
| `04_synaptic_models.md` | AMPA / NMDA / GABA kinetics, Mg block, STP |
| `05_connectivity.md` | Distance-dependent rules, probabilities, construction algorithm |
| `06_noise_and_drive.md` | OU conductance noise, private sensory drive, stimulus protocol |
| `07_simulation_protocol.md` | Time base, seeds, scale sweeps, diagnostics |
| `08_metrics_and_outputs.md` | Required metrics, file outputs, reproducibility checks |
| `09_code_module_map.md` | Recommended package / module structure (no code) |
| `10_validation_gates.md` | Gate checklist before accepting a run |
| `11_anti_patterns.md` | Explicit list of what failed in archived tests and must not be repeated |

---

## Design principle

Every number and every kinetic form must be traceable to:

1. Feng et al. 2019 (eNeuro) + ModelDB 247968, or
2. Kim et al. 2013 + ModelDB 150288, or
3. The supporting experimental papers listed in `Research/Sources/`.

If a required value is missing from those sources, the implementation **stops** and reports the gap. No substitution, no cortical defaults presented as BLA fact, no “reasonable” guesses.

---

## Scope of this architecture

**In scope (isolated BLA Run 1):**
- Principal neurons + PV-like + SOM-like populations
- Local recurrent circuitry with correct kinetics and connectivity
- Graded, desynchronized activity under moderate drive
- Functional interneuron suppression
- Reproducible metrics

**Out of scope for the isolated phase:**
- Long after-discharge / emotional inertia (network-level target)
- Long-term plasticity (LTP/LTD rules)
- Dynamic neuromodulation (DA, NA, ACh)
- Projection-defined ensembles (NAc / CeA / vHPC)
- Full 10-region wiring
- Intermittent gamma as a hard pass/fail criterion (diagnostic only)
