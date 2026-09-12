# Lessons for a Clean Restart

This file is the only one that should be treated as operational guidance for the next implementation.

---

## 1. Do not continue from any previous code or parameter set

- Runs 1–5 used guessed kinetics (especially AMPA τ=2 ms and missing Mg block).
- The literature proxy run introduced further deviations and never reached the mandated population size.
- Start a new code base.

## 2. Non-negotiable biophysical targets (from Feng / Kim)

Before writing code, lock these values:

- AMPA PN→PN: rise 0.3 ms, **decay 6.9 ms**
- NMDA PN→PN: rise 3.7 ms, **decay 125 ms**, **full dynamic Mg²⁺ block**
- E_GABA = **−75 mV**
- Multi-compartment PN + **I_sAHP**
- Conductance-based noise (Feng Table 7 numbers)
- Distance-dependent PN→PN probabilities (not fixed K=3)
- Dynamic short-term depression on every synapse

If any of the above cannot be obtained from ModelDB or the papers, **stop** and report the missing item. Do not invent a substitute.

## 3. After-discharge is not an isolated-BLA success criterion

Record it, but do not tune the isolated model to force ≥10 ms (or seconds-scale) persistence. That target belongs to the multi-region network (VTA, HIP, CeA, PAG, HYP loops).

Isolated success criteria remain:

- syn < 0.5
- CV > 0.3
- active fraction > 0.4
- mean Pyr rate in the biological 10–40 Hz range under moderate drive
- functional PV/SOM suppression
- bit-identical reproducibility under a single global seed

## 4. Environment and tooling constraints discovered so far

- NEURON Python package was unavailable (import failed, pip 502).
- Stepped pure-Python noise loops made the full 150/112/108 network too expensive.
- Any future strict NEURON path requires a working `neuron` package and the ability to load the compiled ModelDB mechanisms without re-implementing them.

Decide explicitly before the next coding session:

- **Strict path** — wait until NEURON is available and use the original `.mod` files, **or**
- **Pragmatic path** — authorize a pure-Python / Brian2 re-implementation that still uses the published numerical values and documents every approximation.

Do not mix the two approaches silently.

## 5. Connectivity scaling

Never again use fixed in-degree while letting inhibitory population size scale freely. Either:

- use the published distance-dependent probabilities inside a volume that preserves density, **or**
- if a fixed-in-degree experiment is required for comparison, scale both E and I connection numbers consistently and report the resulting E/I ratio at every scale.

## 6. Reproducibility and reporting discipline

- One global seed for all random draws.
- Every number in the written summary must be computed from the data files of that run (no template text).
- Calibration and main runs with identical parameters + seed must be bit-identical.
- Deviations from the source papers or ModelDB must be listed explicitly; “none” is an acceptable statement only if it is true.

## 7. Suggested next concrete step

1. Choose strict vs pragmatic path.
2. If pragmatic: write a new prompt that lists the exact published numbers that will be used and the approximations that are explicitly allowed.
3. If strict: obtain a working NEURON environment first, then re-issue the previous strict prompt unchanged.
4. Target population for the first successful full-size run remains 150 Pyr / 112 PV / 108 SOM (or the original blueprint 50/12/8 if a smaller validated core is preferred).

Until one of those two paths is chosen and the corresponding constraints are written down, do not write new simulation code.
