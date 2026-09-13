# BLA Isolated Population Simulation — Full Project Report

**Project:** Emotionally Grounded Conversational AI (PFE)
**Author:** Mohamed Takieddine Nouar
**Institution:** Higher Institute of Sciences — HIS, Algiers
**Date:** September 2026

> **Note:** This monolithic file is kept as a reference archive. Prefer the split modules `00_`–`05_` in this folder for navigation. Full-network pre-history failed across **4** attempts (not 3). Suppression ratio from Run 3 is **~2×** (effectiveness 0.51), not 4×.

---

## Status of this archive

Earlier isolation attempts documented here are **archived failed tests**. The next campaign is clean **Run 1** under `Simulation tests/BLA/Research/architecture/`, with literature provenance in `Research/Sources/`.

See also:
- `00_overview_and_context.md` … `05_parameter_errors_next_steps.md` (split)
- `Research/reports/literature_provenance_audit_sep2026.md`
- `Simulation tests/BLA/reports/00_clean_restart_policy.md`

---

## Full-network pre-history (4 attempts)

A prior full-network simulation (documented in the audit report, not fully in the repo) attempted all 10 regions simultaneously. It failed across **4 attempts**:

- **Attempt 1:** 44 of 45 runs produced zero activity. The 1 non-silent run saturated. The written summary was fabricated — hardcoded text with specific numbers that were never computed from the actual data.
- **Attempt 2:** 5 of 10 regions started working. A "sensitivity ranking" was reported for PFC and NAc — both of which had zero variance across all runs, making correlation mathematically impossible. A suppression-strength claim was off by seven orders of magnitude.
- **Attempt 3:** A `VERIFICATION_AUDIT.txt` correctly diagnosed the wiring problems (VTA had zero inbound connections, NAc received input only from dead VTA, HYP had only fixed external drive) but the fixes were never applied. The summary was not updated.
- **Attempt 4:** Summary rewritten honestly. Root causes identified. Residual issues remain open.

---

## Isolated BLA campaign (archived)

Runs historically labelled 1–5 established:
- Graded desynchronized activity is achievable with private drive
- Interneuron suppression ~**2×** (ratio 0.51)
- Wrong kinetics (AMPA 2 ms, missing Mg block, fixed-K scaling) cause the documented failures
- After-discharge is **not** an isolated-BLA success criterion

Numeric tables and run narratives remain in the split files and in `Simulation tests/BLA/reports/test_run_1/`.

---

## Design conclusion (still valid)

Emotional inertia is a **network-level** property. Isolated BLA correctly returns toward baseline when its only input ends. Persistence in the intact system depends on VTA dopamine, HIP context, BLA↔CeA↔PAG loops, and weakened prefrontal suppression.

---

*Restored September 2026 after accidental empty push. Prefer split report modules + architecture for implementation.*
