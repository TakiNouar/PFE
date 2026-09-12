# BLA Research Dossier — Review and Fixes (September 2026)

**Scope:** Full strict review of `Simulation tests/BLA/Research/` (biology `00_`–`12_` + `architecture/`).  
**Action:** Fixes applied; clean restart policy recorded.

---

## Policy decisions (confirmed)

1. **Blueprint is a living outline**, not fixed doctrine. Simulations and literature can change it.
2. **Archived failed tests** live under `test_run_1/`; they teach anti-patterns only.
3. **Next implementation = Run 1** (not Run 6).

Documents: `00_clean_restart_policy.md` (this folder), `Research/reports/project_policy_blueprint_and_runs.md`.

---

## Issues found and fixes applied

| Issue | Severity | Fix |
|-------|----------|-----|
| Run numbering implied continuity with failed campaign | High | Reframed as clean **Run 1** |
| Unexplained population 150/112/108 next to 50/12/8 | High | Removed; **default only 50/12/8** |
| Intermittent gamma implied as hard requirement | High | Softened to **diagnostic**; gates exclude gamma as pass/fail |
| ±10% heterogeneity invented when source silent | High | **0% extra heterogeneity** unless source ranges exist |
| SOM→PN probability vague | Medium | Named **P_SOM_PN = 0.34** (approx., documented) |
| FSI OU τ left as “see ModelDB” | Medium | Require numeric copy into `full_parameters.json` |
| STP “typical magnitude” only | Medium | Require **Feng Table 4** values in JSON; halt if missing |
| nS vs µS risk | Medium | Standard **nS** (Feng); document conversion |
| No deviations template | Medium | Added `simulation/deviations.md` |
| No Research root README | Low | Added `Research/README.md` |
| Blueprint authority unclear | Low | Policy reports + architecture overview |

## Remaining work before coding Run 1

1. Transcribe Feng Table 4 (STP) and full Table 7 FSI rows into the first `full_parameters.json`.
2. Confirm ModelDB delay and passive values when mechanisms are loaded.
3. Implement against `architecture/` only; update blueprint afterward if Run 1 changes the outline.
