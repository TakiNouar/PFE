# Simulation Tests

Isolated and multi-region simulation studies for the biophysical limbic network.

## Layout

Each region folder:

```
Region/
├── reports/      Run reports, audits, findings
└── simulation/   Code, configs, outputs, plots
```

| Folder | Status |
|--------|--------|
| **BLA/** | First isolation campaign (historically Runs 1–5) **archived as failed tests**. Clean, literature-grounded campaign restarts as **Run 1**. Contains `Research/` dossier + architecture specs + `reports/test_run_1/` archive. |
| **CeA/** | Next isolation study (after clean BLA Run 1) |
| **PFC/** | Pending |
| **HYP/** | Pending |
| **HIP/** | Pending |
| **INS/** | Pending |
| **ACC/** | Pending |
| **NAc/** | Pending |
| **VTA/** | Pending |
| **PAG/** | Pending |
| **Neurons Connected/** | Multi-region sims (BLA→CeA, then full 10-region) |

## Strategy

**Isolation-first:** validate each region with literature-grounded parameters, then wire under `Neurons Connected/`.

See project policy: `Research/reports/project_policy_blueprint_and_runs.md` and BLA clean-restart: `Simulation tests/BLA/reports/00_clean_restart_policy.md`.

Cross-cutting docs:
- Design: `Research/Development/`
- Literature: `Research/Sources/`
- Project reports: `Research/reports/`
