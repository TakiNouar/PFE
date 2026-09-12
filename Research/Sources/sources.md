# Research Sources — Emotionally Grounded Conversational AI (PFE)

**Project:** BLA Isolated Population Simulation / Full Limbic Network
**Author:** Mohamed Takieddine Nouar
**Repository:** https://github.com/TakiNouar/PFE
**Last updated:** September 2026

---

## How to Use This Document

Sources are grouped by role: primary simulation references (papers whose parameters are directly used or should be used in the simulation code), supporting biological references, and general computational neuroscience references. Each entry includes what specifically it contributes and which simulation parameter or design decision it informs.

**Priority reading before Run 6 is marked with ⭐.**

---

## 1. Primary Simulation References — BLA

### ⭐ Feng et al. 2019 — The foundational BLA model

> Feng F, Headley DB, Amir A, Kanta V, Chen Z, Paré D, Nair SS.
> **"Gamma Oscillations in the Basolateral Amygdala: Biophysical Mechanisms and Computational Consequences"**
> *eNeuro*, 6(1), ENEURO.0388-18.2018, 2019.
> DOI: 10.1523/ENEURO.0388-18.2018
> Full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC6361623/
> Code (NEURON): https://github.com/ModelDBRepository/247968
> ModelDB entry: https://modeldb.science/247968

**What it is:** The first large-scale biophysically and anatomically realistic model of the basolateral amygdala nucleus (BL), developed using in vitro and in vivo data from rat BLA. Reproduces in vivo local field potential dynamics, gamma oscillations (50–70 Hz), and spike entrainment patterns. All parameters are constrained by published electrophysiology.

**What it directly provides for the simulation:**

- **Table 1** — Gating parameters of ion channels in BL PN neurons (I_Na, I_DR, I_H, I_KM, I_Ca, I_NaP, I_sAHP). These are the correct HH kinetics for BLA pyramidal cells, including the Ca²⁺-dependent sAHP current responsible for spike frequency adaptation.
- **Table 2** — Maximal conductance densities for each compartment (soma, proximal dendrite, distal dendrite, apical dendrite). Required for the 3-compartment PN model.
- **Table 3 (critical)** — Synaptic parameters: reversal potentials, rise/decay time constants, conductances, and mean/variance of synaptic weight distributions for all connection types (PN→PN AMPA/NMDA, PN→FSI AMPA/NMDA, FSI→PN GABA-A, FSI→FSI GABA-A). These are the parameters that were wrong in Runs 1–5.
- **Table 4** — Short-term presynaptic depression parameters for all connection types.
- **Table 5–6** — Connection probabilities (distance-dependent for PN→PN; probability-based for FSI connections).
- **Table 7** — Point-conductance noise model parameters (Ornstein-Uhlenbeck, separate excitatory and inhibitory components) for both PNs and FSIs.
- **Equation for NMDA Mg²⁺ block:** s(V) = [1 + 0.33 × exp(−0.06V)]⁻¹

**Key parameters extracted (Table 3):**

| Connection | Receptor | Rise τ | Decay τ | Conductance |
|---|---|---|---|---|
| PN → PN | AMPA | 0.3 ms | **6.9 ms** | 1.0 nS |
| PN → PN | NMDA | 3.7 ms | **125 ms** | 0.5 nS |
| PN → FSI | AMPA | 0.1 ms | 2.4 ms | 1.0 nS |
| PN → FSI | NMDA | 3.7 ms | 125 ms | 0.5 nS |
| FSI → PN | GABA-A | 0.5 ms | **6.8 ms** | 0.6 nS |
| FSI → FSI | GABA-A | 0.5 ms | 6.8 ms | 0.2 nS |

**Reversal potentials:** E_AMPA = E_NMDA = 0 mV, **E_GABA = −75 mV**

**Network size used:** 27,000 neurons (1:2.7 scale of estimated 72,000 neurons in rat BL). Composition: 64% PN-A (adapting), 26% PN-C (continuous), 10% FSI.

**How to cite:** "Synaptic kinetics and connectivity parameters follow Feng et al. (2019), which provides the first biophysically and anatomically realistic model of the basolateral amygdala constrained by in vivo and in vitro electrophysiology."

---

### ⭐ Kim et al. 2013 — Single-cell models underlying Feng et al.

