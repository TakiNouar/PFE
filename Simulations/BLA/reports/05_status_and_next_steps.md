# BLA — Status and Next Steps

**Updated:** 2026-11-12
**Purpose:** the self-contained starting point for the next working session.
**Git:** branch `run1-redesign`, merged into `main` on 2026-11-12.
**Specs and history:**
- Main model spec: `Simulations/BLA/Research/architecture/14_simplified_model.md`. Files 00–13 describe Feng's detailed model, now the reference only.
- Decision history: `04_run1_redesign_oct2026.md`.
- Deviations: `Simulations/BLA/simplified/deviations.md` (simplified model, S-DEV-1 to S-DEV-3) and `Simulations/BLA/simulation/deviations.md` (wiring, code values and inputs, DEV-001 to DEV-007).

---

## 1. Where things stand

| Part | Status |
|---|---|
| Direction | **Simplified neurons in GeNN** (decided 2026-10-14 / 15). Feng's detailed NEURON model is the reference |
| Feng reference, single cells (Block A) | **Done**, plus a sharper stage-2 reference: noise-only and dendritic-input rates with more samples (`simulation/outputs/blockA/stage2_reference.json`) |
| Feng reference, network (Block B) | **Done** 2026-10-15: 200 cells, 3 seeds, threat ×2/×4/×8 (`07_blockB_reference_oct2026.md`, `simulation/outputs/blockB/reference_summary.json`) |
| Engine benchmark | **Done** (`06`): GPU real time up to ~70,000 neurons; CPU ~2,000–3,000 |
| Simplified synapses (gate S2) | **PASS with 1 approved exception** (`08`) |
| Simplified cells (gate S1) | **69 of 71 checks pass.** Two open: PN-A latency at 1.5 nA (3.7 vs 3.3 ms) and PN-A dendritic-input rate (0.50 vs 0.70 Hz). **Decision pending** (`08` section 2) |
| 1,000-cell simplified network (gates S3–S6) | Not started |
| Live mode with the LLM | Not started (spec 14 section 7) |
| Detailed-model tools | Kept: launcher, live viewer, gate R2, benchmark (`simulation/bla_sim/`) |
| Block C, 6-segment main level | Dropped (2026-10-14) |

## 2. Decisions in force (all by M. T. Nouar)

| Decision | Choice |
|---|---|
| Main model | Simplified neurons fitted to Feng's cells; Feng's paper and code taken as documented facts |
| Engine | GeNN (PyGeNN 5.4) as the single model: exact CPU mode (double precision) for fitting and checks, GPU (single precision) for large and live runs; Brian2 only as a cross-check |
| Synapses | Rise-and-decay conductances fitted to Feng's waveforms, with saturation and per-spike depression (S-1 b); S2 exception approved 2026-10-15 |
| FSI depolarization block | Not reproduced by default; documented option |
| Fitting optimiser | SciPy differential evolution |
| Cells | PN-A, PN-C, FSI; no SOM. Network size 1,000 (640 / 260 / 100) |
| Wiring and inputs | Feng's inputs per cell (25 / 43 / 215 / 22), Feng's noise and afferent trains; threat = afferent rate ×2, ×4, ×8 |
| FSI rest-rate target | Rat data (22–27 Hz, Amir et al. 2018), not Block B's 35 Hz (U30) |
| Machine | The laptop (Ryzen 5 4600H, GTX 1650 Ti 4 GB). Smart App Control turned off by M. T. Nouar on 2026-10-21 (it blocked the locally built GeNN) |

## 3. Next steps, in order

1. **Decide the two open S1 checks** (`08` section 2).
   - (a), recommended: approve both as exceptions in `simplified/config/gate_exceptions.json` (add an "S1" list, then make `cell_check.py` read it as `synapse_check.py` does) and record them in S-DEV-1.
   - (b) One more PN-A fitting attempt first.
