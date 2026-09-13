# 03 — Local Connectivity

## Principal → Principal

- Sparse and **distance-dependent**.
- Feng et al. / anatomical sources:
  - ~3 % at <50 µm
  - ~2 % at 50–100 µm
  - ~1 % at 100–200 µm
  - ~0.5 % at 200–600 µm
- Reciprocal connections exist but are not obligatory.
- Short-term depression present (PN→PN D_max = 0.5 from Silberberg et al. 2004 neocortex per Feng Table 4 — not BLA-measured).

## Principal → Interneuron

- PN → PV: ~12 % unidirectional, ~16 % reciprocal (Woodruff & Sah 2007).
- PN → SOM: present; exact probabilities less completely quantified.
- Many synapses onto interneurons use **calcium-permeable AMPA** (GluR2-lacking), enabling NMDA-independent LTP at some IN synapses (Mahanty & Sah 1998).

## Interneuron → Principal

- PV → PN: ~34 % unidirectional; perisomatic (basket) or AIS (chandelier).
- SOM → PN: distal dendritic targeting.
- CCK → PN: perisomatic, CB1-modulated.
- Single PV basket cells contact a given PN with few boutons on average; many PV cells converge.

## Interneuron → Interneuron

- PV → PV: ~26 % total connectivity (chemical + gap junctions ~8 % if modeled).
- **PV inhibits SOM** — functionally critical for fear acquisition: CS drives PV → PV suppresses SOM → removes SOM dendritic inhibition from PNs → PNs disinhibited to encode CS–US. Core circuit motif, not a minor side path. (Perumal & Sah 2021; Báldi et al. 2025.)
- VIP preferentially inhibits other interneurons (SOM, PV), producing disinhibition of PNs.
- Gap junctions among PV cells support fast synchrony.

## Feedback vs feedforward inhibition (circuit motif assignment)

| Interneuron | Drive source | Inhibitory motif | Primary target |
|-------------|--------------|------------------|----------------|
| **SOM** | Local PCs (**feedback**) | Feedback inhibition | Distal dendrites of PCs |
| **VIP** | Extrinsic afferents (**feedforward**) | Feedforward → disinhibition | Other INs (SOM, PV) |
| **PV** | Both local PCs and extrinsic afferents | Both feedback and feedforward | Perisomatic (soma, AIS) |

**Consequence:** SOM tracks local excitatory state (follows PCs). VIP tracks incoming information (afferent drive). PV sits at the intersection. SOM is a natural readout of local network activity; VIP gates external input impact.

**Source:** Báldi et al. (2025), *Cell Reports* — systematic side-by-side in BLA.

## Computational consequences

- Reciprocal PN–PV loops are the core of **PING**.
- Dense perisomatic PV innervation allows strong feedback inhibition and competition between PN ensembles.
- Dendritic SOM inhibition can selectively gate afferent pathways.
- Fixed in-degree while scaling only population size distorts E/I balance; distance-dependent probabilities in a realistic volume preserve the biological regime.