> Kim D, et al.
> **"Distinct Dynamics of Amygdalar Neurons Underlying Fear Learning"**
> *Journal of Neurophysiology*, 2013.

**What it provides:** The individual PN and FSI neuron models that Feng et al. 2019 are built on. Contains the detailed conductance parameters for the multi-compartment BLA PN (including the I_sAHP current that produces spike adaptation) and the fast-spiking FSI model. Required reading before implementing the single-cell models.

**Access:** The NEURON implementation is included in the Feng et al. ModelDB repository at https://github.com/ModelDBRepository/247968 — look for the cell definition `.hoc` files.

---

### ⭐ Weisskopf and LeDoux 1999 — NMDA kinetics in BLA

> Weisskopf MG, LeDoux JE.
> **"Distinct populations of neurons in the amygdala encode sensory and conditioned fear signals"**
> *The Journal of Neuroscience*, 19(23), 1999.

**What it provides:** Direct electrophysiological measurement of NMDA receptor kinetics at synapses in the basolateral amygdala. Source for the **τ_NMDA = 125 ms** decay constant used in Feng et al. Table 3. This is not an estimate from cortex — it is measured in rat amygdala tissue specifically.

**Why it matters:** The simulation used τ_NMDA = 80–120 ms (guessed) in Runs 4–5. The correct value from direct measurement is 125 ms. This is also the value at which the biologically realistic NMDA/AMPA ratio (~26/74) holds.

---

### ⭐ Mahanty and Sah 1998 — AMPA kinetics in BLA

> Mahanty NK, Sah P.
> **"Calcium-permeable AMPA receptors mediate long-term potentiation in interneurons in the amygdala"**
> *Nature*, 394(6694), 1998.

**What it provides:** Direct electrophysiological measurement of AMPA receptor kinetics at BLA synapses. Source for **τ_AMPA_decay = 6.9 ms** (PN→PN) and **τ_AMPA_decay = 2.4 ms** (PN→FSI) in Feng et al. Table 3.

**Why it matters:** The simulation used τ_AMPA = 2 ms uniformly across all Pyr→Pyr connections in Runs 1–5. The correct PN→PN value is 6.9 ms — 3.5× longer. Because AMPA decays in 2 ms but ISI is ~23 ms, recurrent AMPA was contributing almost nothing to sustained activity. Correcting this alone will substantially change the dynamics.

---

### ⭐ Woodruff and Sah 2007 — BLA interneuron connectivity

> Woodruff AR, Sah P.
> **"Networks of parvalbumin-positive interneurons in the basolateral amygdala"**
> *Journal of Neuroscience*, 27(3), 2007.

**What it provides:** In vitro measurements of connectivity probabilities between PV interneurons and pyramidal neurons in the BLA, and among PV interneurons. Source for the FSI→PN (34%), PN→FSI (12% unidirectional, 16% reciprocal), and FSI→FSI (26% total) probabilities in Feng et al. Tables 5–6. Also the source for the short-term depression parameters (D_max, d1, d2, τ_D).

---

### Destexhe et al. 2001 — Ornstein-Uhlenbeck conductance noise model

> Destexhe A, Rudolph M, Paré D.
> **"The high-conductance state of neocortical neurons in vivo"**
> *Nature Reviews Neuroscience*, 4(9), 2001.

**What it provides:** The point-conductance model used for background synaptic noise in Feng et al. (Table 7 and Equations 8–9). Models stochastic background activity as separate excitatory and inhibitory conductance channels following OU processes, rather than as a Gaussian current injection. This is the correct noise model — current injection noise does not change the membrane time constant or integration properties, while conductance-based noise does.

**Parameters for BLA PNs:** g_e0 = 3.2 nS, σ_e = 3 nS, τ_e = 2.73 ms, E_e = 0 mV, g_i0 = 21 nS, σ_i = 8 nS, τ_i = 10.49 ms, E_i = −75 mV

---

## 2. Supporting Biological References — BLA

### Abatis et al. 2017 — PN→PN connectivity in BLA

> Abatis M, et al.
> **"Distance-dependent connectivity of BLA principal neurons"**
> 2017.

**What it provides:** Distance-dependent PN→PN connection probabilities in BLA: 3% at <50 μm, 2% at 50–100 μm, 1% at 100–200 μm, 0.5% at 200–600 μm. Source for Feng et al. Table 5. The simulation used a flat K=3 fixed in-degree (~6% at baseline scale) — substantially over-dense at all distance ranges.

