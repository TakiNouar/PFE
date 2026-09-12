# 10 — Computational Models

## Feng et al. 2019 (eNeuro) — primary reference

- First large-scale (~27 000 cell) biophysically and anatomically realistic model of rat BL.
- Multi-compartment PNs + FSIs, conductance-based synapses, short-term depression, distance-dependent connectivity, detailed LFP calculation.
- Intrinsically generates intermittent gamma matching in-vivo statistics.
- ModelDB accession **247968**.
- All kinetic parameters constrained by published electrophysiology.

## Kim et al. 2013 and related LA models

- 1000-cell LA network focused on fear-conditioning plasticity and memory allocation.
- Introduced the detailed single-cell PN and FSI mechanisms later reused by Feng.
- ModelDB accession **150288**.
- Demonstrated competitive synaptic interactions that keep the size of the memory trace relatively constant.

## Later extensions

- Models that add VIP and SOM with their specific currents (D-current, NaP, H-current) to explain a broader set of BLA rhythms and their role in fear learning (e.g. 2024 computational work).
- Projection-specific and valence-specific ensemble models that incorporate NAc-, CeA- and vHPC-projecting populations.

## Practical rule for the PFE

When in doubt, start from the Feng/Kim parameter set and the ModelDB implementations. Deviations must be documented and justified. Guessed time constants or omitted currents (especially sAHP and Mg block) have already been shown to produce the failures recorded in `test_run_1`.
