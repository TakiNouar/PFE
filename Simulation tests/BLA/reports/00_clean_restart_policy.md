# BLA Clean Restart Policy

**Date:** September 2026  
**Location:** `Simulation tests/BLA/reports/`

---

## Blueprint status

The Design Blueprint (`Research/Development/`) is a **project outline**, not a fixed authority. It is updated when simulations, literature, or design decisions require it. Simulation results and literature constraints take priority over any earlier blueprint number when they conflict.

This policy is project-wide: the blueprint tracks the project; the project does not obey the blueprint as unchangeable text.

---

## Run numbering — clean restart

All earlier BLA isolation attempts (historically labelled Runs 1–5 in archived material) are **failed tests**. They are kept only as an archive of mistakes to avoid repeating.

| Archive location | Content |
|------------------|---------|
| `Simulation tests/BLA/reports/test_run_1/` | Detailed post-mortem of the failed campaign |
| `Research/reports/` | Project-level synthesis of those failures and literature corrections |

**The next implementation is Run 1** of a new, literature-grounded campaign.

- Do not call it Run 6.
- Do not inherit parameters, seeds, or success criteria from the failed campaign except as **anti-patterns** (what not to do).
- Anti-patterns are frozen in `Research/architecture/11_anti_patterns.md` (under BLA Research).

---

## What we keep from the archive

1. Lessons (shared drive → synchrony, AMPA 2 ms → dead recurrence, fixed-K → large-N collapse, etc.).
2. The conclusion that **long after-discharge is not an isolated-BLA success criterion**.
3. Pointers to Feng et al. 2019 / Kim et al. 2013 / supporting electrophysiology.

## What we do not keep

1. Guessed kinetics, fixed K=3 as the connectivity rule, or any “best” E/I set from the failed sweeps.
2. Any requirement to match the failed campaign’s numeric tables.
3. Run numbering continuity.

---

## Authority order for the new Run 1

1. Peer-reviewed parameters (Feng / Kim / ModelDB + Sources).
2. `Simulation tests/BLA/Research/architecture/` (implementation spec).
3. `Simulation tests/BLA/Research/` biology dossier (context).
4. Design Blueprint (outline only; update it when the above change the design).
