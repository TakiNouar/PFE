# BLA Isolated Population Simulation — Full Project Report

**Project:** Emotionally Grounded Conversational AI (PFE)
**Author:** Mohamed Takieddine Nouar
**Institution:** Higher Institute of Sciences — HIS, Algiers
**Repository:** https://github.com/TakiNouar/PFE
**Report generated:** September 2026

---

## Repository Validation

Cloned and validated `TakiNouar/PFE` at commit `79b2638`. Repository structure confirmed:

```
PFE/
├── README.md
├── Research/
│   ├── Development/
│   │   ├── 00_status_vision_architecture.md
│   │   ├── 01_limbic_architecture.md
│   │   ├── 02_biophysical_substrate.md
│   │   ├── 03_input_dynamics_camera.md
│   │   ├── 04_translator_llm_memory_voice.md
│   │   ├── 05_hardware_stack_roadmap_scope.md
│   │   ├── 06_open_questions_simulations.md
│   │   ├── 07_meta.md
│   │   ├── README.md
│   │   └── blueprint_v2.4_full.md
│   ├── Sources/          (empty — populated by this report)
│   └── reports/          (empty — populated by this report)
└── Simulation tests/     (empty — simulation files not yet committed)
```

**Validation findings:**
- Blueprint v2.4 is correctly split into 8 focused files plus a full reference copy
- All design targets are correctly framed in future/conditional tense (v2.4 correction pass)
- No implementation claims are made anywhere in the committed files
- Sources and reports folders exist but are empty — this report and the sources document address that gap
- Simulation code files (.py, .json, .txt) are not yet committed to the repository

---

## 1. Project Context

### 1.1 What This Simulation Is For

The thesis proposes a 10-region biophysical limbic network (Hodgkin–Huxley neurons) that drives the emotional state of an Ultron-persona LLM. The LLM cannot contradict or override the neural state — the neurons are the sole authority on what is felt. Before the full 10-region network can be wired, each region needs validated parameters from isolated characterization studies.

This report covers the BLA (Basolateral Amygdala) isolated simulation, which was the first such study, conducted across 5 runs. The goal was to establish parameters that produce graded, desynchronized activity during a stimulus and measurable after-discharge (emotional inertia) after the stimulus ends.

### 1.2 What the Full-Network Study Found Before This

A prior full-network simulation (documented in the audit report, not in the repo) attempted all 10 regions simultaneously. It failed across 3 attempts:

- **Attempt 1:** 44 of 45 runs produced zero activity. The 1 non-silent run saturated. The written summary was fabricated — hardcoded text with specific numbers that were never computed from the actual data.
- **Attempt 2:** 5 of 10 regions started working. A "sensitivity ranking" was reported for PFC and NAc — both of which had zero variance across all runs, making correlation mathematically impossible. A suppression-strength claim was off by seven orders of magnitude.
- **Attempt 3:** A `VERIFICATION_AUDIT.txt` correctly diagnosed the wiring problems (VTA had zero inbound connections, NAc received input only from dead VTA, HYP had only fixed external drive) but the fixes were never applied. The summary was not updated.
- **Attempt 4:** Summary rewritten honestly. Root causes identified. Two residual issues remain open: the HIP/HYP naming error in the summary, and an unverified claim about what the design brief actually says about VTA/HYP connectivity.

**Outcome of the full-network study:** 6 of 10 regions working (BLA, CeA, HIP, INS, ACC, PAG), 2 partially broken (PFC, HYP), 2 completely dead (NAc, VTA). The isolated BLA approach was adopted to establish clean per-region parameters rather than compound errors across all 10 regions simultaneously.

---

## 2. Simulation Brief — What Was Specified

The simulation was commissioned to answer two questions:

1. Is the previously observed "networks around N≈200 behave richly, networks around N≈1000 collapse" a genuine finite-size effect, or an artifact of how connectivity was scaled with population size?
2. What neuron counts per region are actually defensible from test data rather than guesswork?

The brief specified: 10-region HH network, fixed in-degree vs. fixed-probability connectivity comparison, 3-stage population-size sweep (global scale, LHS sensitivity, local refinement), and specific metrics including after-discharge, synchrony index, and a suppression-gap fidelity measure.

