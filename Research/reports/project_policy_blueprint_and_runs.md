# Project Policy — Blueprint and Run Numbering

**Date:** September 2026  
**Applies to:** entire PFE repository

---

## 1. The blueprint is an outline

`Research/Development/` (Design Blueprint v2.5 and successors) is the **living project outline**. It is not fixed doctrine.

- It may change when simulations, literature, or scope decisions require it.
- Simulation evidence and published parameters override older blueprint numbers when they conflict.
- Corrections are recorded (e.g. `Research/reports/blueprint_corrections_v2.5.md`) so the thesis can show *why* the outline moved.

## 2. Failed tests are archived, not continued

Early BLA isolation attempts are **archived failed tests**. Their purpose is to document mistakes (synchrony from shared drive, wrong AMPA τ, fixed-K collapse, fabricated summaries, etc.).

The next BLA implementation starts as **Run 1** of a clean, literature-grounded campaign — not as “Run 6”.

Detail: `Simulation tests/BLA/reports/00_clean_restart_policy.md`.

## 3. Authority order

1. Literature + ModelDB (see `Research/Sources/`)
2. Region architecture specs (e.g. `Simulation tests/BLA/Research/architecture/`)
3. Region research dossiers
4. Design Blueprint (outline; update when 1–3 demand it)
