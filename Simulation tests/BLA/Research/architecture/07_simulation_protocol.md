# 07 — Simulation Protocol

## Time base

| Parameter | Value |
|-----------|-------|
| dt | 0.05 ms (or the exact step used in Feng/Kim NEURON code) |
| Total duration | 300 ms |
| Stimulus window | 50–150 ms |
| After-discharge observation window | 150–250 ms |

Use native simulator advance (fixed-step or CVODE). Stepped Python loops that update noise every dt are forbidden when they make the full population intractable.

## Randomness

- One **global seed** (report it). All placement, connectivity, heterogeneity, and noise draws derive from it.
- Calibration run and main run with identical parameters + seed must produce **bit-identical** spike times.

## Required run set

1. **Calibration** at the chosen 1.0× population.
2. **Scale sweep** at 0.5×, 1.0×, 1.5×, 3.0× (relative proportions preserved).
3. **Diagnostic A:** AMPA conductances on PN→PN set to zero (NMDA + Mg block only).
4. **Diagnostic B:** all recurrent excitation removed (feed-forward only).
5. **Diagnostic C (optional):** all inhibitory synapses silenced → compute suppression ratio.

## Initialization

- Resting potential ≈ −70 mV (or the value consistent with the passive parameters).
- Allow a short equilibration period if the noise model requires it; document the length.
