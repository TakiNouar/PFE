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
