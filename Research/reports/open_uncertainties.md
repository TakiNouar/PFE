# Open Uncertainties — BLA / Research Track

**Date:** September 2026; updated October 2026 after the consistency pass and verification against Feng’s full text and ModelDB 247968
**Purpose:** Unresolved provenance, implementation, and design questions. Fixed errors are logged in `literature_provenance_audit_sep2026.md` and `consistency_and_source_verification_oct2026.md`.

**Authority while open:** Feng tables + ModelDB + `Simulations/BLA/Research/architecture/`. No invented fill-ins. Temporary choices go in `Simulations/BLA/simulation/deviations.md`.

---

## 1. Literature provenance

| ID | Uncertainty | Status |
|----|-------------|--------|
| U1 | Feng source for τ_NMDA = 125 ms | **Resolved** — Weisskopf, Bauer & LeDoux 1999 (Feng ref. [115]) |
| U2 | Guzman 2016 exact Feng ref | **Resolved** — *Science* 353:1117–1123 (CA3) |
| U3 | Full Silberberg 2004 line | **Resolved** — *J Physiol* 556:19–27 |
| U4 | Abatis 2017 DOI / venue | **Resolved** — SfN 2017 poster; no DOI; cite Feng |
| **U5** | Primary paper for VIP/CR **percentage** in rat BLA | **Still open**. Báldi 2025 / Perumal & Sah 2021 confirm the functional four-subtype taxonomy, not a definitive VIP % count |
| U6 | Exact Galarreta & Hestrin 1997 line | **Resolved** — *J Neurosci* 17:7220–7227 |
| U7 | Mahanty & Sah 1999 role vs Feng Table 3 (1998 + Guzman) | Settled: 1999 is supporting only |

**Settled:** AMPA attribution per Feng Table 3; Destexhe 2001 methods vs 2003 review; Headley Kyriazi; Kim 2013 Learn Mem; Rainnie 1993 title; W&B 1996 = ING; Hermans et al. 2017 (not Ritchey).

---

## 2. Architecture / Run 1

| ID | Uncertainty | Status / default |
|----|-------------|------------------|
| U8 | FSI OU τ / E from Table 7 | **Resolved** — τ_e 2.728 ms, τ_i 10.49 ms, E_e 0 mV, E_i −75 mV (same as PN) |
| U9 | Synaptic delay | **Resolved** — not 1.5 ms. Feng: distance / (1 mm/ms) + 0.8 ms + U(−0.1, 0.1) ms + dt |
| **U10** | SOM = PV kinetics | Allowed only with a `deviations.md` entry |
| **U11** | P_SOM_PN = 0.34 | Approximation; goes in `deviations.md` |
| **U12** | Heterogeneity | Passive values verified (Feng Methods). Feng gives no passive ranges, so 0 % extra spread. Synaptic weights *are* heterogeneous (lognormal, see U20) |
| **U13** | NEURON vs Brian2 | **Open decision** — NEURON preferred (strict path) |
| **U14** | Gamma at N=70 | Diagnostic only |
| **U20** | Synaptic weight multipliers (“strength”) | Paper Table 3: PN→PN AMPA 5/3, NMDA 2/1, PN→FSI 7/2, FSI→PN 12/2, FSI→FSI 20/10. ModelDB `function_ConnectInternal_simplify_online_op.hoc` draws E→E `lognormal(2,1)` shared by AMPA+NMDA. Confirm which version `BL_main.hoc` uses |
| **U21** | STP d1/d2 pairing | Table 4: d1/d2 = 0.9/0.95 with τ 40/70 ms. `pyrD2pyrD_STFD_new.mod` defaults: d1 = 0.95 (τD1 40), d2 = 0.9 (τD2 70). Check hoc overrides; record the value used |
| **U22** | Synapse formalism | ModelDB uses the Destexhe 1994 kinetic scheme; dual-exponential is an approximation → `deviations.md` if used |
| **U23** | Recurrent PN→PN sparsity at N=70 | With density preserved (cube ≈ 190 µm) and 0.5–3 % probabilities, the estimate is < 1 PN→PN input per PN at 1.0× and ≈ 1.6 at 3.0×. Recurrent effects and Gate 5 diagnostics may be near-null. Report realized counts; decide whether this is acceptable before interpreting results |
| **U24** | Stimulus window length | A 100 ms stimulus at 10–40 Hz yields 1–4 spikes per cell, so ISI-CV is statistically weak and the “>5 Hz” active criterion means ≥ 1 spike. The window is also short relative to NMDA (125 ms) and sAHP timescales. Consider a longer stimulus window before locking Gate 2 |
| **U25** | Extrinsic drive model | Feng drives with Poisson surrogate spike trains (≈ 3 afferents per PN); Run 1 uses private OU drive. This is a protocol choice and must be stated as a departure from Feng’s input model |

---

## 3. Design

| ID | Uncertainty |
|----|-------------|
| **U15** | Mid-generation LLM state-injection mechanism |
| **U16** | Computational definition of face `neutral` |
| **U17** | Suppression-gap *k* and prefrontal fatigue law |
| **U18** | Scaling for non-BLA regions |
| **U19** | Whether 50/12/8 stays after Feng-faithful Run 1. The archived runs used wrong kinetics, so 50/12/8 is a default, **not** a validated size |

---

## 4. From 2026 paper batch (documented, not Run 1 params)

- SOM as suppression readout; valence competition via INs; experience-dependent projection routing; astrocyte tonic arousal. See `Simulations/BLA/Research/12_implications_for_simulation.md` and `Research/Sources/08_bla_2026_paper_batch.md`.

---

## 5. Conflicting secondary reports

Older audits that say “use Destexhe 2003 for OU” or “Mahanty 1999 for 6.9 ms AMPA” lose to **Feng primary text**. See `literature_provenance_audit_sep2026.md`.

---

*Related:* `literature_provenance_audit_sep2026.md` · `consistency_and_source_verification_oct2026.md` · `Simulations/BLA/reports/03_paper_batch_2026_applied.md` · `Simulations/BLA/Research/architecture/12_sources_map.md`
