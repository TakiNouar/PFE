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

## Decisions (M. T. Nouar, 2026-10-13)

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

**Decision (M. T. Nouar, 2026-10-14):** option D, two levels.
- **Reference level:** Feng's files unchanged. Single cells, plus one 200-cell network for 30 s of rest and 3 threat trials. About one night.
- **Main level:** the full 1,000-cell protocol, run with a reduced PN (DEV-006; finally Feng's cell on a 6-segment grid, see Block A below) and event-driven synapses (DEV-007). It must match the reference (Gates R1 and R2) before its results count. Estimated at "one to two nights" here; revised to about 1.5 days after Block A, then measured at about 2 days in Phase 0.

The main level also prototypes the simplifications the live engine will need (U26).

## Update 2026-10-14 — Block A results

| Step | Result |
|---|---|
| A1, Feng's full cells | Resting −70.2 mV (PN; Feng −70.3), input resistance 136 MΩ (Feng ~140), time constant 34.9 ms (Feng ~30; U29). PN-A: 1 spike per 1 s step at every current (U28); PN-C: 10–28 spikes/s, steady; FSI: 24–221 spikes/s. Noise alone: PN-A 0.35 Hz, PN-C 1.65 Hz, FSI 0 Hz (rat BLA: 0.21 and 1.55 Hz; Amir et al. 2018). FSI gap coupling 0.069 (Woodruff & Sah ≈ 0.05) |
| A2, reduced principal cell | **Final choice: `coarse_d2_p3`**, Feng's cell rebuilt on 6 segments (soma 1, apical 2, basal 3), no fitted values, 25 µs per cell per step (Feng's: 83). Gate R1 passed with one approved exception (PN-C at 1.5 nA: 6 spikes before depolarization block instead of 9). Under Feng's afferent trains on the dendrite it fires like Feng's cell (PN-A 0.66 vs 0.69 Hz, PN-C 3.36 vs 3.25 Hz). Choice: M. T. Nouar |
| A2, history of the choice | The **two-piece** cell (soma + one lumped dendrite, 8.4 µs) was chosen first on current-injection results. The network smoke test then showed principal cells firing 2–3× less than in full detail. A new dendritic-input test traced this to the lumped dendrite (35 % too weak: it loses the local depolarization that relieves the NMDA Mg²⁺ block). A latency test traced the early first spike at strong current to the basal dendrite being one segment. Both are fixed by keeping Feng's two dendrites with ≥ 2 and ≥ 3 segments. One-piece, two-piece and apical 2 + basal 1 were rejected; apical 2 + basal 7 passes with no exception but costs 41 µs |
| A3, event-driven synapses | Identical to Feng's synapse files to floating-point precision (largest relative difference 1.4e-13) for all four pathways and all trains; 0.003 µs per connection per step vs 1.32 µs |
| Network code | `network.py`, `inputs.py`, `run.py`, `metrics.py` written and smoke-tested at 100 cells (1.2 s): full detail real-time factor 280 (PN-A 0.62, PN-C 1.65, FSI 52.8 Hz); two-piece 22.6 (0.36 / 0.58 / 23.0 Hz, rejected); coarse `coarse_d2_p3` 53.3 (0.61 / 1.38 / 49.3 Hz) |

Code: `Simulations/BLA/simulation/bla_sim/` and `mechanisms_run1/`. Results: `Simulations/BLA/simulation/outputs/blockA/` and `outputs/bench_*_n100_smoke*/`.

## Update 2026-10-14 — Phase 0 benchmark, Gate 2, run tools and viewer

| Item | Result |
|---|---|
| Phase 0 benchmark | Main level 112 / 279 / 565× slower than real time at 200 / 500 / 1,000 cells; reference level 656× at 200 cells; synapses ~9 % of the cost; 5 parallel runs ×1.15 slower each. Block B about 12 h, Block C about 237 CPU-hours (about 2 days), up from the earlier 10 h and 1.5 days |
| Gate 2 (U29) | Passed. Feng's "~30 ms" is the slowest membrane time constant (30.9 ms measured); Block A's 34.9 ms was the 63 %-rise time. The effective time constant is set mainly by Ih |
| Run tools | `launcher.py` (parallel jobs, resume, keeps Windows awake), `gate_r2.py` (tested on synthetic data) |
| Live viewer | Built (`architecture/13`). Identical spikes with the broadcast on and off at 100 and 1,000 cells; cost ≤ 2 % |
| New open item | U30: FSIs fire ~42 Hz at every size and at both levels in 1 s samples (Gate 3: 10–30 Hz). FSI depolarization block seen in the 100-cell ×8 demo. Checked in Block B before Block C |

## Decision 2026-10-14 (M. T. Nouar) — simplified neurons; Feng as the documented reference

| Question | Decision | Reason |
|---|---|---|
| Main model | **Simplified neurons in Brian2**: PN-A and PN-C as adaptive integrate-and-fire cells with a dendrite carrying NMDA, FSI as a point neuron, all fitted to Feng's cells as measured in Block A | The project builds an emotional engine, not new neuroscience. Feng's paper and code are taken as the documented facts. The final live system needs simple neurons anyway (U26), and only they leave room for the other limbic populations |
| Feng's detailed model | Kept as the **reference** only: Block A (done) gives the single-cell fitting targets, Block B gives the network reference | It costs no further work. Detailed network runs take days on the laptop |
| Block B | **Full level only, 3 seeds, one threat trial each at ×2, ×4, ×8** (57 s each; started 2026-10-14 16:40) | Gives the simplified network a dose response to match, from Feng's own network under the same inputs |
| Block C and the 6-segment main level | **Dropped** | Their purpose (a detailed main run) is replaced by the simplified model |
| Targets Feng does not document | Threat dose response and recovery come from experimental papers, checked against Block B | Feng's paper covers rest firing and gamma, not graded threat input |

**Next:** see `05_status_and_next_steps.md`.

## What did not change

The clean-restart policy (`00_clean_restart_policy.md`), the archive (`test_run_1/`), the authority order, and the rule that every number has a source.
