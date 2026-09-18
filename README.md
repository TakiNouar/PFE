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

> **Status (September 2026):** Early simulation phase. Design Blueprint v2.5 is complete.  
> Early full-network attempts and the first BLA isolation campaign (historically labelled Runs 1–5) are **archived as failed tests**.  
> A clean, literature-grounded BLA campaign restarts as **Run 1** under the isolation-first strategy. Full pipeline is not yet built.

---

## Repository Layout

```
PFE/
├── README.md
├── Research/
│   ├── Development/     Design Blueprint v2.5 (split)
│   ├── Sources/         Literature & parameter references
│   └── reports/         Project-level simulation reports & audits
└── Simulation tests/
    ├── BLA/ … PAG/      One folder per limbic region
    │   ├── reports/      Region-specific run reports
    │   └── simulation/   Code, configs, outputs
    └── Neurons Connected/   Multi-region / full-network sims
```

---

## Start Here

| What | Where |
|------|--------|
| Design Blueprint v2.5 | [Research/Development/](Research/Development/) |
| Literature (Feng et al. 2019 ⭐) | [Research/Sources/](Research/Sources/) |
| Project reports & clean-restart policy | [Research/reports/](Research/reports/) |
| Per-region sim work | [Simulation tests/](Simulation%20tests/) |
| BLA clean restart policy | [Simulation tests/BLA/reports/00_clean_restart_policy.md](Simulation%20tests/BLA/reports/00_clean_restart_policy.md) |

---

## Core Constraint

The language model may **never** invent, override, or perform an emotion that is not present in the neural state vector.
