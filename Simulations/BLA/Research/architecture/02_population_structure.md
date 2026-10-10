# 02 — Population Structure

## Authoritative reference population for the next implementation

**Locked choice: Blueprint scale**

| Population | Count | Role |
|------------|-------|------|
| Principal (Pyr / PN) | **50** | Glutamatergic, long-range projecting |
| PV-like (fast-spiking) | **12** | Perisomatic inhibition, PING partner |
| SOM-like | **8** | Distal dendritic inhibition |
| **Total** | **70** | |

Ratio ≈ 1 : 0.24 : 0.16 (excitatory-dominant, consistent with biological BLA ≈ 80–90 % principal cells).

### Why not 150 / 112 / 108?

A later experimental request used 150 Pyr / 112 PV / 108 SOM (near 1 : 0.75 : 0.72). That composition is **not** interchangeable with the blueprint:

- It makes inhibitory cells almost as numerous as principal cells, which does not match BLA histology.
- Distance-dependent and probability-based connectivity were derived under excitatory-dominant densities.
- Using the expanded counts without re-deriving connection probabilities would distort E/I balance.

**Decision:** All future isolated-BLA characterization runs use **50 / 12 / 8** (or exact proportional scales of that ratio). The 150/112/108 figures are retained only as historical notes in test_run_1 reports and must not be used as the design target.

## Scale sweep

Multiply every population by the same factor (0.5×, 1.0×, 1.5×, 3.0×) so relative proportions stay constant.

## Spatial layout

- Place somata randomly in a cubic volume sized to preserve literature density. Feng places 27 000 cells in a 1.4 mm cube (≈ 9 800 cells/mm³). For N = 70 that gives a cube ≈ 190 µm on a side; at 3.0× (N = 210), ≈ 275 µm.
- Minimum inter-soma distance > 25 µm.
- Euclidean distances drive PN→PN connection probabilities and synaptic delays.
- Consequence: PN→PN recurrence is very sparse at this scale (see `05_connectivity.md`, U23).

### Status of 50 / 12 / 8

This is the locked **default**, not a validated size. The archived runs that used it had wrong kinetics, so they cannot validate it (U19). Clean Run 1 and its scale sweep are the first real test.