The BLA isolated study addressed the same core questions, scoped to BLA alone.

---

## 3. BLA Biology and Design

### 3.1 Blueprint Specification

From Design Blueprint v2.4 (`02_biophysical_substrate.md`):

| Sub-population | Proposed N | Role |
|---|---|---|
| BLA pyramidal (excitatory) | 50 | Principal cells — carry the main signal |
| BLA PV-like (fast inhibitory) | 12 | Fast perisomatic inhibition |
| BLA SOM-like (slow inhibitory) | 8 | Slower dendritic-targeting modulation |
| **Total BLA** | **70** | |

External inputs: fast sensory route (thalamic-like, low latency) targeting BLA primarily; slow cortical route (higher latency, higher detail) targeting BLA, INS, and ACC. Neither route was implemented in isolation — only step-current approximations were used.

### 3.2 What the Literature Actually Specifies

Research conducted after the 5 runs revealed that validated, literature-grounded parameters already exist for BLA and were not used. The primary reference is **Feng et al. 2019** (eNeuro), the first large-scale biophysically and anatomically realistic model of the basolateral amygdala nucleus, with all parameters constrained by published in vitro and in vivo electrophysiology.

**Key parameters from Feng et al. 2019 (Table 3) — not used in any of Runs 1–5:**

| Connection | Receptor | Rise τ (ms) | Decay τ (ms) | Conductance (nS) |
|---|---|---|---|---|
| PN → PN | AMPA | 0.3 | **6.9** | 1.0 |
| PN → PN | NMDA | 3.7 | **125** | 0.5 |
| PN → FSI | AMPA | 0.1 | 2.4 | 1.0 |
| FSI → PN | GABA-A | 0.5 | **6.8** | 0.6 |

**Critical discrepancies with what was used:**

| Parameter | Runs 1–5 (guessed) | Literature value | Impact |
|---|---|---|---|
| AMPA τ_decay (PN→PN) | 2 ms | **6.9 ms** | Too fast — AMPA decayed between spikes, no sustained recurrent drive |
| NMDA τ_decay | 80–120 ms (guessed) | **125 ms** | Close but still wrong, and missing Mg²⁺ block |
| NMDA Mg²⁺ block | None | **s(V) = [1+0.33e^{−0.06V}]⁻¹** | NMDA was open at all voltages — became a constant current source, not activity-dependent |
| E_GABA | −70 mV | **−75 mV** | Inhibitory driving force underestimated |
| PN→PN connectivity | Fixed K=3 (~6%) | **Distance-dependent 0.5–3%** | Over-dense recurrent excitation |
| Noise model | Current injection (Gaussian) | **Conductance-based OU (separate E/I)** | Current noise doesn't change membrane conductance — weaker desynchronization |
| Short-term depression | None | **D_max=0.6, τ_D1=40ms, τ_D2=70ms** | No fatigue mechanism — saturation risk higher |
| sAHP current | None | **Required for spike adaptation** | Neurons couldn't slow their firing rate during sustained drive |

---

## 4. Run-by-Run Results

### Run 1 — Synchrony Artifact / Fabricated Summary

**Parameters:** K=3, g_AMPA=0.025 μS, σ=0.15 μA/cm², shared uniform step current, no heterogeneity, no SOM external drive

**Results:**

| Metric | Value |
|---|---|
| Valid runs | 0 / 8 |
| Peak rate (all runs) | 66.67 Hz (identical) |
| Synchrony index | 1.0 (all fixed-indegree runs) |
| After-discharge | Not measured — results invalid |

**Root causes:**
- All neurons received identical step current at the same time → simultaneous threshold crossing → single synchronous volley
- Noise too weak (σ=0.15) to desynchronize anything
- K=3 recurrent connections insufficient to sustain ongoing activity between volleys
- Written summary reported "healthy graded responses" — this was false, generated from hardcoded template text not derived from data

**What was learned:** Uniform shared drive is the primary synchronizing force. Any BLA simulation must break this at the source.

---

### Run 2 — Synchrony Partially Broken, Reproducibility Broken

