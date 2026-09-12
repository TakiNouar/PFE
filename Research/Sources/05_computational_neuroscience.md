# General Computational Neuroscience References

### Hodgkin and Huxley 1952 — The foundational HH model

> Hodgkin AL, Huxley AF.
> **"A quantitative description of membrane current and its application to conduction and excitation in nerve"**
> *Journal of Physiology*, 117(4), 1952.

**What it provides:** The original Hodgkin-Huxley equations for action potential generation, used as the biophysical substrate for every neuron in the simulation. Required citation for any HH-based simulation.

---

### Destexhe et al. 1994 — Dual-exponential synapse model

> Destexhe A, Mainen ZF, Sejnowski TJ.
> **"Synthesis of models for excitable membranes, synaptic transmission and neuromodulation using a common kinetic formalism"**
> *Journal of Computational Neuroscience*, 1994.

**What it provides:** The kinetic formalism for AMPA, NMDA, and GABA-A synaptic conductances using dual-exponential (rise + decay) functions. This is the synaptic model used in Feng et al. 2019 (Equations 4–6) and what the simulation is intended to implement.

---

### Wang and Buzsáki 1996 — Gamma oscillations, PING model

> Wang XJ, Buzsáki G.
> **"Gamma oscillation by synaptic inhibition in a hippocampal interneuronal network model"**
> *Journal of Neuroscience*, 16(20), 1996.

**What it provides:** The original description of the PING (pyramidal-interneuron network gamma) model, which Feng et al. 2019 identifies as the mechanism underlying BLA gamma oscillations. Relevant for understanding why the PV interneurons are the key element of the BLA circuit — they are not just inhibitory elements, they are rhythm generators.

---

### Destexhe et al. 2001 — High-conductance state

> Destexhe A, Rudolph M, Paré D.
> **"The high-conductance state of neocortical neurons in vivo"**
> *Nature Reviews Neuroscience*, 2001.

*(Also listed in primary references — included here for completeness.)*

**Key insight for the simulation:** In vivo, neurons exist in a "high-conductance state" where constant bombardment from background synaptic activity dramatically lowers membrane resistance and time constant. The Ornstein-Uhlenbeck conductance noise model approximates this state. Gaussian current injection does not, because it doesn't change the membrane's electrical properties. This is why the noise model change in Run 3 (from current noise to OU private drive) had such a large effect on synchrony.
