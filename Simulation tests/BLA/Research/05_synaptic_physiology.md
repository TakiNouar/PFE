# 05 — Synaptic Physiology

Values below are taken primarily from Feng et al. 2019 (Table 3) and the papers they cite (Mahanty & Sah 1998, Weisskopf et al. 1999, Woodruff & Sah 2007).

## Glutamatergic (AMPA / NMDA)

| Connection | Receptor | Rise τ (ms) | Decay τ (ms) | Typical g (nS) | Notes |
|------------|----------|-------------|--------------|----------------|-------|
| PN → PN | AMPA | 0.3 | **6.9** | ~1.0 | Linear I–V (GluR2-containing) |
| PN → PN | NMDA | 3.7 | **125** | ~0.5 | Mg block mandatory |
| PN → FSI | AMPA | 0.1 | 2.4 | ~1.0 | Often Ca-permeable (GluR2-lacking) |
| PN → FSI | NMDA | 3.7 | 125 | ~0.5 | Smaller contribution at many IN synapses |

**Mg²⁺ block (standard form used in Feng):**  
`s(V) = 1 / (1 + 0.33 * exp(−0.06 * V))`

Reversal potentials: E_AMPA = E_NMDA = 0 mV.

## GABAergic

| Connection | Rise τ (ms) | Decay τ (ms) | Typical g (nS) | E_Cl |
|------------|-------------|--------------|----------------|------|
| FSI → PN | 0.5 | 6.8 | ~0.6 | **−75 mV** |
| FSI → FSI | 0.5 | 6.8 | ~0.2 | −75 mV |

## Short-term plasticity

- Present on essentially all synapses in biological BLA.
- Depression dominates at FSI↔PN connections (Woodruff & Sah 2007): D_max ≈ 0.6, dual time constants ~40 ms and ~70 ms.
- PN→PN depression often imported from neocortical measurements when BLA-specific data are incomplete.
- Facilitation can appear at some connections under specific conditions.

## Functional consequences for simulation

- Using AMPA decay of 2 ms (instead of 6.9 ms) makes recurrent excitation vanish between spikes at realistic rates → impossible to sustain reverberation.
- Omitting the Mg block turns NMDA into a tonic current source.
- Omitting short-term depression removes a natural brake that helps the network return toward baseline after strong activation.
