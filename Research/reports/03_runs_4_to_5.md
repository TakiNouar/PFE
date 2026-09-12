# Run-by-Run Results (Runs 4–5)

### Run 4 — E/I Balance Sweep, Wrong Parameter Selected

**Changes from Run 3:** 12 combinations of (K, g_AMPA, g_GABA_PV, g_GABA_SOM) tested at N_pyr=50 fixed_indegree to find an E/I ratio that enables after-discharge.

**Key finding:** Only 2 of 12 E/I combinations produced any after-discharge (both 5 ms, neither reaching the 10 ms target). **After-discharge cannot be solved by E/I tuning alone at N=50 with AMPA-only kinetics.** The AMPA decay time (τ=2 ms) is far shorter than the inter-spike interval (~23 ms) — the recurrent conductance decays completely between spikes and cannot sustain reverberation.

**Selection algorithm failure:** The scoring function selected R3_baseline as the winner (too conservative). Correct winner was K3_higherE_lowerI (syn=0.446, after_d=5 ms).

---

### Run 5 — NMDA-like Slow Recurrent Excitation

**Changes from Run 4:** Dual-component Pyr→Pyr synapse: AMPA (τ=2 ms) plus NMDA-like slow conductance (τ swept: 50, 80, 120 ms). No Mg²⁺ voltage block (simplification). E/I baseline corrected to K3_higherE_lowerI.

**Selected:** τ=120 ms, g_NMDA=0.040 μS

**Scale sweep results:**

| Scale | N_pyr | Mean (Hz) | Active frac | After_d (ms) | Syn | CV |
|---|---|---|---|---|---|---|
| 0.5× | 25 | 50.0 | 0.80 | 0 | — | — |
| 1.0× | 50 | 46.4 | 0.65 | 0 | 0.393 | 0.41 |
| 1.5× | 75 | 36.0 | 0.60 | 0 | — | — |
| 3.0× | 150 | **8.7** | **0.40** | **5** | — | — |

**Critical findings:**

1. **After-discharge failed again.** At stimulus offset, PV and SOM interneurons briefly outlast excitation — inhibition wins at the transition.
2. **NMDA fraction = 0.852.** 85% of recurrent excitatory current from NMDA. Biologically realistic ratio is ~50/50. Confirms the τ_AMPA=2 ms error was the root problem.
3. **Large-N collapse substantially mitigated.** 3× run improved from 0.7 Hz (Run 3) to 8.7 Hz.
4. **NMDA-only diagnostic:** With AMPA disabled, mean=41.2 Hz — network fires robustly on NMDA alone. Problem is post-stimulus inhibitory overshoot, not excitation strength.
