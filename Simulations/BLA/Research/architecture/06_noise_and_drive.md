# 06 — Noise and External Drive

**Source of truth:**
- Equations: **Destexhe, Rudolph, Fellous, Sejnowski (2001)**, *Neuroscience* 107(1):13–24 — what Feng Methods cite for the point-conductance / OU formalism.
- Coefficients: **Feng Table 7** (adapted from that formalism).
- Docs: `Research/Sources/01_primary_bla_references.md`, `05_computational_neuroscience.md`, `12_sources_map.md`.

**Do not cite Destexhe, Rudolph & Paré (2003) *Nat Rev Neurosci* as the methods source** — that is a different paper (review, different co-authors).

## Background noise (Feng Table 7)

Conductance-based Ornstein–Uhlenbeck / point-conductance processes (separate E and I).

| Parameter | Principal cells | Fast-spiking interneurons (PV; SOM in Run 1) |
|-----------|-----------------|----------------------------------------------|
| g_e0 | 3.2 nS | 1.2 nS |
| σ_e | 3 nS | 0.1 nS |
| τ_e | 2.728 ms | 2.728 ms |
| E_e | 0 mV | 0 mV |
| g_i0 | 21 nS | 5.7 nS |
| σ_i | 8 nS | 2.6 nS |
| τ_i | 10.49 ms | 10.49 ms |
| E_i | −75 mV | −75 mV |

All values verified against Feng Table 7 (Oct 2026). Copy them into `full_parameters.json` with citation keys.

**Rule:** Prefer ModelDB `Gfluct_new_exc.mod` / `Gfluct_new_inh.mod`. Use an analytic OU in Brian2/Python only if NEURON is unavailable, with identical coefficients and a `deviations.md` entry. Giving SOM the FSI noise values is part of the SOM = PV-kinetics deviation (U10).

## Sensory / external drive

- Private fraction ≥ **75 %**; common ≤ **25 %**.
- Preferred form: OU current or conductance, τ ≈ 3 ms (or ModelDB equivalent).
- Timing: see `07_simulation_protocol.md` (current default stimulus 50–150 ms; window length under review, U24).
- Amplitudes so mean Pyr rate during stimulus is ~**10–40 Hz**. Report amplitudes and rates.

**Departure from Feng’s input model (U25):** Feng drives the network with Poisson surrogate spike trains from recorded PFC / perirhinal / entorhinal units. PNs receive 2.97 ± 1.7 afferents, FSIs 3.4 ± 1.9, and each train targets 40 PNs. The OU stimulus above is a protocol choice for isolating a graded “threat-like” step, not a Feng parameter. State this in the run report and in `deviations.md`.

## Apply drive to all populations

Pyr, PV-like, and SOM-like all receive background noise. Do not leave interneurons with zero external drive at small N (archived failure).

## Archived failures — do not repeat

- Shared step current → synchrony = 1.0
- Current-injection Gaussian (no conductance noise) → weak desynchronization
- Drive only on Pyr → silent PV/SOM
