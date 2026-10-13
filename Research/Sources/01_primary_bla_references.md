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
| PN → PN | NMDA | 3.7 ms | **125 ms** | 0.5 nS | 2 / 1 | **Weisskopf, Bauer & LeDoux 1999** (cited by Feng; "[115]" is the PMC anchor number, not printed in eNeuro. That paper reports **no** NMDA rise/decay constants, so cite the values to Feng — U1) |
| PN → FSI | AMPA | 0.1 ms | 2.4 ms | 1.0 nS | 7 / 2 | Mahanty & Sah 1998; Guzman et al. 2016 |
| PN → FSI | NMDA | 3.7 ms | 125 ms | 0.5 nS | 7 / 2 | Weisskopf, Bauer & LeDoux 1999 (via Feng) |
| FSI → PN | GABA-A | 0.5 ms | **6.8 ms** | 0.6 nS | 12 / 2 | **Galarreta & Hestrin 1997** |
| FSI → FSI | GABA-A | 0.5 ms | 6.8 ms | 0.2 nS | 20 / 10 | **Galarreta & Hestrin 1997** |
| FSI – FSI | gap junction | — | — | coupling coeff. ≈ 0.05 | — | Woodruff & Sah 2007 |

E_AMPA = E_NMDA = 0 mV; **E_GABA = −75 mV**. Mg block: s(V) = [1 + 0.33·exp(−0.06V)]⁻¹ (Zador et al. 1990), multiplying the NMDA conductance: G_NMDA = g_max · STP · s(V) · r_NMDA.

**"Strength" column:** Feng's Eq. 4–6 write each synaptic current as w·G·(V−E), with w "the synaptic weight for the synapse"; Table 3 gives its mean and variance. Only the distribution (lognormal) comes from the code: `function_ConnectInternal_simplify_online_op.hoc` draws per connection E→E `lognormal(2,1)`, E→I `lognormal(7,2)`, I→E `lognormal(12,2)`, I→I `lognormal(20,10)`. NEURON's `lognormal(a, b)` takes the mean a and variance b of the weight itself. Effective peak conductance is g × W. **U20 resolved (Oct 2026):** `BL_main.hoc` loads that file (line 378) and calls `ConnectInternal()` (line 381). The E→E draw (line 24) is one weight shared by AMPA and NMDA (`W = W_nmda = initW`, `pyrD2pyrD_STFD_new.mod` lines 134/138), so Table 3's PN→PN AMPA 5/3 is **not** in the code. The mod's unused default `initW = 5` may be where the "5" came from.

**Short-term depression (Table 4) — values and sources:**

| Connection | D_max | d1/d2 | τD1/τD2 (ms) | Experimental basis per Feng |
|---|---|---|---|---|
| FSI → PN | **0.6** | 0.9/0.95 | 40/70 | Woodruff & Sah 2007 (BLA) |
| PN → FSI | **0.7** | 0.9/0.95 | 40/70 | Woodruff & Sah 2007 (BLA) |
| PN → PN | **0.5** | 0.9/0.95 | 40/70 | **Silberberg et al. 2004 (neocortex)** — Feng explicitly notes lack of BLA-specific data |

Do not claim PN→PN depression is BLA-measured; the source paper flags it as imported.

**Meaning of "D_max" in the ModelDB code:** in `pyrD2pyrD_STFD_new.mod` the release factor is `facfactor = F · D1 · D2`. After each presynaptic spike `D1 ← D1·d1` and `D2 ← D2·d2`, each recovering toward 1 with its own τ. The listed limit is a **floor**: `if (facfactor < 0.5) { facfactor = 0.5 }`. So D_max = 0.5 means depression can never take the synapse below 50 % of its weight. Facilitation (`F`) stays at 1 in all four synapse files. **U21 resolved (Oct 2026):** no `.hoc` file overrides any depression or kinetic parameter. All four files use `d1 = 0.95` with τD1 = 40 ms and `d2 = 0.9` with τD2 = 70 ms, the reverse of Table 4's pairing (≈ 1 % effect at the second spike). Floors in the code: PN→PN 0.5, and **0.7 for PN→FSI, FSI→PN and FSI→FSI** (Table 4 gives FSI→PN 0.6 and has no FSI→FSI row).

