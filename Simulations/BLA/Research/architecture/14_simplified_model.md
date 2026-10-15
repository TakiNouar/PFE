# 14 — Simplified BLA Model (main model since 2026-10-15)

**Status:** draft spec, 2026-10-15. Decisions behind it: `reports/04_run1_redesign_oct2026.md` (last sections). Measurements behind it: `reports/06_engine_benchmark_oct2026.md` (engine), `reports/07_blockB_reference_oct2026.md` (network reference), Block A outputs (single-cell reference).
**Relation to 00–13:** files 00–13 describe Feng's detailed model, which is now the **reference** only. This file is the binding spec for the model the project will use. Wiring, inputs, metrics and gates reuse 02, 05, 06 and 08 wherever this file does not say otherwise.

---

## 1. In one paragraph

The BLA is rebuilt from **simple neurons** that are fitted to Feng's cells:
- **Principal cells:** a soma with adaptation, plus one dendrite where the excitatory synapses and NMDA sit.
- **FSIs:** one compartment.

Everything else is Feng's, as documented in his paper and code: the population mix, inputs per cell, synapse kinetics and depression, noise and afferent input.

The model is written **once, in GeNN**. Its exact single-core CPU mode is used for fitting and checks; its GPU mode is used for large and live runs. It passes when:
- each cell reproduces Feng's measured cell (Block A);
- the 1,000-cell network fires like the rat BLA at rest;
- the network responds to threat in a graded way and settles back, like Feng's network in Block B.

## 2. Engine and numerics

| Item | Choice | Reason / source |
|---|---|---|
| Engine | PyGeNN 5.4 (GeNN), one model code | Decision 2026-10-15; `reports/06` |
| Checks and fitting | GeNN `single_threaded_cpu` backend, **double** precision, fixed seeds | Exact and repeatable: same seed → identical spikes |
| Large and live runs | GeNN `cuda` backend, **single** precision | ~70,000 neurons in real time on the laptop GPU (`reports/06`) |
| Time step | **0.1 ms** | GPU budget. Fitting is done at 0.1 ms, so fitted values belong to this step. A check at 0.05 ms (CPU) must give the same statistics (gate S6) |
| Integration | Exact exponential updates for every linear part (synaptic conductances, noise, passive decay of adaptation); forward Euler for the membrane equations | Fewer numerical errors at 0.1 ms |
| Cross-check | Brian2 2.10 (CPU), the same equations, once per model version at 1,000 cells | Independent second implementation (statistics must agree) |
| Environment | `C:\Users\nouar\.venvs\brian2`; run through `Simulations/BLA/simplified/with_gpu_env.cmd` | `reports/06` setup notes |

## 3. Cells

Units: mV, ms, nF, µS, nA. All values below marked *fit* are fitted to Block A (`simulation/outputs/blockA/single_cells_full.json`, `drive_test.json`, `passive_tau.json`). Nothing is hand-set without a source.

### 3.1 Principal cells (PN-A and PN-C)

**Equations (two compartments):**

```
soma:      C_s dV/dt  = −g_Ls (V − E_L) + g_Ls Δ_T exp((V − V_T)/Δ_T) + g_c (V_d − V)
                        − Σ w_k + I_noise + I_GABA + I_inject
dendrite:  C_d dV_d/dt = −g_Ld (V_d − E_L) + g_c (V − V_d) + I_AMPA + I_NMDA
adaptation: τ_k dw_k/dt = a_k (V − E_L) − w_k ;   at a spike: V → V_r, w_k → w_k + b_k
spike when V > V_cut (= V_T + 5 Δ_T)
```

