# BLA Research Dossier — Cell-Type Taxonomy Citation Check

**Date:** September 2026  
**Scope:** `Simulation tests/BLA/Research/02_cell_types.md`  
**Method:** Interneuron percentages checked against McDonald/Mascagni primary literature.

---

## Confirmed accurate

| Claim | Status |
|-------|--------|
| PV ~40–50% of INs | Matches McDonald & Betette (2001), *Neuroscience* 102:413–425 (“∼50% of the interneuronal population”) |
| SOM+/SST ~15–20% | Close to McDonald & Mascagni (2002), *Brain Res* 943:237–244 (11–18% of GABAergic population); top of range slightly generous |
| ~25% of LA PNs recruited into fear memory trace | Matches Kim et al. 2013 text (citing Quirk 1995, Repa 2001, Rumpel 2005) |
| Four subtypes PV / SOM / VIP / CCK as standard rat BLA taxonomy | Confirmed across McDonald/Mascagni series |

---

## Finding (fixed)

**Problem:** The taxonomy table was attributed to a single blanket phrase: “Mascagni & McDonald 2003 and later reviews.”  
Mascagni & McDonald (2003), *Brain Res* 976:171–184, is **CCK-specific** and is not the source for PV or SOM percentages.

**Correction applied in `02_cell_types.md`:**

| Table row | Citation |
|-----------|----------|
| PV+ | McDonald & Betette (2001) |
| SOM+/SST | McDonald & Mascagni (2002) |
| CCK | Mascagni & McDonald (2003) |
| VIP / CR | **Not yet traced** — left explicitly open; not folded into 2003 |

Numbers were already in the right ballpark; this is provenance, not fabrication.

---

## Severity

Lower than the AMPA / GABA-A / STP / Destexhe provenance errors (`literature_provenance_audit_sep2026.md`), but required for a strict thesis citation pass.

## Open

Locate a primary paper for the VIP/CR percentage before citing that row independently in the thesis.
