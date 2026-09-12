# 05 — Connectivity

**Source of truth:** Feng Tables 5–6 (distance bands via Abatis et al. 2017); Woodruff & Sah 2007 / Feng for FSI probabilities.  
See `Research/Sources/01_primary_bla_references.md`, `02_supporting_biological.md`, and `12_sources_map.md`.

## PN → PN (distance-dependent)

After placing somata, for every ordered pair (i ≠ j):

1. Euclidean distance d (µm).
2. Connection probability:

| Distance band | Probability | Source |
|---------------|-------------|--------|
| d < 50 µm | 0.03 | Feng Tables 5–6 ← Abatis et al. 2017 |
| 50 ≤ d < 100 | 0.02 | same |
| 100 ≤ d < 200 | 0.01 | same |
| 200 ≤ d < 600 | 0.005 | same |
| d ≥ 600 | 0 | same |

3. Bernoulli trial from the global RNG; on success, AMPA + NMDA on the postsynaptic dendrite.

**Forbidden:** fixed in-degree K while freely scaling N (archived failure mode).

## PV → PN

- **P_PV_PN = 0.34** (unidirectional) — Woodruff & Sah 2007 / Feng.
- Target: soma / proximal dendrite (perisomatic).

## PN → PV

- ~0.12 unidirectional + ~0.16 reciprocal — Woodruff & Sah 2007 / Feng.
- Report realized uni/reciprocal fractions after wiring.

## PV → PV

- ~0.26 total chemical connectivity — Woodruff & Sah / Feng.
- Gap junctions (~8% in Feng-scale descriptions) only if ModelDB includes them without invention; else omit + `deviations.md`.

## SOM → PN / PN → SOM

- GABA-A / AMPA kinetics as in `04_synaptic_models.md`.
- **Run 1:** `P_SOM_PN = 0.34` (same as PV→PN) — **approximation**, not a Feng Table value. Must be listed in `deviations.md`.
- PN→SOM default probability = PN→PV unidirectional unless ModelDB specifies otherwise; report the value used.

## Construction order

1. Place somata (density + min distance > 25 µm per Feng-style exclusion).
2. PN→PN from distance probabilities.
3. PV↔PN and PV↔PV from fixed probabilities above.
4. SOM→PN and PN→SOM.
5. Attach synapses (`04`) + dynamic STP (Feng Table 4).
6. Report volume, mean PN–PN distance, synapse counts, **realized** probabilities.