---

### Paré et al. 1995, Samson and Paré 2006 — Recurrent connections in BLA

> Paré D, et al. 1995. *Journal of Neurophysiology.*
> Samson RD, Paré D. 2006.

**What these provide:** Evidence for recurrent connections within BLA (cited in Feng et al. Introduction). Establishes that the BLA is not a purely feedforward network — recurrent connectivity is a key feature, and the model must account for it. These connections enable the reverberatory activity (after-discharge / emotional inertia) that the thesis requires.

---

### Rainnie et al. 1993 — BLA neuron electrophysiology

> Rainnie DG, et al.
> **"Adenosine inhibition of mesolimbic dopamine release and motor activity"**
> *Journal of Neurophysiology*, 1993.

**What it provides:** Electrophysiological characterization of BLA neurons in vitro, including the two PN subtypes (adapting vs. continuous spiking) and FSI properties. Used by Feng et al. to set the adaptation ratio cutoff (1.5) for classifying PN types. The sAHP magnitude difference (50 mS/cm² for adapting vs. 0.2 mS/cm² for continuous) comes from this work.

---

### Zador et al. 1990 — NMDA Mg²⁺ block

> Zador A, Koch C, Brown TH.
> **"Biophysical model of a Hebbian synapse"**
> *PNAS*, 87(17), 1990.

**What it provides:** The voltage-dependent Mg²⁺ block function for NMDA receptors: s(V) = [1 + 0.33 × exp(−0.06V)]⁻¹. This function gates NMDA conductance by membrane voltage — at resting potential (~−70 mV), NMDA is largely blocked; it opens as the membrane depolarizes. This was completely absent from Runs 1–5, causing NMDA to behave as a constant current source at all voltages.

---

## 3. Extended BLA / Amygdala Computational Models

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

---

## 4. Fear Memory and Amygdala Network Dynamics

### Werne et al. 2026 — Fear memory consolidation model

> Werne L, et al.
> **"Learning, sleep replay and consolidation of contextual fear memories: A neural network model"**
> *PLoS Computational Biology*, 22(3), e1013251, March 2026.
> https://pubmed.ncbi.nlm.nih.gov/41843866/

**What it provides:** Recent (2026) computational model showing how contextual fear memories form and persist through hippocampal-amygdala replay during sleep. Relevant for understanding the longer-timescale mechanisms behind emotional inertia that are beyond the scope of the isolated BLA simulation. Key finding: persistent fear states emerge from coordinated replay across hippocampus and amygdala — not from BLA alone. This directly supports the design-level conclusion that after-discharge is a network property, not a single-region property.

---

### LeDoux 2000, Duvarci and Paré 2014 — BLA emotional behavior

> LeDoux JE. (2000). *Annual Review of Neuroscience.*
> Duvarci S, Paré D. (2014). *Neuron.*

**What these provide:** Reviews of how BLA supports emotional learning and expression. Establish that BLA function is fundamentally a circuit-level property — evaluation in BLA drives expression through CeA, suppression through PFC feedback, and context through HIP. These are the cross-regional dependencies that make after-discharge impossible in the isolated BLA.

---

### Cerebral Cortex 2017 — Amygdala-Hippocampus connectivity

> Ritchey M, et al.
> **"Persistence of Amygdala–Hippocampal Connectivity and Multi-Voxel Correlation Structures During Awake Rest After Fear Learning Predicts Long-Term Expression of Fear"**
> *Cerebral Cortex*, 27(5), 2017.
> https://academic.oup.com/cercor/article/27/5/3028/3060757

**What it provides:** Human fMRI evidence that fear memory consolidation involves amygdala-hippocampal functional connectivity that persists after learning and predicts long-term fear expression. Relevant for understanding why the HIP↔BLA loop in the blueprint is essential — without it, fear states do not consolidate into persistent representations.

---

## 5. General Computational Neuroscience References

### Hodgkin and Huxley 1952 — The foundational HH model

> Hodgkin AL, Huxley AF.
> **"A quantitative description of membrane current and its application to conduction and excitation in nerve"**
> *Journal of Physiology*, 117(4), 1952.

**What it provides:** The original Hodgkin-Huxley equations for action potential generation, used as the biophysical substrate for every neuron in the simulation. Required citation for any HH-based simulation.

---

### Destexhe et al. 1994 — Dual-exponential synapse model

