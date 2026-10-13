# 02 — Population Structure

## Cell types and counts

Feng's model has three cell types. Run 1 uses exactly these, in Feng's proportions.

| Population | Share | Run 1 (1.0×) | Scale check (0.5×) | What it is |
|------------|-------|--------------|--------------------|------------|
| PN-A | 64 % | **640** | 320 | Excitatory principal cell, strong adaptation (high sAHP) |
| PN-C | 26 % | **260** | 130 | Same cell, almost no adaptation (low sAHP) |
| FSI | 10 % | **100** | 50 | Fast-spiking inhibitory interneuron (PV-like) |
| **Total** | | **1,000** | **500** | |

Source: Feng et al. 2019 (64 % PN-A, 26 % PN-C, 10 % FSI). Feng also used "a 1,000-neuron reduced model with similar connectivity rules and proportions". The Nair lab's own Feng-network rebuild uses the same 640 / 260 / 100 split (`feng_homogenous` in github.com/tjbanks/AmygdalaTheta).

### Why 1,000 cells and not 70

Each principal cell in Feng's network receives about **43 inhibitory inputs** (Feng 2019: 42.6 ± 12.9). A network needs at least that many FSIs to wire this without tricks. With 10 % FSIs that means ≥ 430 cells. At 1,000 cells each FSI→PN link has a 43 % chance, close to the 50 % Feng uses for pairs within 300 µm (34 % one-way + 16 % reciprocal, Woodruff & Sah 2007). The old 50 / 12 / 8 design gave each principal cell about 0.65 excitatory and 7 inhibitory inputs instead of 25 and 43. It could not test recurrent dynamics. See `reports/04_run1_redesign_oct2026.md`.

### Why no SOM cells

Feng's model has none. Adding SOM required two invented values (old U10, U11). SOM can be added later from Cattani et al. 2024, as a separate, logged extension.

### Why 90 / 10 and not the biological ~80 / 20

About 80 % of BLA neurons are principal cells, but the remaining 20 % include several interneuron types (PV, SOM, VIP, CCK). Feng models only the PV-like FSIs, which he sets at 10 %. Run 1 copies Feng; it does not claim to represent the other interneuron types.

## Sizes allowed

| Size | Use | Gated? |
|------|-----|--------|
| 1,000 | Main Run 1 network | Yes |
| 500 | Scale check (Gate 5) | Yes |
| 100 (64 / 26 / 10) | Debugging only, fast iteration | No |

If the Phase 0 benchmark shows 1,000 cells are too slow to finish the protocol, 500 becomes the main size and 250 the scale check. Record the change in `deviations.md`.

## Spatial placement

Positions are used **only for synaptic delays** (connection choice ignores distance, see `05_connectivity.md`).

- Somata placed uniformly at random in a cube at Feng's density: 9,840 cells/mm³ (27,000 cells in 1.4 mm³). Side = (N / 9,840)^(1/3) mm: about 0.467 mm at N = 1,000 and 0.370 mm at N = 500.
- Minimum inter-soma distance 25 µm (Feng). Re-draw a position that violates it.
- Positions are stored in **mm**, as in Feng's code.
