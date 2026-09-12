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

**BLA note (updated September 2026):** The N_pyr=50, N_PV=12, N_SOM=8 baseline has been empirically tested in the BLA isolated simulation study (5 runs). It produces desynchronized graded activity (synchrony index < 0.5, CV > 0.3, active_frac > 0.60) during a threat stimulus at the baseline scale under fixed in-degree connectivity with private Ornstein-Uhlenbeck drive. PV and SOM interneurons produce approximately 4× suppression of Pyr mean rate when active. These counts remain subject to revision once Feng et al. 2019 parameters are fully applied in Run 6, but they are no longer unjustified guesses. Full detail in Research/reports/.

**All other regions:** Numbers chosen for plausibility and computational tractability only. Not derived from empirical analysis. Each region will be characterized in isolation (CeA next, then BLA→CeA two-region network) before full-network wiring begins.

**5.2.2 Intended Biophysical Substrate**

- **Pyramidal neurons (BLA):** 3-compartment Hodgkin–Huxley model (soma + apical dendrite + passive dendrite), following Feng et al. 2019 and Kim et al. 2013. Three compartments are required to correctly implement the Ca²⁺-dependent slow afterhyperpolarization current (I_sAHP) that produces spike frequency adaptation in real BLA principal cells. Omitting this compartmentalization removes the adaptation mechanism and produces unrealistically uniform firing throughout a sustained stimulus.

  If computational tractability requires it, a single-compartment model is acceptable as a first approximation, but the sAHP current must be explicitly included as a simplified somatic conductance (with the caveat that its interaction with Ca²⁺ will be less realistic). This simplification must be stated in any thesis chapter describing the simulation.

- **Interneurons (PV, SOM, VIP):** Single-compartment fast-spiking models. PV interneurons use standard HH Na/K conductances only. SOM interneurons additionally require a persistent Na⁺ current (I_NaP) and a hyperpolarization-activated cation current (I_H) to reproduce their spontaneous activity at low drive. VIP interneurons additionally require a D-current (slowly inactivating K⁺). These additional currents explain why SOM neurons were silent in BLA simulation Runs 1–3 — they received insufficient drive to fire without their intrinsic depolarizing currents. (Source: eLife 2024, "BLA oscillations enable fear learning".)

- Conductance-based synapses with axonal/synaptic delays.

- Short-term presynaptic depression on all synapse types (D_max=0.6, τ_D1=40ms, τ_D2=70ms for FSI→PN and PN→PN; source: Woodruff and Sah 2007).

- An explicit dopamine variable (VTA-sourced) and a slower noradrenaline-like arousal variable (design incomplete — see open question [6]).

- Structured (non-random) connectivity following the primary loops in §4.7, with distance-dependent connection probabilities for PN→PN (3% at <50μm, 2% at 50–100μm, 1% at 100–200μm, 0.5% at 200–600μm; source: Feng et al. 2019 citing Abatis et al. 2017).

**Synaptic kinetics for BLA** (from Feng et al. 2019, constrained by direct BLA electrophysiology):

| Connection | Receptor | Rise τ | Decay τ | Conductance |
| ---------- | -------- | ------ | ------- | ----------- |
| PN → PN    | AMPA     | 0.3 ms | 6.9 ms  | 1.0 nS      |
| PN → PN    | NMDA     | 3.7 ms | 125 ms  | 0.5 nS      |
| PN → FSI   | AMPA     | 0.1 ms | 2.4 ms  | 1.0 nS      |
| FSI → PN   | GABA-A   | 0.5 ms | 6.8 ms  | 0.6 nS      |

NMDA Mg²⁺ block: s(V) = [1 + 0.33 × exp(−0.06V)]⁻¹. E_GABA = −75 mV.

These parameters replace any earlier placeholder values used in exploratory simulations. Full derivation and sources in Research/Sources/.

None of the full multi-structure network has been implemented as a coupled system. The informal simulations in §19 and the BLA isolated study (Runs 1–5) tested isolated pieces of this substrate, not the complete architecture.

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
