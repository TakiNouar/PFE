# 07 — Oscillations and Network Dynamics

## Gamma (40–100 Hz, typically 50–70 Hz in BL)

- Observed in vivo in BLA during heightened vigilance and emotionally salient stimuli.
- Feng et al. 2019: biophysically realistic BL network **intrinsically generates intermittent gamma bursts** matching experimental LFP and spike–field statistics.
- Core mechanism: **PING** — reciprocal excitation–inhibition between PNs and PV-like fast-spiking interneurons.
- Connections among PNs and among FSIs further tune frequency and spatial extent.
- Gamma synchronizes PN ensembles and mediates competition: the strongest ensemble recruits the FSI network and suppresses weaker ones.
- Bursts are spatially restricted; entrainment depends on afferent connection count.

**State-tracking:** SOM and PV dynamically track behavioral-state transitions across fear conditioning and extinction in vivo, often in opposite directions (SOM decreases during CS in acquisition; PV increases). Local oscillatory state — shaped by SOM/PV balance — shifts between acquisition, expression, and extinction. (Báldi et al. 2025.)

## Other rhythms and Cattani et al. 2024

Cattani et al. (2024, *eLife*) extend the Feng-style architecture with SOM and VIP classes (NaP + H for SOM; D-current for VIP) and STDP:

- PV, SOM, and VIP each contribute distinct BLA rhythms (gamma, low theta, high theta respectively) and are each **individually necessary** for fear-circuit plasticity — removing any one class prevents formation of a dedicated fear circuit (non-substitutable).
- **Low theta (~3–6 Hz) is a biomarker of successful fear conditioning** in the model. High theta (~6–12 Hz) and gamma (>30 Hz) are also present; rhythm pattern predicts conditioning outcome.

For **Run 1** (isolated BLA, no plasticity), this is background. When multi-region learning begins, rhythm–plasticity links become testable predictions.

## Computational consequences for the PFE

- Local gamma is a substrate for binding and selective routing.
- Competition among PN ensembles is a plausible microcircuit implementation of valence / threat-priority selection.
- Intermittent gamma under realistic drive is **desirable evidence** of healthy recurrent PN–PV dynamics. For isolated Run 1 it is a **diagnostic**, not a hard pass/fail gate. Scaled nets may not match Feng’s ~27k-cell gamma statistics; graded rates, functional inhibition, and correct kinetics take priority.