2. **Build the 1,000-cell simplified network in GeNN** (spec 14 sections 5, 6, 8):
   - `bla_simple/network.py`: wiring with the `simulation/bla_sim` named streams and in-degree rule; per-connection delays via dendritic delays.
   - `bla_simple/inputs.py`: Feng's afferent trains and the threat.
   - `bla_simple/run.py`: CPU and GPU backends.
   - `bla_simple/gates.py`: gates S3–S6, reusing `simulation/bla_sim/metrics.py`.
   - Watch FSI rates (target 22–27 Hz, U30).
3. Gates **S3** (rest against rat data), **S4** (threat response shaped like Block B), **S5** (inhibition-off, size 500 vs 1,000), **S6** (GPU = CPU statistics, dt 0.05 vs 0.1, Brian2 cross-check, ≤ 0.5× real time).
4. Live mode (spec 14 section 7) and the viewer for the simplified model; then the other limbic populations.

## 4. How to run things

**Simplified model** (from `Simulations/BLA/simplified`, through the toolchain script):

```
with_gpu_env.cmd C:\Users\nouar\.venvs\brian2\Scripts\python.exe -m <module>
```

| Task | Module |
|---|---|
| Fit synapses to Feng's waveforms | `bla_simple.fit_synapses` |
| Gate S2 | `bla_simple.synapse_check` |
| Fit FSI / PN stage 1 / PN stage 2 (GPU; PN2 ~20 min) | `bla_simple.fit_cells FSI` / `PN` / `PN2` |
| Gate S1 (exact CPU mode, ~5 min) | `bla_simple.cell_check` |
| Engine benchmark | `engine_benchmark.run_bench gpu` / `cpu --threads 1 3 6` |

**Feng reference** (from `Simulations/BLA/simulation`, system Python with NEURON):

| Task | Command |
|---|---|
| Synapse reference traces (~1 min; writes the 16 MB `synapse_reference.npz`, not in git) | `python -m bla_sim.synapse_reference` |
| Stage-2 reference: noise and dendritic input (~65 min) | `python -m bla_sim.stage2_reference` |
| Block B summary | `python -m bla_sim.blockb_summary` |
| Earlier tools: single cells, Gate 2, benchmark, runs, launcher, viewer | see `architecture/07`, `09`, `13` |

## 5. Key numbers

| Item | Value |
|---|---|
| Feng's cells, noise only | PN-A 0.345 Hz (CV 0.21), PN-C 1.54 Hz (CV 0.79), FSI silent |
| Feng's cells, dendritic input | PN-A 0.70 Hz, PN-C 3.19 Hz |
| Feng's network, rest (Block B) | PN-A 0.51, PN-C 0.97, FSI 35.1 Hz; threat PN 0.84 / 1.00 / 1.37 Hz at ×2 / ×4 / ×8 |
| Simplified cells (S1) | passive exact; firing curves within 6 %; noise rates within 2 %; dendritic input PN-C 3.66, PN-A 0.50 Hz |
| Simplified synapses (S2) | within 2.8 % on physiological trains |
| GeNN GPU | ~0.35× real time up to 20,000 neurons; real time up to ~70,000 |

## 6. Open items

| ID | Item |
|---|---|
| U31 | PN-A's response to dendritic input is 28 % below Feng's (S1); its effect on the network is to be judged by S3/S4 |
| U30 | FSI rate in our wiring (35 Hz with Feng's cells) above the rat range; cause open |
| U26 | Live engine: the exchange loop with the LLM (spec 14 section 7) |
| U27 | Threat pathway: later, a dedicated thalamic input |
| — | `reports/` and `research_notes/` at the repo root (the October verification report) are still not committed; decide whether to keep them |

## 7. Practical notes

- **Two Python environments:**
  - System Python 3.12 with NEURON (`C:\nrn`, needs `NEURONHOME`) for Feng's reference.
  - `C:\Users\nouar\.venvs\brian2` (Brian2, PyGeNN, SciPy) for the simplified model.

  Never pip-install into NEURON's Python while simulations run.
- GeNN and Brian2 compiled runs need `with_gpu_env.cmd` (MSVC 2022 + CUDA 12.9).
- GeNN stores explicit connections sorted by (pre, post); give per-connection values in that order.
- Feng's files must never be edited (Gate 0 hashes them).
- PowerShell 5.1 strips quotes in `python -c`; put scripts in files.
