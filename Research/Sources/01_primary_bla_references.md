# Research Sources — Emotionally Grounded Conversational AI (PFE)

**Project:** BLA Isolated Population Simulation / Full Limbic Network
**Author:** Mohamed Takieddine Nouar
**Repository:** https://github.com/TakiNouar/PFE
**Last updated:** September 2026 (strict primary-source verification pass)

---

## How to Use This Document

Sources are grouped by role. Priority reading before the next implementation is marked with ⭐.

**Provenance rule:** When Feng et al. 2019 Table 3/4 cites an upstream experimental paper, that upstream paper is listed here. Do not attribute a number to Feng alone when Feng itself points elsewhere.

---

## 1. Primary Simulation References — BLA

### ⭐ Feng et al. 2019 — The foundational BLA model

> Feng F, Headley DB, Amir A, Kanta V, Chen Z, Paré D, Nair SS.
> **"Gamma Oscillations in the Basolateral Amygdala: Biophysical Mechanisms and Computational Consequences"**
> *eNeuro*, 6(1), ENEURO.0388-18.2018, 2019.
> DOI: 10.1523/ENEURO.0388-18.2018 · PMID: 30805556
> ModelDB: https://modeldb.science/247968

**Provides:** Tables 1–7 and the Mg²⁺ block equation. Network scale 27 000 cells (1:2.7 of ~72 000). Composition ~64 % PN-A / 26 % PN-C / 10 % FSI. Single FSI class (PV-like).

**Key synaptic parameters (Table 3) — numbers are exact; sources below are what Feng cites:**

| Connection | Receptor | Rise τ | Decay τ | g | Upstream source cited by Feng |
|---|---|---|---|---|---|
| PN → PN | AMPA | 0.3 ms | **6.9 ms** | 1.0 nS | Mahanty & Sah 1998; Guzman et al. 2016 |
| PN → PN | NMDA | 3.7 ms | **125 ms** | 0.5 nS | (confirm from Feng footnotes) |
| PN → FSI | AMPA | 0.1 ms | 2.4 ms | 1.0 nS | Mahanty & Sah 1998; Guzman et al. 2016 |
| PN → FSI | NMDA | 3.7 ms | 125 ms | 0.5 nS | |
| FSI → PN | GABA-A | 0.5 ms | **6.8 ms** | 0.6 nS | **Galarreta & Hestrin 1997** |
| FSI → FSI | GABA-A | 0.5 ms | 6.8 ms | 0.2 nS | **Galarreta & Hestrin 1997** |

E_AMPA = E_NMDA = 0 mV; **E_GABA = −75 mV**. Mg block: s(V) = [1 + 0.33·exp(−0.06V)]⁻¹ (Zador et al. 1990).

**Short-term depression (Table 4) — values and sources:**

| Connection | D_max | d1/d2 | τD1/τD2 (ms) | Experimental basis per Feng |
|---|---|---|---|---|
| FSI → PN | **0.6** | 0.9/0.95 | 40/70 | Woodruff & Sah 2007 (BLA) |
| PN → FSI | **0.7** | 0.9/0.95 | 40/70 | Woodruff & Sah 2007 (BLA) |
| PN → PN | **0.5** | 0.9/0.95 | 40/70 | **Silberberg et al. 2004 (neocortex)** — Feng explicitly notes lack of BLA-specific data |

Do not claim PN→PN depression is BLA-measured; the source paper flags it as imported.

---

### ⭐ Kim et al. 2013 — Single-cell models used by Feng

> Kim D, Paré D, Nair SS.
> **"Mechanisms contributing to the induction and storage of Pavlovian fear memories in the lateral amygdala"**
> *Learning & Memory*, 20(8):421–430, 2013.
> DOI: 10.1101/lm.030262.113 · PMID: 23864645 · ModelDB 150288

---

### ⭐ Mahanty & Sah 1998 — AMPA kinetics (cited by Feng for both PN and FSI)

> Mahanty NK, Sah P.
> **"Calcium-permeable AMPA receptors mediate long-term potentiation in interneurons in the amygdala"**
> *Nature*, 394:683–687, 1998.
> DOI: 10.1038/29312

Feng Table 3 cites this (together with Guzman et al. 2016) for AMPA kinetics at both PN→PN and PN→FSI synapses.

