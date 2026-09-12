# Research Sources — Emotionally Grounded Conversational AI (PFE)

**Project:** BLA Isolated Population Simulation / Full Limbic Network
**Author:** Mohamed Takieddine Nouar
**Repository:** https://github.com/TakiNouar/PFE
**Last updated:** September 2026 (full accuracy verification pass)

---

## How to Use This Document

Sources are grouped by role. Priority reading before the next implementation is marked with ⭐.

---

## 1. Primary Simulation References — BLA

### ⭐ Feng et al. 2019 — The foundational BLA model

> Feng F, Headley DB, Amir A, Kanta V, Chen Z, Paré D, Nair SS.
> **"Gamma Oscillations in the Basolateral Amygdala: Biophysical Mechanisms and Computational Consequences"**
> *eNeuro*, 6(1), ENEURO.0388-18.2018, 2019.
> DOI: 10.1523/ENEURO.0388-18.2018
> Full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC6361623/
> ModelDB: https://modeldb.science/247968

**Provides:** Tables 1–7 (channel kinetics, maximal conductances, synaptic parameters, STP, distance-dependent connectivity, OU noise) and the Mg²⁺ block equation. Network scale 27 000 cells (1:2.7 of ~72 000). Composition ~64 % PN-A / 26 % PN-C / 10 % FSI. Single FSI class (PV-like); distinct SOM currents come from later work.

**Key synaptic parameters (Table 3):**

| Connection | Receptor | Rise τ | Decay τ | g |
|---|---|---|---|---|
| PN → PN | AMPA | 0.3 ms | **6.9 ms** | 1.0 nS |
| PN → PN | NMDA | 3.7 ms | **125 ms** | 0.5 nS |
| PN → FSI | AMPA | 0.1 ms | 2.4 ms | 1.0 nS |
| PN → FSI | NMDA | 3.7 ms | 125 ms | 0.5 nS |
| FSI → PN | GABA-A | 0.5 ms | **6.8 ms** | 0.6 nS |
| FSI → FSI | GABA-A | 0.5 ms | 6.8 ms | 0.2 nS |

E_AMPA = E_NMDA = 0 mV; **E_GABA = −75 mV**. Mg block: s(V) = [1 + 0.33·exp(−0.06V)]⁻¹.

---

### ⭐ Kim et al. 2013 — Single-cell models used by Feng

> Kim D, Paré D, Nair SS.
> **"Mechanisms contributing to the induction and storage of Pavlovian fear memories in the lateral amygdala"**
> *Learning & Memory*, 20(8):421–430, 2013.
> DOI: 10.1101/lm.030262.113 · PMID: 23864645 · ModelDB 150288

**Provides:** Multi-compartment PN (including I_sAHP) and FSI mechanisms later reused in Feng et al. 2019.

---

### ⭐ Mahanty & Sah 1998 — Interneuron (FSI) AMPA kinetics

> Mahanty NK, Sah P.
> **"Calcium-permeable AMPA receptors mediate long-term potentiation in interneurons in the amygdala"**
> *Nature*, 394:683–687, 1998.
> DOI: 10.1038/29312

**Provides:** Fast, calcium-permeable AMPA at interneuron synapses (source for the **2.4 ms** PN→FSI AMPA decay used in Feng Table 3).

---

### ⭐ Mahanty & Sah 1999 — Pyramidal (PN) excitatory synaptic inputs

> Mahanty NK, Sah P.
> **"Excitatory synaptic inputs to pyramidal neurons of the lateral amygdala"**
> *European Journal of Neuroscience*, 11(4):1217–1222, 1999.
> DOI: 10.1046/j.1460-9568.1999.00528.x · PMID: 10103117

**Provides:** Excitatory synaptic currents onto LA pyramidal neurons (AMPA + NMDA). Primary experimental basis for the slower PN→PN AMPA kinetics (**6.9 ms** decay) adopted in Feng Table 3. (Earlier drafts incorrectly attributed both τ values to the 1998 paper only.)

---

### ⭐ Weisskopf, Bauer & LeDoux 1999 — Thalamo-amygdala LTP

> Weisskopf MG, Bauer EP, LeDoux JE.
> **"L-Type Voltage-Gated Calcium Channels Mediate NMDA-Independent Associative Long-Term Potentiation at Thalamic Input Synapses to the Amygdala"**
> *Journal of Neuroscience*, 19(23):10512–10519, 1999.
> DOI: 10.1523/JNEUROSCI.19-23-10512.1999 · PMID: 10575047

**Provides:** NMDA-independent, L-type VGCC-dependent LTP at thalamic input synapses to LA. **Not** the primary measurement paper for τ_NMDA = 125 ms. That value is the one adopted in Feng Table 3; the exact experimental source should be confirmed from Feng’s footnotes before treating 125 ms as a direct Weisskopf measurement.

---

### ⭐ Woodruff and Sah 2007 — PV interneuron networks & STP

> Woodruff AR, Sah P.
> **"Networks of parvalbumin-positive interneurons in the basolateral amygdala"**
> *Journal of Neuroscience*, 27(3), 2007.

**Provides:** Connectivity probabilities and short-term depression behaviour used (via Feng Table 4) for FSI↔PN and FSI↔FSI synapses.

---

### Destexhe et al. 2003 — High-conductance state / OU noise framework

> Destexhe A, Rudolph M, Paré D.
> **"The high-conductance state of neocortical neurons in vivo"**
> *Nature Reviews Neuroscience*, 4:739–751, 2003.
> DOI: 10.1038/nrn1198

**Provides:** Framework for the point-conductance (OU) noise model used in Feng Table 7. (Year corrected from earlier 2001 listings.)
