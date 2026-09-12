# 06 — Noise and External Drive

**Source of truth:**
- Equations: **Destexhe, Rudolph, Fellous, Sejnowski (2001)**, *Neuroscience* 107(1):13–24 — what Feng Methods cite for the point-conductance / OU formalism.
- Coefficients: **Feng Table 7** (adapted from that formalism).
- Docs: `Research/Sources/01_primary_bla_references.md`, `05_computational_neuroscience.md`, `12_sources_map.md`.

**Do not cite Destexhe, Rudolph & Paré (2003) *Nat Rev Neurosci* as the methods source** — that is a different paper (review, different co-authors).

## Background noise (Feng Table 7)

Conductance-based Ornstein–Uhlenbeck / point-conductance processes (separate E and I).

**Principal cells**

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

τ_e, τ_i, E_e, E_i for FSIs: copy **exactly** from Feng Table 7 / ModelDB 247968 into `full_parameters.json`. Do not leave “as in ModelDB” without numbers in the run package.

**Rule:** Prefer ModelDB Gfluct (or equivalent). Analytic OU in Brian2/Python only if NEURON is unavailable, with identical coefficients + `deviations.md` entry.

## Sensory / external drive

- Private fraction ≥ **75 %**; common ≤ **25 %**.
- Preferred form: OU current or conductance, τ ≈ 3 ms (or ModelDB equivalent).
- Total run **300 ms**; stimulus **50–150 ms**; post-stimulus window **150–250 ms**.
- Amplitudes so mean Pyr rate during stimulus is ~**10–40 Hz**. Report amplitudes and rates.

## Apply drive to all populations

Pyr, PV-like, and SOM-like all receive background noise. Do not leave interneurons with zero external drive at small N (archived failure).

## Archived failures — do not repeat

- Shared step current → synchrony = 1.0
- Current-injection Gaussian (no conductance noise) → weak desynchronization
- Drive only on Pyr → silent PV/SOM
