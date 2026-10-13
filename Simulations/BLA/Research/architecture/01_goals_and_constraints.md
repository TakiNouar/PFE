# 01 — Goals and Constraints

## Goals of Run 1

1. **Install check:** Feng's ModelDB 247968 files compile and run under NEURON 9.0.2 on the project machine.
2. **Single cells behave like Feng's:** PN-A adapts, PN-C fires steadily, FSI fires fast.
3. **The network rests like a real BLA:** with background input only, principal cells fire slowly (about 0.2–3 Hz) and FSIs faster (about 10–30 Hz), as recorded in rats.
4. **The network responds and recovers:** a threat input raises principal-cell firing in proportion to its strength, inhibition limits it, and activity returns to rest afterwards.
5. **Reproducible:** same seed, same spikes.
6. **Speed is measured:** the real-time factor of the network is known, so the live engine can be designed from data.

## Non-goals

- After-discharge or seconds-scale persistence (recorded, never tuned for).
- Learning, neuromodulation, other regions.
- Matching every statistic of Feng's 27,000-cell model. The 1,000-cell network keeps Feng's cells, synapses, noise and inputs per cell; it does not reproduce his spatial structure.
- Gamma oscillations as a pass/fail criterion (recorded as a diagnostic).
- Real-time speed (that is the live engine's job).

## Hard constraints

| Constraint | Rule | Where specified |
|------------|------|-----------------|
| Feng's files | `.mod` and cell `.hoc` files from ModelDB 247968 are used **byte-for-byte unchanged**; a hash list proves it | `03`, `09` |
| Code over paper | Where Feng's code and paper differ, use the **code** value and log the paper value in `deviations.md` | `04`, `12` |
| Cells | Feng's `Cell_A` (PN-A), `Cell_C` (PN-C), and FSI template. No SOM | `02`, `03` |
| Wiring | Same in-degree rule for **every** pathway (Feng's realised inputs per cell) | `05` |
| Weights | Per-synapse lognormal weights as drawn in Feng's code | `04` |
| Delays | Feng's distance rule for internal connections; U(0.5, 1) ms for afferents | `05`, `06` |
| Noise | Feng's `Gfluct` point-conductance noise in every cell, Feng's code values | `06` |
| Time step | dt = 0.05 ms, 31 °C, v_init = −70 mV (Feng's code) | `07` |
| Seed | One global seed; every random draw derives from it | `07` |
| Units | NEURON units (µS, mV, ms); tables in this spec quote nS where Feng does | `04` |
| Missing value | Stop and report; never invent | `12` |

## Success criteria

The authoritative list is `10_validation_gates.md`. In short: provenance proven, reproducible, single cells correct, resting rates in the rat range, dose-dependent threat response with return to rest, inhibition measurably limits firing, and results stable between 500 and 1,000 cells.
