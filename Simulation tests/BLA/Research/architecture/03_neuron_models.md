# 03 — Neuron Models

## Principal neuron (PN)

### Morphology

- Multi-compartment: **soma + apical (or proximal) dendrite + passive / distal dendrite**.
- Geometry numbers (L, diam, nseg) taken from the Kim/Feng cell templates, not invented.

### Currents (all from ModelDB / Kim–Feng)

| Current | Role |
|---------|------|
| I_Na | Fast spike |
| I_Kdr | Repolarization |
| I_A | A-type K |
| I_M | M-current |
| I_H | Hyperpolarization-activated |
| I_Ca | High-threshold Ca |
| I_NaP | Persistent Na |
| **I_sAHP** | Slow Ca-dependent AHP — **mandatory for adaptation** |
| Leak | Resting conductance |

Passive parameters (C_m, R_a, g_L, E_L) and maximal conductance densities must be copied from the same source files / tables.

### Heterogeneity

- If the source files specify ranges, use them.
- Otherwise apply a uniform ±10 % variation on C_m, g_L and E_L only, drawn once per neuron from the global seed.

## PV-like fast-spiking interneuron

- Morphology and currents from the FSI templates in Kim/Feng (typically soma + dendrite).
- Short action-potential duration, essentially non-adapting high-frequency trains.
- Lower C_m / higher leak relative to PNs as in the source models.

## SOM-like

- Phase-1 (isolated characterization): identical kinetics to PV-like is acceptable and must be documented.
- Phase-2 (optional extension): add NaP and H currents from Cattani et al. 2024; document as a post-Feng addition.

## Implementation rule

Prefer loading the compiled NMODL mechanisms from ModelDB 247968 / 150288. If the environment cannot run NEURON, a pure-Python or Brian2 re-implementation is allowed **only** if every coefficient is taken from the published tables / `.mod` files and every approximation is listed in a deviations section. Re-deriving α/β expressions from memory is forbidden.
