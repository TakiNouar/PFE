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

**Provides:** Tables 1–7 and the Mg²⁺ block equation. Network scale 27 000 cells (1:2.7 of ~72 000) in a 1.4 × 1.4 × 1.4 mm cuboid, minimum inter-soma distance 25 µm. Composition 64 % PN-A (17 280) / 26 % PN-C (7 020) / 10 % FSI. Single FSI class (PV-like). Fixed integration step dt = 0.05 ms (NEURON).

**Key synaptic parameters (Table 3) — numbers are exact; sources below are what Feng cites:**

| Connection | Receptor | Rise τ | Decay τ | g | Strength (mean/var) | Upstream source cited by Feng |
|---|---|---|---|---|---|---|
| PN → PN | AMPA | 0.3 ms | **6.9 ms** | 1.0 nS | 5 / 3 | Mahanty & Sah 1998; Guzman et al. 2016 |
| PN → PN | NMDA | 3.7 ms | **125 ms** | 0.5 nS | 2 / 1 | **Weisskopf, Bauer & LeDoux 1999** (Feng ref. [115], confirmed) |
| PN → FSI | AMPA | 0.1 ms | 2.4 ms | 1.0 nS | 7 / 2 | Mahanty & Sah 1998; Guzman et al. 2016 |
| PN → FSI | NMDA | 3.7 ms | 125 ms | 0.5 nS | 7 / 2 | Weisskopf, Bauer & LeDoux 1999 (via Feng) |
| FSI → PN | GABA-A | 0.5 ms | **6.8 ms** | 0.6 nS | 12 / 2 | **Galarreta & Hestrin 1997** |
| FSI → FSI | GABA-A | 0.5 ms | 6.8 ms | 0.2 nS | 20 / 10 | **Galarreta & Hestrin 1997** |
| FSI – FSI | gap junction | — | — | coupling coeff. ≈ 0.05 | — | Woodruff & Sah 2007 |

E_AMPA = E_NMDA = 0 mV; **E_GABA = −75 mV**. Mg block: s(V) = [1 + 0.33·exp(−0.06V)]⁻¹ (Zador et al. 1990), multiplying the NMDA conductance: G_NMDA = g_max · STP · s(V) · r_NMDA.

**"Strength" column:** the paper does not define it. ModelDB 247968 shows it is a **per-synapse weight multiplier** (`initW`) applied to the conductance, drawn per connection as `lognormal(mean, var)` in `function_ConnectInternal_simplify_online_op.hoc` (E→E `lognormal(2,1)`, E→I `lognormal(7,2)`, I→E `lognormal(12,2)`, I→I `lognormal(20,10)`). Effective peak conductance is therefore g × W, not g alone. **Open (U20):** Table 3 lists PN→PN AMPA strength 5/3, but the ModelDB E→E line draws one weight `lognormal(2,1)` shared by AMPA and NMDA (`W = W_nmda = initW` in `pyrD2pyrD_STFD_new.mod`).

**Short-term depression (Table 4) — values and sources:**

| Connection | D_max | d1/d2 | τD1/τD2 (ms) | Experimental basis per Feng |
|---|---|---|---|---|
| FSI → PN | **0.6** | 0.9/0.95 | 40/70 | Woodruff & Sah 2007 (BLA) |
| PN → FSI | **0.7** | 0.9/0.95 | 40/70 | Woodruff & Sah 2007 (BLA) |
| PN → PN | **0.5** | 0.9/0.95 | 40/70 | **Silberberg et al. 2004 (neocortex)** — Feng explicitly notes lack of BLA-specific data |

Do not claim PN→PN depression is BLA-measured; the source paper flags it as imported.

