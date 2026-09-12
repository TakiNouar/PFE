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
| **BLA/** | Isolated characterization — Runs 1–5 complete; Run 6 (Feng et al. 2019 params) pending. Contains `Research/` notes + `reports/test_run_1/`. |
| **CeA/** | Next isolation study |
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

Cross-cutting docs:
- Design: `Research/Development/`
- Literature: `Research/Sources/`
- Project reports: `Research/reports/`