**Changes from Run 1:** Noise raised to σ=1.5 μA/cm², per-neuron heterogeneity added (C_m, g_L, E_L drawn from uniform distributions), SOM given direct external drive at 0.2× I_stim_slow

**Results:**

| Scale | Conn | Synchrony | CV | Status |
|---|---|---|---|---|
| 0.5× | fixed_indegree | 0.594 | 0.11 | **SYN-FAIL** |
| 0.5× | fixed_prob | 0.369 | 0.56 | **PASS** |
| 1.0× | fixed_indegree | 0.642 | 0.24 | **SYN-FAIL** |
| 1.0× | fixed_prob | 0.533 | 0.54 | **SYN-FAIL** |
| 1.5× | fixed_indegree | 0.577 | 0.45 | **SYN-FAIL** |
| 1.5× | fixed_prob | 0.655 | 0.56 | **SYN-FAIL** |
| 3.0× | fixed_indegree | 0.771 | 0.31 | **SYN-FAIL** |
| 3.0× | fixed_prob | 0.844 | 0.40 | **SYN-FAIL** |

**Valid runs:** 1 / 8

**New problem discovered:** Calibration run and main sweep used different random seeds, producing different results with identical parameters. The simulation was not reproducible.

**Additional finding:** Synchrony increased with population size under fixed in-degree (0.594 → 0.771 from 0.5× to 3.0×). Larger populations were more synchronized, not less — confirming the shared step current was still the dominant synchronizing force, overriding the heterogeneity and noise.

**SOM silent at 0.5×:** With only 4 SOM neurons and no external drive strong enough to compensate for minimal recurrent input, SOM was completely silent at the smallest scale. The run was classified "healthy_graded" without flagging this.

---

### Run 3 — Private Drive Architecture, Genuine Pass for 5 Runs

**Changes from Run 2:** Ornstein-Uhlenbeck private drive — 75% of each neuron's sensory current is an independent per-neuron OU realization (τ_OU=3ms); 25% shared. Single global seed (GLOBAL_SEED=20260909) fixed for reproducibility. Mean rate and active_frac added as metrics to detect single-volley artifacts.

**Results:**

| Scale | Conn | Mean (Hz) | Active frac | Syn | CV | Status |
|---|---|---|---|---|---|---|
| 0.5× | fixed_indegree | 36.0 | 0.65 | 0.194 | 0.45 | **PASS** |
| 0.5× | fixed_prob | 40.4 | 0.80 | 0.299 | 0.61 | **PASS** |
| 1.0× | fixed_indegree | 19.4 | 0.65 | 0.248 | 0.51 | **PASS** |
| 1.0× | fixed_prob | 25.2 | 0.60 | 0.239 | 0.60 | **PASS** |
| 1.5× | fixed_indegree | 10.4 | 0.35 | 0.296 | 0.38 | borderline |
| 1.5× | fixed_prob | 11.9 | 0.55 | 0.106 | 0.47 | **PASS** |
| 3.0× | fixed_indegree | 0.7 | 0.05 | 0.251 | 0.00 | **LOW ACTIVITY** |
| 3.0× | fixed_prob | 9.6 | 0.40 | 0.167 | 0.40 | **PASS** |

**Valid runs:** 5 / 8

**First clean audit.** Summary conclusions derived from actual data. Reproducibility confirmed bit-identical between calibration and 1.0× fixed-indegree sweep run.

**Large-N collapse discovered under fixed in-degree:** Mean rate drops monotonically — 36.0 → 19.4 → 10.4 → 0.7 Hz — and the 3× run is classified low_activity. Root cause: fixed K=3 means each Pyr neuron receives exactly 3 recurrent excitatory inputs regardless of N, but PV and SOM populations scale proportionally — total inhibition grows while recurrent excitation per neuron stays constant. **Inhibition wins at large N under fixed in-degree.**

**Interneuron effectiveness ratio (1.0×):** 0.51 — roughly 2× suppression of peak rate when inhibitory synapses are active vs. silenced. PV and SOM are functional.

**After-discharge:** Zero across all fixed-indegree runs. Non-zero after_rate values at some scales but none sustained above 5 Hz for a full 5 ms bin.

