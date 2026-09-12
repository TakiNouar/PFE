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

These numbers were chosen for plausibility and computational tractability, not derived from a resolved analysis. The exploratory simulations in §19 suggest that population size interacts with connectivity scaling in ways that could make these specific numbers too small, too large, or simply untested for the intended dynamics (see open question [2]).

**5.2.2 Intended Biophysical Substrate**

- Single-compartment Hodgkin–Huxley neurons.
- Conductance-based synapses with axonal/synaptic delays.
- Short-term synaptic depression.
- An explicit dopamine variable and a slower noradrenaline-like arousal variable.
- Structured (non-random) connectivity following the primary loops in §4.7.

None of the above has been implemented as a coupled system. The informal simulations in §19 tested small, isolated pieces of this substrate (a single-region population with conductance-based recurrent synapses), not the full multi-structure network.

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
