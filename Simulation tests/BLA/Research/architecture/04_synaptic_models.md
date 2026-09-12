# 04 — Synaptic Models

**Source of truth:** `Research/Sources/01_primary_bla_references.md` (Feng Table 3/4 + upstream papers).  
See also `12_sources_map.md`.

Units: time **ms**, conductance **nS**, voltage **mV** (Feng convention).

## Receptor kinetics (Feng Table 3)

| Connection | Receptor | Rise τ | Decay τ | Peak g | E_rev | Upstream (Feng cites) |
|------------|----------|--------|---------|--------|-------|------------------------|
| PN → PN | AMPA | 0.3 | **6.9** | 1.0 | 0 | Mahanty & Sah **1998**; Guzman et al. **2016** |
| PN → PN | NMDA | 3.7 | **125** | 0.5 | 0 | Confirm Feng footnote (do not assume Weisskopf) |
| PN → PV/SOM | AMPA | 0.1 | 2.4 | 1.0 | 0 | Mahanty & Sah 1998; Guzman et al. 2016 |
| PN → PV/SOM | NMDA | 3.7 | 125 | 0.5 | 0 | |
| PV/SOM → PN | GABA-A | 0.5 | **6.8** | 0.6 | **−75** | **Galarreta & Hestrin 1997** |
| PV → PV | GABA-A | 0.5 | 6.8 | 0.2 | −75 | Galarreta & Hestrin 1997 |

**Do not** attribute the 6.9 ms / 2.4 ms AMPA decays to Mahanty & Sah 1999.

## NMDA Mg²⁺ block (mandatory, dynamic)

```
s(V) = 1 / (1 + 0.33 * exp(-0.06 * V))
```

Source: **Zador et al. 1990** (via Feng). Apply every timestep. Listed in `Research/Sources/02_supporting_biological.md`.

## Synaptic delay

Fixed **1.5 ms** unless ModelDB 247968 specifies otherwise — then copy ModelDB into `full_parameters.json`.

## Short-term depression (Feng Table 4)

| Connection | D_max | d1/d2 | τD1/τD2 (ms) | Experimental basis |
|------------|-------|-------|--------------|--------------------|
| FSI → PN | **0.6** | 0.9/0.95 | 40/70 | Woodruff & Sah **2007** (BLA) |
| PN → FSI | **0.7** | 0.9/0.95 | 40/70 | Woodruff & Sah 2007 (BLA) |
| PN → PN | **0.5** | 0.9/0.95 | 40/70 | **Silberberg et al. 2004 (neocortex)** — Feng: no BLA-specific data |

Depression state updates on every presynaptic spike. Static weights alone are insufficient.

**Do not** claim PN→PN depression is BLA-measured or cite Woodruff & Sah for that row.

## Implementation notes

- Dual-exponential conductances (Destexhe kinetic formalism — see `Research/Sources/05_computational_neuroscience.md`).
- If the simulator uses µS, document conversion (`1 nS = 0.001 µS`) in `full_parameters.json`.
- PN→FSI AMPA uses **2.4 ms** decay, not 6.9 ms.
