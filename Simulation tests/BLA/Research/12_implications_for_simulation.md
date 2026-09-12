# 12 — Implications for the PFE Simulation

## Isolated BLA characterization (current phase)

Must reproduce:
- Graded, desynchronized PN firing under moderate drive (10–40 Hz biological range).
- Functional PV- and SOM-mediated suppression.
- Intermittent gamma or at least the recurrent dynamics that support it.
- Spike-frequency adaptation via I_sAHP.
- Correct synaptic time constants (AMPA 6.9 ms, NMDA 125 ms + Mg block).

Must **not** be required to produce long after-discharge.

## Parameter sources that override earlier guesses

| Item | Use |
|------|-----|
| Synaptic kinetics | Feng Table 3 |
| Mg block | s(V) = 1/(1+0.33·exp(−0.06V)) |
| Connectivity | Distance-dependent probabilities |
| Noise | Conductance-based OU, Feng Table 7 |
| Short-term depression | Woodruff & Sah / Feng Table 4 |
| PN currents | Kim/Feng multi-compartment + sAHP |
| E_GABA | −75 mV |

## Population size

Blueprint starting point was 50 Pyr / 12 PV / 8 SOM. Later experimental requests used 150/112/108. Either is acceptable provided density and connection probabilities remain consistent with the anatomical data; fixed-K scaling must be avoided.

## Path to the full limbic core

1. Validated isolated BLA (this research dossier + new implementation).
2. Isolated CeA.
3. BLA ↔ CeA two-region network (first place where after-discharge and suppression-gap dynamics become testable).
4. Progressive addition of PFC, VTA, HIP, HYP, PAG.

Every new region should receive the same literature-grounded treatment before being wired into the larger network.
