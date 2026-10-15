# 10 — Validation Gates

Run 1 passes only when every gate below passes. If a gate fails, stop and report. Do not tune parameters to get past it: every value in this spec has a source, and a failure means something is built wrong or a source is wrong.

**Exceptions** are recorded, never silent: any check that fails but is accepted must name the measure, the reason, who approved it and when, and must appear in `deviations.md`.

Tolerances marked *(project)* are project choices, not literature values.

## Gate 0 — Provenance

- [ ] Every Feng file in `mechanisms/` matches its recorded SHA-256 hash (unchanged).
- [ ] Our own mechanism and template files (`mechanisms_run1/`) are committed, and each is named in a `deviations.md` entry.
- [ ] Every value we set is in `run1.json` / `full_parameters.json` with a source key.
- [ ] `deviations.md` lists every departure (DEV-001 … ) and nothing else changed.
- [ ] Realised inputs per cell are within 10 % of the K targets in `05_connectivity.md` *(project)*.
- [ ] Reference level: synaptic weights after a run equal the weights drawn at wiring (Feng's inert LTP term changed nothing).

## Gate 1 — Reproducibility

- [ ] Same seed → identical spike file (step C7 of `07`, run with the live broadcast off, so this also proves the viewer changes nothing). *Preliminary 2026-10-14: identical spike files with and without the broadcast at 100 cells (678 spikes) and 1,000 cells (5,821 spikes, Phase 0).*

## Gate 2 — Single cells, Feng's originals (step A1)

**Passed 2026-10-14** (`outputs/blockA/single_cells_full.json`, `passive_tau.json`):
- [x] PN-A fires fewer spikes than PN-C at every current level, and in the 4 s steps its spikes are separated by long silent periods (strong adaptation). *PN-A 1 spike per 1 s step at every level vs PN-C 9–28; 4 s at 0.4 nA: spikes at 12 and 2,107 ms.*
- [x] PN-C fires steadily (last ISI ÷ first ISI within 0.8–1.25 at levels with ≥ 3 spikes) *(project)*. *1.03–1.11.*
- [x] FSI fires at high rates with little adaptation. *24–221 Hz, ratio 0.98–1.01.*
- [x] Resting potential, input resistance and membrane time constant of PN-A are reported next to Feng's stated −70.3 mV, ~140 MΩ, ~30 ms. A difference of more than 10 % is investigated and explained before continuing (the paper text and code disagree on the leak, see DEV-002). *−70.2 mV, 136 MΩ (−3 %). Time constant 30.9 ms as the slowest time constant (Rall's peeling); the 63 %-rise time of 34.9 ms is a different method. All estimates 29–39 ms (U29, `bla_sim/passive_check.py`).*
- [x] Coupling coefficient of gap-junction pairs is reported next to Woodruff & Sah's ≈ 0.05. *0.069.*

## Gate R1 — Main-level PN matches Feng's full PN (step A2)

For PN-A and PN-C separately, against Feng's full cell under the identical protocol *(all tolerances project)*:

**Current injection at the soma** (`bla_sim/single_cell.py`, `reduce_pn.py`):
- [x] Resting potential within ±1 mV.
- [x] Input resistance and membrane time constant within ±10 %.
- [x] Spike count at every current level (1 s ladder and 4 s steps) within ±10 %, or ±1 spike when the count is below 10. *Exception: PN-C at 1.5 nA.*
- [x] First-spike latency within ±10 % at every level that fires.
- [x] Noise only (60 s): firing rate within ±15 %, and ISI CV within ±0.1 when there are ≥ 20 spikes.

**Synaptic input on the dendrite** (`bla_sim/drive_test.py`; added 2026-10-14 after the two-piece cell passed current injection but failed in a network):
- [x] Under Feng's background noise plus three of Feng's afferent trains through Feng's afferent synapse at `dend(0.9)` (8 cells per type, 20 s, identical inputs at every level), the mean PN-A and PN-C rates are within ±15 % of Feng's full cell.

**Result 2026-10-14 for `coarse_d2_p3`: passed with one approved exception** (`outputs/blockA/reduction_R1_coarse_d2_p3.json`). Approved by M. T. Nouar on 2026-10-14 and recorded in DEV-006: at 1.5 nA, PN-C fires 6 spikes before depolarization block instead of Feng's 9. The block itself is reproduced.

**Rejected cells** (same gate): one-piece (late first spike at every current); two-piece (early first spike at strong current, and 35 % too weak under dendritic input); apical 2 + basal 1 (early first spike at strong current). Apical 2 + basal 7 passes with no exception but costs 1.6× more.

## Gate R2 — Reduced network matches the full-detail network (Block B, 200 cells, 3 seeds)

*Superseded 2026-10-14: the 6-segment main level is dropped in favour of simplified neurons (`reports/04`). Gates 3–6 will be re-stated for the simplified model; `gate_r2.py` stays available.*

The same 200-cell network, built once with Feng's originals (B1) and once with the reductions (B2):

- [ ] Mean PN-A, PN-C and FSI resting rates of B2 are within 2 SD (across B1's seeds) of B1's values.
- [ ] The PN and FSI rate increase during the ×4 threat in B2 is within 2 SD of B1's.
- [ ] Recovery after the threat behaves the same: both return inside their rest range, or neither does.
- [ ] Synchrony index < 0.5 in both, and the B1–B2 difference is below 0.1 *(project)*.
- [ ] The synapse unit test (step A3) is reported, including the largest train difference.

If Gate R2 fails, the main level cannot be used. Either fix the reduction and repeat R1–R2, or fall back to the full-detail network at a size that fits the available time, and record the decision.

## Gate 3 — Rest (main level, 1,000 cells, 5 seeds)

- [ ] Mean PN rate between **0.2 and 3 Hz**. Rat BLA principal cells: 0.21 and 1.55 Hz for the two cell classes (Amir et al. 2018); lateral amygdala average 2.7 Hz (Repa et al. 2001).
- [ ] Mean FSI rate between **10 and 30 Hz**. Rat BLA interneurons: 10–15 Hz (Paré & Gaudreau 1996); 22–27 Hz (Amir et al. 2018).
- [ ] Synchrony index < 0.5 *(project guard against the archived all-cells-fire-together failure)*.

## Gate 4 — Threat response and inhibition (main level, 1,000 cells, 5 seeds)

- [ ] PN rate during the threat is higher than before it, at every dose.
- [ ] The PN response grows with dose (×2 < ×4 < ×8, comparing means across seeds).
- [ ] FSI rate also rises during the threat (FSIs follow PN activity, as Feng designed).
- [ ] Recovery: PN rate in the last 2 s after the threat is inside the rest range (`08`), at every dose.
- [ ] Suppression ratio > 1 at rest and at ×4, with the 95 % interval across seeds excluding 1.

## Gate 5 — Size check (main level, 500 vs 1,000 cells)

- [ ] Mean PN and FSI resting rates at 500 cells are within 2 SD (across seeds) of the 1,000-cell values. If they are not, the in-degree rule is not holding the network steady, and that must be explained before Run 1 results are used.

## Gate 6 — Reporting

- [ ] Every number in `summary.txt` appears in `metrics.json`.
- [ ] No template sentences, no claims beyond the measured tables.

## Recorded but never gated

After-discharge, gamma power, ISI CV in the network, NMDA-only and no-recurrence diagnostics, real-time factors.

Only after all gates pass may Run 1's parameters and the reduced model be used for the BLA → CeA network.
