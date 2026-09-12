# 07 — Oscillations and Network Dynamics

## Gamma (40–100 Hz, typically 50–70 Hz in BL)

- Observed in vivo in BLA during states of heightened vigilance and during emotionally salient stimuli.
- Feng et al. 2019 demonstrated that a biophysically realistic BL network **intrinsically generates intermittent gamma bursts** whose statistics match experimental LFPs and spike–field coupling.
- Core mechanism: **PING** — reciprocal excitation–inhibition between PNs and PV-like fast-spiking interneurons.
- Connections among PNs and among FSIs further tune frequency and spatial extent.
- Gamma synchronizes PN ensembles and mediates competition: the currently strongest ensemble recruits the FSI network and suppresses weaker ensembles.
- Bursts are spatially restricted; entrainment of a given neuron depends on the number of afferent connections it receives.

## Other rhythms

- Theta-band activity is also present and interacts with gamma (theta–gamma coupling) during fear and safety states.
- Later models (e.g. 2024 eLife-style extensions) incorporate VIP and SOM currents to generate a richer set of oscillatory regimes relevant to fear learning.

## Computational consequences for the PFE

- Local gamma provides a natural substrate for binding and for selective routing of information to downstream targets.
- Competition among PN ensembles is a plausible microcircuit implementation of valence or threat-priority selection.
- Intermittent gamma under realistic drive is **desirable evidence** that recurrent PN–PV dynamics are healthy. It is a **diagnostic**, not a hard pass/fail gate for isolated Run 1 (see `architecture/10_validation_gates.md`). Scaled populations may not reproduce every statistic of Feng’s ~27 000-cell model; graded desynchronized rates, functional inhibition, and correct kinetics take priority.
