# 08 — Metrics and Outputs

## Metrics

| Metric | Definition | Used by |
|---|---|---|
| Resting rate | Mean spikes/s per cell over the 30 s rest epoch; reported separately for PN-A, PN-C, all PN, and FSI (mean ± SD across cells, then across seeds) | Gate 3, 5 |
| Silent fraction | Fraction of PNs with zero spikes in the rest epoch | report |
| Synchrony index | Mean pairwise correlation of spike counts in 5 ms bins, over 100 randomly chosen PN pairs (seeded) | Gate 3 |
| ISI CV | Coefficient of variation of inter-spike intervals, PNs with ≥ 5 spikes in the rest epoch | report |
| Threat response | Mean PN and FSI rate in the 2 s threat window minus the 2 s before it, per dose (mean ± SD across trials and seeds) | Gate 4 |
| Recovery | Mean PN rate in the last 2 s of the 4 s after-window, compared with the rest epoch | Gate 4 |
| Suppression ratio | PN resting rate with FSI→PN weights at 0 ÷ PN resting rate intact (> 1 means inhibition works); also for the ×4 threat | Gate 4 |
| After-discharge | PN rate in 100 ms bins over the 4 s after the threat; time until it returns within the rest range | report only |
| Population spectrum | Power spectrum of the summed PN spike train in the rest epoch (gamma check) | report only |
| Single-cell | Resting potential, input resistance, membrane time constant, f–I curve, first-spike latency, adaptation ratio (last ISI ÷ first ISI at each step), noise-only rate and ISI CV | Gates 2, R1 |
| Reduction match | One-piece vs full PN on every single-cell measure; reduced vs full-detail 200-cell network on rest rates, ×4 threat response, recovery and synchrony | Gates R1, R2 |
| Synapse unit test | Largest conductance difference, Feng's vs event-driven synapse, per synapse type and train | Gate R2 (reported) |
| Gap coupling | Coupling coefficient of coupled FSI pairs | Gate 2 |
| Realised wiring | Inputs per cell per pathway (mean ± SD), gap-junction pairs, delays (min / mean / max) | Gate 0, report |
| Speed | Real-time factor and peak memory per run | report |

**Rest range** for the recovery test: mean ± 2 SD of PN rate across the fifteen 2 s windows of the rest epoch.

## Output files (under `Simulations/BLA/simulation/outputs/<run_id>/`)

- `full_parameters.json`: every value we set (counts, K targets, p, weight distributions, noise settings, afferent settings, threat doses, durations, seeds), each with a source key from `12_sources_map.md`, plus paths and SHA-256 hashes of every Feng file used.
- `connections.csv`: pre, post, pathway, weight, delay.
- `spikes_<seed>.csv`: cell, time.
- Block A (run id `blockA`):
  - `single_cells_<level>.json` (level = `full`, `twopiece`, `onepiece`): steps A1–A2, same protocol.
  - `reduction_R1_<level>.json`: Gate R1, measure by measure, with pass/fail and any approved exceptions.
  - `synapse_test.json`: step A3.
- Block B: `reduction_R2.json`, Gate R2 comparison of the full-detail and reduced 200-cell networks.
- `metrics.json` + `metrics.txt`: every metric above.
- `benchmark.csv` (Phase 0).
- `summary.txt`: written **only** from the numbers in `metrics.json`. No template sentences.
- `deviations.md` is maintained in `Simulations/BLA/simulation/`, not per run.
- `live/`: rolling snapshots for the live viewer (`13`). **Display only, never used for metrics**, deleted as the run goes, and gitignored.

## Reproducibility check

Step C7 of `07` re-runs seed #1 with the live broadcast off. Its spike file must be identical to the first run's (byte-for-byte after sorting by time and cell). This also proves the broadcast does not change results.
