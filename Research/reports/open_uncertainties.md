# Open Uncertainties — BLA / Research Track

**Date:** September 2026 (updated after 2026 paper batch)  
**Purpose:** Unresolved provenance, implementation, and design questions. Known fixed errors live in `ACCURACY_VERIFICATION_CORRECTIONS.md`.

**Authority while open:** Feng tables + `architecture/`. No invented fill-ins. Temporary choices → `simulation/deviations.md`.

---

## 1. Literature provenance

| ID | Uncertainty | Status |
|----|-------------|--------|
| **U1** | Feng footnote for τ_NMDA = 125 ms | **Open** |
| **U2** | Guzman 2016 exact Feng ref (CA3 paper is best match) | **Open** |
| **U3** | Full Silberberg 2004 bibliographic line from Feng | **Open** |
| **U4** | Full Abatis 2017 DOI / venue | **Open** |
| **U5** | Primary paper for VIP/CR **percentage** in rat BLA | **Still open** — Báldi 2025 / Perumal & Sah 2021 confirm functional four-subtype taxonomy, not a definitive VIP % count |
| **U6** | Exact Galarreta & Hestrin 1997 line as Feng lists it | **Open** |
| **U7** | Mahanty & Sah 1999 role vs Feng Table 3 (1998+Guzman) | Settled stance: 1999 supporting only unless Feng says otherwise |

**Settled:** AMPA attribution per Feng Table 3; Destexhe 2001 methods vs 2003 review; Headley Kyriazi; Kim 2013 Learn Mem; Rainnie 1993 title; W&B 1996 = ING.

---

## 2. Architecture / Run 1

| ID | Uncertainty | Default |
|----|-------------|--------|
| **U8** | FSI OU τ / E from Table 7 ModelDB | Copy into `full_parameters.json` before run |
| **U9** | Delay 1.5 ms vs ModelDB per-type | 1.5 ms unless ModelDB differs |
| **U10** | SOM = PV kinetics | Only with `deviations.md` |
| **U11** | P_SOM_PN = 0.34 | Approximation → `deviations.md` |
| **U12** | Passive params / heterogeneity | Source templates; else 0% extra spread |
| **U13** | NEURON vs Brian2 | NEURON preferred |
| **U14** | Gamma at N=70 | Diagnostic only |

---

## 3. Design

| ID | Uncertainty |
|----|-------------|
| **U15** | Mid-generation LLM state injection mechanism |
| **U16** | Computational definition of face `neutral` |
| **U17** | Suppression-gap *k* and prefrontal fatigue law |
| **U18** | Scaling for non-BLA regions |
| **U19** | Whether 50/12/8 stays after Feng-faithful Run 1 |

---

## 4. From 2026 paper batch (documented, not Run 1 params)

- SOM as suppression readout; valence competition via INs; experience-dependent projection routing; astrocyte tonic arousal — see `12_implications_for_simulation.md` and `08_bla_2026_paper_batch.md`.

---

## 5. Conflicting secondary reports

Older audits that say “use Destexhe 2003 for OU” or “Mahanty 1999 for 6.9 ms AMPA” lose to **Feng primary text**. See `literature_provenance_audit_sep2026.md`.

---

*Related:* `ACCURACY_VERIFICATION_CORRECTIONS.md` · `bla_2026_paper_batch_applied.md` · `architecture/12_sources_map.md`
