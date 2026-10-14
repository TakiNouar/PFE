# 12 — Sources Map (Architecture ↔ Sources)

**Authority:** every number in this architecture resolves to a row below. Feng's paper and code are documented in `Research/Sources/01_primary_bla_references.md`; code values were read from the ModelDB 247968 GitHub mirror in October 2026.

If a value is not here, implementation **stops** and the gap goes to `Simulations/BLA/simulation/deviations.md`.

Source keys (use them in `run1.json`): **F19** = Feng et al. 2019 paper; **F19code** = ModelDB 247968 file; **W&S07** = Woodruff & Sah 2007; **PROTO** = our protocol choice (always also in `deviations.md`).

---

## Values inside Feng's files (we do not set these)

| Item | Value used | Key | Where documented |
|---|---|---|---|
| Cell templates, channels, geometry | `Cell_A`, `Cell_C`, FSI template | F19code | `03` |
| Synapse kinetics, Mg²⁺ block, depression | four `*_STFD*.mod` files | F19code | `04` |
| Noise τ and reversal | 2.728 / 10.49 ms; 0 / −75 mV | F19code (mod defaults) | `06` |

## Values we set (copied from Feng's code or paper)

| Item | Value | Key | Spec file |
|---|---|---|---|
| Cell shares | 64 / 26 / 10 % | F19 | `02` |
| Reduced size | 1,000 cells | F19 ("1,000-neuron reduced model"); Nair-lab `feng_homogenous` | `02` |
| Density, minimum spacing | 9,840 cells/mm³; 25 µm | F19 | `02` |
| Inputs per cell | PN→PN 24.98, FSI→PN 42.6, PN→FSI 214.8, FSI→FSI 21.6 | F19 (Results) | `05` |
| Gap-junction pairs | 8 % of FSI pairs | F19 ← W&S07 | `05` |
| Gap-junction conductance | `HalfGap`, 5,000 MΩ (0.2 nS) each way | F19code (`function_ConnectInternal_gj_simplify.hoc`) | `04` |
| Weights PN→PN | lognormal(2, 1), shared AMPA/NMDA | F19code (`function_ConnectInternal_simplify_online_op.hoc` line 24) | `04` |
| Weights PN→FSI / FSI→PN / FSI→FSI | lognormal(7, 2) / (12, 2) / (20, 10) | F19code (same file); match F19 Table 3 | `04` |
| Internal delay | d (mm) × 1 ms/mm + 0.8 + U(−0.1, 0.1) + dt | F19 Methods + F19code | `05` |
| Noise PN | g_e0 3.2, σ_e 3, g_i0 21, σ_i 8 nS | F19 Table 7 = F19code | `06` |
| Noise FSI | g_e0 1.21, σ_e 0.12, g_i0 5.73, σ_i 2.64 nS | F19code (`BL_main.hoc` 305–318) | `06` |
| Afferent trains | Feng's recorded-cell surrogates, `input/` | F19code ← Headley et al. 2015 | `06` |
| Afferent fan-out | 40 PNs per train; 2.97 trains per PN; 3.4 per FSI | F19 | `06` |
| Afferent weights | PN lognormal(9, 0.05); FSI lognormal(2, 0.2) | F19code (`function_ConnectInputs_invivo_op.hoc`) | `06` |
| Afferent delay | U(0.5, 1) ms | F19code (same file) | `06` |
| dt, temperature, v_init | 0.05 ms, 31 °C, −70 mV | F19 + F19code (`BL_main.hoc`) | `07` |
| Seeds per condition | 5 | F19 ("averaging five network model runs") | `07` |

## Main-level reductions (each also in `deviations.md`)

| Item | Value / method | Key | Spec file |
|---|---|---|---|
| Two-piece PN | Feng's soma copied exactly; Feng's two dendrites merged into one compartment (area and channel totals summed); coupling = their half-length axial resistances in parallel. No fitted values | F19code + PROTO (DEV-006) | `03` |
| Event-driven synapses | Exact kinetic-synapse method of Destexhe, Mainen & Sejnowski 1994, *Neural Comput* 6:14–18 (the paper Feng cites), with Feng's code constants | F19code + Destexhe 1994 + PROTO (DEV-007) | `04` |

## Protocol choices (ours; each also in `deviations.md` where it departs from Feng)

| Item | Value | Key |
|---|---|---|
| Distance-independent wiring at p = K / n_pre | `05` | PROTO (DEV-001) |
| Threat = afferent rate × D, D = 2, 4, 8 | `06` | PROTO (DEV-005) |
| Epoch lengths, trial counts | `07` | PROTO |
| Synchrony guard < 0.5 | `10` | PROTO (archive lesson) |
| Reduction tolerances (Gates R1, R2) | `10` | PROTO |
| 200-cell reference size | `02` | PROTO (chosen from measured cost) |

## Gate reference values (literature)

| Gate value | Source |
|---|---|
| PN resting rate 0.2–3 Hz | Amir et al. 2018, *Neuron* (0.21 / 1.55 Hz; PMC5809002); Repa et al. 2001 (LA mean 2.7 Hz) |
| FSI resting rate 10–30 Hz | Paré & Gaudreau 1996 (10–15 Hz); Amir et al. 2018 (22–27 Hz) |
| PN Vrest −70.3 mV, Rin ~140 MΩ, τm ~30 ms | F19 Methods (text) |
| Gap coupling ≈ 0.05 | W&S07 |

## Upstream citations Feng gives for values inside his files

These are cited as "Feng et al. 2019, citing …", never as direct sources of the numbers.

| Value | Feng cites | Caveat |
|---|---|---|
| AMPA kinetics | Mahanty & Sah 1998; Guzman et al. 2016 | Guzman is hippocampal CA3 |
| NMDA 3.7 / 125 ms | Weisskopf, Bauer & LeDoux 1999 | That paper reports **no** NMDA time constants (U1); cite the values to Feng |
| GABA-A kinetics | Galarreta & Hestrin 1997 | Neocortex; reports 0.46 / 7.5 ms |
| FSI ↔ PN depression | W&S07 | BLA, mouse |
| PN → PN depression | Silberberg et al. 2004 | Neocortex; Feng: no BLA data |
| Mg²⁺ block | Zador et al. 1990 | — |
| Noise formalism | Destexhe, Rudolph, Fellous & Sejnowski 2001 | Not the 2003 review |

## Forbidden substitutions

| Do not use | Instead |
|---|---|
| Any edited copy of a Feng `.mod` or cell `.hoc` | The unchanged file (hash-checked) |
| Kim 2013 / ModelDB 150288 principal-cell parameters | Feng 247968 `Cell_A` / `Cell_C` |
| Paper value where Feng's code differs, unlogged | Code value + `deviations.md` |
| `gap.mod` | `halfgap.mod` |
| Invented Poisson rates for afferents | Feng's train files |
| Mahanty & Sah 1999 as the AMPA source | Feng, citing Mahanty & Sah 1998 + Guzman 2016 |
| Destexhe 2003 as the noise-methods paper | Destexhe et al. 2001 |
| Abatis 2017 as a standalone citation | Feng et al. 2019 (Abatis is an SfN poster) |
