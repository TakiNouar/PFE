## 20. Proposed PFE Title

*Emotionally Grounded Conversational AI: A Biophysical Limbic Simulation as the Sole Authority on Affective State*

## 21. Out of Scope for This Blueprint

Exact Hodgkin–Huxley parameter tables, integrator settings, training corpus format, QLoRA hyperparameters, hardware scheduling, process placement, and concrete camera/microphone/TTS driver code belong in implementation notes and engineering appendices, not in this design-level document.

## 22. Version History

| Version | Focus | Change |
|---|---|---|
| 2.1 | Original | Full vision, structure list, suppression gap, roadmap, technical stack, hardware, PFE scope |
| 2.2 | Gap fill | BLA/CeA split, sensory routes, arousal dimension, PAG, bypass rule, affective priming mechanism |
| 2.3 | Master synthesis | Unified document; added an (incorrectly-framed) "current implementation" snapshot |
| **2.4** | **Correction pass** | **Removed all "implemented"/"current prototype" framing — nothing has been built. Reframed §5.2 as a proposed target, not a measured snapshot. Consolidated all open questions (including six surfaced while building the architecture diagram) into a single §18. Added §19 documenting two informal exploratory simulations and the open scaling question they raised. Tense corrected throughout to reflect pre-implementation status.** |
| **2.5** | **Simulation alignment** | **Updated status block, open question [2], §19 simulation notes, §5.2.1 BLA population note, §5.2.2 biophysical substrate, §16 roadmap to reflect: BLA isolated study (5 runs complete), Feng et al. 2019 parameter sources, Erasmus+ timeline (Oct 2026 – Feb 2027), and isolation-first simulation strategy.** |
| **2.5.1** | **Consistency pass (Oct 2026)** | **Aligned with the clean-restart policy: archived BLA Runs 1–5 and the full-network attempts are failed tests that validated no parameters; Q[2] and §19 reworded (fixed K≈3 is an anti-pattern; 50/12/8 is an unvalidated default); roadmap says Run 1 not Run 6; NMDA source = Weisskopf 1999; dt = 0.05 ms; weight multipliers and distance-dependent delays noted; PAG status and §5.2.3/§5.2.4 contradiction fixed; simulator row updated. See `Research/reports/consistency_and_source_verification_oct2026.md`.** |

| **2.5.2** | **BLA Run 1 redesign (2026-10-13)** | **§5.2.1 BLA rows and note, §5.2.2 principal-cell bullet, Q[2], §19 and the §13 simulation-speed row aligned with the redesigned Run 1: Feng's 640 / 260 / 100 at 1,000 cells, Feng's NEURON files unchanged, wiring by Feng's inputs per cell, no SOM in Run 1; "3 compartments required" corrected (sAHP is somatic; Feng's PN has 16 segments); live-engine size and speed deferred to U26. See `Simulations/BLA/reports/04_run1_redesign_oct2026.md`.** |

*End of Design Blueprint v2.5.2*
