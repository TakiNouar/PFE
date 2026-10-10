# 07 — Simulation Protocol

## Time base

| Parameter | Value |
|-----------|-------|
| dt | **0.05 ms** fixed step (verified: Feng et al. 2019 Methods, NEURON) |
| Total duration | 300 ms |
| Stimulus window | 50–150 ms |
| After-discharge observation window | 150–250 ms |

Use native simulator advance (fixed-step or CVODE). Stepped Python loops that update noise every dt are forbidden when they make the full population intractable.

**Under review (U24):** at 10–40 Hz a 100 ms stimulus gives each cell only 1–4 spikes. ISI-CV (Gate 2) is then statistically weak, and the “> 5 Hz” active criterion reduces to “fired at least once”. The window is also short relative to the NMDA decay (125 ms) and the slow sAHP. Decide before Run 1 whether to lengthen the stimulus window (and, if so, update `06_noise_and_drive.md`, `08_metrics_and_outputs.md` and `10_validation_gates.md` together).

## Randomness

- One **global seed** (report it). All placement, connectivity, weight, delay-jitter, heterogeneity, and noise draws derive from it.
- The calibration run and the main run, with identical parameters and seed, must produce **bit-identical** spike times.

## Required run set

1. **Calibration** at the chosen 1.0× population.
2. **Scale sweep** at 0.5×, 1.0×, 1.5×, 3.0× (relative proportions preserved).
3. **Diagnostic A:** AMPA conductances on PN→PN set to zero (NMDA + Mg block only).
4. **Diagnostic B:** all recurrent excitation removed (feed-forward only).
5. **Diagnostic C (optional):** all inhibitory synapses silenced → compute suppression ratio.

Diagnostics A and B depend on PN→PN recurrence, which is expected to be very sparse at N=70 (U23). Report realized PN→PN in-degree next to their results.

## Initialization

- Resting potential ≈ −70.3 mV (Feng PN value, consistent with the passive parameters).
- Allow a short equilibration period if the noise model requires it; document its length.
