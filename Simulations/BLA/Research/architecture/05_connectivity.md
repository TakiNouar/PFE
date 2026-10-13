# 05 — Connectivity

## The idea in one line

Every cell receives **the same number of inputs as in Feng's full network**, whatever the network size. This keeps the balance between excitation and inhibition that Feng's model had.

## Targets: inputs per cell (Feng 2019, Results)

| Pathway | Inputs per receiving cell (K) | Feng's reported value |
|---|---|---|
| PN → PN | 25 | 24.98 ± 9.5 |
| FSI → PN | 43 | 42.6 ± 12.9 |
| PN → FSI | 215 | 214.8 ± 58 |
| FSI → FSI (chemical) | 22 | 21.6 ± 7.4 |

"PN" means PN-A and PN-C together. A presynaptic PN is chosen without regard to its type, so about 71 % of a cell's PN inputs come from PN-A and 29 % from PN-C, as in Feng.

## Rule

For each pathway with n_pre possible presynaptic cells:

1. Connection probability **p = min(1, K / n_pre)**.
2. For every ordered pair (pre ≠ post; no self-connections, as in Feng), connect with probability p using the seeded stream.
3. If K > n_pre (only possible in debug sizes), every pair connects and each weight is multiplied by **K / n_pre** so total input stays the same. Record this whenever it happens.

| Pathway | p at 1,000 cells | p at 500 cells |
|---|---|---|
| PN → PN | 25 / 899 ≈ 0.028 | 25 / 449 ≈ 0.056 |
| FSI → PN | 43 / 100 = 0.43 | 43 / 50 = 0.86 |
| PN → FSI | 215 / 900 ≈ 0.24 | 215 / 450 ≈ 0.48 |
| FSI → FSI | 22 / 99 ≈ 0.22 | 22 / 49 ≈ 0.45 |

Connections are chosen **independently of distance**. This is the same simplification the Nair lab uses in its 1,000-cell BLA networks (uniform PN→PN probability, all probabilities divided by the scale factor). It drops three details of Feng's full model, all logged as DEV-001:

- PN → PN distance bands (3 / 2 / 1 / 0.5 % at < 50 / 50–100 / 100–200 / 200–600 µm);
- the ~300 µm limit on interneuron connections;
- the extra reciprocal PN ↔ FSI pairs and the dependence of FSI → FSI chemical links on gap-junction coupling.

## Gap junctions

8 % of all FSI pairs, chosen at random (unordered pairs, no self-pairs). Mechanism in `04_synaptic_models.md`.

## Delays

Internal connections use Feng's rule, with positions from `02_population_structure.md`:

```
delay (ms) = distance (mm) × 1 ms/mm + 0.8 + U(−0.1, 0.1) + dt
```

At 1,000 cells (cube ≈ 0.47 mm, longest diagonal ≈ 0.81 mm) delays fall between about 0.8 and 1.8 ms. Afferent inputs use U(0.5, 1) ms (`06`).

## Construction order

1. Place cells (`02`).
2. For each pathway, choose pairs by the rule above.
3. Choose gap-junction pairs.
4. For each connection: draw the weight (`04`), then the delay jitter. Feng's code seeds each connection's own random stream from the pair of cell IDs (`post_id × N_total + pre_id + 1`), then draws weight first and jitter second. Copy that scheme, adding the global seed, so connections do not depend on build order.
5. Write the connection list (pre, post, pathway, weight, delay) to `outputs/connections.csv`.

## Report after wiring

Mean ± SD of inputs per cell for every pathway (compare with the Feng table above), number of gap-junction pairs, and min / mean / max delay.
