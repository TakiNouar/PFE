# Research Sources — Emotionally Grounded Conversational AI (PFE)

**Project:** BLA Isolated Population Simulation / Full Limbic Network
**Author:** Mohamed Takieddine Nouar
**Repository:** https://github.com/TakiNouar/PFE
**Last updated:** September 2026 (accuracy verification pass)

---

## How to Use This Document

Sources are grouped by role: primary simulation references (papers whose parameters are directly used or should be used in the simulation code), supporting biological references, and general computational neuroscience references. Each entry includes what specifically it contributes and which simulation parameter or design decision it informs.

**Priority reading before the next implementation is marked with ⭐.**

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

- **Table 1** — Gating parameters of ion channels in BL PN neurons (I_Na, I_DR, I_H, I_KM, I_Ca, I_NaP, I_sAHP).
- **Table 2** — Maximal conductance densities for each compartment.
- **Table 3 (critical)** — Synaptic parameters for all connection types.
- **Table 4** — Short-term presynaptic depression parameters.
- **Tables 5–6** — Connection probabilities (distance-dependent for PN→PN).
- **Table 7** — Point-conductance noise model parameters (Ornstein-Uhlenbeck).
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

**Note on SOM class:** Feng models a single FSI class (PV-like). Distinct SOM kinetics (NaP, H-current, etc.) come from later extensions (e.g. 2024 eLife-style models) and must be labelled as such if used.

---

### ⭐ Kim et al. 2013 — Single-cell models underlying Feng et al.

> Kim D, Paré D, Nair SS.
> **"Mechanisms contributing to the induction and storage of Pavlovian fear memories in the lateral amygdala"**
> *Learning & Memory*, 20(8):421–430, 2013.
> ModelDB: 150288

**What it provides:** The individual PN and FSI neuron models that Feng et al. 2019 are built on, including the multi-compartment PN with I_sAHP.

---

### ⭐ Weisskopf, Bauer & LeDoux 1999 — Thalamo-amygdala LTP (and related kinetics)

> Weisskopf MG, Bauer EP, LeDoux JE.
> **"L-Type Voltage-Gated Calcium Channels Mediate NMDA-Independent Associative Long-Term Potentiation at Thalamic Input Synapses to the Amygdala"**
> *Journal of Neuroscience*, 19(23):10512–10519, 1999.
> DOI: 10.1523/JNEUROSCI.19-23-10512.1999 · PMID: 10575047

**What it actually provides:** Demonstration that a form of LTP at thalamic input synapses to LA is NMDA-independent and requires L-type voltage-gated calcium channels. It is **not** the primary source paper for a measured NMDA decay constant of 125 ms in BLA.

**Note on τ_NMDA = 125 ms:** Feng et al. Table 3 lists 125 ms. The exact experimental measurement that produced that number should be traced in the Feng methods / citations before treating it as a direct BLA measurement from Weisskopf 1999. Until that tracing is complete, treat 125 ms as the value adopted by the Feng model, not as an independent Weisskopf measurement.

(Previous draft listed an incorrect title that belonged to a different paper; corrected here.)

---

### ⭐ Mahanty and Sah 1998 — AMPA kinetics in BLA

> Mahanty NK, Sah P.
> **"Calcium-permeable AMPA receptors mediate long-term potentiation in interneurons in the amygdala"**
> *Nature*, 394(6694), 1998.

**What it provides:** Direct electrophysiological measurement of AMPA receptor kinetics at BLA synapses. Source for **τ_AMPA_decay = 6.9 ms** (PN→PN) and **τ_AMPA_decay = 2.4 ms** (PN→FSI) in Feng et al. Table 3.

---

### ⭐ Woodruff and Sah 2007 — BLA interneuron connectivity & STP

> Woodruff AR, Sah P.
> **"Networks of parvalbumin-positive interneurons in the basolateral amygdala"**
> *Journal of Neuroscience*, 27(3), 2007.

**What it provides:** Connectivity probabilities (FSI→PN ≈34 %, PN→FSI uni/reciprocal, FSI→FSI) and short-term depression behaviour. Feng Table 4 is the immediate source of the two-factor depression parameters used in the model; Woodruff & Sah is the experimental foundation.

---

### Destexhe et al. 2003 — High-conductance state / OU noise framework

> Destexhe A, Rudolph M, Paré D.
> **"The high-conductance state of neocortical neurons in vivo"**
> *Nature Reviews Neuroscience*, 4:739–751, 2003.
> DOI: 10.1038/nrn1198

**What it provides:** Conceptual and quantitative framework for the point-conductance (OU) noise model used in Feng et al. Table 7. (Year corrected from an earlier 2001 listing; a different Destexhe 2001 paper exists with different co-authors.)

**Parameters for BLA PNs (Feng Table 7):** g_e0 = 3.2 nS, σ_e = 3 nS, τ_e = 2.73 ms; g_i0 = 21 nS, σ_i = 8 nS, τ_i = 10.49 ms.
