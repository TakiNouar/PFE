# BLA Literature — Strict Verification Corrections

**Date:** September 2026 (open items resolved October 2026)  
**Scope:** `Research/Sources/` and `Research/Development/02_biophysical_substrate.md`  
**Method:** Citations and numeric parameters checked against primary source text (Feng et al. 2019 Methods/Tables 1–7; Kim 2013; supporting papers), not only against prior repo “corrected” versions.

---

## Verdict

An earlier accuracy pass fixed some errors but left or introduced provenance mistakes. **None change the isolated-BLA kinetic targets** (AMPA 6.9 ms, NMDA 125 ms, E_GABA −75 mV, etc.). All four citation fixes below are applied so the thesis can defend every number.

Clean **Run 1** (not “Run 6”) uses the same numeric targets with corrected upstream attribution. See `Simulations/BLA/reports/00_clean_restart_policy.md`.

---

## Correction 1 — AMPA kinetics attribution

**Wrong:** Mahanty & Sah **1999** as source of 6.9 ms / 2.4 ms decays.  
**Feng Table 3 actually cites:** Mahanty & Sah **1998** + **Guzman et al. 2016** for both PN→PN and PN→FSI AMPA.

**Applied:** Restored 1998 + Guzman. Mahanty & Sah 1999 kept only as general LA glutamatergic support if listed. Guzman SJ, Schlögl A, Frotscher M, Jonas P (2016) *Science* 353:1117–1123 added. **Confirmed Oct 2026** against Feng’s reference list. Caveat: it is a CA3 paper, not amygdala.

---

## Correction 2 — GABA-A upstream missing

**Feng Table 3 cites:** Galarreta & Hestrin **1997** for FSI→PN / FSI→FSI 0.5 / 6.8 ms.  
**Applied:** Entry added under primary sources.

---

## Correction 3 — STP values and sources

| Connection | D_max | Source |
|------------|-------|--------|
| FSI→PN | **0.6** | Woodruff & Sah 2007 (BLA) |
| PN→FSI | **0.7** | Woodruff & Sah 2007 (BLA) |
| PN→PN | **0.5** | Silberberg et al. 2004 (**neocortex** — Feng’s explicit approximation) |

All: d1/d2 = 0.9/0.95, τ = 40/70 ms.

**Applied** in `02_biophysical_substrate.md`, `01_primary_bla_references.md`, architecture STP notes already required Table 4 fidelity.

---

## Correction 4 — Destexhe noise model year

**Feng Methods cite:** Destexhe et al. **2001** (*Neuroscience* 107:13–24; Fellous & Sejnowski co-authors) — point-conductance / OU formalism.  
**Not:** Destexhe, Rudolph & Paré **2003** *Nat Rev Neurosci* (different paper, review).

**Applied:** 2001 as methods source; 2003 as conceptual background only.

---

## Item 6 — Population inconsistency (resolved for Run 1)

150 Pyr / 112 PV / 108 SOM appeared in archived notes beside 50/12/8. Different E/I ratios; not interchangeable.

**Resolution:** Clean Run 1 default = **50 / 12 / 8** only (`architecture/02_population_structure.md`). 150/112/108 is historical archive text only.

---

## Verified accurate (no change)

Feng 2019 identity/DOI/ModelDB 247968, scale 27k, composition 64/26/10; Table 3 kinetics numbers; Mg block → Zador 1990; connectivity % and distance bands; Kim 2013 DOI / ModelDB 150288; Headley 2021 (Kyriazi); Cattani 2024.

---

## Formerly open — resolved October 2026

Checked against Feng’s full text and reference list (PMC6361623). Details in `consistency_and_source_verification_oct2026.md`.

1. **τ_NMDA = 125 ms source** — Feng Table 3 cites **Weisskopf, Bauer & LeDoux 1999** (ref. [115]). The earlier hedge is removed.
2. **Guzman 2016** — confirmed as Guzman, Schlögl, Frotscher & Jonas, *Science* 353:1117–1123 (CA3).
3. **Silberberg 2004** — *J Physiol* 556:19–27, “Synaptic dynamics control the timing of neuronal excitation in the activated neocortical microcircuit.”
4. **Abatis 2017** — an SfN 2017 **poster**, so no DOI exists. Cite Feng for the numbers.

*This audit absorbed the former `Research/Sources/ACCURACY_VERIFICATION_CORRECTIONS.md`, which duplicated it and has been removed.*