**Meaning of "D_max" in the ModelDB code:** in `pyrD2pyrD_STFD_new.mod` the release factor is `facfactor = F · D1 · D2`. After each presynaptic spike `D1 ← D1·d1` and `D2 ← D2·d2`, each recovering toward 1 with its own τ. The listed limit is a **floor**: `if (facfactor < 0.5) { facfactor = 0.5 }`. So D_max = 0.5 means depression can never take the synapse below 50 % of its weight. Facilitation (`F`) is declared but never updated, so it stays at 1. **Open (U21):** the `.mod` defaults pair `d1 = 0.95` with τD1 = 40 ms and `d2 = 0.9` with τD2 = 70 ms, the reverse of Table 4's d1/d2 = 0.9/0.95. Check whether the hoc code overrides these defaults before transcribing them.

**Synapse formalism in ModelDB:** the code uses the Destexhe et al. 1994 kinetic scheme (`r' = AlphaTmax·on·(1−r) − Beta·r`, with a transmitter pulse of duration `Cdur`), not a dual-exponential. The Table 3 rise/decay values summarise it; for example AMPA `Beta = 0.1429 /ms` gives ≈ 7 ms decay, and NMDA `Beta = 0.008 /ms` gives 125 ms. A dual-exponential re-implementation is an approximation and must be logged in `deviations.md`. The `.mod` also contains a Ca²⁺-dependent weight-update (LTP) term. Run 1 must keep weights fixed.

### Connectivity (Tables 5–6)

| Connection | Probability | Source per Feng |
|---|---|---|
| PN → PN | 3 % (<50 µm), 2 % (50–100), 1 % (100–200), 0.5 % (200–600) | Abatis et al. 2017 (SfN poster — see `02_supporting_biological.md`) |
| FSI → PN | 34 % unidirectional | Woodruff & Sah 2007 |
| PN → FSI | 12 % unidirectional + 16 % reciprocal | Woodruff & Sah 2007 |
| FSI → FSI chemical | 26 % overall (20 % uni, 3 % bidirectional); 50 % uni / 25 % bi among electrically coupled pairs, 19 % / 3 % among uncoupled | Woodruff & Sah 2007; Cammarota et al. 2013 (supporting) |
| FSI – FSI gap junctions | 8 % of pairs | Woodruff & Sah 2007 |

Interneuron connections are limited to pairs within ~300 µm.

### Synaptic delay (Methods + ModelDB)

Delay = distance / (1 mm/ms) + **0.8 ms** minimum + uniform jitter **±0.1 ms** + dt. In the ModelDB code this is `del = (dis/maxdis)·maxdelay + mindelay + del_fluc + dt`, with `maxdelay = maxdis = 2.425` (the cube diagonal in mm). It is **not** a fixed 1.5 ms.

### Background noise (Table 7) — point conductance, Destexhe et al. 2001

| Cell | g_e0 | σ_e | τ_e | E_e | g_i0 | σ_i | τ_i | E_i |
|---|---|---|---|---|---|---|---|---|
| PN | 3.2 nS | 3 nS | 2.728 ms | 0 mV | 21 nS | 8 nS | 10.49 ms | −75 mV |
| FSI | 1.2 nS | 0.1 nS | 2.728 ms | 0 mV | 5.7 nS | 2.6 nS | 10.49 ms | −75 mV |

ModelDB mechanisms: `Gfluct_new_exc.mod`, `Gfluct_new_inh.mod`.

### Extrinsic input (Methods)

Feng drives the network with 1 800 surrogate spike trains built from PFC / perirhinal / entorhinal units recorded in quiet-waking rats (Headley et al. 2015). Each 1 ms bin passes through a Poisson generator, and each train projects to 40 random PNs. PNs receive 2.97 ± 1.7 extrinsic inputs and FSIs 3.4 ± 1.9; each input also contacts FSIs within 300 µm of its PNs with 0.3 % probability. The paper does not give the per-synapse conductance of these inputs.

### Passive parameters (Methods)

PN: R_m = 55 kΩ·cm², C_m = 2.4 µF/cm², R_a = 150 Ω·cm, E_L = −75 mV. FSI: R_m = 20 kΩ·cm², C_m = 1.0 µF/cm², R_a = 150 Ω·cm (the paper does not state FSI E_L; take it from `leakinter.mod`).

