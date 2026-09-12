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

- Place somata randomly in a cubic volume sized to preserve literature density (Feng reference: ~27 000 cells in a 1.4 mm cube for the full rat BL model, scaled to N = 70).
- Minimum inter-soma distance > 25 µm.
- Euclidean distances drive PN→PN connection probabilities.
