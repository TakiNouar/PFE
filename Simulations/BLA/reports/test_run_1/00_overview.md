# Test Run 1 — Overview (archived failed BLA campaign, historically “Runs 1–5”)

**Location:** `Simulations/BLA/reports/test_run_1/`
**Purpose:** Record everything that was attempted, what broke, and what must change before the clean start.
**Status:** Historical record only. Do not continue from any of the code or parameters described here. The simulation code was never committed to the repository.

This folder is the **single** archive of the first BLA campaign. The earlier duplicate synthesis in `Research/reports/` (files `00_`–`05_`, the monolithic `BLA_isolated_simulation_report.md`, and its CORRECTIONS overlay) was merged into this folder in October 2026.

---

## What the campaign was for

It was the first isolated-region study, run after the full-network attempts failed (see `Simulations/Neurons_Connected/reports/full_network_attempts_1_to_4.md`). The goal was parameters that produce graded, desynchronized activity during a stimulus and measurable after-discharge (emotional inertia) after it ends, using the blueprint population of 50 Pyr / 12 PV / 8 SOM. External input was approximated with step or OU currents; neither the fast thalamic nor the slow cortical route was modelled.

## What this folder contains

| File | Content |
|------|---------|
| `00_overview.md` | This file — scope and reading order |
| `01_runs_1_to_3.md` | Runs 1–3: synchrony, private drive, large-N collapse |
| `02_runs_4_to_5.md` | Runs 4–5: E/I sweep, NMDA attempt, after-discharge failure |
| `03_literature_mismatches.md` | Exact parameter errors vs Feng et al. 2019 / Kim et al. 2013 |
| `04_rebuild_attempt_and_blockers.md` | Literature rebuild attempt, deviations, environment blockers |
| `05_lessons_for_clean_restart.md` | Concrete list of what must be fixed / avoided next time |
| `06_accuracy_verification_corrections.md` | Corrections log for these archive documents |
| `07_established_results_and_conclusion.md` | What was (and was not) established + design-level conclusion |

---

## One-sentence summary

Five empirical runs established graded desynchronized activity and reproducibility, but used guessed kinetics. A later literature-constrained rebuild could not be executed because NEURON was unavailable, and its proxy run introduced further deviations.

After-discharge (≥10 ms) was never achieved in isolation. It is now treated as a **network-level** target, not an isolated-BLA success criterion.

---

## Recommended reading order for a clean restart

1. `03_literature_mismatches.md` — know the correct numbers before writing any code.
2. `05_lessons_for_clean_restart.md` — know the non-negotiable constraints.
3. `01_runs_1_to_3.md` + `02_runs_4_to_5.md` — understand what already failed and why.
4. `07_established_results_and_conclusion.md` — what carries forward as a lesson.
5. `04_rebuild_attempt_and_blockers.md` — the environment and tooling limits that stopped the last attempt.

The authoritative build spec for the new campaign is `Simulations/BLA/Research/architecture/`, not this folder.
