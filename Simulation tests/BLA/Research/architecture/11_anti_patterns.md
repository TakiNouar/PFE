# 11 — Anti-Patterns (archived failed tests — must not recur in Run 1)

| Anti-pattern | Consequence in archived failed tests | Required alternative |
|--------------|--------------------------------------|----------------------|
| Shared step current to all neurons | Synchrony = 1.0, single volley | ≥75 % private drive |
| AMPA τ_decay = 2 ms on PN→PN | Recurrent excitation dies between spikes | **6.9 ms** |
| NMDA without Mg block | NMDA acts as tonic current; ~85 % of excitatory current | Dynamic s(V) every step |
| Fixed in-degree K=3 while scaling N | Large-N collapse (inhibition wins) | Distance-dependent probabilities |
| No I_sAHP | Unadapted high-rate volleys | Multi-compartment PN with sAHP |
| Current-injection Gaussian noise | Weak desynchronization | Conductance-based OU (Feng Table 7) |
| No short-term depression | Missing natural brake after strong activation | Dynamic STP (Feng Table 4) |
| Different seeds for calibration vs sweep | Non-reproducible results | Single global seed |
| Scoring that ignores the only after-discharge candidates | Wrong parameter set selected | Explicit, documented selection rule |
| Fabricated / template summary text | False claims of healthy graded responses | Summary derived only from measured tables |
| Pure-Python re-implementation of `.mod` kinetics without listing deviations | Lost claim to literature fidelity | Load ModelDB mechanisms or document every approximation |
| Stepped Python OU update on full large net | Run became intractable | Native simulator advance |
| Treating isolated after-discharge as a success criterion | Wasted tuning effort | Record it; do not optimize for it in isolation |

Any future implementation that re-introduces an anti-pattern above is considered invalid regardless of the numeric scores it produces.

Archive detail: `Simulation tests/BLA/reports/test_run_1/`.
