# Extended BLA / Amygdala Computational Models

### eLife 2024 — BLA oscillations enable fear learning

> (Authors TBC — published November 2024)
> **"Basolateral amygdala oscillations enable fear learning in a biophysical model"**
> *eLife*, 2024.
> Full text: https://elifesciences.org/articles/89519

**What it provides:** Extends the Feng et al. 2019 architecture by adding VIP (vasoactive intestinal peptide) and SOM (somatostatin) interneuron subtypes with their specific additional currents:
- VIP interneurons: standard fast-spiking HH + **D-current** (slowly inactivating K+ current)
- SOM interneurons: standard HH + **NaP current** (persistent Na+) + **H-current** (hyperpolarization-activated)

These additional currents explain why the BLA SOM sub-population in Runs 1–3 was silent — our SOM model had no intrinsic currents that could drive spontaneous or low-stimulus firing. The NaP current provides persistent depolarization that keeps SOM neurons closer to threshold even without strong external drive.

**Also confirms:** The PING (pyramidal-interneuron network gamma) mechanism, where PV interneurons are driven by Pyr activity and in turn deliver feedback inhibition, is the correct model for BLA rhythmogenesis.

---

### Headley et al. 2021 — LA and BL models

> Headley DB, Kanta V, Feng F, Nair SS, Paré D.
> **"Gamma Oscillations in the Basolateral Amygdala: Localization, Microcircuitry, and Behavioral Correlates"**
> *PMC8276735*, 2021.

**What it provides:** Extends Feng et al. 2019 to the lateral amygdala (LA), with identical synaptic parameters applied to both LA and BL models. Confirms that the Feng et al. parameter set generalizes within the BLA complex. Also confirms the Ornstein-Uhlenbeck point-conductance model is used for all background activity.

---

### Kim et al. (lateral amygdala) — 1000-cell network model

> Kim D, et al.
> **"A 1000 cell network model for Lateral Amygdala"**
> ModelDB accession number.

**What it provides:** A complementary 1000-neuron LA model with similar architecture to Feng et al. BL model. Useful for understanding how larger population counts affect dynamics, and as a cross-check on the Feng et al. parameters.

---

### NMDA kinetics — chaotic firing study (2026)

> (Authors — published 2026)
> **"NMDA receptor kinetics drive distinct routes to chaotic firing in pyramidal neurons"**
> *PMC13272316*, 2026.
> Full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC13272316/

**What it provides:** Hodgkin-Huxley-type computational model incorporating NMDA, AMPA, and GABA receptor kinetics. Systematic analysis of how NMDA receptor closing rate (β_NMDA) and glutamatergic stimulation frequency control neuronal dynamics. Demonstrates that both AMPA and NMDA are required for normal firing patterns — NMDA alone produces qualitatively different dynamics than the combined case. Directly relevant for understanding why the Run 5 NMDA-only diagnostic (mean=41.2 Hz) looked different from the expected combined-component behavior.