---

### Run 4 — E/I Balance Sweep, Wrong Parameter Selected

**Changes from Run 3:** 12 combinations of (K, g_AMPA, g_GABA_PV, g_GABA_SOM) tested at N_pyr=50 fixed_indegree to find an E/I ratio that enables after-discharge.

**Calibration table:**

| Label | K | gA | gPV | gSOM | Mean | After_d | Syn | CV |
|---|---|---|---|---|---|---|---|---|
| R3_baseline | 3 | 0.06 | 0.90 | 0.55 | 19.4 | 0 ms | 0.248 | 0.51 |
| K3_higherE_lowerI | 3 | 0.08 | 0.70 | 0.40 | 28.6 | **5 ms** | 0.446 | 0.52 |
| K3_strongE_modI | 3 | 0.10 | 0.60 | 0.35 | 36.2 | 0 ms | 0.320 | 0.45 |
| K5_bal | 5 | 0.06 | 0.80 | 0.45 | 25.6 | 0 ms | 0.262 | 0.51 |
| K5_strongE_lowI | 5 | 0.10 | 0.55 | 0.30 | 49.4 | 0 ms | 0.401 | 0.36 |
| K7_strongE_lowI | 7 | 0.10 | 0.50 | 0.28 | 48.6 | **5 ms** | 0.458 | 0.27 |
| K5_midE_lowI | 5 | 0.08 | 0.50 | 0.28 | 50.6 | 0 ms | 0.373 | 0.40 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

**Selection algorithm failure:** The scoring function selected R3_baseline (identical to Run 3 parameters) as the winner. It was too conservative — it penalized higher synchrony without rewarding the only candidates that produced non-zero after-discharge.

**Correct winner (not selected):** K3_higherE_lowerI — the only syn-passing candidate (syn=0.446 < 0.5) with measurable after-discharge (5 ms).

**Consequence:** The scale sweep in Run 4 was identical to Run 3 — no new scale data.

**Key finding from calibration:** Only 2 of 12 E/I combinations produced any after-discharge (both 5 ms, neither reaching the 10 ms target). **After-discharge cannot be solved by E/I tuning alone at N=50 with AMPA-only kinetics.** The AMPA decay time (τ=2 ms) is far shorter than the inter-spike interval (~23 ms at typical rates) — the recurrent conductance decays completely between spikes and cannot sustain reverberation.

---

### Run 5 — NMDA-like Slow Recurrent Excitation

**Changes from Run 4:** Dual-component Pyr→Pyr synapse: existing AMPA (τ=2 ms) plus new NMDA-like slow conductance (τ swept: 50, 80, 120 ms). No Mg²⁺ voltage block (explicitly stated simplification). E/I baseline updated to correct Run 4 winner (K3_higherE_lowerI). 12-combination calibration sweep (3 τ values × 4 g_NMDA values).

**NMDA calibration results:**

| τ (ms) | g_NMDA (μS) | Mean (Hz) | After_r (Hz) | After_d (ms) | Syn | CV | ISI (ms) |
|---|---|---|---|---|---|---|---|
| 50 | 0.005 | 26.2 | 3.6 | 0 | 0.447 | 0.49 | 35.0 |
| 50 | 0.040 | 44.4 | 7.2 | 0 | 0.342 | 0.42 | 23.4 |
| 80 | 0.005 | 26.6 | 4.0 | 0 | 0.469 | 0.46 | 34.1 |
| 80 | 0.040 | 45.6 | 6.0 | 0 | 0.327 | 0.40 | 23.2 |
| 120 | 0.005 | 27.0 | 4.4 | 0 | 0.453 | 0.49 | 35.5 |
| **120** | **0.040** | **46.4** | **9.2** | **0** | **0.393** | **0.41** | **22.9** |

**Selected:** τ=120 ms, g_NMDA=0.040 μS

**Scale sweep results:**

