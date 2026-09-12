# 06 — Noise and External Drive

## Background noise (Feng Table 7)

Conductance-based Ornstein–Uhlenbeck processes with separate excitatory and inhibitory components.

**Principal cells (required numbers)**

| Parameter | Value |
|-----------|-------|
| g_e0 | 3.2 nS |
| σ_e | 3 nS |
| τ_e | 2.73 ms |
| E_e | 0 mV |
| g_i0 | 21 nS |
| σ_i | 8 nS |
| τ_i | 10.49 ms |
| E_i | −75 mV |

**Fast-spiking interneurons**

| Parameter | Value |
|-----------|-------|
| g_e0 | 1.2 nS |
| σ_e | 0.1 nS |
| g_i0 | 5.7 nS |
| σ_i | 2.6 nS |

τ_e, τ_i, E_e, E_i for FSIs: **copy exactly from Feng Table 7 / ModelDB** into `full_parameters.json`. Do not leave “as given in ModelDB” without the numeric values in the run package. If Table 7 lists them as identical to PN time constants, write that explicitly.

**Rule:** Prefer compiled Gfluct (or equivalent) from ModelDB. Analytic OU in Brian2/Python is allowed only when NEURON is unavailable, with identical coefficients and a `deviations.md` entry.

## Sensory / external drive

- **Private fraction ≥ 75 %** — independent realization per neuron.
- **Common fraction ≤ 25 %** — shared across the population.
- Preferred form: OU current or conductance with τ ≈ 3 ms (or ModelDB equivalent).
- Total run **300 ms**; stimulus window **50–150 ms**; after-stimulus observation **150–250 ms**.
- Amplitudes chosen so mean Pyr rate during stimulus falls in **~10–40 Hz**. Report amplitudes and resulting rates.

## Apply drive to all populations

Pyr, PV-like, and SOM-like all receive background noise. Sensory-like drive may be stronger on Pyr; interneurons must not be left with zero external drive at small N (archived failure mode).

## What failed in archived tests and must not recur

- Shared uniform step current to all neurons → synchrony = 1.0.
- Current-injection Gaussian noise without conductance change → weak desynchronization.
- Drive only on Pyr → silent PV/SOM at small N.