**Other code values that differ from the paper (Oct 2026):** FSI→PN GABA-A kinetics 0.60 / 7.14 ms (`interD2pyrD_STFD_new.mod`: AlphaTmax 1.52, Beta 0.14); Table 3's 0.5 / 6.8 ms match the FSI→FSI file. PN→PN AMPA decay 7.0 ms (Beta 0.1429). FSI noise 1.21 / 0.12 / 5.73 / 2.64 nS (`BL_main.hoc` lines 305–318). Run 1 uses the code values; see `Simulations/BLA/simulation/deviations.md`.

**Synapse formalism in ModelDB:** the code uses the Destexhe et al. 1994 kinetic scheme (`r' = AlphaTmax·on·(1−r) − Beta·r`, with a transmitter pulse of duration `Cdur`), not a dual-exponential. The Table 3 rise/decay values summarise it; for example AMPA `Beta = 0.1429 /ms` gives ≈ 7 ms decay, and NMDA `Beta = 0.008 /ms` gives 125 ms. A dual-exponential re-implementation is an approximation and must be logged in `deviations.md`. The `.mod` also contains a Ca²⁺-dependent weight-update (LTP) term, multiplied by 1e-12 so it is inert; Feng: "Our model did not have long-term synaptic plasticity."

### Connectivity (Tables 5–6)

| Connection | Probability | Source per Feng |
|---|---|---|
| PN → PN | 3 % (<50 µm), 2 % (50–100), 1 % (100–200), 0.5 % (200–600) | Abatis et al. 2017 (SfN poster — see `02_supporting_biological.md`) |
| FSI → PN | 34 % unidirectional | Woodruff & Sah 2007 |
| PN → FSI | 12 % unidirectional + 16 % reciprocal | Woodruff & Sah 2007 |
| FSI → FSI chemical | 26 % overall (20 % uni, 3 % bidirectional); 50 % uni / 25 % bi among electrically coupled pairs, 19 % / 3 % among uncoupled | Woodruff & Sah 2007; Cammarota et al. 2013 (supporting) |
| FSI – FSI gap junctions | 8 % of pairs | Woodruff & Sah 2007 |

Interneuron connections are limited to pairs within ~300 µm.

**Realised inputs per cell (Feng Results):** each PN receives 24.98 ± 9.5 PN and 42.6 ± 12.9 FSI inputs; each FSI receives 214.8 ± 58 PN and 21.6 ± 7.4 FSI inputs. No self-connections. Feng also used "a 1,000-neuron reduced model with similar connectivity rules and proportions". The code loads a precomputed 27,000-cell connection list (`input/active_syn_op`); the generator script is not in the repository.

**Gap junctions in the code:** `HalfGap` (`halfgap.mod`) at each FSI soma, r = 5,000 MΩ (0.2 nS) each way (`function_ConnectInternal_gj_simplify.hoc`). `gap.mod` is not used. The ≈ 0.05 coupling coefficient is an outcome, not a parameter.

### Synaptic delay (Methods + ModelDB)

Delay = distance / (1 mm/ms) + **0.8 ms** minimum + uniform jitter **±0.1 ms** + dt. In the ModelDB code this is `del = (dis/maxdis)·maxdelay + mindelay + del_fluc + dt`, with `maxdelay = maxdis = 2.425` (the cube diagonal in mm). It is **not** a fixed 1.5 ms.

### Background noise (Table 7) — point conductance, Destexhe et al. 2001

| Cell | g_e0 | σ_e | τ_e | E_e | g_i0 | σ_i | τ_i | E_i |
|---|---|---|---|---|---|---|---|---|
| PN | 3.2 nS | 3 nS | 2.728 ms | 0 mV | 21 nS | 8 nS | 10.49 ms | −75 mV |
| FSI | 1.2 nS | 0.1 nS | 2.728 ms | 0 mV | 5.7 nS | 2.6 nS | 10.49 ms | −75 mV |

ModelDB mechanisms: `Gfluct_new_exc.mod`, `Gfluct_new_inh.mod`.

### Extrinsic input (Methods)

