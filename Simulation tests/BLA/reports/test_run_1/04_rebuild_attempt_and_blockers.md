# Literature Rebuild Attempt and Blockers

After Runs 1–5 a clean rebuild was attempted that required **exact** ModelDB mechanisms (no re-derived kinetics, no pure-Python substitutes).

## What was attempted

1. Target population: 150 Pyr / 112 PV / 108 SOM (later requested sizes).
2. Source of truth: ModelDB 247968 (Feng) + 150288 (Kim) `.mod` / `.hoc` files.
3. Mandatory mechanisms:
   - Compiled NMODL channels (including I_sAHP, multi-compartment morphology).
   - Dynamic Mg²⁺ block on NMDA evaluated every time step.
   - Dynamic two-factor short-term depression.
   - ModelDB Gfluct conductance noise (Feng Table 7 coefficients).
   - Native NEURON advance (no stepped Python OU loop).

## What actually ran

Only a **small-N proxy** finished:

- N = 20 Pyr / 15 PV / 12 SOM
- Mean Pyr rate = 10.0 Hz (inside 10–40 Hz target)
- Synchrony = 0.186 (< 0.5)
- Active fraction = 1.0
- CV ISI = 0.0 (insufficient spikes)
- PV / SOM rates = 0 (drive applied only to Pyr; recurrent excitation too weak at this scale)
- After-discharge = 0 ms

Full 370-cell network and the requested scale sweep were never completed.

## Documented deviations (from the proxy run)

- Noise replaced by pure-Python analytic OU current (Gfluct Random binding failed under the available NEURON Python interface).
- Cell templates reconstructed in Python instead of executing original `.hoc` templates.
- NMDA Mg²⁺ block formula recorded but **not applied** on every time step.
- Short-term depression parameters taken from tables but **not updated dynamically** on spikes.
- Stepped Python update loop used because native advance + Python noise was not working → made full size intractable.

These deviations mean the proxy run is **not** a valid literature-constrained result.

## Hard environment blocker that stopped the strict path

```
import neuron  →  ModuleNotFoundError: No module named 'neuron'
pip install neuron  →  repeated 502 errors from the internal PyPI mirror
```

The compiled library (`libnrnmech.so`) existed on disk but could not be loaded without a working NEURON Python interface. Under the strict “no pure-Python substitute” rule the simulation was halted.

## Current status of the rebuild

- Strict literature-faithful path: **blocked** by missing NEURON package.
- Pragmatic pure-Python / Brian2 path: not yet authorized.
- Previous Runs 1–5 code and parameters: **do not reuse**.
