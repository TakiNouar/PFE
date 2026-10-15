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

**Measured 2026-10-14** (`python -m bla_sim.benchmark` → `outputs/benchmark/benchmark.csv` and `.json`; laptop on mains power, High performance plan). Each row: 0.2 s warm-up, then 1 s timed. The **real-time factor** is wall-clock seconds per simulated second (below 1 would be faster than real time):

| Row | Real-time factor | Peak memory | Rates in the timed second (PN-A / PN-C / FSI, Hz) |
|---|---|---|---|
| Main level, 200 cells | 112 | 91 MB | 0.55 / 1.12 / 42.7 |
| Main level, 500 cells | 279 | 116 MB | 0.58 / 1.01 / 43.0 |
| Main level, 1,000 cells | 565 | 162 MB | 0.57 / 0.97 / 41.8 |
| Main level, 1,000 cells, cells and noise only (no synapses, no afferents) | 516 | 121 MB | 0.47 / 2.08 / 0 |
| Main level, 1,000 cells, dt 0.1 ms (information only) | 276 | 162 MB | 0.54 / 1.04 / 41.9 |
| **Reference level (Feng's files), 200 cells** | **656** | 160 MB | 0.60 / 1.10 / 42.8 |
| Main level, 1,000 cells, **5 processes at once** (seeds 1–5) | 650 each (645–655) | 163 MB each | seed 1: 0.57 / 0.97 / 41.8 |
| Main level, 1,000 cells, live broadcast on (viewer open) | 578 | 161 MB | 0.57 / 0.97 / 41.8 (identical spikes) |

What the rows show:
- **Cost grows linearly with size** (about 0.56 s of computing per simulated second per cell at the main level).
- **Synapses are about 9 % of the cost** (565 vs 516). Cells and their noise are the rest, so a faster live engine (U26) needs cheaper cells, not cheaper synapses.
- **Parallel runs:** 5 processes at once are each 15 % slower than one alone, so throughput is about 4.3× one process.
- **The broadcast does not change spikes**: runs with and without `--broadcast` gave identical spike files at 100 cells (678 spikes) and at 1,000 cells (5,821 spikes). Its cost is about 2 % at most (578 vs 565 at 1,000 cells; 53.7 vs 53.3 at 100), within timing noise.
- **Time estimates** (`benchmark.json` → `estimates`; runs slowed by the measured 5-process factor): Block B about **12 h** (full detail, 3 seeds in parallel; the reduced half takes about 2 h). Block C about **237 CPU-hours, about 2 days** on 5 parallel processes.

## Run sequence

### Block A — Single cells (seconds)

| Step | What |
|---|---|
| A1 | Feng's full PN-A, PN-C and FSI: single-cell protocol below. *Done 2026-10-14* |
| A2 | Build the reduced PNs (`03`) with `python -m bla_sim.reduce_pn`; run the same protocol; Gate R1. *Done 2026-10-14* |
| A2b | Dendritic-input test with `python -m bla_sim.drive_test`: Feng's afferent trains on the dendrite, full vs reduced cells (Gate R1, synaptic part). *Done 2026-10-14* |
| A3 | Synapse unit test: Feng's vs event-driven synapses (`04`) with `python -m bla_sim.synapse_test`. *Done 2026-10-14: identical to floating-point precision* |

**Block A outcome:** main-level PN = `coarse_d2_p3` (Feng's cell, 6 segments; Gate R1 passed with one approved exception). Event-driven synapses identical to Feng's. See `03`, `04`, `10`.

### Block B — Reference comparison (about 12 h, one night)

**Changed 2026-10-14 (decision in `reports/04`):** only B1 runs, as the reference behaviour of Feng's network for the simplified model, with **one threat trial each at ×2, ×4 and ×8** instead of three at ×4 (same 57 s). B2, B3 and Block C are dropped; command `python -m bla_sim.launcher B --level full --max-procs 3`. The text below is the original plan.

The **same** 200-cell network (same seeds, wiring, weights, delays, noise and afferent streams) is run twice: once with Feng's originals (reference level), once with the reductions (main level).

| Step | What | Seeds | Simulated time per seed | Estimated time (3 seeds in parallel) |
|---|---|---|---|---|
| B1 | Full detail: settle 3 s, rest 30 s, then 3 threat trials at ×4 | 3 | 57 s | ~12 h (measured) |
| B2 | Reduced: identical protocol | 3 | 57 s | ~2 h (measured) |
| B3 | Compare B1 and B2: Gate R2 | — | — | — |

Commands (from `Simulations/BLA/simulation`): `python -m bla_sim.launcher B` starts the six runs (at most one per core, longest first, each broadcasting to the viewer; `--dry-run` lists them with time estimates). A single run by hand: `python -m bla_sim.run --block B --level full --n 200 --seed 1 [--broadcast]`.
Results go to `outputs/B_<level>_n200/seed<k>/`. Then `python -m bla_sim.gate_r2` writes `outputs/blockB/reduction_R2.json` and `.png` (Gate R2, `10`).

### Block C — Main run (about 2 days)

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

C1–C3 run as one continuous simulation per seed (`--block C_main`); C4 `--block C_rest --n 500`; C5 `--block C_inhoff`; C6 `--block C_nmda` and `--block C_noff`; C7 `--block C_rest --seed 1` **without** `--broadcast`. `python -m bla_sim.launcher C` starts all 18 runs in that way. Measured (Phase 0): the main level at 1,000 cells runs at a real-time factor of 565 alone and 650 with 5 runs in parallel. C1–C3 then take about 28 h per seed, with the 5 seeds in parallel; C5 about 13 h; C4 about 3 h; C6 and C7 about 6 h. All of Block C is about 237 CPU-hours, roughly 2 days of wall-clock time on 5 parallel processes.

**Why these lengths.** The principal cell's adaptation brake builds up over a Ca²⁺ pool with a 1 s time constant, so 3 s of settling is about three time constants. At ~1 Hz resting rates, a 30 s rest epoch gives about 30 spikes per PN, enough for rates and ISI statistics. Feng averaged over 5 random seeds and analysed 165 s runs.

The durations are **starting values**. If a block cannot finish in a reasonable time, shorten the rest epoch or the trials per dose. Do not drop below 3 seeds or 3 doses. Record any change in `deviations.md`.

## Single-cell protocol (A1, A2)

Same protocol for Feng's full cells and the reduced cells:

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
