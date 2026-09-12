# 09 — Neuromodulation

## Dopamine (primarily VTA → BLA)

- Encodes salience and aversive prediction; distinct VTA ensembles target different BLA populations.
- Suppresses feed-forward inhibition (D2 on fast-spiking INs) → facilitates plasticity in principal cells.
- Critical for both fear acquisition and extinction; optogenetic manipulation of VTA→BLA terminals bidirectionally alters extinction.
- Strong candidate for raising post-stimulus excitability (support for emotional inertia at the network level).

## Noradrenaline (locus coeruleus)

- Increases gain and heightens sensitivity to threat.
- Contributes to the “heat” of emotional states independent of pure valence.

## Acetylcholine (basal forebrain)

- Targets both PNs and multiple interneuron classes (PV, VIP, SOM, CCK).
- Enhances encoding precision and cortical signal-to-noise.

## Serotonin (raphe)

- Innervates PNs, PV and NPY-containing interneurons.
- Influences mood stability and impulse control.

## Relevance to PFE design

- Dopamine is treated as first-class in the current blueprint.
- A slower noradrenaline-like arousal variable is intended to supply intensity independent of valence.
- In an isolated BLA simulation these modulators can be omitted or clamped; once VTA and brainstem nodes are added they become dynamic drivers of state persistence and sensitization.