- **PN-A and PN-C share** the passive and spike parameters (Feng's two types have identical passive properties and first-spike latencies: Block A).
- **They differ only in adaptation:**
  - **PN-A** needs a strong slow adaptation current (k = s, decaying over ~1–2 s). It stands for Feng's Ca²⁺-dependent sAHP with a 1 s Ca²⁺ pool. Target: one spike per 1 s step at every current, and inter-spike gaps of 2.1 s (0.4 nA) and 1.65 s (1.0 nA) in 4 s steps.
  - **PN-C** needs at most a weak adaptation. Target: last ISI ÷ first ISI of 1.03–1.11.
- **Up to two adaptation currents** (fast k = f, slow k = s). The simplest form that passes the gates is used. A conductance-based slow current (g_s (V − E_K)) may replace the subtractive w_s if the subtractive one cannot meet both gaps.
- **Not modelled:** Ih, spike shape, and the 1.5 nA depolarization block of PN-C (decision 2026-10-15: no block by default). The effective time constant (set mainly by Ih in Feng's cell, U29) is fitted directly.

| Target (Feng's PN, Block A) | Value |
|---|---|
| Resting potential | −70.2 mV |
| Input resistance (−0.05 nA) | 136 MΩ |
| Membrane time constant | 30.9 ms slowest; 34.9 ms 63 % rise (`passive_tau.json`) |
| First-spike latency, 0.1 / 0.2 / 0.3 / 0.4 / 0.6 / 0.8 / 1.0 / 1.5 nA | 38.4 / 21.6 / 15.3 / 12.0 / 8.3 / 6.3 / 5.0 / 3.3 ms (both types) |
| PN-C spikes in 1 s, same currents | 10 / 15 / 18 / 20 / 22 / 25 / 28 / *(9: block, not fitted)* |
| PN-A spikes in 1 s, every current | 1 |
| 4 s steps | PN-A 2 spikes (0.4 nA), 3 (1.0 nA); PN-C 78 and 110 |
| Feng's background noise only, 60 s | PN-A 0.35 Hz (ISI CV 0.27); PN-C 1.65 Hz (CV 0.82) |
| Feng's afferent trains on the dendrite + noise, 20 s (dendritic-input test) | PN-A 0.69 Hz, PN-C 3.25 Hz |

The dendritic-input test is what fixes g_c, C_d and g_Ld: the two-piece reduction failed exactly there (−35 %, loss of the local NMDA boost; DEV-006 history).

### 3.2 FSI

**Equation (one compartment, no adaptation):**

```
C dV/dt = −g_L (V − E_L) + g_L Δ_T exp((V − V_T)/Δ_T) + I_noise + I_AMPA + I_NMDA + I_GABA + I_gap + I_inject
```

**No depolarization block** (decision 2026-10-15). A refractory period is added only if needed to reach 221 Hz without unrealistic V_r.

| Target (Feng's FSI, Block A) | Value |
|---|---|
| Resting potential | −70.0 mV |
| Input resistance | 371 MΩ |
| Membrane time constant (63 % rise) | 19.9 ms |
| Spikes in 1 s, 0.1 / 0.2 / 0.3 / 0.4 / 0.6 / 0.8 / 1.0 / 1.5 nA | 24 / 61 / 89 / 111 / 144 / 168 / 187 / 221 |
| First-spike latency, same currents | 39.7 / 14.3 / 9.1 / 6.8 / 4.6 / 3.5 / 2.9 / 2.0 ms |
| Adaptation (last ÷ first ISI) | 0.98–1.01 (none) |
| Feng's FSI background noise only | 0 Hz (FSIs fire only with PN input, by Feng's design) |
| Gap-junction coupling coefficient | 0.069 in Feng's model; Woodruff & Sah 2007 ≈ 0.05 |

### 3.3 Fitting

- Cells are fitted on the CPU backend, PN-A, PN-C and FSI separately, against the targets above with the same protocols as Block A (`07` single-cell protocol, dendritic-input test).
- The cost function is a weighted sum of relative errors, with weights recorded with the result.
- The optimiser is SciPy (installed 2026-10-15 with approval): differential evolution, then a local refinement.
- Output: `simplified/config/cells_fitted.json` with values, errors per target and the fit settings.

## 4. Synapses

Kinetics and depression are Feng's code values (DEV-003, DEV-004; `simulation/mechanisms_run1/exc_ev.mod`, `inh_ev.mod`, identical to Feng's files to 1.4e-13 in `synapse_test.json`):

| Pathway | Target | Receptors (pulse Cdur ms, αT_max /ms, β /ms, ḡ nS) | Depression floor |
|---|---|---|---|
| PN→PN | PN dendrite | AMPA 1.421, 3.8142, 0.1429, 1.0; NMDA 16.765, 0.2659, 0.008, 0.5 | 0.5 |
| PN→FSI | FSI | AMPA 0.713, 10.1571, 0.4167, 1.0; NMDA as PN→PN | 0.7 |
| FSI→PN | PN soma | GABA-A 0.7254, 1.52, 0.14, 0.6; E = −75 mV | 0.7 |
| FSI→FSI | FSI | GABA-A 0.7254, 1.853, 0.147, 0.2; E = −75 mV | 0.7 |

- **Depression**, every pathway: d1 0.95 (τ 40 ms) and d2 0.9 (τ 70 ms), multiplied, with the floor above.
- **NMDA Mg²⁺ block:** Feng's form, B(V) = 1 / (1 + 0.33 exp(−0.06 V)), evaluated at the compartment holding the synapse (the PN dendrite).

**Choice S-1: decided 2026-10-15 (M. T. Nouar): option (b).**
- (a) Implement Feng's pulse kinetics exactly in GeNN. It's possible, using per-connection state and a delayed end-of-pulse event, but complex.
- (b) Use a rise-and-decay (dual-exponential) conductance per receptor, fitted to Feng's unitary conductance waveform, with Feng's depression rule unchanged.

(b) is simpler and faster, and is a recorded deviation (S-DEV-3). Gate S2 compares unitary waveforms and train responses with `synapse_test.json`. **Watch point:** Feng's pulse scheme saturates when spikes from one connection overlap within the pulse (NMDA pulse 16.8 ms), and a plain rise-and-decay curve does not. If S2 fails at 20–50 Hz, add a per-connection saturation term.

## 5. Network, noise and inputs (from 02, 05, 06 unless stated)

| Item | Value | Source |
|---|---|---|
| Size and mix | 1,000 cells: 640 PN-A, 260 PN-C, 100 FSI (size check 500) | Feng; `02` |
| Inputs per cell | PN←PN 24.98, PN←FSI 42.6, FSI←PN 214.8, FSI←FSI 21.6; p = min(1, K/n_pre), weights ×K/n_pre when p = 1 | DEV-001; `05` |
| Weights | lognormal(mean, var): PN→PN (2, 1), PN→FSI (7, 2), FSI→PN (12, 2), FSI→FSI (20, 10), as multipliers of ḡ | DEV-003 |
| Delays | distance / (1 mm/ms) + 0.8 ms + U(−0.1, 0.1) ms, placement in a cube at 9,840 cells/mm³, ≥ 25 µm apart; per-connection delays via GeNN dendritic delays, rounded to 0.1 ms | Feng code; `05` |
| Gap junctions | 8 % of FSI pairs; conductance set so the coupling coefficient matches (target 0.05–0.07, see 3.2) | Woodruff & Sah 2007; Feng |
| Background noise | Feng's point-conductance noise (OU): PN g_e0 3.2, σ_e 3.0, g_i0 21, σ_i 8 nS; FSI 1.21, 0.12, 5.73, 2.64 nS; τ_e 2.728 ms, τ_i 10.49 ms; E_e 0, E_i −75 mV; exact OU update | DEV-002; Gfluct |
| Afferent input | Feng's spike trains, 2.97 trains per PN, 40 PNs per train, 3.4 per FSI; weights lognormal (9, 0.05) PN, (2, 0.2) FSI; delays U(0.5, 1) ms; on the PN dendrite | `06`; DEV-005 |
| Threat | afferent rate ×2, ×4, ×8 for 2 s (offline); a runtime "threat level" multiplier (live) | `07`; DEV-005 |
| Seeds | 5, named random streams as in `07` | `07` |

**FSI rate (U30):** if the network gives FSIs above the rat range, the FSI background or afferent input is adjusted to reach the rat value. That's a recorded deviation, because Block B's 35 Hz is not a target.

## 6. Gates

**S1 — Single cells (CPU, double precision), against Block A:**
- **Passive:** resting potential within ±1 mV; input resistance and time constant within ±10 %.
- **Firing:** spike counts within ±10 % (±1 below 10 spikes) at 0.1–1.0 nA (PN-C 1.5 nA exempt: block not modelled).
- **Latency** within ±10 %.
- **PN-A pattern:** one spike per 1 s step, and 4 s-step gaps within ±15 %.
- **Noise-only rates** within ±15 %; ISI CV within ±0.1.
- **Dendritic-input test** rates within ±15 %.

**S2 — Synapses:**
- unitary conductance peak and decay within ±5 % of Feng's;
- the response to 5, 20 and 50 Hz trains (with depression) within ±5 % (`synapse_test.json` protocols).

**S3 — Network at rest** (1,000 cells, 5 seeds, CPU):
- mean PN rate 0.2–3 Hz (Gate 3; rat 0.21 / 1.55 Hz, Amir et al. 2018);
- FSI rate in the rat range, target 22–27 Hz (Amir et al. 2018), guard 10–30 Hz;
- synchrony index < 0.5;
- PN ISI CV > 0.5 (irregular; Block B 0.71).

**S4 — Threat** (5 seeds):
- PN and FSI rates rise at every dose, and the PN response grows with dose;
- back inside the rest range in the last 2 s after each trial;
- response sizes of the same order as Block B (PN +0.2 / +0.4 / +0.7 Hz at ×2 / ×4 / ×8). These are a guide, not a tolerance, because the FSI rate differs (U30).

**S5 — Inhibition and size:**
- with FSI→PN off, PN rates rise (suppression ratio > 1);
- 500 vs 1,000 cells within 2 SD (Gate 5).

**S6 — Engine:**
- CPU same seed gives identical spikes;
- GPU (single precision) statistics within 2 SD of CPU (double precision);
- dt 0.05 vs 0.1 ms statistics within 2 SD;
- Brian2 cross-check statistics within 2 SD;
- 1,000-cell BLA at or below 0.5× real time on the GPU.

## 7. Live mode (later, after S1–S6)

- Python steps the GPU model in blocks: one exchange every 100 steps (10 ms of brain time), never every step. Each step's fixed cost is ~35 µs of a 100 µs budget (`reports/06`).
- **In:** threat level (afferent-rate multiplier), later inputs from other regions.
- **Out:** population rates of PN-A, PN-C and FSI per 50 ms window. Downstream regions and the LLM read the *population*: single PNs change only 0.65 → 1.4 Hz under threat (Block B).
- The viewer (`13`) is reused; its snapshot files do not depend on the engine.

## 8. Code layout (planned)

```
Simulations/BLA/simplified/
├── with_gpu_env.cmd            ✔ toolchain environment (MSVC 2022 + CUDA 12.9)
├── engine_benchmark/           ✔ CPU vs GPU benchmark (reports/06)
├── config/bla_simple.json      ☐ every value above with its source key
├── config/cells_fitted.json    ☐ fitted cell values (written by fit_cells.py)
├── bla_simple/
│   ├── cells.py                ☐ GeNN neuron models (PN two-compartment, FSI)
│   ├── synapses.py             ☐ GeNN synapse and depression models (choice S-1)
│   ├── fit_cells.py            ☐ S1 fitting against Block A
│   ├── synapse_check.py        ☐ S2
│   ├── network.py              ☐ wiring, delays, gaps (reuses simulation/bla_sim streams and wiring rules)
│   ├── inputs.py               ☐ noise, Feng's afferent trains, threat
│   ├── run.py                  ☐ offline runs (CPU or GPU backend)
│   ├── gates.py                ☐ S3–S6 (metrics reused from simulation/bla_sim/metrics.py)
│   └── live.py                 ☐ live stepping loop (section 7)
└── outputs/
```

## 9. Planned deviations (recorded in `simplified/deviations.md` when implemented)

| ID | Deviation from Feng's model |
|---|---|
| S-DEV-1 | Simplified cells: two-compartment adaptive integrate-and-fire PN, point FSI; no Ih (its effect fitted into the passive values), no spike shape |
| S-DEV-2 | No depolarization block (FSI, and PN-C at 1.5 nA) |
| S-DEV-3 | Synapse kinetics: rise-and-decay conductances fitted to Feng's pulse-scheme waveforms (choice S-1 b); Feng's depression rule unchanged |
| S-DEV-4 | Time step 0.1 ms (Feng 0.05 ms); single precision on the GPU |
| S-DEV-5 | FSI rate tuned to the rat range if needed (U30) |

## 10. Decisions taken (M. T. Nouar)

- 2026-10-15: GeNN as the single model; FSIs without depolarization block; S-1 = (b) fitted rise-and-decay synapses; SciPy as the fitting optimiser.
