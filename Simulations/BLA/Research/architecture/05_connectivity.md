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

**Expected sparsity at Run 1 scale (U23):** a density-preserving cube for 70 cells is ≈ 190 µm on a side, so most PN pairs fall in the 1–2 % bands. The rough estimate is **< 1 PN→PN input per PN at 1.0×** (≈ 35 synapses in total) and ≈ 1.6 at 3.0×. Report realized counts. If recurrence is near-null, Diagnostics A/B (`07_simulation_protocol.md`) will show little difference. That is an expected property of the scale, not a bug.

## PV → PN

- **P_PV_PN = 0.34** (unidirectional) — Woodruff & Sah 2007 / Feng.
- Target: soma / proximal dendrite (perisomatic).

## PN → PV

- ~0.12 unidirectional + ~0.16 reciprocal — Woodruff & Sah 2007 / Feng.
- Report realized uni/reciprocal fractions after wiring.

## PV → PV

- Chemical: 0.26 overall (0.20 unidirectional + 0.03 bidirectional). Feng also conditions this on electrical coupling: 50 % uni / 25 % bi among gap-junction-coupled pairs, 19 % / 3 % among uncoupled pairs. Source: Woodruff & Sah 2007 / Feng Table 6.
- Gap junctions: 8 % of PV pairs, coupling ≈ 0.05 (ModelDB `gap.mod`). Include only from ModelDB; otherwise omit and add a `deviations.md` entry.

## Interneuron distance limit

Feng restricts interneuron connections (PN↔PV, PV↔PV) to pairs within **~300 µm**. At N=70 (cube ≈ 190 µm) nearly all pairs fall inside this limit, but apply the rule so it scales correctly at 3.0×.

## SOM → PN / PN → SOM

- GABA-A / AMPA kinetics as in `04_synaptic_models.md`.
- **Run 1:** `P_SOM_PN = 0.34` (same as PV→PN) — **approximation**, not a Feng Table value. Must be listed in `deviations.md`.
- PN→SOM default probability = PN→PV unidirectional unless ModelDB specifies otherwise; report the value used.

## Construction order

1. Place somata (density + min distance > 25 µm per Feng-style exclusion).
2. PN→PN from distance probabilities.
3. PV↔PN and PV↔PV from fixed probabilities above.
4. SOM→PN and PN→SOM.
5. Attach synapses (`04`): draw lognormal weights, compute distance-dependent delays, add dynamic STP (Feng Table 4).
6. Report volume, mean PN–PN distance, synapse counts, **realized** probabilities, and mean PN→PN in-degree.
