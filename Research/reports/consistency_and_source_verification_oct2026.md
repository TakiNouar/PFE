# Consistency Pass and Source Verification — October 2026

**Date:** 2026-10-10
**Scope:** Whole repository.
**Method:**
1. Every file was read and cross-checked for contradictions.
2. Open provenance items were checked against the **Feng et al. 2019 full text and reference list** (PMC6361623).
3. Key mechanisms were checked against the **ModelDB 247968 code** (github.com/ModelDBRepository/247968): `pyrD2pyrD_STFD_new.mod`, `function_ConnectTwoCells.hoc`, `function_ConnectInternal_simplify_online_op.hoc`.
4. One author attribution was checked by web search.

---

## 1. Repository reorganisation

| Change | Reason |
|--------|--------|
| `Simulation tests/` → `Simulations/`; `Neurons Connected/` → `Neurons_Connected/` | Spaces in paths break NEURON `nrnivmodl` |
| `Research/reports/00_`–`05_`, `BLA_isolated_simulation_report.md`, `BLA_isolated_simulation_report_CORRECTIONS.md` → merged into `Simulations/BLA/reports/test_run_1/` | They duplicated the archive and had drifted from it. Unique details (full Run 3 table, Run 1 units, GLOBAL_SEED, Run 5 syn/CV) were kept. The established-results table became `test_run_1/07_established_results_and_conclusion.md` |
| Full-network history → `Simulations/Neurons_Connected/reports/full_network_attempts_1_to_4.md` | Multi-region material belongs with multi-region work |
| `Research/reports/cell_type_taxonomy_citation_check.md` → `Simulations/BLA/reports/02_cell_type_taxonomy_citation_check.md` | BLA-specific |
| `Research/reports/bla_2026_paper_batch_applied.md` → `Simulations/BLA/reports/03_paper_batch_2026_applied.md` | BLA-specific |
| `Research/Sources/sources.md` removed | Monolithic copy that had drifted (still said Weisskopf “not confirmed”). `Sources/README.md` is now the index |
| `Research/Sources/ACCURACY_VERIFICATION_CORRECTIONS.md` merged into `literature_provenance_audit_sep2026.md` | Duplicate log; `Sources/` now holds literature only |

## 2. Contradictions fixed

| # | Contradiction | Fix |
|---|---------------|-----|
| 1 | NMDA τ = 125 ms source marked “confirmed” in some files and “open/unconfirmed” in seven others | Confirmed everywhere: Weisskopf, Bauer & LeDoux 1999 (Feng ref. [115]) |
| 2 | Blueprint roadmap and Sources said “Run 6” and “BLA done”, contradicting the clean-restart policy | Now Run 1; the first campaign is archived as failed |
| 3 | Blueprint Q[2] and §19 called 50/12/8 “validated with literature-grounded parameters” and recommended fixed K≈3, which the architecture forbids | Reworded: 50/12/8 is an unvalidated default; fixed-K is an anti-pattern; the collapse explanation is a hypothesis to re-test |
| 4 | Status block said the BLA runs established “validated baseline parameters” | Reworded to match the archive |
| 5 | `test_run_1/05_lessons` named 150/112/108 as the target population | Now 50/12/8 per `architecture/02` |
| 6 | Archive log recorded “Destexhe 2001 → 2003” as a correction, but that change was itself wrong and later reverted | Log corrected; 2001 is the methods source |
| 7 | `07_reading_priority` listed Destexhe 2003 for the noise model and split Mahanty 1998/1999 between FSI and PN | Fixed per Feng Table 3 |
| 8 | Several files applied D_max ≈ 0.6 to all synapses | Per-connection 0.6 / 0.7 / 0.5 |
| 9 | Sources said “port to Brian2”, but the architecture says NEURON is preferred | Sources now match the architecture; the decision remains open (U13) |
| 10 | The suppression ratio was defined as on/off (≈ 0.51), yet Gate 3 required it to be “> 1” | Redefined as off/on (> 1 means inhibition works), applied consistently in `08_metrics` and `10_gates` |
| 11 | Blueprint said a 0.1 ms timestep; Feng and the architecture use 0.05 ms | 0.05 ms |
| 12 | Blueprint §5.2.3 said the mesh covers all ten structures “including PAG”, while §5.2.4 defers PAG | §5.2.3 now covers nine; PAG deferred |
| 13 | Blueprint said PAG was never instantiated, but the full-network attempts included it | PAG status reworded |
| 14 | `09_code_module_map` used `parameters.json`; everything else uses `full_parameters.json` | Unified on `full_parameters.json` |
| 15 | Clean-restart policy pointed to `Research/architecture/11_anti_patterns.md`, a path that does not exist | Corrected path |

