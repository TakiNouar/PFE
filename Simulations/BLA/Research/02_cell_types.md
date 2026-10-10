# 02 — Cell Types

## Principal neurons (PNs / pyramidal-like)

- Glutamatergic, long-range projecting.
- Exhibit spike-frequency adaptation of varying strength (Type-A strong adaptation, Type-C continuous firing in Kim/Feng classification).
- Adaptation is largely produced by the slow Ca²⁺-dependent after-hyperpolarization current (I_sAHP).
- Receive both cortical and thalamic excitatory input; form the majority of the local recurrent excitatory network.

**Fear-memory recruitment:** only a minority of LA principal neurons become plastic and join the memory trace — ~**25 %** in classic studies, as stated by Kim et al. 2013 (citing Quirk et al. 1995, Repa et al. 2001, Rumpel et al. 2005).

**Valence-specific PN subpopulations (mouse data):** Excitatory principal neurons are not functionally uniform. In mouse BLA, two genetically distinct, spatially biased PN populations participate in opposing valence behaviors and compete via mutual inhibition through local interneurons:

- *Rspo2+* (anterior BLA / LA) — negative-valence / aversive.
- *Ppp1r1b+* (posterior BLA) — positive-valence / appetitive.

A finer mouse taxonomy reports ~11 glutamatergic clusters, some mixed or social. **Caveat:** genetic labels are mouse-specific; Feng/Kim models are rat. For simulation, the relevant take-away is **competition via interneurons**, not the marker names.

**Source:** Kim et al. (2016), *Nat Neurosci*; Lim et al. (2024), *Nat Commun*.

## Interneuron taxonomy (GABAergic)

Approximate contributions in **rat** basolateral complex. **Each row has its own primary source** — do not cite Mascagni & McDonald 2003 as a blanket source for the whole table (that paper is CCK-specific).

| Subtype | ~% of INs | Main axonal target | Key markers | Primary source |
|---------|-----------|--------------------|-------------|----------------|
| PV+ (basket + chandelier) | **~40–50 %** (lower in LA, ~20 %) | Basket: perisomatic; **chandelier (axo-axonic): AIS only** | Parvalbumin | **McDonald & Betette (2001)**, *Neuroscience* 102:413–425 |
| SOM+ / SST | **~15–20 %** | Distal dendrites & spines | Somatostatin; many also NPY | **McDonald & Mascagni (2002)**, *Brain Res* 943:237–244 |
| CCK large (CCKL) | ~7 % | Perisomatic (basket) | Cholecystokinin, often CB1 | **Mascagni & McDonald (2003)**, *Brain Res* 976:171–184 |
| VIP / CR / small CCK | ~30–35 % (combined class in many summaries) | Distal dendrites + other INs | VIP, calretinin, CCK | **Not yet traced to a single primary % paper** — leave open (U5) |
| Neurogliaform / NPY | smaller | Volume transmission / distal | NPY | Secondary / overlap with SOM+NPY |

**Standard four-subtype taxonomy** (PV / SOM / VIP / CCK) is confirmed across McDonald–Mascagni and recent work (Perumal & Sah 2021; Báldi et al. 2025).

### Functional specializations

- **PV basket cells** — perisomatic (soma + proximal dendrites); fastest, strongest control of PN output firing; many baskets converge on one PN; drive the PING inhibitory rebound.
- **PV chandelier (axo-axonic) cells** — cartridge synapses **exclusively on the axon initial segment (AIS)**; control spike *initiation*, not somatic integration; a **functionally distinct** PV subtype. Do not model as identical to basket cells. (Perumal & Sah 2021 Fig. 1; Báldi et al. 2025.)
- **SOM cells** — gate dendritic excitatory input; receive inhibition from PV and VIP.
- **VIP / CR cells** — often interneuron-selective; disinhibit PNs by suppressing other INs.
- **CCK basket cells** — perisomatic, CB1-sensitive, slower kinetics than PV.

**Stimulus-dependent activity polarity (PV vs SOM during fear learning)**

- **CS presentation** → drives **PV**, **inhibits SOM**.
- **US (shock)** → inhibits **both** PV and SOM.

CS-evoked PV → PV→SOM inhibition → SOM off distal dendrites → PN disinhibition for CS–US encoding. This PV-mediated disinhibition motif is central to fear acquisition.

VIP is activated by the US and is strongly **expectation-modulated** (greater response to unexpected shock), acting as a disinhibitory gate during associative learning.

**Sources:** Perumal & Sah (2021); Báldi et al. (2025); Yau et al. (2021).

**PV as aversive prediction-error encoder:** PV activity at the US is expectation-modulated (unexpected > expected shock). PV activity during reinforcement controls **fear acquisition**; PV activity during nonreinforcement does **not** control extinction. (Yau et al. 2021.)

**SOM state-tracking and extinction engrams:** SOM activity decreases during CS in acquisition (opposite to PV). After conditioning, elevated SOM associates with reduced fear / safety / extinction, including theta in safety contexts. During extinction, a tagged **SOM+** population forms an inhibitory engram; silencing those cells **restores fear**. High SOM ≈ fear circuit suppressed; low SOM ≈ expression possible. (Báldi et al. 2025; Zhang et al. 2026.)

Firing phenotypes:
- PV: fast-spiking, short APs, little adaptation.
- SOM and many non-PV INs: broader spikes, more adaptation.

### Run 1 implication

Minimal set: **PN + PV-like + SOM-like**. CCK and VIP out of scope for Run 1. SOM may use PV-like kinetics only with a `deviations.md` entry. Chandelier vs basket is a future refinement, not required for Run 1 pass gates.
