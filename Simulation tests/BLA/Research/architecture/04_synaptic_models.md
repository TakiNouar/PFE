# 04 — Synaptic Models

All values below are the required targets. Units: time in ms, conductance in nS, voltage in mV.

## Receptor kinetics (Feng Table 3 + supporting papers)

| Connection | Receptor | Rise τ | Decay τ | Peak g | E_rev |
|------------|----------|--------|---------|--------|-------|
| PN → PN | AMPA | 0.3 | **6.9** | 1.0 | 0 |
| PN → PN | NMDA | 3.7 | **125** | 0.5 | 0 |
| PN → PV/SOM | AMPA | 0.1 | 2.4 | 1.0 | 0 |
| PN → PV/SOM | NMDA | 3.7 | 125 | 0.5 | 0 |
| PV/SOM → PN | GABA-A | 0.5 | 6.8 | 0.6 | **−75** |
| PV → PV | GABA-A | 0.5 | 6.8 | 0.2 | −75 |

## NMDA Mg²⁺ block (mandatory, dynamic)

```
s(V) = 1 / (1 + 0.33 * exp(−0.06 * V))
```

This factor multiplies the NMDA conductance on every time step. Recording the formula without applying it is not acceptable.

## Synaptic delay

Fixed axonal/synaptic delay = **1.5 ms** on every connection (Feng).

## Short-term depression (dynamic)

- Present on **every** synapse.
- Two-factor depression formalism with parameters from Feng Table 4 (experimental foundation: Woodruff & Sah 2007).
- Typical order of magnitude: D_max ≈ 0.6, dual recovery time constants ~40 ms and ~70 ms.
- Depression state must be updated on every presynaptic spike; static weights alone are insufficient.

## Implementation notes

- Dual-exponential (rise + decay) conductance waveforms are the expected form (Destexhe kinetic formalism).
- Weight units must be consistent with the simulator (nS vs µS). Document the conversion if any.
- For PN→FSI AMPA the faster 2.4 ms decay and calcium-permeable character (Mahanty & Sah 1998) must be respected; do not use the 6.9 ms PN→PN value on interneurons.