**Note:** Mahanty & Sah 1999 (*Eur J Neurosci* 11:1217–1222) is a real companion paper on glutamatergic transmission onto LA principal cells. It is **not** what Feng Table 3 cites for the 6.9 ms / 2.4 ms AMPA decays. Keep it only as general supporting evidence if listed elsewhere.

---

### Guzman et al. 2016 — Co-source for AMPA kinetics in Feng Table 3

> Guzman SJ, Schlögl A, Frotscher M, Jonas P.
> **"Synaptic mechanisms of pattern completion in the hippocampal CA3 network"**
> *Science*, 353(6304):1117–1123, 2016.
> DOI: 10.1126/science.aaf1836

**Status:** Best-identified match for Feng’s “Guzman et al., 2016” co-citation with Mahanty & Sah 1998 on AMPA kinetics. **Caveat:** the paper is hippocampal CA3, not amygdala. Confirm against Feng’s reference-list entry before independent thesis citation; until confirmed, attribute the kinetic *numbers* to Feng Table 3 and the *upstream pair* as Feng states.

---

### Galarreta & Hestrin 1997 — GABA-A kinetics (cited by Feng Table 3)

> Galarreta M, Hestrin S.
> **"A specialized subclass of interneurons mediates feedforward inhibition among projection neurons in neocortex"** / properties of fast IPSCs (confirm exact title against Feng ref list).
> Commonly: work establishing fast GABA-A kinetics used in models; Feng Table 3 cites for FSI→PN / FSI→FSI 0.5 / 6.8 ms.

**Provides:** Upstream source Feng cites for FSI→PN / FSI→FSI GABA-A rise/decay. Neocortical measurement adopted into the BLA model.

---

### Silberberg et al. 2004 — PN→PN short-term depression (cited by Feng)

> Silberberg G, Wu C, Markram H.
> **"Synaptic dynamics of neocortical networks"** (confirm exact title/pages against Feng reference list).
> *2004* — neocortical short-term depression parameters.

Feng states PN→PN depression was taken from neocortical data **because BLA-specific measurements were lacking**. D_max = **0.5** for PN→PN in Table 4. Do not attribute this parameter to Woodruff & Sah 2007.

---

### ⭐ Woodruff and Sah 2007 — FSI connectivity & FSI-related STP

> Woodruff AR, Sah P.
> **"Networks of parvalbumin-positive interneurons in the basolateral amygdala"**
> *Journal of Neuroscience*, 27(3), 2007.

**Provides:** Connectivity probabilities and short-term depression for **FSI↔PN** (D_max 0.6 / 0.7). **Not** the source for PN→PN D_max.

---

### Destexhe et al. 2001 — Point-conductance (OU) noise model (methods source)

> Destexhe A, Rudolph M, Fellous JM, Sejnowski TJ.
> **"Fluctuating synaptic conductances recreate in vivo-like activity in neocortical neurons"**
> *Neuroscience*, 107(1):13–24, 2001.
> DOI: 10.1016/S0306-4522(01)00344-X · PMID: 11744242

**This is the paper Feng cites for the point-conductance equations.** It contains the fluctuating excitatory/inhibitory conductance formalism whose coefficients appear (adapted) in Feng Table 7.

**Do not confuse with:** Destexhe, Rudolph & Paré (2003) *Nat Rev Neurosci* 4:739–751 (“The high-conductance state…”), which is a review with different co-authors and is **not** the methods source for the OU parameters.

---

### Destexhe et al. 2003 — High-conductance state (review only)

> Destexhe A, Rudolph M, Paré D.
> **"The high-conductance state of neocortical neurons in vivo"**
> *Nature Reviews Neuroscience*, 4:739–751, 2003.
> DOI: 10.1038/nrn1198

Useful conceptual background; **not** the citation for the numerical noise model used by Feng.

---

### Weisskopf, Bauer & LeDoux 1999 — Thalamo-amygdala LTP

> Weisskopf MG, Bauer EP, LeDoux JE.
> **"L-Type Voltage-Gated Calcium Channels Mediate NMDA-Independent Associative Long-Term Potentiation at Thalamic Input Synapses to the Amygdala"**
> *Journal of Neuroscience*, 19(23):10512–10519, 1999.
> PMID: 10575047

Feng’s “Weisskopf et al., 1999” (et al. form) more plausibly points here. Still **not** confirmed as the measurement source of τ_NMDA = 125 ms; confirm from Feng footnotes.
