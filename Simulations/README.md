# Simulations

Isolated and multi-region simulation studies for the biophysical limbic network.

## Layout

Each region folder:

```
Region/
├── reports/      Run reports, audits, findings, archives
└── simulation/   Code, configs, outputs, plots
```

BLA additionally has `Research/` (biology dossier + `architecture/` build spec).

| Folder | Status |
|--------|--------|
| **BLA/** | First isolation campaign (historically Runs 1–5) **archived as failed tests** in `reports/test_run_1/`. The clean, literature-grounded campaign restarts as **Run 1** (spec: `Research/architecture/`). |
| **CeA/** | Next isolation study (after clean BLA Run 1) |
| **PFC/** | Pending |
| **HYP/** | Pending |
| **HIP/** | Pending |
| **INS/** | Pending |
| **ACC/** | Pending |
| **NAc/** | Pending |
| **VTA/** | Pending |
| **PAG/** | Pending (deferred in the first implementation phase) |
| **Neurons_Connected/** | Multi-region sims (BLA→CeA, then full network). `reports/` holds the archived full-network attempts 1–4. |

## Strategy

**Isolation-first:** validate each region with literature-grounded parameters, then wire them together under `Neurons_Connected/`.

Paths must not contain spaces, because NEURON’s `nrnivmodl` (used to compile ModelDB `.mod` files) breaks on them.

See the project policy `Research/reports/project_policy_blueprint_and_runs.md` and the BLA clean restart `Simulations/BLA/reports/00_clean_restart_policy.md`.

Cross-cutting docs:
- Design: `Research/Development/`
- Literature: `Research/Sources/`
- Project reports: `Research/reports/`
