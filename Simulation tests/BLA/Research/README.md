# BLA Research Dossier

Literature synthesis and implementation architecture for isolated basolateral amygdala simulations.

## Layout

| Path | Role |
|------|------|
| `00_`–`12_*.md` | Biology and functional reference |
| `architecture/` | **Authoritative** build spec for clean **Run 1** |
| `../reports/` | Run reports, clean-restart policy, archived failed tests |

## Authority order

1. Literature + ModelDB (`Research/Sources/`)
2. `architecture/` (this folder)
3. Biology files `00_`–`12_`
4. Design Blueprint (living outline only)

## Clean restart

Previous isolation attempts are archived under `../reports/test_run_1/`. The next campaign is **Run 1**, not “Run 6”.

See `../reports/00_clean_restart_policy.md`.