## 3. Source verification results

### Resolved open items

| ID | Finding |
|----|---------|
| U1 | Feng Table 3 cites Weisskopf et al. 1999 (ref. [115]) for NMDA 3.7 / 125 ms |
| U2 | Guzman et al. 2016 = *Science* 353:1117–1123 (CA3), confirmed in Feng’s reference list |
| U3 | Silberberg, Wu & Markram 2004, *J Physiol* 556:19–27, “Synaptic dynamics control the timing of neuronal excitation in the activated neocortical microcircuit” |
| U4 | Abatis et al. 2017 is an **SfN poster**, so no DOI exists. PN→PN distance bands must be cited via Feng 2019; this is a thesis limitation |
| U6 | Galarreta & Hestrin 1997 = “Properties of GABAA receptors underlying inhibitory synaptic currents in neocortical pyramidal neurons”, *J Neurosci* 17:7220–7227. The earlier placeholder title was wrong |
| U8 | FSI noise: τ_e 2.728 ms, τ_i 10.49 ms, E_e 0 mV, E_i −75 mV. PN τ_e is 2.728 ms (was rounded to 2.73) |
| U9 | Delay = distance/(1 mm/ms) + 0.8 ms + U(−0.1, 0.1) ms + dt. **The architecture’s fixed 1.5 ms was wrong** |

### Citation errors corrected

- `04_fear_memory_dynamics.md`: the *Cerebral Cortex* 2017 paper is by **Hermans EJ, Kanen JW, et al.**, 27(5):3028–3041, not “Ritchey M”.
- Added full lines and DOIs: Woodruff & Sah 2007 (27:553–563), Zador 1990 (87:6718–6722), Weisskopf 1999 DOI.

### Omissions in the architecture spec (now added)

| Item | Finding | Where |
|------|---------|-------|
| Synaptic weight multipliers | Feng Table 3 has a “strength” column (mean/var) that the spec had dropped. In ModelDB it is a per-synapse lognormal `initW` multiplying the conductance (roughly 2–20×) | `architecture/04`, `05`, `12` |
| Synapse formalism | ModelDB uses the Destexhe 1994 kinetic scheme (AlphaTmax/Beta/Cdur), not a dual-exponential | `architecture/04`, U22 |
| STP semantics | “D_max” is a floor on the release factor F·D1·D2; facilitation is inactive | `architecture/04` |
| Gap junctions | 8 % of FSI pairs, coupling ≈ 0.05 | `architecture/04`, `05` |
| Interneuron distance limit | ~300 µm | `architecture/05` |
| Extrinsic input | Feng uses Poisson surrogate trains (≈ 3 per PN); Run 1’s OU stimulus is a protocol departure | `architecture/06`, U25 |
| Passive parameters | Verified (PN 55 kΩ·cm² / 2.4 µF/cm² / 150 Ω·cm / −75 mV; FSI 20 / 1.0 / 150) | `architecture/03` |

### New open items (paper vs code)

- **U20:** Table 3 gives PN→PN AMPA strength 5/3, while ModelDB draws one E→E weight `lognormal(2,1)` shared by AMPA and NMDA.
- **U21:** Table 4 gives d1/d2 = 0.9/0.95, while the `.mod` defaults are d1 = 0.95 (τ 40) and d2 = 0.9 (τ 70).

Both must be resolved by reading `BL_main.hoc` before transcribing `full_parameters.json`.

### New design risks recorded

- **U23:** At N=70 with Feng density, PN→PN recurrence is estimated at < 1 input per PN.
- **U24:** A 100 ms stimulus gives 1–4 spikes per cell, which makes CV/active-fraction gates weak.

## 4. Not changed

- All numeric kinetic targets (AMPA 6.9 ms, NMDA 125 ms, E_GABA −75 mV, STP floors, connectivity bands, PN noise) were verified as correct.
- Historical records (`blueprint_corrections_v2.5.md`, run narratives) were annotated rather than rewritten.
- Title strings marked “confirm exact title” for the McDonald / Mascagni papers were **not** verified in this pass.

## Sources consulted

- Feng et al. 2019, full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC6361623/
- ModelDB 247968 code: https://github.com/ModelDBRepository/247968
- Hermans et al. 2017 attribution: https://arxiv.org/pdf/2011.00257 (reference list) and https://neuroscience.cam.ac.uk/publications/persistence-of-amygdalahippocampal-connectivity-and-multivoxel-correlation-structures-during-awake-rest-after-fear-learning-predicts-longterm-expression-of-fear
