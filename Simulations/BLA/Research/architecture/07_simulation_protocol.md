# 07 — Simulation Protocol

## Fixed settings (Feng code)

| Setting | Value |
|---|---|
| Time step | dt = **0.05 ms**, fixed step |
| Temperature | 31 °C |
| Starting voltage | v_init = −70 mV |
| Advance | NEURON's own solver (`pc.psolve` in 50 ms chunks). Between chunks, Python may only save data (live viewer snapshots, `13`). No Python code that runs every time step |
| Cores | **One per run.** Feng's files are not thread safe (`pc.nthread(n > 1)` fails: "na3 is not thread safe"). Independent runs (seeds, conditions) execute as **separate processes in parallel**, at most one per physical core (6 on the project laptop) |

## Phase 0 — Setup and speed benchmark

**Done (2026-10-14):**
1. NEURON 9.0.2 installed from the official Windows installer into `C:\nrn` (SHA-256 checked against GitHub). `pip install neuron` does **not** work on native Windows.
2. ModelDB 247968 cloned into `Simulations/BLA/simulation/mechanisms/` (GitHub mirror commit `b5b2127`), SHA-256 of every file in `HASHES.txt`, compiled with `nrnivmodl` (`nrnmech.dll`).
3. Preliminary measurements (one process, laptop on mains power, High performance, 3.0 GHz):

| Item | Cost per 0.05 ms step |
|---|---|
| NEURON built-in `hh`, per segment | 0.13 µs |
| Feng PN, per segment (11 mechanisms) | 5.2 µs, so ~83 µs per 16-segment PN |
| Feng synapse, each | 1.0–1.4 µs |
| `extracellular`, per segment | ~0.3 µs |

From these, the full-detail network costs about **1 hour of computing per simulated second at 1,000 cells**, hence the two levels (`00`).

**Still to measure:** time 1 s of simulated activity for each row and write `benchmark.csv`. It records wall-clock seconds per simulated second (the **real-time factor**; below 1 is faster than real time) and peak memory:

| Row | Purpose |
|---|---|
| Full-detail vs reduced, 200 cells | Real cost of the reference run and of the reductions |
| Reduced, 500 and 1,000 cells | Real cost of the main run |
| Reduced, 1,000 cells, **cells without synapses** (noise only) | How much of the cost is synapses (informs U26) |
| Reduced, 1,000 cells, **1 vs 5 processes at once** | Real throughput of parallel runs on the laptop (heat and memory limits) |
| Reduced, 1,000 cells, **live broadcast on** (`13`) | The viewer's overhead |
| Reduced, 1,000 cells, dt 0.1 ms | Information only; gate runs always use 0.05 ms |

## Run sequence

### Block A — Single cells (seconds)

| Step | What |
|---|---|
| A1 | Feng's full PN-A, PN-C and FSI: single-cell protocol below |
| A2 | Build the one-piece PN-A and PN-C (`03`); run the same protocol; Gate R1. Fit only if Gate R1 fails |
| A3 | Synapse unit test: Feng's vs event-driven synapses (`04`) |

### Block B — Reference comparison (one night)

The **same** 200-cell network (same seeds, wiring, weights, delays, noise and afferent streams) is run twice: once with Feng's originals (reference level), once with the reductions (main level).

| Step | What | Seeds | Simulated time per seed | Estimated time (3 seeds in parallel) |
|---|---|---|---|---|
| B1 | Full detail: settle 3 s, rest 30 s, then 3 threat trials at ×4 | 3 | 57 s | ~10 h |
| B2 | Reduced: identical protocol | 3 | 57 s | ~30 min |
| B3 | Compare B1 and B2: Gate R2 | — | — | — |

### Block C — Main run (one to two nights)

Runs only after Gates R1 and R2 pass.

| Step | What | Size | Seeds | Simulated time per seed |
|---|---|---|---|---|
| C1 | Settle: run and discard | 1,000 | each | 3 s |
| C2 | Rest: background noise + afferents only | 1,000 | 5 | 30 s |
| C3 | Threat trials: 2 s before, 2 s threat, 4 s after; 5 trials per dose, doses ×2, ×4, ×8 | 1,000 | 5 | 120 s |
| C4 | Size check: C1–C2 | 500 | 5 | 33 s |
| C5 | Inhibition-off: C1–C2, then 5 trials at ×4, with FSI→PN weights at 0 | 1,000 | 5 | 73 s |
| C6 | Diagnostics (report only): PN→PN AMPA at 0 (NMDA only); PN→PN connections removed | 1,000 | 1 | 33 s each |
| C7 | Reproducibility: repeat C1–C2 with seed #1, **live broadcast off** | 1,000 | 1 | 33 s |

C1–C3 run as one continuous simulation per seed. Rough estimate for the main level at 1,000 cells: about 160 s of computing per simulated second, so C1–C3 take about 7 h per seed, and the 5 seeds run in parallel. Phase 0 replaces these estimates with measurements.

**Why these lengths.** The principal cell's adaptation brake builds up over a Ca²⁺ pool with a 1 s time constant, so 3 s of settling is about three time constants. At ~1 Hz resting rates, a 30 s rest epoch gives about 30 spikes per PN, enough for rates and ISI statistics. Feng averaged over 5 random seeds and analysed 165 s runs.

The durations are **starting values**. If a block cannot finish in a reasonable time, shorten the rest epoch or the trials per dose. Do not drop below 3 seeds or 3 doses. Record any change in `deviations.md`.

## Single-cell protocol (A1, A2)

Same protocol for Feng's full cells and the one-piece cells:

1. **Passive:** resting potential; input resistance and membrane time constant from a small hyperpolarising step (−0.05 nA, 1 s).
2. **Current ladder:** 1 s depolarising steps at ≥ 6 levels from just below threshold to 1.5 nA. Record spike times.
3. **Long steps:** 4 s steps at 0.4 and 1.0 nA. PN-A fires about once every 2 s at 0.4 nA (preliminary, 2026-10-14), so a 1 s step shows its adaptation poorly.
4. **Noise only:** 60 s with Feng's background noise and nothing else; record firing rate and ISI CV.

No noise and no synapses in steps 1–3.

**Gap-junction check (FSI, both levels):** inject a 1 s hyperpolarising step into one FSI of a coupled pair and measure the coupling coefficient (ΔV of the partner ÷ ΔV of the injected cell).

## Randomness

- One **global seed** per network seed. Everything derives from it: placement, wiring, weights, delay jitter, noise streams, which afferent trains go where, and threat spikes.
- Use separate, named streams for each purpose, so changing one (for example threat spikes) never changes another (for example wiring).
- The reference and reduced versions of the 200-cell network use **identical** streams, so they differ only in the reductions.
- Network seeds: 1, 2, 3, 4, 5 (record them).
