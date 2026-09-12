# Design Blueprint — Emotionally Grounded Conversational AI

**Version:** 2.5 (Pre-Implementation Edition — simulation-aligned)  
**Author:** Mohamed Takieddine Nouar  
**Institution:** Higher Institute of Sciences — HIS, Algiers  
**Project:** Bachelor PFE | Computer Science

---

## Status

The full 10-region integrated system has not been built. Simulation work has begun (full-network attempts + BLA isolated study, Runs 1–5). See the updated status block in `00_status_vision_architecture.md` and the reports in `Research/reports/`.

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

*Last updated: September 2026 — v2.5 simulation alignment*
