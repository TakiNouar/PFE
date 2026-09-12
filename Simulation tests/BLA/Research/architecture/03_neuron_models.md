# 03 — Neuron Models

## Principal neuron (PN)

### Morphology

- Multi-compartment: **soma + apical (or proximal) dendrite + passive / distal dendrite**.
- Geometry (L, diam, nseg) taken from Kim/Feng cell templates, not invented.

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

Passive parameters (C_m, R_a, g_L, E_L) and maximal conductance densities must be copied from the same source files / tables into `full_parameters.json`.

### Heterogeneity

- If the source files specify ranges, use those ranges only.
- If the source does **not** specify ranges, use **0%** extra heterogeneity for Run 1 (identical passive parameters across cells of a class). Do not invent ±10% (or any other spread) without a cited justification and an entry in `deviations.md`.

## PV-like fast-spiking interneuron

- Morphology and currents from the FSI templates in Kim/Feng.
- Short action-potential duration, essentially non-adapting high-frequency trains.
- Lower C_m / higher leak relative to PNs as in the source models.

## SOM-like

- Run 1: identical kinetics to PV-like is acceptable **only with a `deviations.md` entry**.
- Later: add NaP and H currents from the extended literature; document as post-Feng.

## Implementation rule

Prefer loading compiled NMODL mechanisms from ModelDB 247968 / 150288.

If the environment cannot run NEURON, a Brian2 (or pure-Python) re-implementation is allowed **only** if:
1. Every coefficient is taken from published tables / `.mod` files, and
2. Every approximation is listed in `deviations.md`.

Re-deriving α/β expressions from memory is forbidden.

**Simulator preference:** NEURON + ModelDB first; Brian2 second with full coefficient table in `full_parameters.json`.
