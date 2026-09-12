# 12 — Implications for the PFE Simulation

## Clean restart (Run 1)

Earlier isolation attempts are archived under `reports/test_run_1/` as failed tests. The next implementation is **Run 1** of a new campaign: literature-constrained parameters only, no inheritance of guessed kinetics from the archive.

See `reports/00_clean_restart_policy.md`.

## Isolated BLA characterization — what Run 1 must reproduce

- Graded, desynchronized PN firing under moderate drive (target mean rate ~10–40 Hz during stimulus).
- Functional PV- and SOM-mediated suppression.
- Spike-frequency adaptation via I_sAHP.
- Correct synaptic kinetics (AMPA PN→PN decay **6.9 ms**, NMDA decay **125 ms** + dynamic Mg²⁺ block).
- Distance-dependent PN→PN connectivity (not fixed in-degree while scaling N).

## What Run 1 must **not** be required to produce

- Long after-discharge / seconds-scale emotional inertia (network-level target; record it, do not optimize for it in isolation).
- Intermittent gamma as a hard pass/fail criterion (desirable if recurrent dynamics are correct; treat as a diagnostic, not a gate — see `architecture/10_validation_gates.md`).

## Parameter sources that override any earlier guesses

| Item | Use |
|------|-----|
| Synaptic kinetics | Feng et al. 2019 Table 3 |
| Mg²⁺ block | `s(V) = 1 / (1 + 0.33 * exp(−0.06 * V))` |
| Connectivity | Distance-dependent probabilities (Feng / Abatis) |
| Noise | Conductance-based OU, Feng Table 7 |
| Short-term depression | Feng Table 4 (Woodruff & Sah 2007 foundation) |
| PN currents | Kim / Feng multi-compartment + I_sAHP |
| E_GABA | **−75 mV** |

## Population size (default)

**Default for Run 1:** N_pyr = 50, N_PV = 12, N_SOM = 8 (total 70).

Scale sweeps keep the same proportions. Density and connection *probabilities* stay fixed; do not use fixed in-degree K while freely scaling N.

## Path to the full limbic core

1. Validated isolated BLA (this dossier + architecture + Run 1 implementation).
2. Isolated CeA.
3. BLA ↔ CeA two-region network (first place where after-discharge and suppression-gap dynamics become meaningful test targets).
4. Progressive addition of PFC, VTA, HIP, HYP, PAG.

Every new region gets the same literature-grounded treatment before wiring.

## Blueprint note

The Design Blueprint is a living outline. When Run 1 (or later work) changes justified parameters or scope, the blueprint is updated to match — not the other way around.
