# 02 — Cell Types

## Principal neurons (PNs / pyramidal-like)

- Glutamatergic, long-range projecting.
- Exhibit spike-frequency adaptation of varying strength (Type-A strong adaptation, Type-C continuous firing in Kim/Feng classification).
- Adaptation is largely produced by the slow Ca²⁺-dependent after-hyperpolarization current (I_sAHP).
- Receive both cortical and thalamic excitatory input; form the majority of the local recurrent excitatory network.

**Fear-memory recruitment:** only a minority of LA principal neurons become plastic and join the memory trace — ~**25 %** in classic studies, as stated by Kim et al. 2013 (citing Quirk et al. 1995, Repa et al. 2001, Rumpel et al. 2005).

## Interneuron taxonomy (GABAergic)

Approximate contributions in **rat** basolateral complex. **Each row has its own primary source** — do not cite Mascagni & McDonald 2003 as a blanket source for the whole table (that paper is CCK-specific).

| Subtype | ~% of INs | Main axonal target | Key markers | Primary source |
|---------|-----------|--------------------|-------------|----------------|
| PV+ | **~40–50 %** (lower in LA, ~20 %) | Perisomatic (soma, proximal dendrites, AIS) | Parvalbumin; basket + axo-axonic (chandelier) | **McDonald & Betette (2001)**, *Neuroscience* 102:413–425 — reports PV+ as “∼50% of the interneuronal population” in rat BLA |
| SOM+ / SST | **~15–20 %** | Distal dendrites & spines | Somatostatin; many also NPY | **McDonald & Mascagni (2002)**, *Brain Res* 943:237–244 — SOM+ = 11–18% of GABAergic population (repo range slightly generous at top end; essentially correct) |
| CCK large (CCKL) | ~7 % | Perisomatic (basket) | Cholecystokinin, often CB1 | **Mascagni & McDonald (2003)**, *Brain Res* 976:171–184 — CCK-containing neurons specifically |
| VIP / CR / small CCK | ~30–35 % (combined small-peptide class in many summaries) | Distal dendrites + other interneurons | VIP, calretinin, CCK | **Not yet traced to a single primary paper** — do not attribute to Mascagni & McDonald 2003. Locate a specific VIP/CR count before thesis citation; until then treat as approximate secondary synthesis |
| Neurogliaform / NPY | smaller | Volume transmission / distal | NPY | Secondary / overlapping with SOM+NPY populations |

**Standard four-subtype taxonomy** (PV / SOM / VIP / CCK) for rat BLA is confirmed across the McDonald–Mascagni series as a whole; percentages must still be cited per paper as above.

### Functional specializations

- **PV basket cells** — strongest control of PN spiking; major share of perisomatic GABAergic boutons; many PV cells converge onto a single PN.
- **PV axo-axonic cells** — cartridge synapses on the axon initial segment; control spike initiation.
- **SOM cells** — gate dendritic excitatory input and local dendritic computation; receive inhibition from PV and VIP cells.
- **VIP / CR cells** — often interneuron-selective; disinhibit principal cells by suppressing other INs.
- **CCK basket cells** — perisomatic, cannabinoid-sensitive, slower kinetics than PV.

Firing phenotypes:
- PV: fast-spiking, short action potentials, little adaptation.
- SOM and many non-PV INs: broader spikes, more adaptation.

### Run 1 implication

Isolated characterization uses the minimal viable set **PN + PV-like + SOM-like**. CCK and VIP are out of scope for Run 1 (see `architecture/`). SOM may use PV-like kinetics only if listed in `deviations.md`.
