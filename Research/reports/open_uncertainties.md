# Open Uncertainties — BLA / Research Track

**Date:** September 2026; updated October 2026 after the consistency pass and verification against Feng’s full text and ModelDB 247968
**Purpose:** Unresolved provenance, implementation, and design questions. Fixed errors are logged in `literature_provenance_audit_sep2026.md` and `consistency_and_source_verification_oct2026.md`.

**Authority while open:** Feng tables + ModelDB + `Simulations/BLA/Research/architecture/`. No invented fill-ins. Temporary choices go in `Simulations/BLA/simulation/deviations.md`.

---

## 1. Literature provenance

| ID | Uncertainty | Status |
|----|-------------|--------|
| **U1** | Feng source for τ_NMDA = 125 ms | **Reopened as a limitation (Oct 2026)**: Feng cites Weisskopf, Bauer & LeDoux 1999 ("[115]" is only the PMC anchor number), but that paper reports **no** NMDA rise/decay constants. Cite 3.7 / 125 ms to Feng 2019 and state that the upstream constants are untraceable. Not blocking: Run 1 uses Feng's synapse files |
| U2 | Guzman 2016 exact Feng ref | **Resolved** — *Science* 353:1117–1123 (CA3) |
| U3 | Full Silberberg 2004 line | **Resolved** — *J Physiol* 556:19–27 |
| U4 | Abatis 2017 DOI / venue | **Resolved** — SfN 2017 poster; no DOI; cite Feng |
| U5 | Primary paper for VIP/CR **percentage** in rat BLA | **Resolved (Oct 2026)**: Vereczki et al. 2021, *J Neurosci* 41:4575–4595 (PMID 33837051), **mouse**: VIP and/or CR cells 29–38 % of GABAergic neurons, CCK basket 7–9 %. Rat anchor: McDonald & Mascagni 2001 (PMID 11516833), CR ≈ 20 % of GABA+ neurons. No rat paper gives the full breakdown. Not used by Run 1 (no VIP/SOM cells) |
| U6 | Exact Galarreta & Hestrin 1997 line | **Resolved** — *J Neurosci* 17:7220–7227 |
| U7 | Mahanty & Sah 1999 role vs Feng Table 3 (1998 + Guzman) | Settled: 1999 is supporting only |

**Settled:** AMPA attribution per Feng Table 3; Destexhe 2001 methods vs 2003 review; Headley Kyriazi; Kim 2013 Learn Mem; Rainnie 1993 title; W&B 1996 = ING; Hermans et al. 2017 (not Ritchey).

---

## 2. Architecture / Run 1

Resolutions below come from the October 2026 Run 1 redesign (`Simulations/BLA/reports/04_run1_redesign_oct2026.md`), based on reading the ModelDB 247968 code.

