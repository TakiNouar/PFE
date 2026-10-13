# 12 — Implications for the PFE Simulation

## Clean restart (Run 1)

Earlier isolation attempts are archived under `reports/test_run_1/` as failed tests. The next implementation is **Run 1**: literature-constrained parameters only.

See `reports/00_clean_restart_policy.md`.

## Isolated BLA characterization — what Run 1 must reproduce

*Revised 2026-10-13 (`reports/04_run1_redesign_oct2026.md`). The binding list is `architecture/10_validation_gates.md`.*

- Resting rates like rat BLA: principal cells about 0.2–3 Hz, FSIs about 10–30 Hz.
- A dose-dependent response to a threat input, then a return to rest.
- Functional FSI (PV-like) inhibition.
- Spike-frequency adaptation via I_sAHP (PN-A strong, PN-C weak).
- Feng's synapse files unchanged (AMPA ~7 ms, NMDA 125 ms + dynamic Mg²⁺ block, short-term depression).
- Feng's inputs per cell on every pathway (25 / 43 / 215 / 22), at 1,000 cells.

## What Run 1 must **not** be required to produce

- Long after-discharge / seconds-scale emotional inertia.
- Intermittent gamma as a hard pass/fail criterion (diagnostic only).
- Astrocyte dynamics, LTP/LTD rules, projection-defined ensembles, VIP/CCK as separate classes.

## Parameter sources

| Item | Use |
|------|-----|
| Cells, synapses, Mg²⁺ block, STP, noise mechanisms | Feng's ModelDB 247968 files, unchanged |
| Values where paper and code differ | Code (`simulation/deviations.md` DEV-002 to DEV-004) |
| Connectivity | Feng's realised inputs per cell, distance-independent (DEV-001) |
| Afferent input | Feng's recorded-cell spike trains |

Full map: `architecture/12_sources_map.md`.

**Population:** 640 PN-A / 260 PN-C / 100 FSI (Feng's reduced-model size). No SOM in Run 1.

## Path to the full limbic core

1. Validated isolated BLA (Run 1).
2. Isolated CeA.
3. BLA ↔ CeA two-region network.
4. Progressive PFC, VTA, HIP, HYP, PAG.

## What the 2026 literature batch establishes for multi-region work

1. **SOM activity level = suppression-state indicator.** When BLA is wired to PFC and CeA, SOM rate is a primary measurable proxy for local top-down suppression. Monitoring SOM population rate is the simulation’s window into the suppression gap inside BLA.

2. **Valence competition is local and interneuron-mediated.** Mutual feedforward inhibition between positive- and negative-valence PN ensembles can be tested in isolated BLA if two PN ensembles with cross-inhibitory INs are instantiated.

3. **Projection-specific routing is experience-dependent.** Same input routes differently to NAc vs CeA vs BNST based on history — requires wired targets and updateable weights, not fixed isolated-BLA parameters.

4. **Astrocytes carry tonic arousal.** NA → α1 → astrocyte → sustained anxiety tone is not captured by neuron-only HH simulation. Multi-region design should plan a slow scalar (or equivalent) for that tone even if external at first.

## Blueprint note

The Design Blueprint is a living outline. When Run 1 or later work changes justified parameters or scope, the blueprint is updated to match — not the other way around.
