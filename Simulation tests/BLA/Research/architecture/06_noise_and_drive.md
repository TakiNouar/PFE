# 06 — Noise and External Drive

## Background noise (Feng Table 7)

Conductance-based Ornstein–Uhlenbeck / point-conductance processes with separate excitatory and inhibitory components.

**Methods provenance:** Feng cites Destexhe et al. 2001 (*Neuroscience* 107:13–24; Destexhe, Rudolph, Fellous, Sejnowski) for the point-conductance equations. The 2003 *Nat Rev Neurosci* review is related conceptual background only.

**Principal cells (Feng Table 7)**

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

**Rule:** Prefer compiled Gfluct (or equivalent) from ModelDB. Pure-Python analytic OU is allowed only when NEURON is unavailable, must use the identical coefficients, and must be listed in deviations.

## Sensory / external drive

- **Private fraction ≥ 75 %** — independent realization per neuron.
- **Common fraction ≤ 25 %**.
- Preferred form: OU current or conductance with τ ≈ 3 ms (or ModelDB equivalent).
- Stimulus window: **50–150 ms** (total run 300 ms).
- Amplitudes chosen so mean Pyr rate during stimulus falls in **10–40 Hz**. Report exact amplitudes and resulting rates.

## Anti-patterns (do not repeat)

- Shared uniform step current → synchrony = 1.0.
- Current-injection Gaussian noise without conductance change.
- Drive only on Pyr → silent interneurons at small N.