| ID | Uncertainty | Status / default |
|----|-------------|------------------|
| U8 | FSI OU τ / E from Table 7 | **Resolved**: τ_e 2.728 ms, τ_i 10.49 ms, E_e 0 mV, E_i −75 mV (same as PN). Code amplitudes are 1.21 / 0.12 / 5.73 / 2.64 nS (DEV-002) |
| U9 | Synaptic delay | **Resolved**: not 1.5 ms. Feng: distance / (1 mm/ms) + 0.8 ms + U(−0.1, 0.1) ms + dt |
| U10 | SOM = PV kinetics | **Moot**: Run 1 has no SOM cells (Feng's model has none) |
| U11 | P_SOM_PN = 0.34 | **Moot**: no SOM cells in Run 1 |
| U12 | Heterogeneity | **Resolved**: none added. Feng's templates are used unchanged; variety comes from lognormal weights, delays, noise and random wiring |
| U13 | NEURON vs Brian2 | **Resolved for Run 1**: NEURON 9.0.2, installed 2026-10-14 from the Windows installer (no native-Windows pip wheel). Feng's files are not thread safe, so each run uses one core. The live engine is U26 |
| U14 | Gamma | Diagnostic only. The 1,000-cell network has no spatial structure (DEV-001), so Feng's localised gamma bursts are not expected |
| U20 | Synaptic weight multipliers ("strength") | **Resolved**: `BL_main.hoc` loads `function_ConnectInternal_simplify_online_op.hoc`. E→E draws one lognormal(mean 2, var 1) shared by AMPA and NMDA; E→I (7, 2), I→E (12, 2), I→I (20, 10). Table 3's AMPA 5/3 is not implemented. Code used (DEV-003) |
| U21 | STP d1/d2 pairing | **Resolved**: no `.hoc` overrides. All four files: d1 0.95 @ 40 ms, d2 0.9 @ 70 ms; floors 0.5 (PN→PN) and 0.7 (all others, incl. FSI→PN and FSI→FSI). Code used (DEV-004) |
| U22 | Synapse formalism | **Resolved**: the reference level uses Feng's kinetic-scheme files unchanged. The main level uses an event-driven version of the same kinetic scheme (Destexhe, Mainen & Sejnowski 1994), not a dual-exponential (DEV-007) |
| U23 | Recurrent PN→PN sparsity at N=70 | **Resolved**: not acceptable (0.65 excitatory, ~7 inhibitory inputs per PN vs Feng's 25 and 43). Run 1 uses 1,000 cells wired to Feng's inputs per cell (DEV-001) |
| U24 | Stimulus window length | **Resolved**: 3 s settle, 30 s rest, 2 s threat windows with 2 s before and 4 s after; 5 seeds (`architecture/07`) |
| U25 | Extrinsic drive model | **Resolved**: Feng's own afferent trains with code weights and delays. Threat = afferent rate × 2, 4, 8 (DEV-005) |
| **U26** | Live engine: simulator and cell detail | **Open**, informed by measurements (2026-10-14): Feng's PN costs 5.2 µs per segment per step and each Feng synapse 1.0–1.4 µs; Feng's files cannot multithread. Even the main level's one-piece PN (~5 µs per cell per step) is far from real time at hundreds of cells, so the live engine needs cheaper cell code, event-driven synapses and several cores, or fewer neurons. Decide after Phase 0 |
| **U27** | Threat pathway | **Open, later**: Run 1 uses "more afferent input"; a dedicated thalamic threat input is a later refinement |
| **U28** | PN-A single-cell firing | **Open**: Feng's unchanged PN-A fires one spike and then stays silent for about 2 s under steady current (0.2–1.5 nA; preliminary, 2026-10-14). Consistent with its very large sAHP (50 mS/cm²) and 1 s Ca²⁺ pool, but check against Feng's (and Kim's) description of type-A adaptation before Gate 2 |

---

## 3. Design

| ID | Uncertainty |
|----|-------------|
| **U15** | Mid-generation LLM state-injection mechanism |
| **U16** | Computational definition of face `neutral` |
| **U17** | Suppression-gap *k* and prefrontal fatigue law |
| **U18** | Scaling for non-BLA regions |
| U19 | Whether 50/12/8 stays after Feng-faithful Run 1. **Superseded (Oct 2026)**: Run 1 uses Feng's 640 / 260 / 100. The BLA size in the live network depends on U26 |

---

## 4. From 2026 paper batch (documented, not Run 1 params)

- SOM as suppression readout; valence competition via INs; experience-dependent projection routing; astrocyte tonic arousal. See `Simulations/BLA/Research/12_implications_for_simulation.md` and `Research/Sources/08_bla_2026_paper_batch.md`.

---

## 5. Conflicting secondary reports

Older audits that say “use Destexhe 2003 for OU” or “Mahanty 1999 for 6.9 ms AMPA” lose to **Feng primary text**. See `literature_provenance_audit_sep2026.md`.

---

*Related:* `literature_provenance_audit_sep2026.md` · `consistency_and_source_verification_oct2026.md` · `Simulations/BLA/reports/03_paper_batch_2026_applied.md` · `Simulations/BLA/Research/architecture/12_sources_map.md`
