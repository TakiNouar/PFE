# 07 — Simulation Protocol

## Fixed settings (Feng code)

| Setting | Value |
|---|---|
| Time step | dt = **0.05 ms**, fixed step |
| Temperature | 31 °C |
| Starting voltage | v_init = −70 mV |
| Advance | NEURON's own solver (`pc.psolve` in 50 ms chunks). Between chunks, Python may only save data (live viewer snapshots, `13`). No Python code that runs every time step |

## Phase 0 — Setup and speed benchmark (before any gate)

1. Install NEURON 9.0.2: the Windows installer `nrn-9.0.2.w64-mingw-py-310-311-312-313-314-setup.exe` (GitHub releases), or WSL2 Ubuntu + `pip install neuron==9.0.2`. `pip install neuron` does **not** work on native Windows.
2. Copy the ModelDB 247968 files into `Simulations/BLA/simulation/mechanisms/`, compile with `nrnivmodl`, and record a SHA-256 hash of every file.
3. Time **1 s of simulated activity** for each combination:

| Factor | Values |
|---|---|
| Size | 100, 500, 1,000 cells |
| Threads (`pc.nthread`) | 1 and 6 |
| dt | 0.05 ms (and 0.1 ms, only to know the cost) |

Plus two extra rows at 1,000 cells, 6 threads, dt 0.05 ms:
- **cells without synapses** (noise only): shows how much of the cost is synapses, which informs the live engine (U26);
- **live broadcast on** (`13`): measures the viewer's overhead.

4. Write `benchmark.csv`: wall-clock seconds per simulated second (the **real-time factor**; below 1 is faster than real time) and peak memory.

The benchmark decides:
- whether the protocol below fits in a night at 1,000 cells, or 500 becomes the main size (`02`);
- what the live engine will need (a later decision, outside Run 1).

Gate runs always use dt = 0.05 ms. dt = 0.1 ms is measured only for information.

## Run sequence

| Step | What | Size | Seeds | Simulated time per seed |
|---|---|---|---|---|
| 1 | Single cells: current steps on PN-A, PN-C and FSI alone | 1 cell | — | 1 s per step |
| 2 | Settle: run and discard | 1,000 | each | 3 s |
| 3 | Rest: background noise + afferents only | 1,000 | 5 | 30 s |
| 4 | Threat trials: 2 s before, 2 s threat, 4 s after; 5 trials per dose, doses ×2, ×4, ×8 | 1,000 | 5 | 120 s |
| 5 | Scale check: steps 2–3 | 500 | 5 | 33 s |
| 6 | Inhibition-off: steps 2–3, then 5 trials at ×4, with FSI→PN weights at 0 | 1,000 | 5 | 73 s |
| 7 | Diagnostics (report only): PN→PN AMPA at 0 (NMDA only); PN→PN connections removed | 1,000 | 1 | 33 s each |
| 8 | Reproducibility: repeat step 3 with seed #1, **live broadcast off** | 1,000 | 1 | 33 s |

Steps 3–4 run in one continuous simulation per seed (settle → rest → trials).

**Why these lengths.** The principal cell's adaptation brake builds up over a Ca²⁺ pool with a 1 s time constant, so 3 s of settling is about three time constants. At ~1 Hz resting rates, a 30 s rest epoch gives about 30 spikes per PN, enough for rates and ISI statistics. Feng averaged over 5 random seeds and analysed 165 s runs.

The durations are **starting values**. If the benchmark shows the full sequence cannot finish in a reasonable time, shorten the rest epoch or the trials per dose. Do not drop seeds below 3 or doses below 3. Record any change in `deviations.md`.

## Single-cell step protocol (step 1)

No noise, no synapses. Inject 1 s current steps into the soma, from just below threshold to strong drive (≥ 6 levels). Record voltage and spike times. Also measure resting potential, input resistance (small hyperpolarising step) and membrane time constant.

For the gap-junction check, inject a 1 s hyperpolarising step into one FSI of a coupled pair and measure the coupling coefficient (ΔV of the partner ÷ ΔV of the injected cell).

## Randomness

- One **global seed** per network seed. Everything derives from it: placement, wiring, weights, delay jitter, noise streams, which afferent trains go where, and threat spikes.
- Use separate, named streams for each purpose, so changing one (for example threat spikes) never changes another (for example wiring).
- Network seeds: 1, 2, 3, 4, 5 (record them).