### ModelDB 247968 file map

Main file `BL_main.hoc`. Cells: `BLcells_template_LFP_segconsider_all_Iinject_recordingimembrane.hoc` (PN) and `interneuron_template_gj_LFP_Iinject_recordingimembrane.hoc` (FSI). Wiring: `function_ConnectInternal_simplify_online_op.hoc`, `function_ConnectInternal_gj_simplify.hoc`, `function_ConnectTwoCells.hoc`, `function_ConnectInputs_invivo_op.hoc`. Synapses: `pyrD2pyrD_STFD_new.mod`, `pyrD2interD_STFD.mod`, `interD2pyrD_STFD_new.mod`, `interD2interD_STFD_new.mod`, `gap.mod`. Channels: `na3`, `nat`, `nap`, `kdrca1`, `kaprox`, `kadist`, `im`, `h`, `cal2`, `ca`, `cadyn`, `capool`, `sahp`, `leak`, plus interneuron `nainter`, `kdrinter` and `leakinter`. Noise: `Gfluct_new_exc/inh.mod`. Per the README: compile the `.mod` files and create an empty `LFPs/` folder before running.

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

**Status:** **Confirmed** against Feng’s reference list (Oct 2026) — this is the paper Feng co-cites with Mahanty & Sah 1998 for AMPA kinetics. **Caveat:** it is a hippocampal CA3 study, not amygdala. In the thesis, attribute the kinetic *numbers* to Feng Table 3 and name the *upstream pair* as Feng does.

---

### Galarreta & Hestrin 1997 — GABA-A kinetics (cited by Feng Table 3)

> Galarreta M, Hestrin S.
> **"Properties of GABAA receptors underlying inhibitory synaptic currents in neocortical pyramidal neurons"**
> *Journal of Neuroscience*, 17:7220–7227, 1997.
> (Title confirmed against Feng’s reference list, Oct 2026. The earlier placeholder title was wrong.)

**Provides:** Upstream source Feng cites for FSI→PN / FSI→FSI GABA-A rise/decay. Neocortical measurement adopted into the BLA model.

---

### Silberberg et al. 2004 — PN→PN short-term depression (cited by Feng)

> Silberberg G, Wu C, Markram H.
> **"Synaptic dynamics control the timing of neuronal excitation in the activated neocortical microcircuit"**
> *Journal of Physiology*, 556:19–27, 2004.
> DOI: 10.1113/jphysiol.2004.060962
> (Confirmed against Feng’s reference list, Oct 2026.)

Feng states PN→PN depression was taken from neocortical data **because BLA-specific measurements were lacking**. D_max = **0.5** for PN→PN in Table 4. Do not attribute this parameter to Woodruff & Sah 2007.

---

### ⭐ Woodruff and Sah 2007 — FSI connectivity & FSI-related STP

> Woodruff AR, Sah P.
> **"Networks of parvalbumin-positive interneurons in the basolateral amygdala"**
> *Journal of Neuroscience*, 27(3):553–563, 2007.
> DOI: 10.1523/JNEUROSCI.3686-06.2007

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

### Weisskopf, Bauer & LeDoux 1999 — Upstream for NMDA kinetics (Feng Table 3)

> Weisskopf MG, Bauer EP, LeDoux JE.
> **"L-Type Voltage-Gated Calcium Channels Mediate NMDA-Independent Associative Long-Term Potentiation at Thalamic Input Synapses to the Amygdala"**
> *Journal of Neuroscience*, 19(23):10512–10519, 1999.
> DOI: 10.1523/JNEUROSCI.19-23-10512.1999 · PMID: 10575047

**Confirmed:** Feng et al. 2019 Table 3 cites this paper (reference [115] in the Feng bibliography) for the PN→PN and PN→FSI NMDA rise/decay values (3.7 / 125 ms). The earlier “unconfirmed” hedge has been removed after full-text verification of Feng’s Table 3 and reference list.
