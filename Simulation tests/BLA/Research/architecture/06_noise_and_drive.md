# 06 — Noise and External Drive

## Background noise (Feng Table 7)

Conductance-based Ornstein–Uhlenbeck processes with separate excitatory and inhibitory components.

**Principal cells**

| Parameter | Value |
|-----------|-------|
| g_e0 | 3.2 nS |
| σ_e | 3 nS |
| τ_e | 2.73 ms |
| g_i0 | 21 nS |
| σ_i | 8 nS |
| τ_i | 10.49 ms |

**Fast-spiking interneurons**

| Parameter | Value |
|-----------|-------|
| g_e0 | 1.2 nS |
| σ_e | 0.1 nS |
| g_i0 | 5.7 nS |
| σ_i | 2.6 nS |
| τ values | as given in Feng / ModelDB |

**Rule:** Prefer the compiled Gfluct (or equivalent) mechanisms from ModelDB. Pure-Python analytic OU is allowed only when NEURON is unavailable, and must use the identical coefficients and be listed in the deviations section.

## Sensory / external drive

- **Private fraction ≥ 75 %** — independent realization per neuron.
- **Common fraction ≤ 25 %** — shared across the population.
- Preferred form: OU current or conductance with τ ≈ 3 ms (or the ModelDB equivalent).
- Stimulus window: **50–150 ms** (inside a total run of 300 ms).
- Amplitudes (baseline + stimulus) chosen so that population mean Pyr rate during the stimulus falls inside the **10–40 Hz** biological range. Report the exact amplitudes used and the resulting rates.

## What failed before and must not be repeated

- Shared uniform step current to all neurons → perfect synchrony (Run 1).
- Current-injection Gaussian noise without conductance change → weak desynchronization.
- Drive applied only to Pyr while interneurons receive nothing → silent PV/SOM at small N.
