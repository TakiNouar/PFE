# Runs 4–5 — E/I Sweep, NMDA Attempt, After-Discharge Failure

## Run 4 — E/I balance sweep, wrong winner selected

**Changes:** 12 combinations of K, g_AMPA, g_GABA_PV, g_GABA_SOM at N=50.

**Result:** Scoring algorithm selected the old R3_baseline (no after-discharge). The only syn-passing candidate that produced any after-discharge was ignored:

- Correct (unselected) winner: K=3, gA=0.08, gPV=0.70, gSOM=0.40 → mean 28.6 Hz, after_d=5 ms, syn=0.446.

**Key finding:** Only 2 of 12 combinations produced any after-discharge (both 5 ms). AMPA τ=2 ms is far shorter than the typical ISI (~23 ms) → recurrent conductance dies between spikes. After-discharge cannot be solved by E/I tuning alone with AMPA-only kinetics.

**Valid new scale data:** 0 (scale sweep simply repeated Run 3).

---

## Run 5 — NMDA-like slow recurrent excitation

**Changes:** Dual-component Pyr→Pyr (AMPA τ=2 ms + NMDA-like τ swept 50/80/120 ms). **No Mg²⁺ voltage block** (explicit simplification). Baseline taken from the correct Run-4 winner.

**Best calibration point:** τ=120 ms, g_NMDA=0.040 → mean 46.4 Hz, after_r=9.2 Hz, **after_d=0 ms**, syn=0.393, NMDA current fraction ≈ 0.85.

**Scale sweep (selected parameters):**

| Scale | N_pyr | Mean (Hz) | Active frac | After_d |
|-------|-------|-----------|-------------|---------|
| 0.5×  | 25    | 50.0      | 0.80        | 0 ms |
| 1.0×  | 50    | 46.4      | 0.65        | 0 ms |
| 1.5×  | 75    | 36.0      | 0.60        | 0 ms |
| 3.0×  | 150   | 8.7       | 0.40        | 5 ms |

**Findings:**
- Large-N collapse partially mitigated by NMDA (3× went from 0.7 Hz → 8.7 Hz).
- NMDA-only diagnostic (AMPA off) still fired robustly (mean 41.2 Hz) → problem is not excitation strength.
- At stimulus offset, inhibition briefly outlasts the NMDA tail → no sustained after-discharge.
- 85 % NMDA fraction is biologically unrealistic; caused by the still-too-fast AMPA (2 ms).

**After-discharge ≥ 10 ms:** Never achieved in any of the 12 calibration combinations or the scale sweep.

---

## Design-level conclusion (end of Runs 1–5)

The simulation engine was functioning. The biological target (isolated after-discharge) was out of scope.

Emotional inertia is a **network-level** property (VTA dopamine tone, HIP contextual reactivation, BLA→CeA→PAG loops, HYP bypass). An isolated BLA correctly returns to baseline when its only input is a step current that ends.

Isolated characterization should only be required to deliver:
- graded desynchronized activity,
- functional interneuron suppression,
- reproducible parameters.

Those were achieved (with caveats on kinetics). After-discharge belongs to the multi-region phase.
