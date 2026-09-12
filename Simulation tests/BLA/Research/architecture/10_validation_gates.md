# 10 — Validation Gates

A run is accepted only when every gate below passes. Failure of any gate stops the campaign; do not “tune past” a failed gate.

## Gate 0 — Source fidelity

- [ ] Every kinetic coefficient and probability is present in `full_parameters.json` with a literature citation or ModelDB path.
- [ ] `deviations.md` exists and is either empty (“no deviations”) or lists only environment-forced approximations that were pre-authorized.

## Gate 1 — Reproducibility

- [ ] Same parameters + same global seed → identical spike times (bit-level).

## Gate 2 — Activity quality (1.0×)

- [ ] Synchrony index < 0.5
- [ ] CV of ISIs > 0.3
- [ ] Active fraction > 0.4
- [ ] Mean Pyr rate ∈ [10, 40] Hz during stimulus

## Gate 3 — Inhibition functional

- [ ] Suppression ratio (inhibition on / inhibition off) clearly > 1 (expect ~2× from prior measurement).
- [ ] PV and SOM populations are not silent under the chosen drive.

## Gate 4 — Scale behaviour

- [ ] Scale sweep completed at 0.5× / 1.0× / 1.5× / 3.0×.
- [ ] No catastrophic collapse to near-zero activity at 3.0× under distance-dependent connectivity.
- [ ] Synchrony remains < 0.5 at all scales that have healthy rates.

## Gate 5 — Diagnostics

- [ ] AMPA-off (NMDA-only) run produces interpretable activity (confirms Mg block and NMDA pathway).
- [ ] Feed-forward-only run shows the expected loss of recurrent amplification.

## Gate 6 — Reporting discipline

- [ ] Summary text contains only numbers that appear in the JSON/CSV tables of that run.
- [ ] No template sentences, no invented claims.

Only after all gates pass may the parameters be promoted for use in the multi-region network.