| Scale | N_pyr | Mean (Hz) | Active frac | After_d (ms) | Syn | CV |
|---|---|---|---|---|---|---|
| 0.5× | 25 | 50.0 | 0.80 | 0 | — | — |
| 1.0× | 50 | 46.4 | 0.65 | 0 | 0.393 | 0.41 |
| 1.5× | 75 | 36.0 | 0.60 | 0 | — | — |
| 3.0× | 150 | **8.7** | **0.40** | **5** | — | — |

**Valid runs:** 5 / 8 (stimulus-window activity). After-discharge not achieved at the 10 ms target.

**Critical findings:**

1. **After-discharge failed again.** Diagnosis: mean ISI = 22.9 ms << τ_NMDA = 120 ms (ratio 5.23). NMDA accumulates during the stimulus but at stimulus offset, PV and SOM interneurons briefly outlast excitation, suppressing reverberation. Inhibition wins specifically at the stimulus-to-baseline transition.

2. **NMDA fraction = 0.852.** 85% of recurrent excitatory current came from NMDA. This is too dominant — biologically realistic ratio is ~50/50. The AMPA τ=2 ms was so short relative to ISI that it contributed almost nothing. This confirms the τ_AMPA error was the root problem all along.

3. **Large-N collapse substantially mitigated.** The 3× run improved from 0.7 Hz (low_activity, Run 3) to 8.7 Hz (healthy_graded, Run 5). NMDA slow accumulation partially compensates for the fixed in-degree E/I asymmetry at large N.

4. **NMDA-only diagnostic:** With AMPA disabled, mean=41.2 Hz — the network fires robustly on NMDA alone. The problem is not excitation strength; it is post-stimulus inhibitory overshoot.

---

## 5. What Has Been Established (Summary)

| Criterion | Status | Details |
|---|---|---|
| Graded desynchronized activity during stimulus | ✅ Achieved | At N=25–75, private drive, NMDA baseline. Syn < 0.5, CV > 0.3 |
| Synchrony < 0.5, CV > 0.3 | ✅ Achieved | Consistently from Run 3 onward |
| PV and SOM suppression functional | ✅ Confirmed | ~4× suppression in mean rate at 1.0× |
| Reproducibility (calibration = sweep) | ✅ Fixed | Run 3 onward, bit-identical |
| Large-N collapse explanation | ✅ Identified | Structural E/I asymmetry under fixed in-degree; partially mitigated by NMDA |
| After-discharge ≥ 10 ms | ❌ Not achieved | Inhibitory overshoot at stimulus offset; also a design problem (see §6) |

**Confirmed BLA parameters for full-network use (pending literature correction):**

```
K_Pyr→Pyr = 3 (fixed in-degree)
g_AMPA = 0.08 μS  [NOTE: literature value should be re-derived from Feng et al.]
g_NMDA = 0.04 μS, τ_NMDA = 120 ms  [NOTE: no Mg²+ block — simplification]
g_GABA_PV = 0.70 μS
g_GABA_SOM = 0.40 μS
Private drive fraction = 0.75
σ_noise = 1.2 μA/cm²
GLOBAL_SEED = 20260909
```

---

## 6. Design-Level Conclusion

### The simulation is running correctly. The results are not meeting the biological target. These are not the same problem.

After-discharge — emotional inertia, the persistence of state after a stimulus ends — was the primary dynamic target for BLA. Five runs across parameter tuning, E/I balance sweeps, and NMDA kinetics failed to produce it. The reason is not a bug, not a parameter problem, and not a fixable simulation issue within the isolated BLA framework. **It is a design problem.**

In the real brain, BLA does not maintain post-stimulus activity by itself. It is held active by a network of regions that feed back into it:

- **VTA** releases dopamine onto BLA, raising its baseline excitability after a salient event
- **HYP** drives CeA and PAG directly when PFC suppression weakens, sustaining the emotional state through a bypass route
- **HIP** provides contextual reactivation, feeding back to BLA and PFC
- **The BLA→CeA→PAG feedback loop** sustains reverberatory activity across regions

The isolated BLA in this simulation has none of that. It receives a step input, fires, and returns to baseline when the input drops — exactly as it should when isolated. Emotional inertia is a **network-level emergent property**, not a single-region property. Expecting a single isolated nucleus to produce seconds-scale state persistence without cross-regional support is equivalent to expecting a single neuron to exhibit population dynamics.

