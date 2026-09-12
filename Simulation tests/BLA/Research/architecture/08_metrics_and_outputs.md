# 08 — Metrics and Outputs

## Metrics (compute for every run)

| Metric | Definition |
|--------|------------|
| Mean / peak firing rate | Pyr, PV, SOM during 50–150 ms |
| Active fraction | Fraction of Pyr cells with rate > 5 Hz in the stimulus window |
| Synchrony index | Pairwise spike-count correlation in 5 ms bins |
| CV of ISIs | Coefficient of variation of inter-spike intervals of active Pyr cells |
| Mean ISI | From the same spike trains |
| After-discharge profile | Mean rate in successive 5 ms bins from 150–250 ms; duration above 5 Hz |
| NMDA current fraction | Fraction of total excitatory synaptic current carried by NMDA (Mg block active) during stimulus |
| Interneuron suppression ratio | Mean Pyr rate with inhibition intact / mean Pyr rate with all inhibitory synapses off |

## Required output files

- `full_parameters.json` — every conductance, time constant, probability, seed, volume, path to source mechanisms.
- `calibration_table.json` + `.txt`
- `scale_sweep_table.json` + `.txt`
- `summary.txt` — derived only from the numbers in the tables (no template sentences).
- Spike time files (or raster data) for the 1.0× case and each scale.
- After-discharge profile plot if any post-stimulus bin exceeds 5 Hz.
- `deviations.md` — every place the implementation differed from ModelDB / papers, or the explicit statement “no deviations”.

## Reproducibility check

Re-run the 1.0× configuration with the same seed. Spike times must match bit-for-bit. If they do not, the run is invalid.
