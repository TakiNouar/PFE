# 02 — Population Structure

## Reference population (1.0×)

Two admissible reference sizes are defined. Choose one and keep it fixed for the entire characterization run series.

### Option A — Blueprint scale (preferred for first successful full run)

| Population | Count | Role |
|------------|-------|------|
| Principal (Pyr / PN) | 50 | Glutamatergic, long-range projecting |
| PV-like (fast-spiking) | 12 | Perisomatic inhibition, PING partner |
| SOM-like | 8 | Distal dendritic inhibition |
| **Total** | **70** | |

### Option B — Expanded scale (later request)

| Population | Count |
|------------|-------|
| Principal | 150 |
| PV-like | 112 |
| SOM-like | 108 |
| **Total** | **370** |

**Rule:** All scale-sweep factors (0.5×, 1.5×, 3.0×) multiply every population by the same factor so relative proportions stay constant.

## Spatial layout

- Place somata uniformly at random inside a cubic volume whose side length is chosen so that the resulting density matches the literature density used by Feng (~27 000 cells in a 1.4 mm cube for the full rat BL model, scaled appropriately for the chosen N).
- Enforce a minimum inter-soma distance (Feng used >25 µm) to avoid spatial collapse.
- Compute Euclidean pairwise distances for all PN–PN pairs; these distances drive the connection probabilities.

## Cell-type identity for this isolated phase

- **PN:** multi-compartment, adapting (I_sAHP present). Optionally split into Type-A (strong adaptation) and Type-C (weak adaptation) if the ModelDB templates distinguish them; otherwise a single adapting class is acceptable.
- **PV-like:** fast-spiking interneuron model from Kim/Feng.
- **SOM-like:** for the first isolated characterization, the same fast-spiking kinetics as PV may be used (as previously authorized). Distinct SOM currents (NaP, H) from Cattani et al. 2024 may be added later and must be labelled as a post-Feng extension.

## What must not be done

- Do not keep PN count fixed while scaling only inhibitory populations (or vice versa).
- Do not use a pure feed-forward architecture; recurrent PN→PN connections are required.
