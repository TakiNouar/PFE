# PFE — Emotionally Grounded Conversational AI

**Authors / Contributors:**  
- Mohamed Takieddine Nouar  
- Maria Loghrab  

**Institution:** Higher Institute of Sciences — HIS, Algiers  
**Degree:** Bachelor PFE | Computer Science

---

## Vision

A conversational AI whose emotional state is produced by a continuous **biophysical limbic simulation** (Hodgkin–Huxley neurons), not by scripted role-play.

The limbic core is the sole authority on what is felt. The LLM only translates that state.

Target character: **Ultron** — cold, precise, intelligent, genuinely curious, hostile only when earned.

> **Status (October 2026):** Early simulation phase. Design Blueprint v2.5.2.  
> Early full-network attempts and the first BLA isolation campaign (historically labelled Runs 1–5) are **archived as failed tests**.  
> A clean, literature-grounded BLA campaign restarts as **Run 1** under the isolation-first strategy. Full pipeline is not yet built.

---

## Repository Layout

```
PFE/
├── README.md
├── Research/                 Project-wide material only
│   ├── Development/          Design Blueprint (living outline)
│   ├── Sources/              Literature & parameter references
│   └── reports/              Policy, literature audits, open uncertainties
└── Simulations/              One folder per limbic region
    ├── BLA/ … PAG/
    │   ├── Research/         Region dossier + architecture spec (BLA so far)
    │   ├── reports/          Region run reports & archives
    │   └── simulation/       Code, configs, outputs
    └── Neurons_Connected/    Multi-region / full-network sims (+ archived full-network attempts)
```

Folder names have no spaces, because NEURON’s `nrnivmodl` breaks on paths with spaces.

---

## Start Here

| What | Where |
|------|--------|
| Design Blueprint | [Research/Development/](Research/Development/) |
| Literature (Feng et al. 2019 ⭐) | [Research/Sources/](Research/Sources/) |
| Project policy, audits, open uncertainties | [Research/reports/](Research/reports/) |
| BLA Run 1 build spec | [Simulations/BLA/Research/architecture/](Simulations/BLA/Research/architecture/) |
| BLA clean restart policy | [Simulations/BLA/reports/00_clean_restart_policy.md](Simulations/BLA/reports/00_clean_restart_policy.md) |
| Per-region sim work | [Simulations/](Simulations/) |

---

## Core Constraint

The language model may **never** invent, override, or perform an emotion that is not present in the neural state vector.
