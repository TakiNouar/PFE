# Deviations log — BLA Run 1

Every departure from Feng et al. 2019 (paper or ModelDB 247968 code) or from `Simulations/BLA/Research/architecture/`.

DEV-001 to DEV-005 are **planned** deviations, decided in the October 2026 redesign (`Simulations/BLA/reports/04_run1_redesign_oct2026.md`) before any code was written. DEV-006 and DEV-007 were added on 2026-10-14, after measuring speed (option D). Add implementation-time deviations below them with the next free number.

**Levels:** DEV-001 to DEV-005 apply to both levels. DEV-006 and DEV-007 apply to the **main level only**; the reference level uses Feng's cell and synapse files unchanged.

Template:

```
## DEV-00N
- What: ...
- Why required: ...
- Source of substitute value (if any): ...
- Impact on gates: ...
```

---

## DEV-001 — Reduced network wired by inputs per cell, not by distance

- **What:** 1,000 cells (640 PN-A, 260 PN-C, 100 FSI) instead of 27,000. Each pathway is wired with p = K / n_pre so every cell keeps Feng's realised number of inputs (PN→PN 25, FSI→PN 43, PN→FSI 215, FSI→FSI 22). Connection choice ignores distance, so Feng's PN→PN distance bands, the ~300 µm interneuron limit, the extra reciprocal PN↔FSI pairs and the gap-coupling-dependent FSI→FSI probabilities are not reproduced. Positions are still used for delays.
- **Why required:** keeping Feng's distance probabilities in a small volume left ~0.65 excitatory and ~7 inhibitory inputs per PN (U23). Feng's own code loads a precomputed 27,000-cell connection list and cannot be shrunk.
- **Source of substitute:** Feng 2019 realised in-degrees (Results). Precedent: Feng's own 1,000-neuron reduced model; Nair-lab 1,000-cell BLA networks scale all probabilities by 1/scale with uniform PN→PN probability (github.com/tjbanks/AmygdalaTheta). Theory: van Albada, Helias & Diesmann 2015.
- **Impact on gates:** no spatial structure, so no spatially restricted gamma bursts. Gamma is not gated. Gate 5 checks that rates do not depend on size.

## DEV-002 — Code values used where Feng's paper text differs

- **What:** principal-cell leak 2.5e-5 / 4.71e-5 S/cm² (soma / dendrites) and E_leak −72 mV (paper text: Rm 55 kΩ·cm², E_L −75 mV); FSI E_leak −70 mV (paper silent; `leakinter.mod` default −75 overridden by the template); PN dendritic Na 15 mS/cm² (paper Table 2: 45); FSI noise 1.21 / 0.12 / 5.73 / 2.64 nS (Table 7 rounds to 1.2 / 0.1 / 5.7 / 2.6).
- **Why required:** the templates and `BL_main.hoc` produced Feng's published results; they are used unchanged.
- **Source of substitute:** ModelDB 247968 PN template (lines 54–55, 76, 99, 128), interneuron template (lines 52, 69), `BL_main.hoc` (lines 305–318).
- **Impact on gates:** Gate 2 compares measured Vrest / Rin / τm with Feng's text values and explains any gap above 10 %.

## DEV-003 — Synapse values from the code where Table 3 differs

- **What:** (a) PN→PN weight: one lognormal(mean 2, var 1) per connection, shared by AMPA and NMDA (Table 3: AMPA 5/3, NMDA 2/1). (b) FSI→PN GABA-A rise 0.60 ms, decay 7.14 ms (code: AlphaTmax 1.52, Beta 0.14 /ms) instead of Table 3's 0.5 / 6.8 ms; the Table 3 values match the FSI→FSI file exactly. (c) PN→PN AMPA decay 7.0 ms (Table 3: 6.9).
- **Why required:** Feng's wiring code and synapse files produced his published results; the files are used unchanged and the weights are drawn as his code draws them (U20).
- **Source of substitute:** ModelDB 247968 `function_ConnectInternal_simplify_online_op.hoc` line 24; `pyrD2pyrD_STFD_new.mod` lines 40–44, 134, 138; `interD2pyrD_STFD_new.mod` lines 34–38.
- **Impact on gates:** recurrent AMPA about 2.5× weaker than Table 3 would give; slightly longer inhibition onto PNs. Both match Feng's own simulations.

## DEV-004 — Short-term depression settings from the code

- **What:** d1 = 0.95 with τ 40 ms and d2 = 0.9 with τ 70 ms in all four synapse files (Table 4: 0.9 with 40 ms, 0.95 with 70 ms). FSI→PN floor 0.7 (Table 4: 0.6). FSI→FSI depresses with floor 0.7 (not in Table 4).
- **Why required:** synapse files used unchanged; no `.hoc` file overrides these values (U21).
- **Source of substitute:** ModelDB 247968 `*_STFD*.mod` defaults (lines 69–86) and floor checks (lines 237–246).
- **Impact on gates:** about 1 % difference at the second spike; less inhibitory fatigue at FSI→PN than the paper implies. None expected.

