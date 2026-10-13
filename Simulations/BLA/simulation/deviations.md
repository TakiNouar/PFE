# Deviations log — BLA Run 1

Every departure from Feng et al. 2019 (paper or ModelDB 247968 code) or from `Simulations/BLA/Research/architecture/`.

DEV-001 to DEV-005 are **planned** deviations, decided in the October 2026 redesign (`Simulations/BLA/reports/04_run1_redesign_oct2026.md`) before any code was written. Add implementation-time deviations below them with the next free number.

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