> Destexhe A, Mainen ZF, Sejnowski TJ.
> **"Synthesis of models for excitable membranes, synaptic transmission and neuromodulation using a common kinetic formalism"**
> *Journal of Computational Neuroscience*, 1994.

**What it provides:** The kinetic formalism for AMPA, NMDA, and GABA-A synaptic conductances using dual-exponential (rise + decay) functions. This is the synaptic model used in Feng et al. 2019 (Equations 4–6) and what the simulation is intended to implement.

---

### Wang and Buzsáki 1996 — Gamma oscillations, PING model

> Wang XJ, Buzsáki G.
> **"Gamma oscillation by synaptic inhibition in a hippocampal interneuronal network model"**
> *Journal of Neuroscience*, 16(20), 1996.

**What it provides:** The original description of the PING (pyramidal-interneuron network gamma) model, which Feng et al. 2019 identifies as the mechanism underlying BLA gamma oscillations. Relevant for understanding why the PV interneurons are the key element of the BLA circuit — they are not just inhibitory elements, they are rhythm generators.

---

### Destexhe et al. 2001 — High-conductance state

> Destexhe A, Rudolph M, Paré D.
> **"The high-conductance state of neocortical neurons in vivo"**
> *Nature Reviews Neuroscience*, 2001.

*(Also listed in §1 — included here for completeness in the general references section.)*

**Key insight for the simulation:** In vivo, neurons exist in a "high-conductance state" where constant bombardment from background synaptic activity dramatically lowers membrane resistance and time constant. The Ornstein-Uhlenbeck conductance noise model approximates this state. Gaussian current injection does not, because it doesn't change the membrane's electrical properties. This is why the noise model change in Run 3 (from current noise to OU private drive) had such a large effect on synchrony.

---

## 6. Software and Tools

### Brian2 — Neural simulation framework

> Stimberg M, Brette R, Goodman DF.
> **"Brian 2, an intuitive and efficient neural simulator"**
> *eLife*, 8, e47314, 2019.
> https://elifesciences.org/articles/47314

**What it provides:** The Python-based neural simulation framework used in Runs 1–5. Conductance-based synapses with axonal delays are well-supported. Recommended for Run 6 onward. The Feng et al. model was built in NEURON — parameters should be ported to Brian2 rather than switching simulators.

---

### NEURON — Reference simulator for Feng et al.

> Carnevale NT, Hines ML.
> **"The NEURON Book"**
> Cambridge University Press, 2006.
> https://neuron.yale.edu

**What it provides:** The simulator used by Feng et al. 2019. The ModelDB code for their model is in NEURON `.hoc` files. Reading these files extracts the exact parameter values used in their simulation. Python-compatible via the `neuron` Python package.

---

### ModelDB — Computational neuroscience model repository

> Hines ML, et al.
> **"ModelDB: A Database to Support Computational Neuroscience"**
> *Journal of Computational Neuroscience*, 2004.
> https://modeldb.science

**What it provides:** The repository hosting the Feng et al. 2019 BLA model code (accession 247968) and thousands of other published neural models. All models are freely downloadable. The BLA model code at https://github.com/ModelDBRepository/247968 contains the complete parameter set in runnable form.

---

## 7. Reading Priority for Run 6

| Priority | Paper | Specific sections to read |
|---|---|---|
| ⭐⭐⭐ | Feng et al. 2019 | Methods: Model Implementation, Tables 1–7 |
| ⭐⭐⭐ | Feng et al. 2019 code | `function_calcconduc.hoc`, cell definition files |
| ⭐⭐ | Kim et al. 2013 | Single-cell model parameters, sAHP current |
| ⭐⭐ | Weisskopf & LeDoux 1999 | NMDA kinetics measurement in rat BLA |
| ⭐⭐ | Mahanty & Sah 1998 | AMPA kinetics measurement in rat BLA |
| ⭐⭐ | Woodruff & Sah 2007 | FSI connectivity probabilities and short-term depression |
| ⭐ | Destexhe et al. 2001 | OU conductance noise model, Table with PN/FSI parameters |
| ⭐ | eLife 2024 (BLA fear learning) | SOM and VIP interneuron additional currents |

---

*This document covers sources identified and used (or found not to have been used) during the BLA isolated simulation study, Runs 1–5. It will be updated as the project progresses to CeA characterization and the full 10-region network.*