## DEV-005 — Threat input is our protocol, not Feng's

- **What:** during a 2 s window, each of Feng's afferent trains gets extra Poisson spikes so its rate is multiplied by D (2, 4, 8).
- **Why required:** Feng's model has no threat stimulus; Run 1 must test a response and recovery.
- **Source of substitute:** none (protocol choice). Train baseline rates come from Feng's own input files.
- **Impact on gates:** Gate 4 tests the response and recovery under this protocol only. A specific thalamic threat pathway is a later refinement.

## DEV-006 — Principal cell on a coarser grid (main level only)

- **What:** the main-level PN (`coarse_d2_p3`) is Feng's PN rebuilt with his geometry and topology on 6 segments instead of 16, with no fitted values.
  - **Soma:** copied exactly.
  - **Apical dendrite** (`dend`, 270 × 3 µm, at soma(0)): 2 segments (Feng: 8).
  - **Basal dendrite** (`p_dend`, 555 × 5 µm, at soma(1)): 3 segments (Feng: 7).
  - **Channel values:** uniform values are copied; `nap` and `im`, which Feng puts only in a section's first segment, keep their total in the new first segment.
  - **Left out:** the LFP recorders (`extracellular`, `xtraimemrec`). A rebuild on Feng's own grid without them reproduces his cell exactly, so they do not affect the dynamics.
  - **Synapses:** at Feng's locations (excitatory at `dend(0.9)`; inhibitory and noise at the soma).
  - Parameters in `mechanisms_run1/reduced_pn.json` (written by `bla_sim/reduce_pn.py`); selected by `main_level_cell` in `bla_sim/config/run1.json`.
- **Why required:** Feng's PN costs 83 µs per cell per step; this cell costs 25 µs (2026-10-14).
- **Source of substitute:** Feng's own full cell (ModelDB 247968 `Cell_A` / `Cell_C`) is the only source and the only target. Feng's files unchanged.
- **Measured (Gate R1, 2026-10-14; `outputs/blockA/reduction_R1_coarse_d2_p3.json`, `drive_test.json`):**
  - **Matches:** resting potential −70.2 vs −70.2 mV; input resistance 136.6 vs 136.2 MΩ; time constant 34.8 vs 34.9 ms; first-spike latency within 3 % at every current; spike counts at every level except one; firing under noise (PN-A 0.35 vs 0.35 Hz, PN-C 1.62 vs 1.65 Hz); under Feng's afferent trains on the dendrite, PN-A 0.66 vs 0.69 Hz, PN-C 3.36 vs 3.25 Hz.
  - **One exception, approved by M. T. Nouar on 2026-10-14:** at 1.5 nA, PN-C fires 6 spikes before depolarization block instead of Feng's 9. The block itself is reproduced.
- **Alternatives tested and rejected (same tests):**
  - one-piece (first spike 15–60 % late at every current);
  - two-piece, i.e. soma + one lumped dendrite (first spike ~1 ms early at strong current, and 35 % too weak under dendritic synaptic input). It was briefly chosen on 2026-10-14 on current-injection results alone; the dendritic-input test reversed that;
  - apical 2 + basal 1 (first spike ~1 ms early at strong current);
  - apical 2 + basal 7 (no exception, but 41 µs, 1.6× the cost).
- **Impact on gates:** Gate R2 (200-cell network, full detail vs reduced) checks the network level.

## DEV-007 — Event-driven synapses (main level only)

- **What:** Feng's four synapse types re-implemented with the exact kinetic-synapse method of Destexhe, Mainen & Sejnowski 1994 (*Neural Comput* 6:14–18): one shared mechanism per receptor type per cell (`ExcEv` for AMPA + NMDA, `InhEv` for GABA-A), with per-connection state touched only at spikes. Same `AlphaTmax`, `Beta`, `Cdur`, `gbar`, reversal potentials, weights, delays, Mg²⁺ block, d1/d2, τ and floors as Feng's code. The whole-conductance depression rescaling, the pulse extension and NEURON's fixed-step event timing are reproduced. The only difference is that Feng's inert long-term-plasticity term (×1e-12) is left out.
- **Why required:** measured cost of Feng's synapse files is 1.0–1.4 µs per synapse per step; with ~88,000 synapses at 1,000 cells that is more than all the cells together.
- **Source of substitute:** Feng's code constants (ModelDB 247968 `*_STFD*.mod`); method from Destexhe, Mainen & Sejnowski 1994, which Feng cites for his synapse formalism. New files `mechanisms_run1/exc_ev.mod` and `inh_ev.mod`; Feng's files unchanged.
- **Measured (step A3, 2026-10-14):** conductances identical to Feng's files to floating-point precision (largest relative difference 1.4e-13) for all four pathways, for isolated spikes, 5/20/50 Hz trains, 1 ms doublets, Poisson trains, and three connections sharing one object (`outputs/blockA/synapse_test.json`). Cost 0.003 µs per connection per step, against 1.32 µs for Feng's files.
- **Impact on gates:** none expected at the synapse level; Gate R2 checks the network level.
