# PFE — Emotionally Grounded Conversational AI

**Author:** Mohamed Takieddine Nouar  
**Institution:** Higher Institute of Sciences — HIS, Algiers  
**Degree:** Bachelor PFE | Computer Science

---

## Project Vision

Build a conversational AI system whose emotional state is produced by a continuous **biophysical limbic simulation** (Hodgkin–Huxley neurons), not by scripted role-play from a language model.

The limbic core is the sole authority on what is felt. The LLM is only the voice that translates the neural state.

Target character: **Ultron** — cold, precise, intelligent, genuinely curious, hostile only when earned.

> Status: **Pre-implementation**. Nothing has been built yet. All documents describe design targets.

---

## Repository Structure

```
PFE/
├── README.md
├── Research/
│   ├── Development/          ← Design Blueprint (split & organized)
│   │   ├── README.md
│   │   ├── 00_status_vision_architecture.md
│   │   ├── 01_limbic_architecture.md
│   │   ├── 02_biophysical_substrate.md
│   │   ├── 03_input_dynamics_camera.md
│   │   ├── 04_translator_llm_memory_voice.md
│   │   ├── 05_hardware_stack_roadmap_scope.md
│   │   ├── 06_open_questions_simulations.md
│   │   ├── 07_meta.md
│   │   └── blueprint_v2.4_full.md
│   ├── reports/              ← Formal reports / thesis material
│   └── Sources/              ← References & source material
└── Simulation tests/         ← Exploratory & validation simulations
```

---

## Design Documents

Start here → **[Research/Development/README.md](Research/Development/README.md)**

The full Design Blueprint v2.4 has been split into focused documents for easier navigation while keeping the original monolithic file available.

---

## Core Constraint

The language model may **never** invent, override, or perform an emotion that is not present in the neural state vector produced by the limbic simulation.
