# PFE — Emotionally Grounded Conversational AI

**Author:** Mohamed Takieddine Nouar  
**Institution:** Higher Institute of Sciences — HIS, Algiers  
**Degree:** Bachelor PFE | Computer Science

---

## Vision

A conversational AI whose emotional state is produced by a continuous **biophysical limbic simulation** (Hodgkin–Huxley neurons), not by scripted role-play.

The limbic core is the sole authority on what is felt. The LLM only translates that state.

Target character: **Ultron** — cold, precise, intelligent, genuinely curious, hostile only when earned.

> Status: **Early simulation phase.** Design Blueprint v2.5 is complete. BLA isolated characterization (Runs 1–5) is done. Full pipeline is not yet built.

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
| BLA simulation report (Runs 1–5) | [Research/reports/](Research/reports/) |
| Per-region sim work | [Simulation tests/](Simulation%20tests/) |

---

## Core Constraint

The language model may **never** invent, override, or perform an emotion that is not present in the neural state vector.
