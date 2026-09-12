# 11 — Anti-Patterns (what failed in test_run_1 and must not recur)

| Anti-pattern | Consequence in test_run_1 | Required alternative |
|--------------|---------------------------|----------------------|
| Shared step current to all neurons | Synchrony = 1.0, single volley | ≥75 % private drive |
| AMPA τ_decay = 2 ms on PN→PN | Recurrent excitation dies between spikes; after-discharge impossible | **6.9 ms** |
| NMDA without Mg block | NMDA acts as tonic current; ~85 % of excitatory current | Dynamic s(V) every step |
| Fixed in-degree K=3 while scaling N | Large-N collapse (inhibition wins) | Distance-dependent probabilities |
| No I_sAHP | Unadapted high-rate volleys | Multi-compartment PN with sAHP |
| Current-injection Gaussian noise | Weak desynchronization | Conductance-based OU (Feng Table 7) |
| No short-term depression | Missing natural brake after strong activation | Dynamic two-factor STP |
| Different seeds for calibration vs sweep | Non-reproducible results | Single global seed |
| Scoring that ignores the only after-discharge candidates | Wrong parameter set selected (Run 4) | Explicit, documented selection rule |
| Fabricated / template summary text | False claims of healthy graded responses (Run 1) | Summary derived only from measured tables |
| Pure-Python re-implementation of `.mod` kinetics without listing deviations | Lost claim to literature fidelity | Either load ModelDB mechanisms or document every approximation |
| Stepped Python OU update on full 370-cell net | Run became intractable; only proxy finished | Native simulator advance |
| Treating isolated after-discharge as a success criterion | Wasted tuning effort | Record it; do not optimize for it in isolation |

Any future implementation that re-introduces an anti-pattern above is considered invalid regardless of the numeric scores it produces.
