# 09 — Code Module Map (no source code)

Recommended package layout so that the architecture above maps cleanly onto files. Names are suggestive; the important point is separation of concerns.

```
bla_sim/
├── config/
│   ├── full_parameters.json     # all numeric values (Feng/Kim tables) + citation keys
│   └── seeds.json               # global seed + derived streams
├── neurons/
│   ├── pn.py / pn.hoc           # multi-compartment PN + currents
│   ├── fsi.py / fsi.hoc         # PV-like
│   └── som.py                   # SOM-like (phase-1 = FSI kinetics)
├── synapses/
│   ├── ampa_nmda.py             # ModelDB kinetic scheme (or logged dual-exp approx.) + dynamic Mg block + weight W
│   ├── gaba_a.py
│   └── stp.py                   # two-factor depression state
├── network/
│   ├── placement.py             # volume, density, min-distance
│   ├── connectivity.py          # distance-dependent + fixed-p rules, lognormal weights, delays
│   └── builder.py               # wires cells + synapses + STP
├── drive/
│   ├── ou_noise.py              # Feng Table 7 coefficients
│   └── sensory_drive.py         # private/common stimulus
├── protocol/
│   ├── runner.py                # time loop / native advance
│   ├── scale_sweep.py
│   └── diagnostics.py           # AMPA-off, inhibition-off, …
├── metrics/
│   ├── rates.py
│   ├── synchrony.py
│   ├── isi_cv.py
│   ├── afterdischarge.py
│   └── suppression.py
├── io/
│   ├── write_parameters.py
│   ├── write_tables.py
│   └── write_spikes.py
└── main.py                      # single entry point, reads config, runs protocol
```

Place the package under `Simulations/BLA/simulation/`. If the NEURON path is chosen, the ModelDB `.mod` files go in a `mechanisms/` folder there and are compiled with `nrnivmodl`. Keep the path free of spaces.

The run package writes `full_parameters.json` (a resolved copy of `config/full_parameters.json` plus seed, volume and mechanism paths) next to its outputs, as required by `08_metrics_and_outputs.md`.

## Module responsibilities

- **config** — single source of truth for numbers; nothing hardcoded elsewhere.
- **neurons** — morphology + mechanism insertion only; no network knowledge.
- **synapses** — pure kinetic objects; STP state lives here.
- **network** — geometry and graph construction; returns lists of NetCon / synapse objects.
- **drive** — noise and stimulus; never touches connectivity.
- **protocol** — orchestration only.
- **metrics** — pure functions of spike times / currents; no side effects.
- **io** — serialization; the summary writer may only read the metric tables.

## Forbidden coupling

- Do not put kinetic constants inside the runner.
- Do not recompute connection probabilities inside the metric code.
- Do not generate random numbers outside the seeded streams defined in `config/seeds.json`.
