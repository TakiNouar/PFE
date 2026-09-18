# Design Blueprint — Emotionally Grounded Conversational AI

**Version:** 2.5 (Pre-Implementation Edition — simulation-aligned)  
**Authors / Contributors:** Mohamed Takieddine Nouar, Maria Loghrab  
**Institution:** Higher Institute of Sciences — HIS, Algiers  
**Project:** Bachelor PFE | Computer Science

---

## Status

The full 10-region integrated system has not been built. Simulation work has begun (full-network attempts + early BLA isolation campaign).

- Early full-network attempts and the first BLA isolation campaign (historically labelled Runs 1–5) are **archived as failed tests**.
- A clean, literature-grounded BLA campaign restarts as **Run 1** under the isolation-first strategy.
- See the status block in `00_status_vision_architecture.md`, project policy in `Research/reports/project_policy_blueprint_and_runs.md`, and BLA clean-restart policy in `Simulation tests/BLA/reports/00_clean_restart_policy.md`.

This folder contains the split Design Blueprint **v2.5** (simulation-aligned).

---

## Document Structure

| File | Content |
|------|---------|
| [00_status_vision_architecture.md](00_status_vision_architecture.md) | Document status, Vision, Core Design Principle, Full System Architecture |
| [01_limbic_architecture.md](01_limbic_architecture.md) | Complete Limbic Architecture specification |
| [02_biophysical_substrate.md](02_biophysical_substrate.md) | Hodgkin–Huxley substrate & population targets (updated with Feng et al. 2019) |
| [03_input_dynamics_camera.md](03_input_dynamics_camera.md) | Multimodal input, continuous simulation, camera |
| [04_translator_llm_memory_voice.md](04_translator_llm_memory_voice.md) | Translator, LLM fine-tuning, Memory, Voice |
| [05_hardware_stack_roadmap_scope.md](05_hardware_stack_roadmap_scope.md) | Hardware, stack, roadmap (updated Sep 2026), PFE scope |
| [06_open_questions_simulations.md](06_open_questions_simulations.md) | Open design questions + simulation notes (Q[2] partially resolved) |
| [07_meta.md](07_meta.md) | Title, out of scope, version history |

---

## Core Design Principle (Reminder)

> The continuous biophysical state of the limbic network is the **sole authority** on what is felt.  
> The language model may only express that state — it is never allowed to invent, override, or perform an emotion that is not present in the neural state vector.

---

*Last updated: September 2026 — v2.5 simulation alignment + contributor update*