Feng drives the network with 1 800 surrogate spike trains built from PFC / perirhinal / entorhinal units recorded in quiet-waking rats (Headley et al. 2015). Each 1 ms bin passes through a Poisson generator, and each train projects to 40 random PNs. PNs receive 2.97 ± 1.7 extrinsic inputs and FSIs 3.4 ± 1.9; each input also contacts FSIs within 300 µm of its PNs with 0.3 % probability. The paper does not give the per-synapse conductance of these inputs. **The code does** (`function_ConnectInputs_invivo_op.hoc`): on PNs a `pyrD2pyrD_STFD` synapse at `dend(0.9)` with W ~ lognormal(9, 0.05); on FSIs a `pyrD2interD_STFD` with W ~ lognormal(2, 0.2); delays U(0.5, 1) ms. Trains are in `input/spikesmatrix_op` and `input/spikes_ind` (165 s).

### Passive parameters (Methods)

PN: R_m = 55 kΩ·cm², C_m = 2.4 µF/cm², R_a = 150 Ω·cm, E_L = −75 mV. FSI: R_m = 20 kΩ·cm², C_m = 1.0 µF/cm², R_a = 150 Ω·cm.

**Code values (Oct 2026):** the PN template uses leak 2.5e-5 S/cm² (soma) and 4.71e-5 S/cm² (dendrites), matching Table 2 but not the "55 kΩ·cm²" text, and **E_leak −72 mV** (not −75). The FSI template sets **E_leak −70 mV**, overriding the `leakinter.mod` default of −75, and soma Ra 3,375 Ω·cm. PN dendritic Na is 15 mS/cm² in the code (Table 2: 45). Simulation settings in `BL_main.hoc`: 31 °C, v_init −70 mV. PN geometry: soma 1 segment, `dend` 8, `p_dend` 7 (16 segments); sAHP and the Ca²⁺ pool (τ 1,000 ms) are in the soma only. PN-A vs PN-C: sAHP 0.05 vs 0.0002 S/cm² (and NaP 0.000559 vs 0.000555 in the code only). Use 247968 templates only; Kim 2013 (150288) uses different Cm, Ra, geometry and sAHP.

### ModelDB 247968 file map

Main file `BL_main.hoc`. Cells: `BLcells_template_LFP_segconsider_all_Iinject_recordingimembrane.hoc` (PN) and `interneuron_template_gj_LFP_Iinject_recordingimembrane.hoc` (FSI). Wiring: `function_ConnectInternal_simplify_online_op.hoc`, `function_ConnectInternal_gj_simplify.hoc`, `function_ConnectTwoCells.hoc`, `function_ConnectInputs_invivo_op.hoc`. Synapses: `pyrD2pyrD_STFD_new.mod`, `pyrD2interD_STFD.mod`, `interD2pyrD_STFD_new.mod`, `interD2interD_STFD_new.mod`. Gap junctions: `halfgap.mod`. Inputs: `vecevent.mod` (VecStim). LFP: `xtra_imemrec.mod`. Channels used by the PN: `na3`, `nap`, `kdrca1` (`kdr`), `kaprox` (`kap`), `im`, `h` (`hd`), `cadyn`, `capool`, `sahp`, `leak`; by the FSI: `nainter`, `kdrinter`, `leakinter`. Noise: `Gfluct_new_exc/inh.mod`. Compiled but **not used** by `BL_main.hoc`: `nat`, `kadist`, `cal2`, `ca`, `bg2pyr`, `gap`. `Cell_B` in the PN template is never instantiated. `input/location.txt` is in mm. Per the README: compile the `.mod` files and create an empty `LFPs/` folder before running.

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

**Cited by Feng, but the constants are not in it (U1, Oct 2026):** Feng et al. 2019 Table 3 cites this paper for the PN→PN and PN→FSI NMDA rise/decay values (3.7 / 125 ms); "[115]" is the PMC anchor number, not a number printed in eNeuro. The full text of Weisskopf 1999 reports **no** NMDA rise or decay constants (it is a paper about NMDA-*independent* LTP). Cite the values to Feng et al. 2019 and state that the upstream constants could not be traced.