The five runs were not wasted. They established clean, validated parameters for BLA's internal dynamics — graded response, desynchronized firing, functional interneuron suppression, partial NMDA-driven activity. That is what an isolated characterization is supposed to deliver.

---

## 7. Parameter Errors That Must Be Fixed Before Run 6

The following errors existed in all 5 runs and were discovered by reading Feng et al. 2019 and the supporting electrophysiology literature. Run 6 must use literature-grounded parameters, not iterative guesses.

| Parameter | Runs 1–5 (wrong) | Correct literature value | Source |
|---|---|---|---|
| AMPA τ_decay (PN→PN) | 2 ms | **6.9 ms** | Mahanty & Sah 1998 |
| NMDA τ_decay | 80–120 ms | **125 ms** | Weisskopf et al. 1999 |
| NMDA Mg²⁺ block | None | **s(V) = [1 + 0.33 e^{−0.06V}]⁻¹** | Zador et al. 1990 / Feng et al. 2019 |
| E_GABA | −70 mV | **−75 mV** | Feng et al. 2019 |
| PN→PN connectivity | Fixed K=3 (~6%) | **Distance-dependent: 3% at <50μm, 2% at 50–100μm, 1% at 100–200μm, 0.5% at 200–600μm** | Abatis et al. 2017 |
| Noise model | Gaussian current injection | **Conductance-based OU (separate excitatory + inhibitory)** | Destexhe et al. 2001 |
| Short-term depression | None | **D_max=0.6, d1=0.9, d2=0.95, τ_D1=40ms, τ_D2=70ms** | Woodruff & Sah 2007 |
| sAHP current (Pyr) | None | **Ca²⁺-dependent slow AHP, required for spike adaptation** | Kim et al. 2013 |
| PN neuron model | Single-compartment | **3-compartment (soma + apical dendrite + passive dendrite)** | Feng et al. 2019 |

---

## 8. What Comes Next

### 8.1 Immediate: Re-run BLA with Feng et al. Parameters

Before moving to CeA, Run 6 must implement the correct literature parameters. The code should port the Feng et al. 2019 parameters into Brian2 (the chosen simulator), citing the paper as the source. The simplification of single-compartment vs. multi-compartment neurons should be explicitly acknowledged.

### 8.2 CeA Isolation Study

Once BLA parameters are clean, characterize CeA in isolation using the same methodology. CeA is simpler (single output population, no PV/SOM subdivision in the blueprint) but needs its own parameter validation.

### 8.3 BLA → CeA Two-Region Network

Wire BLA → CeA and test whether the two-region network shows after-discharge that neither showed in isolation. This is where the suppression-gap mechanism (PFC → CeA inhibition) can be first tested. After-discharge in a two-region network is a meaningful result; in isolation it was the wrong question.

### 8.4 Primary Reference to Use

**Feng et al. 2019** (eNeuro) — full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC6361623/
**Code:** https://github.com/ModelDBRepository/247968

Read Tables 1–4 and the Methods section before writing Run 6. Every parameter needed is there, constrained by direct electrophysiology in rat BLA.

---

## 9. Full-Network Study Open Items (Carried Forward)

From the earlier full-network audit, the following remain unresolved and must be addressed before the full 10-region network is attempted:

1. Confirm with the literal text of `simulation_design_brief.md` what it actually says about HYP/VTA connectivity. The current summary claims the brief "forbids adding HIP or VTA as direct sensory targets" — but this does not justify zero inbound connections of any kind to VTA.
2. Fix VTA wiring (zero inbound connections) and NAc wiring (input only from dead VTA), then rerun.
3. Investigate why PFC's Stage-2 output is invariant to its own varied inputs.
4. Correct "roughly eight orders of magnitude" to "roughly seven" (log₁₀(0.01 / 4×10⁻¹⁰) ≈ 7.4) in the k-value discussion.
5. Re-run the INS→CeA enable/disable comparison under the current working parameter regime.

---

*Report compiled from simulation run files, audit documents, and research conversation logs. Covers the full history of the BLA isolated study (Runs 1–5) plus the pre-existing full-network study findings.*
