# 04 — Synaptic Models

All values below are required targets. Units: time in **ms**, conductance in **nS**, voltage in **mV** (Feng convention).

## Receptor kinetics (Feng Table 3 + supporting papers)

| Connection | Receptor | Rise τ | Decay τ | Peak g (nS) | E_rev (mV) |
|------------|----------|--------|---------|-------------|------------|
| PN → PN | AMPA | 0.3 | **6.9** | 1.0 | 0 |
| PN → PN | NMDA | 3.7 | **125** | 0.5 | 0 |
| PN → PV/SOM | AMPA | 0.1 | 2.4 | 1.0 | 0 |
| PN → PV/SOM | NMDA | 3.7 | 125 | 0.5 | 0 |
| PV/SOM → PN | GABA-A | 0.5 | 6.8 | 0.6 | **−75** |
| PV → PV | GABA-A | 0.5 | 6.8 | 0.2 | −75 |

## NMDA Mg²⁺ block (mandatory, dynamic)

```
s(V) = 1 / (1 + 0.33 * exp(-0.06 * V))
```

This factor multiplies the NMDA conductance on **every time step**. Recording the formula without applying it is not acceptable.

## Synaptic delay

Fixed axonal/synaptic delay = **1.5 ms** on every connection unless ModelDB specifies a different per-type delay — in that case copy ModelDB and document in `full_parameters.json`.

## Short-term depression (dynamic)

- Present on **every** synapse.
- Use the two-factor depression formalism and **numeric parameters from Feng Table 4** (experimental foundation: Woodruff & Sah 2007).
- Copy Table 4 values connection-by-connection into `full_parameters.json`. Do not rely on “typical order of magnitude” alone.
- Depression state must update on every presynaptic spike; static weights alone are insufficient.

If a connection type is missing from Table 4, **halt** and record the gap in `deviations.md` — do not silently import neocortical defaults as if they were BLA measurements.

## Implementation notes

- Dual-exponential (rise + decay) conductance waveforms (Destexhe kinetic formalism).
- Weight units must match the simulator; if the simulator uses µS, document `1 nS = 0.001 µS` (or the inverse) in `full_parameters.json`.
- PN→FSI AMPA uses the **2.4 ms** decay (not 6.9 ms).
