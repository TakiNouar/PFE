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

3. Bernoulli trial from the global RNG. On success, create AMPA + NMDA synapses on the postsynaptic dendrite.

**Forbidden:** fixed in-degree K = 3 (or any fixed K) while freely scaling population size. That produced the large-N collapse in the archived failed tests.

## PV → PN

- Probability **P_PV_PN = 0.34** (unidirectional).
- Target: soma / proximal dendrite (perisomatic).

## PN → PV

- ≈ 0.12 unidirectional + ≈ 0.16 reciprocal (Woodruff & Sah / Feng).
- Implement so that realized uni/reciprocal fractions are reported after wiring.

## PV → PV

- ≈ 0.26 total chemical connectivity.
- Gap junctions only if ModelDB includes them and they load without invention; otherwise omit and note in `deviations.md`.

## SOM → PN

- GABA-A kinetics same as PV→PN.
- **Named constant for Run 1:** `P_SOM_PN = 0.34` (same as PV→PN), documented as an approximation because SOM-specific anatomical probabilities are less complete than PV.
- Any other value must be written into `full_parameters.json` and justified in `deviations.md`.

## PN → SOM

- Use PN→PV AMPA/NMDA kinetics (2.4 ms AMPA decay).
- Probability: report the value used; default equal to PN→PV unidirectional probability unless ModelDB specifies otherwise.

## Construction algorithm (required order)

1. Place all somata (density + minimum distance).
2. Build PN→PN edges from distance probabilities.
3. Build PV↔PN and PV↔PV edges from fixed probabilities.
4. Build SOM→PN (and PN→SOM) edges.
5. Attach AMPA/NMDA or GABA-A synapses with §04 kinetics.
6. Enable dynamic STP on every synapse (Feng Table 4 numbers).
7. Report: volume side length, mean pairwise PN–PN distance, synapse counts by type, **realized** connection probabilities.
