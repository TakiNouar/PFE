# 04 — Synaptic Models

All values below are the required targets. Units: time in ms, conductance in nS, voltage in mV.

## Receptor kinetics (Feng Table 3)

| Connection | Receptor | Rise τ | Decay τ | Peak g | E_rev | Upstream source (per Feng) |
|------------|----------|--------|---------|--------|-------|----------------------------|
| PN → PN | AMPA | 0.3 | **6.9** | 1.0 | 0 | Mahanty & Sah 1998; Guzman et al. 2016 |
| PN → PN | NMDA | 3.7 | **125** | 0.5 | 0 | (confirm Feng footnote) |
| PN → PV/SOM | AMPA | 0.1 | 2.4 | 1.0 | 0 | Mahanty & Sah 1998; Guzman et al. 2016 |
| PN → PV/SOM | NMDA | 3.7 | 125 | 0.5 | 0 | |
| PV/SOM → PN | GABA-A | 0.5 | 6.8 | 0.6 | **−75** | **Galarreta & Hestrin 1997** |
| PV → PV | GABA-A | 0.5 | 6.8 | 0.2 | −75 | **Galarreta & Hestrin 1997** |

## NMDA Mg²⁺ block (mandatory, dynamic)

```
s(V) = 1 / (1 + 0.33 * exp(−0.06 * V))
```

(Zador et al. 1990). Evaluated every time step.

## Synaptic delay

Fixed = **1.5 ms** (Feng).

## Short-term depression (Feng Table 4 — corrected)

| Connection | D_max | Experimental basis |
|------------|-------|--------------------|
| FSI → PN | 0.6 | Woodruff & Sah 2007 (BLA) |
| PN → FSI | 0.7 | Woodruff & Sah 2007 (BLA) |
| PN → PN | **0.5** | **Silberberg et al. 2004 (neocortex)** — Feng notes no BLA-specific data |

Dual recovery time constants in the ~40 ms / ~70 ms range as implemented in Feng. Depression state updated on every presynaptic spike.

**Do not** state that PN→PN depression is BLA-measured; the source paper flags the import.
