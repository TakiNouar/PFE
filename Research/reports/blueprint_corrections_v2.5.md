# Blueprint Corrections & Alignment Document

**Project:** Emotionally Grounded Conversational AI (PFE)  
**Author:** Mohamed Takieddine Nouar  
**Applies to:** Design Blueprint v2.4 → v2.5 (split files in Research/Development/)  
**Date:** September 2026  

**Status:** Applied. This document records the misalignments that were corrected when advancing the blueprint from v2.4 to v2.5.

---

## Why This Document Exists

The Design Blueprint v2.4 was finalized before the simulation work began. Since then, five BLA isolated simulation runs have been completed, a prior full-network simulation was audited across four attempts, and a literature review identified validated parameter sources (Feng et al. 2019) that change the biophysical substrate specification. The Erasmus+ exchange (October 2026 – February 2027) also affects the timeline that the roadmap describes.

None of these developments were reflected in the committed blueprint files at the time of v2.4. This document records each misalignment, what it said, what it should say, and confirms the corrections were applied.

---

## Corrections Applied

| # | File | Section | Severity | Summary |
|---|------|---------|----------|---------|
| 1 | `00_status_vision_architecture.md` | Status block | Critical | Updated to reflect simulation work begun (full-network 4 attempts + BLA 5 runs + Feng et al. literature) |
| 2 | `06_open_questions_simulations.md` | Open Q[2] + §19 append | Critical | Q[2] partially resolved for BLA; N≈200 collapse identified as scaling artifact |
| 3 | `02_biophysical_substrate.md` | §5.2.2 | Significant | Single-compartment → 3-compartment for BLA Pyr; Feng et al. synaptic kinetics; SOM/VIP additional currents |
| 4 | `02_biophysical_substrate.md` | §5.2.1 note | Significant | BLA N=50/12/8 now empirically tested, not pure guesswork |
| 5 | `06_open_questions_simulations.md` | §19 opening | Moderate | Points to full simulation history (full-network + BLA runs) |
| 6 | `05_hardware_stack_roadmap_scope.md` | §16 | Minor | Updated roadmap with isolation-first strategy + Erasmus+ window |

Version history entry added in `07_meta.md` → **v2.5 Simulation alignment**.

---

## What Did Not Need Changing

- Vision, core design principle, full system architecture (`00_`)
- 10-region limbic inventory, connectivity, sensory routes (`01_`)
- Open questions [1], [3]–[10] (`06_`) — still genuinely open
- Must-have vs. future work scope (`05_` §17)
- Hardware plan and technical stack (`05_` §13–14)
- LLM fine-tuning, translator, memory, voice (`04_`)
- Affective semantic priming (`01_` §4.9)

---

*This document provides an audit trail of what changed between blueprint v2.4 and v2.5, and why.*
