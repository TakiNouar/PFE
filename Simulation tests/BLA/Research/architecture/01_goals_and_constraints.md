# 01 — Goals and Constraints

## Primary goals of the isolated BLA simulation

1. Produce **graded, desynchronized** principal-cell activity under moderate sensory-like drive.
2. Demonstrate **functional inhibition** by PV-like and SOM-like populations.
3. Use only **literature-constrained** parameters (Feng / Kim + supporting papers).
4. Be **bit-reproducible** under a single global seed.
5. Provide clean, validated parameters that can later be dropped into the multi-region network without re-tuning.

## Explicit non-goals (isolated phase)

- After-discharge ≥ 10 ms (or seconds-scale emotional inertia).
- Learning / plasticity rules.
- Neuromodulatory dynamics.
- Matching every detail of the 27 000-cell Feng model (scaled populations are allowed; kinetics and connectivity rules are not).

## Hard constraints (non-negotiable)

| Constraint | Rule |
|------------|------|
| Kinetics source | ModelDB `.mod` / published tables only; no re-derivation |
| AMPA PN→PN decay | **6.9 ms** (not 2 ms) |
| NMDA | 125 ms decay + **dynamic Mg²⁺ block** evaluated every step |
| E_GABA | **−75 mV** |
| Adaptation | **I_sAHP** present on principal cells |
| Connectivity | Distance-dependent probabilities; **no fixed in-degree K=3** while scaling N freely |
| Noise | Conductance-based OU (Feng Table 7 coefficients) |
| Short-term depression | Dynamic, on every synapse |
| Drive | ≥75 % private (independent per neuron) |
| Seed | Single global seed for all random draws |
| Missing value | Halt and report; do not invent |

## Success criteria (must all pass)

- Synchrony index < 0.5
- CV of ISIs > 0.3
- Active fraction (Pyr rate > 5 Hz) > 0.4
- Mean Pyr rate during stimulus inside ~10–40 Hz biological range
- Interneuron suppression ratio clearly > 1 (target ~2× from measured ratio 0.51)
- Calibration and main run with identical parameters + seed → bit-identical spike times

After-discharge duration is **recorded** but is not a pass/fail criterion.
