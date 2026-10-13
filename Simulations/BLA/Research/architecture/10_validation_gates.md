# 10 — Validation Gates

Run 1 passes only when every gate below passes. If a gate fails, stop and report. Do not tune parameters to get past it: every value in this spec has a source, and a failure means something is built wrong or a source is wrong.

## Gate 0 — Provenance

- [ ] Every Feng file in `mechanisms/` matches its recorded SHA-256 hash (unchanged).
- [ ] Every value we set is in `run1.json` / `full_parameters.json` with a source key.
- [ ] `deviations.md` lists every departure (DEV-001 … ) and nothing else changed.
- [ ] Realised inputs per cell are within 10 % of the K targets in `05_connectivity.md`.
- [ ] Synaptic weights after a run equal the weights drawn at wiring (the inert LTP term changed nothing).

## Gate 1 — Reproducibility

- [ ] Same seed → identical spike file (step 8 of `07`, run with the live broadcast off, so this also proves the viewer changes nothing).

## Gate 2 — Single cells (step 1)

- [ ] PN-A slows down during a strong current step (adaptation ratio clearly > 1); PN-C keeps a steadier rate (its adaptation ratio is lower than PN-A's at every level that gives ≥ 3 spikes).
- [ ] FSI fires at high rates with little adaptation.
- [ ] Resting potential, input resistance and membrane time constant of PN-A are reported next to Feng's stated −70.3 mV, ~140 MΩ, ~30 ms. A difference of more than 10 % is investigated and explained before continuing (the paper text and code disagree on the leak, see DEV-002).
- [ ] Coupling coefficient of gap-junction pairs is reported next to Woodruff & Sah's ≈ 0.05.

## Gate 3 — Rest (1,000 cells, 5 seeds)

- [ ] Mean PN rate between **0.2 and 3 Hz**. Rat BLA principal cells: 0.21 and 1.55 Hz for the two cell classes (Amir et al. 2018); lateral amygdala average 2.7 Hz (Repa et al. 2001).
- [ ] Mean FSI rate between **10 and 30 Hz**. Rat BLA interneurons: 10–15 Hz (Paré & Gaudreau 1996); 22–27 Hz (Amir et al. 2018).
- [ ] Synchrony index < 0.5 (project guard against the archived all-cells-fire-together failure; not a literature value).

## Gate 4 — Threat response and inhibition (1,000 cells, 5 seeds)

- [ ] PN rate during the threat is higher than before it, at every dose.
- [ ] The PN response grows with dose (×2 < ×4 < ×8, comparing means across seeds).
- [ ] FSI rate also rises during the threat (FSIs follow PN activity, as Feng designed).
- [ ] Recovery: PN rate in the last 2 s after the threat is inside the rest range (`08`), at every dose.
- [ ] Suppression ratio > 1 at rest and at ×4, with the 95 % interval across seeds excluding 1.

## Gate 5 — Size check (500 vs 1,000 cells)

- [ ] Mean PN and FSI resting rates at 500 cells are within 2 SD (across seeds) of the 1,000-cell values. If they are not, the in-degree rule is not holding the network steady, and that must be explained before Run 1 results are used.

## Gate 6 — Reporting

- [ ] Every number in `summary.txt` appears in `metrics.json`.
- [ ] No template sentences, no claims beyond the measured tables.

## Recorded but never gated

After-discharge, gamma power, ISI CV, NMDA-only and no-recurrence diagnostics, real-time factor.

Only after all gates pass may Run 1's parameters be used for the BLA → CeA network.
