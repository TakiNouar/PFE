# 06 — Intrinsic Physiology

## Principal neuron currents (Kim et al. 2013 / Feng et al. 2019)

Multi-compartment (soma + apical dendrite + passive dendrite) models include:

- Fast Na⁺ (I_Na)
- Delayed-rectifier K⁺ (I_Kdr)
- A-type K⁺ (I_A)
- M-current (I_M)
- Hyperpolarization-activated cation current (I_h)
- High-threshold Ca²⁺ (I_Ca)
- Persistent Na⁺ (I_NaP)
- Slow Ca²⁺-dependent AHP (I_sAHP) — **critical for adaptation**
- Leak

Passive parameters (exact values from Feng et al. 2019 Materials and Methods):

- C_m = **2.4 µF/cm²** (PN); **1.0 µF/cm²** (FSI) — Feng et al. 2019
- R_m ≈ **55 kΩ·cm²** (PN); **20 kΩ·cm²** (FSI) — Feng et al. 2019
- R_a = **150 Ω·cm** (both PN and FSI) — Feng et al. 2019
- E_L = **−75 mV** (PN) — Feng et al. 2019
- Resulting V_rest ≈ **−70.3 mV**, input resistance ≈ **140 MΩ**, τ_m ≈ **30 ms** (PN) — Feng et al. 2019

Adaptation strength is controlled mainly by the density of I_sAHP (and to a lesser extent I_M). Type-A PNs have high I_sAHP; Type-C have very low I_sAHP and fire continuously.

## Fast-spiking interneurons

- Short action-potential duration (half-width <1 ms).
- Essentially non-adapting high-frequency trains.
- Dominated by fast Na⁺ and delayed-rectifier K⁺; lower C_m and higher leak conductance than PNs (as above).

## Why I_sAHP cannot be omitted

Without the slow AHP, model PNs continue firing at high rates during sustained input and produce artificial synchronous volleys. Biological BLA principal cells slow down; the model must reproduce that adaptation if population dynamics are to be realistic.
