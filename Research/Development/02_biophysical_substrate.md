## 5. Biophysical Substrate

### 5.1 The Hodgkin–Huxley Equation — Every Neuron

Every neuron in the simulation is intended to solve this equation at each 0.1 ms timestep:

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
| BLA pyramidal | 50 | Excitatory principal cells |
| BLA PV-like | 12 | Fast inhibition |
| BLA SOM-like | 8 | Slower dendritic-like inhibition |
| CeA | 20 | Output population |
| PFC | 30 | Suppression / control |
| VTA | 15 | Dopamine source |
| NAc | 25 | Incentive target |
| Hippocampus | 35 | Context / memory |
| Insula | 20 | Interoception |
| Anterior Cingulate | 25 | Conflict / empathy |
| Hypothalamus | 15 | Raw drive |
| **Total** | **255** | Proposed scaled starting point |

**BLA note (updated September 2026):** Default for the clean **Run 1** campaign is N_pyr=50, N_PV=12, N_SOM=8. An alternate 150/112/108 composition appeared in archived material only; it is **not** interchangeable with 50/12/8 (different E/I ratio) and is not used. Architecture: distance-dependent connectivity and Feng kinetics — see `Simulation tests/BLA/Research/architecture/`.

**All other regions:** Numbers chosen for plausibility and computational tractability only. Not derived from empirical analysis. Each region will be characterized in isolation (CeA next, then BLA→CeA two-region network) before full-network wiring begins.

**5.2.2 Intended Biophysical Substrate**

- **Pyramidal neurons (BLA):** 3-compartment Hodgkin–Huxley model (soma + apical dendrite + passive dendrite), following Feng et al. 2019 and Kim et al. 2013. Three compartments are required to correctly implement the Ca²⁺-dependent slow afterhyperpolarization current (I_sAHP) that produces spike frequency adaptation in real BLA principal cells. Omitting this compartmentalization removes the adaptation mechanism and produces unrealistically uniform firing throughout a sustained stimulus.

  If computational tractability requires it, a single-compartment model is acceptable as a first approximation, but the sAHP current must be explicitly included as a simplified somatic conductance (with the caveat that its interaction with Ca²⁺ will be less realistic). This simplification must be stated in any thesis chapter describing the simulation.

- **Interneurons (PV, SOM, VIP):** Single-compartment fast-spiking models. PV interneurons use standard HH Na/K conductances only. SOM interneurons additionally require a persistent Na⁺ current (I_NaP) and a hyperpolarization-activated cation current (I_H) to reproduce their spontaneous activity at low drive. VIP interneurons additionally require a D-current (slowly inactivating K⁺). (Source: Cattani et al. 2024, eLife.)

- Conductance-based synapses with axonal/synaptic delays.

- **Short-term presynaptic depression, per connection type (Feng et al. 2019, Table 4):**
  - FSI→PN: D_max = **0.6** (Woodruff & Sah 2007, BLA)
  - PN→FSI: D_max = **0.7** (Woodruff & Sah 2007, BLA)
  - PN→PN: D_max = **0.5** (**Silberberg et al. 2004, neocortex** — Feng states BLA-specific PN–PN depression data were unavailable; this is an explicit approximation)
  - All connections: d1/d2 = 0.9/0.95, τ_D1/τ_D2 = 40/70 ms

- An explicit dopamine variable (VTA-sourced) and a slower noradrenaline-like arousal variable (design incomplete — see open question [6]).

- Structured (non-random) connectivity following the primary loops in §4.7, with distance-dependent connection probabilities for PN→PN (3% at <50μm, 2% at 50–100μm, 1% at 100–200μm, 0.5% at 200–600μm; source: Feng et al. 2019 citing Abatis et al. 2017).

**Synaptic kinetics for BLA** (Feng et al. 2019 Table 3; upstream sources as cited by Feng):

| Connection | Receptor | Rise τ | Decay τ | Conductance | Upstream (Feng cites) |
| ---------- | -------- | ------ | ------- | ----------- | --------------------- |
| PN → PN    | AMPA     | 0.3 ms | 6.9 ms  | 1.0 nS      | Mahanty & Sah 1998; Guzman et al. 2016 |
| PN → PN    | NMDA     | 3.7 ms | 125 ms  | 0.5 nS      | (confirm Feng footnote) |
| PN → FSI   | AMPA     | 0.1 ms | 2.4 ms  | 1.0 nS      | Mahanty & Sah 1998; Guzman et al. 2016 |
| FSI → PN   | GABA-A   | 0.5 ms | 6.8 ms  | 0.6 nS      | Galarreta & Hestrin 1997 |

NMDA Mg²⁺ block: s(V) = [1 + 0.33 × exp(−0.06V)]⁻¹ (Zador et al. 1990). E_GABA = −75 mV.

These parameters replace any earlier placeholder values. Full provenance in `Research/Sources/`.

None of the full multi-structure network has been implemented as a coupled system. Archived isolated attempts and the biology/architecture dossiers under `Simulation tests/BLA/` inform the clean Run 1 campaign.

**5.2.3 What This Phase Is Intended To Establish**

- Distinct BLA and CeA populations.
- A measurable PFC → CeA suppression pathway.
- A VTA → NAc dopamine route.
- Hypothalamic drive onto amygdala-related populations.
- A cross-structure recurrent mesh covering all ten structures (including the dual amygdala and PAG).

**5.2.4 Deferred Beyond This Phase**

- PAG / brainstem expression stage.
- Explicit dual sensory routes (fast vs. slow) as separate input channels.
- A robust, independently tunable arousal dimension.
- Long-timescale inertia, sensitization, and suppression fatigue.
- The affective-tag memory system.
- Continuous real-time operation coupled to an LLM translator.

These are scope decisions for later phases, not gaps in an existing system.
