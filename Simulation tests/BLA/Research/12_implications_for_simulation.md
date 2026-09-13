# 12 — Implications for the PFE Simulation

## Clean restart (Run 1)

Earlier isolation attempts are archived under `reports/test_run_1/` as failed tests. The next implementation is **Run 1**: literature-constrained parameters only.

See `reports/00_clean_restart_policy.md`.

## Isolated BLA characterization — what Run 1 must reproduce

- Graded, desynchronized PN firing under moderate drive (target mean rate ~10–40 Hz during stimulus).
- Functional PV- and SOM-mediated suppression.
- Spike-frequency adaptation via I_sAHP.
- Correct synaptic kinetics (AMPA PN→PN decay **6.9 ms**, NMDA decay **125 ms** + dynamic Mg²⁺ block).
- Distance-dependent PN→PN connectivity (not fixed in-degree while scaling N).

## What Run 1 must **not** be required to produce

- Long after-discharge / seconds-scale emotional inertia.
- Intermittent gamma as a hard pass/fail criterion (diagnostic only).
- Astrocyte dynamics, LTP/LTD rules, projection-defined ensembles, VIP/CCK as separate classes.

## Parameter sources

| Item | Use |
|------|-----|
| Synaptic kinetics | Feng Table 3 + upstream (see Sources) |
| Mg²⁺ block | Zador formula via Feng |
| Connectivity | Distance-dependent (Feng / Abatis) |
| Noise | Destexhe 2001 formalism; Feng Table 7 |
| STP | Feng Table 4 (Woodruff / Silberberg as attributed) |
| PN currents | Kim / Feng multi-compartment + I_sAHP |
| E_GABA | −75 mV |

**Default population:** 50 Pyr / 12 PV / 8 SOM.

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
