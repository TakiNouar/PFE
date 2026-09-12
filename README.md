# PFE — Emotionally Grounded Conversational AI

**Author:** Mohamed Takieddine Nouar  
**Institution:** Higher Institute of Sciences — HIS, Algiers  
**Degree:** Bachelor PFE | Computer Science

---

## Project Vision

Build a conversational AI system whose emotional state is produced by a continuous **biophysical limbic simulation** (Hodgkin–Huxley neurons), not by scripted role-play from a language model.

The limbic core is the sole authority on what is felt. The LLM is only the voice that translates the neural state.

Target character: **Ultron** — cold, precise, intelligent, genuinely curious, hostile only when earned.

> Status: **Pre-implementation / early simulation phase**. Design targets are specified; isolated BLA characterization (Runs 1–5) is complete. Nothing is yet integrated into a full conversational system.

---

## Repository Structure

```
PFE/
├── README.md
├── Research/
│   ├── Development/          ← Design Blueprint v2.4 (split)
│   ├── Sources/              ← Literature (split by topic)
│   │   ├── 01_primary_bla_references.md   ⭐ Feng et al. 2019
│   │   ├── 02_…07_*.md
│   │   └── sources_full.md
│   └── reports/              ← Simulation reports (split)
│       ├── 00_overview_and_context.md
│       ├── 01_…05_*.md
│       └── BLA_isolated_simulation_report_full.md
└── Simulation tests/         ← Simulation code & run outputs (to be populated)
```

---

## Key Documents

| Document | Start here |
|----------|------------|
| Design Blueprint | [Research/Development/](Research/Development/) |
| Research Sources (⭐ Feng et al. 2019) | [Research/Sources/](Research/Sources/) |
| BLA Isolated Simulation Report (Runs 1–5) | [Research/reports/](Research/reports/) |

---

## Core Constraint

The language model may **never** invent, override, or perform an emotion that is not present in the neural state vector produced by the limbic simulation.
