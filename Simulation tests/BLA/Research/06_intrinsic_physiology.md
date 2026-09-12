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

Passive parameters (typical ranges from the models):
- C_m ≈ 1.2–2.4 µF/cm²
- R_m ≈ 55 kΩ·cm²
- R_a ≈ 150–200 Ω·cm
- E_L ≈ −67 to −75 mV
- Resulting V_rest ≈ −70 mV, input resistance ~140–150 MΩ, τ_m ~30 ms

Adaptation strength is controlled mainly by the density of I_sAHP (and to a lesser extent I_M). Type-A PNs have high I_sAHP; Type-C have very low I_sAHP and fire continuously.

## Fast-spiking interneurons

- Short action-potential duration (half-width <1 ms).
- Essentially non-adapting high-frequency trains.
- Dominated by fast Na⁺ and delayed-rectifier K⁺; lower C_m and higher leak conductance than PNs.

## Why I_sAHP cannot be omitted

Without the slow AHP, model PNs continue firing at high rates during sustained input and produce artificial synchronous volleys. Biological BLA principal cells slow down; the model must reproduce that adaptation if population dynamics are to be realistic.
