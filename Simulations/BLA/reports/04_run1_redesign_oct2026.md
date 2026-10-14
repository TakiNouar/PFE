# Run 1 Redesign — October 2026

**Date:** 2026-10-13
**Applies to:** `Simulations/BLA/Research/architecture/` (all files rewritten), `Simulations/BLA/simulation/deviations.md`, `Research/reports/open_uncertainties.md`
**Evidence:** `reports/PFE claims and design verification.md` (repo root) and its notes in `research_notes/PFE claims and design verification/`, which checked the old spec against Feng's paper, the ModelDB 247968 code and rat recordings.

---

## Why the spec changed

The verification found that the old Run 1 could not test what it was built to test:

| Problem in the old spec | Effect |
|---|---|
| 70 cells at Feng's density, wired with Feng's distance probabilities | Each principal cell got ~0.65 excitatory and ~7 inhibitory inputs, against 25 and 43 in Feng. Recurrent dynamics could not appear |
| Gate: principal cells at 10–40 Hz during a stimulus | Rat BLA principal cells fire about 0.2–3 Hz at rest. Feng tuned his model to those rates |
| 300 ms runs, 100 ms stimulus | Shorter than the principal cell's 1 s Ca²⁺ pool; almost no spikes at real rates |
| Private OU current as the stimulus | Bypassed the synapses, Mg²⁺ block and depression Feng's inputs go through |
| Paper values where Feng's code differs (weights, FSI→PN kinetics, depression floors, leak) | Silent mismatch with the simulations that produced Feng's results |
| SOM cells with two invented values | Not in Feng's model; added deviations with no source |

## Decisions (agreed with the authors, 2026-10-13)

| Question | Decision | Reason |
|---|---|---|
| Simulator for Run 1 | **NEURON 9.0.2**, Feng's files unchanged | No hand-copied equations; strongest provenance. Run 1 is a test campaign; the live engine is decided later (U26) |
| Cell detail | **Feng's full templates** (16 segments per PN) | Authors' choice. Faithful to Feng, and also the least code to write (templates are loaded, not re-implemented) |
| SOM cells | **Left out** | Feng's model has none; removes U10 and U11 |
| Size | **1,000 cells (640 / 260 / 100)** | Feng's own reduced-model size; the smallest size where Feng's 43 inhibitory inputs per cell fit without extra tricks |
| Wiring | **Feng's inputs per cell**, distance-independent | Keeps Feng's E/I balance at any size (Nair-lab practice; van Albada et al. 2015). DEV-001 |
| Replication target | **Feng's code** where it differs from the paper | DEV-002 to DEV-004 |
| Inputs | Feng's noise + Feng's afferent trains; threat = afferent rate × 2, 4, 8 | Real input statistics from Feng's data; dose ladder instead of one invented strength. DEV-005 |
| Gates | Rest rates from rat recordings; dose-dependent response + recovery; inhibition check; 500-vs-1,000 size check | Every threshold has a literature source or is marked as a project guard |

## Two-machine setup (for later phases)

The authors have two machines: a desktop with an RTX 3060 (12 GB) and a laptop with a GTX 1650 Ti (4 GB) and a 6-core Ryzen 5 4600H. Plan: the CPU-bound limbic simulation runs on one machine and streams its state vector over the local network to the GPU machine running the LLM, speech and voice. Run 1 itself is CPU-only and can run on either machine; the Phase 0 benchmark should be run on the machine that will host the live simulation.

## What happens next

1. **Phase 0:** install NEURON 9.0.2, compile Feng's files, hash them, run the speed benchmark (`architecture/07`).
2. **Steps 1–8** of `architecture/07`, checked against `architecture/10`.
3. After Run 1 passes: decide the live engine (U26), then CeA in isolation, then BLA → CeA.

## Update 2026-10-14 — measured speed and option D

Setup was completed and the first measurements were taken on the project laptop (mains power, High performance, 3.0 GHz):

| Finding | Detail |
|---|---|
| Install | Python 3.12.10, NEURON 9.0.2 (`C:\nrn`), Feng's files cloned and hashed (commit `b5b2127`), `nrnmech.dll` compiled |
| First neurons | PN-A rests at −70.2 mV (Feng: −70.3) and fires once, then is silent ~2 s (U28); PN-C fires steadily, 15–20 spikes/s; FSI 61–129 spikes/s without adaptation |
| No multithreading | `pc.nthread(n > 1)` fails: "na3 is not thread safe". Independent runs go in parallel processes instead |
| Cell cost | Feng's PN: 5.2 µs per segment per step (NEURON's `hh`: 0.13 µs), ~83 µs per 16-segment PN |
| Synapse cost | 1.0–1.4 µs per Feng synapse per step; ~88,000 synapses at 1,000 cells |
| Consequence | Full-detail 1,000-cell network: about 1 hour of computing per simulated second. Run 1 as specified: about 11 days with 5 parallel processes. The earlier estimate (4–20 hours) was about 100× too optimistic |

**Decision (agreed with the authors):** option D, two levels.
- **Reference level:** Feng's files unchanged. Single cells, plus one 200-cell network for 30 s of rest and 3 threat trials. About one night.
- **Main level:** the full 1,000-cell protocol, run with a one-piece PN (DEV-006) and event-driven synapses (DEV-007). It must match the reference (Gates R1 and R2) before its results count. About one to two nights.

The main level also prototypes the simplifications the live engine will need (U26).

## What did not change

The clean-restart policy (`00_clean_restart_policy.md`), the archive (`test_run_1/`), the authority order, and the rule that every number has a source.
