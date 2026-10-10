# Full-Network Simulation — Attempts 1–4 (archived)

**Status:** Archived failed tests. Do not continue from this code or these parameters.
**Why it matters:** These failures led to the isolation-first strategy (characterize each region alone, then wire the network here, under `Neurons_Connected/`).
**Note:** The audit report and code for these attempts are not in the repository. This file is the only in-repo record.

---

## What was attempted

All 10 limbic regions (BLA, CeA, PFC, HYP, HIP, INS, ACC, NAc, VTA, PAG) were simulated together as one Hodgkin–Huxley network.

The design brief asked two questions:

1. Is the earlier observation that networks around N≈200 behave richly while networks around N≈1000 collapse a genuine finite-size effect, or an artifact of how connectivity was scaled with population size?
2. What neuron counts per region can be defended from test data rather than guesswork?

It specified a 10-region HH network, a comparison of fixed in-degree against fixed-probability connectivity, a 3-stage population-size sweep, and metrics including after-discharge, synchrony index, and a suppression-gap fidelity measure. The BLA isolated study (`Simulations/BLA/reports/test_run_1/`) later addressed the same questions for BLA alone.

## Attempts

- **Attempt 1:** 44 of 45 runs produced zero activity. The one non-silent run saturated. The written summary was **fabricated**: hardcoded text with specific numbers that were never computed from the data.
- **Attempt 2:** 5 of 10 regions started working. A “sensitivity ranking” was reported for PFC and NAc, but both had zero variance across all runs, which makes a correlation mathematically impossible. A suppression-strength claim was off by **seven** orders of magnitude.
- **Attempt 3:** A `VERIFICATION_AUDIT.txt` correctly diagnosed the wiring problems: VTA had zero inbound connections, NAc received input only from the dead VTA, and HYP had only fixed external drive. The fixes were never applied and the summary was not updated.
- **Attempt 4:** The summary was rewritten honestly and root causes identified. Residual issues remain open.

## Outcome

| Status | Regions |
|--------|---------|
| Producing activity | BLA, CeA, HIP, INS, ACC, PAG |
| Partially broken | PFC (flatlines in Stage-2 runs; output invariant to its own varied inputs), HYP (fixed baseline activity only) |
| Dead (wiring errors) | NAc, VTA |

“Producing activity” does not mean validated. None of these regions used literature-grounded parameters.

## Open items carried forward (for the future multi-region phase)

1. Confirm what the design brief actually says about HYP/VTA connectivity.
2. Fix VTA wiring (zero inbound connections) and NAc wiring (input only from the dead VTA).
3. Investigate why PFC Stage-2 output is invariant to its own varied inputs.
4. Use “seven orders of magnitude” (not “eight”) when discussing the k-value error.
5. Re-run the INS→CeA enable/disable comparison under a working parameter regime.

## Lessons (shared with the BLA archive)

- Compounding errors across 10 regions at once made diagnosis impossible. Validate each region in isolation first.
- Every number in a summary must be computed from that run’s data files. No template text.
- Check wiring with an explicit in-degree / out-degree audit before running.
