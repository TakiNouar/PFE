## 5. Biophysical Substrate

### 5.1 The Hodgkin–Huxley Equation — Every Neuron

Every neuron in the simulation is intended to solve this equation (single-compartment form shown) at a fixed timestep of 0.05 ms, the step used by Feng et al. 2019 and the BLA architecture:

```
C (dV/dt) = −g_Na m³h(V − E_Na) − g_K n⁴(V − E_K) − g_L(V − E_L) + I
```

- V — membrane voltage
- C — membrane capacitance
- g_Na, g_K — sodium / potassium conductance
- m, h, n — gating variables (ion channel state)
- I — input current from connected neurons

### 5.2 Reference Population Target (Phase-4 Scope)

**This section was previously titled "Current Implemented Limbic Core" and described as a working prototype. That was incorrect — nothing has been built. The table below is a proposed starting-point population size for the first implementation phase, not a measured or validated configuration.**

**5.2.1 Population Inventory (Target, Not Yet Built)**

| Population | Proposed N | Notes |
|---|---|---|
| BLA principal (PN-A + PN-C) | TBD (U26) | Excitatory principal cells |
| BLA FSI (PV-like) | TBD (U26) | Fast inhibition |
| CeA | 20 | Output population |
| PFC | 30 | Suppression / control |
| VTA | 15 | Dopamine source |
| NAc | 25 | Incentive target |
| Hippocampus | 35 | Context / memory |
| Insula | 20 | Interoception |
| Anterior Cingulate | 25 | Conflict / empathy |
| Hypothalamus | 15 | Raw drive |
| **Total** | **185 + BLA** | Proposed scaled starting point |

**BLA note (updated 2026-10-14):** BLA **Run 1** is an offline test of Feng et al. 2019 at Feng's own reduced size: 640 PN-A / 260 PN-C / 100 FSI, wired to Feng's inputs per cell. Measured cost made the full-detail network too slow at that size (about 1 hour of computing per simulated second), so Run 1 has two levels: Feng's NEURON files unchanged for single cells and a 200-cell reference network, and a one-piece PN with event-driven synapses for the 1,000-cell run, checked against the reference. The earlier 50 / 12 / 8 default gave each principal cell under one recurrent input and was dropped. The BLA size in the live network is decided after the Run 1 speed benchmark (U26). See `Simulations/BLA/Research/architecture/` and `Simulations/BLA/reports/04_run1_redesign_oct2026.md`.

**All other regions:** Numbers chosen for plausibility and computational tractability only. Not derived from empirical analysis. Each region will be characterized in isolation (CeA next, then BLA→CeA two-region network) before full-network wiring begins.

**5.2.2 Intended Biophysical Substrate**

- **Pyramidal neurons (BLA):** Feng et al. 2019 principal cells: soma + apical dendrite + distal dendrite, **16 segments** in Feng's code, with Na, Kdr, A, M, h, Ca, NaP, sAHP and leak currents. The adaptation current (I_sAHP) and its Ca²⁺ pool (τ = 1 s) sit **in the soma only**; Feng needs the dendrites mainly for synapse placement and his LFP calculation. Without I_sAHP, cells fire unrealistically uniformly during a sustained stimulus.

  BLA Run 1 uses Feng's full templates unchanged at its reference level, and a two-piece cell built from them (Feng's exact soma, with its sAHP and Ca²⁺ pool, plus one lumped dendrite) at its main level. Measured cost of Feng's cell: 5.2 µs per segment per time step on the project laptop (2026-10-14). Any reduced cell, in Run 1 or the live engine, must match Feng's full cell's single-cell recordings, and the simplification must be stated in the thesis.

- **Interneurons (PV, SOM, VIP):** Single-compartment fast-spiking models. PV interneurons use standard HH Na/K conductances only. SOM interneurons additionally require a persistent Na⁺ current (I_NaP) and a hyperpolarization-activated cation current (I_H) to reproduce their spontaneous activity at low drive. VIP interneurons additionally require a D-current (slowly inactivating K⁺). (Source: Cattani et al. 2024, eLife.)

