# 04 — Synaptic Models

**Source of truth:** `Research/Sources/01_primary_bla_references.md` (Feng Table 3/4, Methods, ModelDB 247968 notes, upstream papers).
See also `12_sources_map.md`.

Units: time **ms**, conductance **nS**, voltage **mV** (Feng convention).

## Receptor kinetics (Feng Table 3)

| Connection | Receptor | Rise τ | Decay τ | Peak g | Weight W (mean/var) | E_rev | Upstream (Feng cites) |
|------------|----------|--------|---------|--------|---------------------|-------|------------------------|
| PN → PN | AMPA | 0.3 | **6.9** | 1.0 | 5 / 3 (see U20) | 0 | Mahanty & Sah **1998**; Guzman et al. **2016** |
| PN → PN | NMDA | 3.7 | **125** | 0.5 | 2 / 1 (see U20) | 0 | **Weisskopf, Bauer & LeDoux 1999** (Feng ref. [115]) |
| PN → PV/SOM | AMPA | 0.1 | 2.4 | 1.0 | 7 / 2 | 0 | Mahanty & Sah 1998; Guzman et al. 2016 |
| PN → PV/SOM | NMDA | 3.7 | 125 | 0.5 | 7 / 2 | 0 | Weisskopf, Bauer & LeDoux 1999 |
| PV/SOM → PN | GABA-A | 0.5 | **6.8** | 0.6 | 12 / 2 | **−75** | **Galarreta & Hestrin 1997** |
| PV → PV | GABA-A | 0.5 | 6.8 | 0.2 | 20 / 10 | −75 | Galarreta & Hestrin 1997 |

**Do not** attribute the 6.9 ms / 2.4 ms AMPA decays to Mahanty & Sah 1999.

## Synaptic weights (mandatory)

Effective peak conductance = **g × W**, where W is a per-synapse multiplier drawn once at wiring time from `lognormal(mean, var)` (ModelDB `function_ConnectInternal_simplify_online_op.hoc`). Using g alone underestimates every synapse by roughly 2–20×.

- **U20 (open):** Table 3 gives PN→PN AMPA 5/3 and NMDA 2/1. The ModelDB connection file draws one E→E weight `lognormal(2,1)` shared by AMPA and NMDA. Read `BL_main.hoc` to see which connection file it calls. Record the choice in `full_parameters.json`; if it departs from Table 3, also record it in `deviations.md`.
- Weights stay **fixed** in Run 1. The ModelDB `.mod` contains a Ca²⁺-dependent weight-update (LTP) term, which must be disabled or shown to be inactive.
- Draw weights from the seeded RNG stream (see `07_simulation_protocol.md`).

## NMDA Mg²⁺ block (mandatory, dynamic)

```
s(V) = 1 / (1 + 0.33 * exp(-0.06 * V))
```

Source: **Zador et al. 1990** (via Feng). Apply every timestep: `I_NMDA = W · g_NMDA · r_NMDA · STP · s(V) · (V − E_NMDA)`. Listed in `Research/Sources/02_supporting_biological.md`.

## Synaptic delay (Feng Methods + ModelDB)

```
delay = distance_mm / (1 mm/ms) + 0.8 ms + U(−0.1, 0.1) ms + dt
```

The delay is distance-dependent. **It is not a fixed 1.5 ms** (the earlier placeholder). At N=70 in a density-preserving cube (side ≈ 0.19 mm), delays fall at roughly 0.75–1.2 ms. Draw the jitter from the seeded RNG.

## Short-term depression (Feng Table 4)

| Connection | Floor (“D_max”) | d1/d2 | τD1/τD2 (ms) | Experimental basis |
|------------|-----------------|-------|--------------|--------------------|
| FSI → PN | **0.6** | 0.9/0.95 | 40/70 | Woodruff & Sah **2007** (BLA) |
| PN → FSI | **0.7** | 0.9/0.95 | 40/70 | Woodruff & Sah 2007 (BLA) |
| PN → PN | **0.5** | 0.9/0.95 | 40/70 | **Silberberg et al. 2004 (neocortex)** — Feng: no BLA-specific data |

Update rule (ModelDB): release factor = F · D1 · D2. On each presynaptic spike `D1 ← D1·d1` and `D2 ← D2·d2`; between spikes each recovers toward 1 with τD1 / τD2. The listed value is a **floor** on the release factor (it never drops below it), not a maximum. Facilitation F is inactive (F = 1).

- **U21 (open):** the `.mod` defaults pair d1 = 0.95 with τD1 = 40 and d2 = 0.9 with τD2 = 70, the reverse of Table 4. Check the hoc overrides and record what is used.
- The depression state updates on every presynaptic spike. Static weights alone are insufficient.
- **Do not** claim PN→PN depression is BLA-measured, or cite Woodruff & Sah for that row.

## Gap junctions

FSI–FSI gap junctions in 8 % of pairs, coupling coefficient ≈ 0.05 (Woodruff & Sah 2007, via Feng). Include them only if they are implemented from ModelDB `gap.mod`. Otherwise omit them and add an entry to `deviations.md`.

## Implementation notes

- **Synapse formalism:** ModelDB uses the Destexhe 1994 **kinetic** scheme (`AlphaTmax`, `Beta`, `Cdur`), not a dual-exponential. Loading the ModelDB `.mod` files is preferred. A dual-exponential using the Table 3 rise/decay values is an approximation and must go in `deviations.md` (U22).
- If the simulator uses µS, document the conversion (`1 nS = 0.001 µS`) in `full_parameters.json`. ModelDB `.mod` files use µS (`gbar_ampa = 1e-3` µS = 1 nS).
- PN→FSI AMPA uses **2.4 ms** decay, not 6.9 ms.
