# 05 — Connectivity

## PN → PN (distance-dependent)

After placing somata in the volume, for every ordered pair (i ≠ j):

1. Compute Euclidean distance d (µm).
2. Assign connection probability:

| Distance band | Probability |
|---------------|-------------|
| d < 50 µm | 0.03 |
| 50 ≤ d < 100 | 0.02 |
| 100 ≤ d < 200 | 0.01 |
| 200 ≤ d < 600 | 0.005 |
| d ≥ 600 | 0 |

3. Draw a Bernoulli trial from the global RNG. If success, create AMPA + NMDA synapses on the postsynaptic dendrite.

**Forbidden:** fixed in-degree K = 3 (or any fixed K) while freely scaling population size. That produced the large-N collapse in test_run_1.

## PV → PN

- Probability ≈ **0.34** (unidirectional).
- Target: soma / proximal dendrite (perisomatic).

## PN → PV

- ≈ 0.12 unidirectional + ≈ 0.16 reciprocal (Woodruff & Sah / Feng).
- In practice a combined probability draw that yields the published uni/reciprocal fractions is acceptable.

## PV → PV

- ≈ 0.26 total chemical connectivity.
- Gap junctions only if the ModelDB implementation includes them and they can be loaded without invention.

## SOM → PN

- Use the same GABA-A kinetics as PV→PN.
- Probability may be set equal to (or a documented fraction of) the PV→PN probability for the isolated phase; exact SOM-specific anatomical probabilities are less completely quantified and any choice must be stated.

## Construction algorithm (required order)

1. Place all somata (respecting density and minimum distance).
2. Build PN→PN edges from distance probabilities.
3. Build PV↔PN and PV↔PV edges from fixed probabilities.
4. Build SOM→PN edges.
5. Attach AMPA/NMDA or GABA-A synapses with the kinetic parameters of §04.
6. Enable dynamic STP on every synapse.
7. Report: volume side length, mean pairwise PN–PN distance, number of synapses of each type, realized connection probabilities.