- Conductance-based synapses with axonal/synaptic delays.

- **Short-term presynaptic depression, per connection type (Feng et al. 2019, Table 4):**
  - FSI→PN: D_max = **0.6** (Woodruff & Sah 2007, BLA)
  - PN→FSI: D_max = **0.7** (Woodruff & Sah 2007, BLA)
  - PN→PN: D_max = **0.5** (**Silberberg et al. 2004, neocortex** — Feng states BLA-specific PN–PN depression data were unavailable; this is an explicit approximation)
  - All connections: d1/d2 = 0.9/0.95, τ_D1/τ_D2 = 40/70 ms

- An explicit dopamine variable (VTA-sourced) and a slower noradrenaline-like arousal variable (design incomplete — see open question [6]).

- Structured (non-random) connectivity following the primary loops in §4.7, with distance-dependent connection probabilities for PN→PN (3% at <50μm, 2% at 50–100μm, 1% at 100–200μm, 0.5% at 200–600μm; source: Feng et al. 2019, based on an SfN poster by Abatis et al. 2017) and distance-dependent synaptic delays (0.8 ms minimum + 1 mm/ms conduction).

**Synaptic kinetics for BLA** (Feng et al. 2019 Table 3; upstream sources as cited by Feng):

| Connection | Receptor | Rise τ | Decay τ | Conductance | Upstream (Feng cites) |
| ---------- | -------- | ------ | ------- | ----------- | --------------------- |
| PN → PN    | AMPA     | 0.3 ms | 6.9 ms  | 1.0 nS      | Mahanty & Sah 1998; Guzman et al. 2016 |
| PN → PN    | NMDA     | 3.7 ms | 125 ms  | 0.5 nS      | Weisskopf, Bauer & LeDoux 1999 |
| PN → FSI   | AMPA     | 0.1 ms | 2.4 ms  | 1.0 nS      | Mahanty & Sah 1998; Guzman et al. 2016 |
| PN → FSI   | NMDA     | 3.7 ms | 125 ms  | 0.5 nS      | Weisskopf, Bauer & LeDoux 1999 |
| FSI → PN   | GABA-A   | 0.5 ms | 6.8 ms  | 0.6 nS      | Galarreta & Hestrin 1997 |
| FSI → FSI  | GABA-A   | 0.5 ms | 6.8 ms  | 0.2 nS      | Galarreta & Hestrin 1997 |

Each conductance is multiplied by a per-synapse lognormal weight (Feng Table 3 “strength”). NMDA Mg²⁺ block: s(V) = [1 + 0.33 × exp(−0.06V)]⁻¹ (Zador et al. 1990). E_GABA = −75 mV.

These parameters replace any earlier placeholder values. Full provenance in `Research/Sources/01_primary_bla_references.md`; the binding implementation spec is `Simulations/BLA/Research/architecture/`.

None of the full multi-structure network has been implemented as a coupled system. Archived isolated attempts and the biology/architecture dossiers under `Simulations/BLA/` inform the clean Run 1 campaign.

**5.2.3 What This Phase Is Intended To Establish**

- Distinct BLA and CeA populations.
- A measurable PFC → CeA suppression pathway.
- A VTA → NAc dopamine route.
- Hypothalamic drive onto amygdala-related populations.
- A cross-structure recurrent mesh covering the nine structures in §5.2.1 (including the dual amygdala). PAG is deferred to a later phase (§5.2.4).

**5.2.4 Deferred Beyond This Phase**

- PAG / brainstem expression stage.
- Explicit dual sensory routes (fast vs. slow) as separate input channels.
- A robust, independently tunable arousal dimension.
- Long-timescale inertia, sensitization, and suppression fatigue.
- The affective-tag memory system.
- Continuous real-time operation coupled to an LLM translator.

These are scope decisions for later phases, not gaps in an existing system.
