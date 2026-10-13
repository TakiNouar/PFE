# 04 — Synaptic Models

## Rule

Use Feng's four synapse files from ModelDB 247968 **unchanged**. They already contain the receptor kinetics, the NMDA Mg²⁺ block and the short-term depression. We only choose **which cells connect** (`05_connectivity.md`) and draw each connection's **weight** and **delay**, the way Feng's wiring code does.

Where Feng's paper and code differ, the **code** is used, because the code produced his published results. Each difference is logged in `Simulations/BLA/simulation/deviations.md`. Values below were read from the code in October 2026 (`Research/Sources/01_primary_bla_references.md`).

## Pathways

| Pathway | Feng file → mechanism | Placed on | Receptors | Peak g | Weight W per connection | Depression floor |
|---|---|---|---|---|---|---|
| PN → PN | `pyrD2pyrD_STFD_new.mod` → `pyrD2pyrD_STFD` | target `dend(0.9)` | AMPA + NMDA | 1 nS + 0.5 nS | lognormal(2, 1), one W for both AMPA and NMDA | 0.5 |
| PN → FSI | `pyrD2interD_STFD.mod` → `pyrD2interD_STFD` | target `dend(0.9)` | AMPA + NMDA | 1 nS + 0.5 nS | lognormal(7, 2) | 0.7 |
| FSI → PN | `interD2pyrD_STFD_new.mod` → `interD2pyrD_STFD` | target soma | GABA-A | 0.6 nS | lognormal(12, 2) | 0.7 |
| FSI → FSI | `interD2interD_STFD_new.mod` → `interD2interD_STFD` | target soma | GABA-A | 0.2 nS | lognormal(20, 10) | 0.7 |

Afferent-input synapses reuse the first two mechanisms, with their own weights (see `06_noise_and_drive.md`).

**Weights.** Effective conductance = g × W. NEURON's `Random.lognormal(a, b)` takes the **mean** a and **variance** b of W itself, which is also how Feng's Table 3 lists them. Draw W once per connection, from the seeded stream (`07`). Weights never change during a run.

## Kinetics (inside the files; listed for reference)

Feng's synapses use the Destexhe 1994 kinetic scheme (a transmitter pulse of length `Cdur` opens receptors at rate `AlphaTmax` and they close at rate `Beta`). Rise ≈ 1 / (AlphaTmax + Beta), decay = 1 / Beta.

| Receptor (pathway) | Rise / decay in code (ms) | Paper Table 3 (ms) | Same? |
|---|---|---|---|
| AMPA (PN→PN) | 0.25 / 7.0 | 0.3 / 6.9 | rounding |
| NMDA (both) | 3.65 / 125 | 3.7 / 125 | yes |
| AMPA (PN→FSI) | 0.095 / 2.4 | 0.1 / 2.4 | yes |
| GABA-A (FSI→PN) | **0.60 / 7.14** | 0.5 / 6.8 | **no** (DEV-003) |
| GABA-A (FSI→FSI) | 0.50 / 6.80 | 0.5 / 6.8 | yes |

Reversal potentials: AMPA and NMDA 0 mV, GABA-A −75 mV.

**NMDA Mg²⁺ block** is computed by the file at every time step: s(V) = 1 / (1 + 0.33·exp(−0.06·V)) (Zador et al. 1990, via Feng). In plain terms: NMDA only lets current through when the receiving cell is already depolarised.

## Short-term depression (inside the files)

Each spike weakens the synapse a little; it recovers between spikes. The release factor is D1 × D2. After each presynaptic spike D1 is multiplied by d1 and D2 by d2; each recovers towards 1 with its own time constant. The factor never falls below the **floor**.

| Setting | Code value (all four files) | Paper Table 4 |
|---|---|---|
| d1, τD1 | 0.95, 40 ms | 0.9, 40 ms |
| d2, τD2 | 0.9, 70 ms | 0.95, 70 ms |
| Floor PN→PN | 0.5 | 0.5 |
| Floor PN→FSI | 0.7 | 0.7 |
| Floor FSI→PN | **0.7** | **0.6** |
| Floor FSI→FSI | **0.7** | not listed |

The swapped d1/d2 pairing changes the second spike's strength by about 1 % (DEV-004). Facilitation stays at 1 in all files.

**Long-term plasticity:** the files contain a Ca²⁺-dependent weight-update term, multiplied by 1e-12 so it has no effect (drift < 1e-8 over 165 s). Feng: "Our model did not have long-term synaptic plasticity." It stays as shipped; Gate 0 checks that weights are unchanged after a run.

## Gap junctions (FSI ↔ FSI)

- 8 % of FSI pairs are electrically coupled (Woodruff & Sah 2007, via Feng).
- Mechanism: `HalfGap` from `halfgap.mod`, one half in each cell's soma, resistance 5,000 MΩ, i.e. **0.2 nS** each way. Not `gap.mod`, which Feng's network does not load.
- Connect the two halves as Feng's `function_ConnectInternal_gj_simplify.hoc` does.
- The coupling coefficient (≈ 0.05 in Woodruff & Sah) is an **outcome** to measure in Gate 2, not a setting.

## Units

Feng's files use µS (`gbar = 1e-3 µS` = 1 nS), mV and ms. This spec quotes nS where Feng's paper does.
