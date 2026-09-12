# 03 — Local Connectivity

## Principal → Principal

- Sparse and **distance-dependent**.
- Feng et al. / anatomical sources:  
  - ~3 % at <50 µm  
  - ~2 % at 50–100 µm  
  - ~1 % at 100–200 µm  
  - ~0.5 % at 200–600 µm  
- Reciprocal connections exist but are not obligatory.
- Short-term depression is present (parameters often taken from neocortical data when BLA-specific numbers are missing).

## Principal → Interneuron

- PN → PV: ~12 % unidirectional, ~16 % reciprocal (Woodruff & Sah 2007).
- PN → SOM: also present; exact probabilities less completely quantified.
- Many of these synapses onto interneurons use **calcium-permeable AMPA receptors** (GluR2-lacking), enabling NMDA-independent LTP at some interneuron synapses (Mahanty & Sah 1998).

## Interneuron → Principal

- PV → PN: ~34 % unidirectional; perisomatic targeting.
- SOM → PN: distal dendritic targeting.
- CCK → PN: perisomatic, CB1-modulated.
- Single PV basket cells contact a given PN with only 4–5 boutons on average, but many PV cells converge.

## Interneuron → Interneuron

- PV → PV: ~26 % total connectivity (includes chemical synapses + gap junctions at ~8 %).
- PV inhibits SOM.
- VIP preferentially inhibits other interneurons (including SOM and PV), producing disinhibition of PNs.
- Gap junctions among PV cells support fast synchrony.

## Computational consequences

- Reciprocal PN–PV loops are the core of the **PING** (pyramidal-interneuron network gamma) mechanism.
- Dense perisomatic PV innervation allows strong feedback inhibition and competition between PN ensembles.
- Dendritic SOM inhibition can selectively gate specific afferent pathways.

Any model that uses fixed in-degree while scaling only population size will distort the E/I balance; distance-dependent probabilities inside a realistic volume preserve the biological regime.
