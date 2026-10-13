# 06 — Noise and Inputs

Run 1 uses Feng's two kinds of input as he built them, plus one input of our own (the threat).

| Input | Stands in for | Source | Our choice? |
|---|---|---|---|
| Background noise | thousands of unmodelled synapses onto every cell | Feng code | no |
| Afferent spike trains | cortical inputs to the BLA (PFC, perirhinal, entorhinal) | Feng code + data files | no |
| Threat input | a sensory threat arriving through those afferents | this spec | **yes** (DEV-005) |

## 1. Background noise (Feng code)

Feng's point-conductance noise (Destexhe et al. 2001): a fluctuating excitatory conductance and a fluctuating inhibitory conductance at each cell's soma. Mechanisms `Gfluct2_exc` (`Gfluct_new_exc.mod`) and `Gfluct2_inh` (`Gfluct_new_inh.mod`), unchanged, one each at `soma(0.5)` of **every** cell.

| Setting | PN | FSI | Set where |
|---|---|---|---|
| g_e0 (mean excitatory) | 3.2 nS | 1.21 nS | `BL_main.hoc` |
| σ_e | 3 nS | 0.12 nS | `BL_main.hoc` |
| τ_e, E_e | 2.728 ms, 0 mV | same | mod defaults |
| g_i0 (mean inhibitory) | 21 nS | 5.73 nS | `BL_main.hoc` |
| σ_i | 8 nS | 2.64 nS | `BL_main.hoc` |
| τ_i, E_i | 10.49 ms, −75 mV | same | mod defaults |

PN values match Feng's Table 7. FSI values are the code's unrounded versions of Table 7's 1.2 / 0.1 / 5.7 / 2.6 nS (DEV-002). FSI noise is weak **on purpose**: Feng: FSIs should "spike with input from PNs, but not with solely background inputs".

Each noise process needs its own random stream. Feng uses `Random123` streams indexed by cell ID (`BL_main.hoc` lines 196 and 207); do the same, with the global seed. From Python, attach the stream with `setRandObjRef` and keep a reference to the `Random` object alive (the archived "Random binding failed" error was most likely a missing reference).

## 2. Afferent spike trains (Feng code + data)

Feng drives the network with 1,800 spike trains built from real recordings of cortical cells in quiet, awake rats (Headley et al. 2015). They are stored in ModelDB 247968 `input/` (`spikesmatrix_op`, `spikes_ind`; 165 s long). Run 1 reuses the **first M** of those trains, so the input statistics come from Feng's data rather than from us.

| Setting | Rule | Value at 1,000 cells | Source |
|---|---|---|---|
| Number of trains M | round(2.97 × N_PN / 40) | 67 | keeps Feng's 2.97 trains per PN |
| PN targets per train | 40, random | 40 | Feng |
| FSI targets per train | round(3.4 × N_FSI / M), random | 5 | keeps Feng's 3.4 trains per FSI |
| Synapse on PN | `pyrD2pyrD_STFD` at `dend(0.9)`, W ~ lognormal(9, 0.05) | | Feng code |
| Synapse on FSI | `pyrD2interD_STFD`, placed as in Feng's input code, W ~ lognormal(2, 0.2) | | Feng code |
| Delay | U(0.5, 1) ms | | Feng code |

The trains are fed in with `VecStim` (`vecevent.mod`). If Feng's train files cannot be read, **stop and report**. Do not replace them with invented Poisson rates.

If a protocol needs more than 165 s, loop the trains and record it.

## 3. Threat input (our protocol choice)

A threat is modelled as **the same afferent trains becoming more active** for a short window.

- During the threat window, each train gets extra Poisson spikes at rate (D − 1) × r_i, where r_i is that train's mean rate over Feng's file. Its rate is therefore multiplied by D.
- Doses **D = 2, 4 and 8**. A dose ladder replaces a single invented "threat strength": the result is a dose-response curve.
- Same synapses, weights and targets as the afferents. Extra spikes come from a dedicated seeded stream.

This is not a Feng parameter, so it is logged as DEV-005. It is a simple, explainable stand-in: "more input through the existing pathways". A specific thalamic threat pathway is a later refinement.

## Rules carried from the archived failures

- Every cell gets **private** background noise. Afferent trains are shared only the way Feng shares them (each train reaches 40 PNs).
- No uniform step current to all cells (archived synchrony = 1.0).
- No current-injection Gaussian noise (archived weak desynchronization).
