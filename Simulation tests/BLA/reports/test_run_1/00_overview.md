# Test Run 1 — Overview

**Location:** `Simulation tests/BLA/reports/test_run_1/`  
**Purpose:** Record everything that was attempted, what broke, and what must change before the next clean start.  
**Status:** Historical record only. Do not continue from any of the code or parameters described here.

---

## What this folder contains

| File | Content |
|------|---------|
| `00_overview.md` | This file — scope and reading order |
| `01_runs_1_to_3.md` | Runs 1–3: synchrony, private drive, large-N collapse |
| `02_runs_4_to_5.md` | Runs 4–5: E/I sweep, NMDA attempt, after-discharge failure |
| `03_literature_mismatches.md` | Exact parameter errors vs Feng et al. 2019 / Kim et al. 2013 |
| `04_rebuild_attempt_and_blockers.md` | Literature rebuild attempt, deviations, environment blockers |
| `05_lessons_for_clean_restart.md` | Concrete list of what must be fixed / avoided next time |

---

## One-sentence summary of Test Run 1

Five empirical runs established graded desynchronized activity and reproducibility, but used guessed kinetics; a subsequent literature-constrained rebuild could not be executed because NEURON was unavailable in the environment and the proxy run introduced further deviations.

After-discharge (≥10 ms) was never achieved in isolation. This is now treated as a **network-level** target, not an isolated-BLA success criterion.

---

## Recommended reading order for a clean restart

1. `03_literature_mismatches.md` — know the correct numbers before writing any code.
2. `05_lessons_for_clean_restart.md` — know the non-negotiable constraints.
3. `01_runs_1_to_3.md` + `02_runs_4_to_5.md` — understand what already failed and why.
4. `04_rebuild_attempt_and_blockers.md` — understand the environment and tooling limits that stopped the last attempt.
