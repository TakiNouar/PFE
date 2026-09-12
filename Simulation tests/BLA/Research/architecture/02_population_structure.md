# 02 — Population Structure

## Default population (1.0×) — Run 1

| Population | Count | Role |
|------------|-------|------|
| Principal (Pyr / PN) | 50 | Glutamatergic, long-range projecting |
| PV-like (fast-spiking) | 12 | Perisomatic inhibition, PING partner |
| SOM-like | 8 | Distal dendritic inhibition |
| **Total** | **70** | |

This is the **only default** for Run 1. Scale sweeps use 0.5×, 1.0×, 1.5×, 3.0× with the **same proportions** (e.g. 3.0× → 150 / 36 / 24). Do not change the inhibitory fraction independently of Pyr count.

## Spatial layout

- Place cells in a cubic volume sized so that mean density is consistent with the literature scale used by Feng (rat BL density; exact side length reported in `full_parameters.json`).
- Minimum inter-soma distance > 25 µm (Feng-style exclusion).
- Report: volume side length, mean pairwise PN–PN distance, realized density.

## Cell classes

- **PN:** glutamatergic; may be split into Type-A (strong adaptation) and Type-C (weak adaptation) if ModelDB templates distinguish them; otherwise a single adapting class is acceptable and must be documented.
- **PV-like:** fast-spiking interneuron from Kim/Feng.
- **SOM-like:** for Run 1, the same fast-spiking kinetics as PV-like may be used **only if documented in `deviations.md`** as a temporary limitation. Distinct SOM currents (NaP, H) from later extensions may be added in a later run and labelled as post-Feng.

## What must not be done

- Do not keep PN count fixed while scaling only inhibitory populations (or vice versa).
- Do not use a pure feed-forward architecture; recurrent PN→PN connections are required.
- Do not introduce a second “experimental” baseline without a written decision in `reports/` that updates this file.
