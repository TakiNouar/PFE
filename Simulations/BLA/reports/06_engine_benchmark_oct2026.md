# Engine Benchmark for the Simplified Model — October 2026

**Date:** 2026-10-14
**Question:** how many simplified neurons run in real time on the project laptop, on the GPU (GeNN) and on the CPU (Brian2)? (decision of 2026-10-14 in `04_run1_redesign_oct2026.md`; U26)
**Code:** `Simulations/BLA/simplified/engine_benchmark/`. **Results:** `Simulations/BLA/simplified/outputs/engine_benchmark/results.jsonl`.

---

## The benchmark network

Built like the planned simplified BLA model, with **placeholder parameters**: the real values come from fitting Feng's cells. Speed depends on the structure, not on the exact values.

| Part | Choice |
|---|---|
| Principal cells (90 %) | Adaptive exponential integrate-and-fire soma + passive dendrite; AMPA and NMDA (Mg block) on the dendrite, GABA-A on the soma |
| FSIs (10 %) | One compartment, no adaptation; AMPA, NMDA, GABA-A |
| Wiring | Feng's inputs per cell (PN←PN 25, PN←FSI 43, FSI←PN 215, FSI←FSI 22), one 1 ms delay |
| Background input | Ornstein–Uhlenbeck current per cell, tuned so PNs fire ~0.9 Hz and FSIs ~28 Hz (inside the rat ranges, so the synaptic load is realistic) |
| Numerics | Forward Euler, dt 0.1 ms; identical equations and step order on both engines |
| Timing | 2 s simulated after warm-up; only the simulation loop is timed (not code generation or compilation) |

Both engines give the same firing rates at every size (PN 0.92–0.95 Hz, FSI 26.9–29.1 Hz), so they compute the same network.

## Results (real-time factor = wall-clock seconds per simulated second; below 1 = faster than real time)

| Neurons | Synapses | **GPU, single precision** | GPU, double precision | CPU, 1 core (preliminary) |
|---|---|---|---|---|
| 1,000 | 85 k | 0.41 | 0.34 | 0.52 |
| 2,000 | 170 k | 0.35 | — | 1.03 |
| 5,000 | 424 k | 0.37 | — | 2.55 |
| 10,000 | 849 k | 0.35 | 0.55 | 4.77 |
| 20,000 | 1.7 M | 0.36 | — | — |
| 50,000 | 4.2 M | 0.74 | — | — |
| 100,000 | 8.5 M | 1.29 | — | — |

**CPU on 1, 3 and 6 cores** (measured 2026-10-15 04:19–04:27, nothing else running):

| Neurons | 1 core | 3 cores | 6 cores |
|---|---|---|---|
| 1,000 | 0.48 | 0.44 | 0.57 |
| 2,000 | 0.94 | 0.77 | 0.82 |
| 5,000 | 2.24 | 1.70 | 1.41 |
| 10,000 | 4.47 | 3.37 | 2.74 |
| 20,000 | 8.99 | 6.33 | 5.16 |

Brian2's multithreading helps little here: 6 cores are only 1.6–1.7× faster than one at 10,000–20,000 neurons, and slower at 1,000. The likely reason is that spike delivery and the per-step bookkeeping run on one core. So the CPU reaches real time at about **2,000–3,000 neurons whatever the core count**, against ~70,000 on the GPU: the GPU has roughly **25× the capacity**.

Setup: laptop (Ryzen 5 4600H, GTX 1650 Ti 4 GB, driver 617.42), mains power. PyGeNN 5.4.0 with CUDA 12.9; Brian2 2.10.1 C++ standalone, MSVC 2022. The GPU runs and the first table's CPU column were made while Block B used 3 of the 6 CPU cores (CPU 2–8 % slower than the clean runs); the multi-core table was run after Block B.

## What it means

- **GPU:** real time up to about **70,000–75,000 neurons** (interpolated between 50,000 and 100,000). Up to 20,000 neurons the cost is flat at ~0.35: a fixed overhead of ~35 µs per time step (launching the GPU work from Python), not the network. So the GPU stays about 3× faster than real time up to 20,000 neurons.
- **CPU:** real time up to about **2,000 neurons on one core** (~0.45 ms of computing per neuron per simulated second) and only about **3,000 on six** (multithreading scales poorly here).
- **Against the detailed model:** the same 1,000-cell network took 565× real time with Feng's (6-segment) cells in NEURON, and takes 0.41× on the GPU: about **1,400× faster**.
- **Double precision** costs little at small sizes (overhead-bound) and ~1.6× at 10,000 neurons on this consumer GPU.

## Consequences for the design

1. The live limbic network can have **tens of thousands of neurons** on the laptop GPU, with headroom. Plan for about half the limit (~35,000) to leave room for the viewer and the LLM link.
2. **Fitting and validation run on the CPU** (Brian2, double precision, repeatable), as planned. The GPU runs must reproduce the CPU statistics. Spike-for-spike identity is not expected: single precision, and the GPU adds synaptic inputs in varying order.
3. **PyGeNN** steps the model from Python, which is what the live LLM loop needs. Its fixed per-step overhead (~35 µs of the 100 µs budget) is the floor.

## Setup notes (laptop)

- Separate Python environment `C:\Users\nouar\.venvs\brian2` (Brian2, PyGeNN, matplotlib), so NEURON's environment is never touched.
- GPU and compiled-CPU runs need `Simulations/BLA/simplified/with_gpu_env.cmd` (MSVC 2022 Build Tools 17.14 + CUDA 12.9, including `CUDA_PATH_V12_9` for NVIDIA's build rules).
- PyGeNN 5.4.0 was built from source (`pip install https://github.com/genn-team/genn/archive/refs/tags/5.4.0.zip`) with `vswhere` and `msbuild` on the PATH.
- Shells with `NoDefaultCurrentDirectoryInExePath=1` cannot start Brian2's compiled program; `brian2_net.py` puts the build folder on that process's PATH.
