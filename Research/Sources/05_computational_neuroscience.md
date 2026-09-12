# General Computational Neuroscience References

### Hodgkin and Huxley 1952 — The foundational HH model

> Hodgkin AL, Huxley AF.
> **"A quantitative description of membrane current and its application to conduction and excitation in nerve"**
> *Journal of Physiology*, 117(4), 1952.

**Provides:** The original HH equations used as the biophysical substrate for every neuron in the simulation.

---

### Destexhe et al. 1994 — Dual-exponential synapse model

> Destexhe A, Mainen ZF, Sejnowski TJ.
> **"Synthesis of models for excitable membranes, synaptic transmission and neuromodulation using a common kinetic formalism"**
> *Journal of Computational Neuroscience*, 1994.

**Provides:** Dual-exponential (rise + decay) kinetic formalism for AMPA, NMDA and GABA-A conductances used in Feng et al. (Equations 4–6).

---

### Wang and Buzsáki 1996 — Interneuron-network gamma (ING)

> Wang XJ, Buzsáki G.
> **"Gamma oscillation by synaptic inhibition in a hippocampal interneuronal network model"**
> *Journal of Neuroscience*, 16(20), 1996.

**Provides:** Classic **ING** (interneuron-only) gamma model. Foundational background for gamma oscillation modelling and cited by Feng et al.  
**Important distinction:** The mechanism demonstrated in Feng et al. 2019 for BLA is **PING** (pyramidal–interneuron network gamma), which requires reciprocal PN↔FSI interactions. Formal PING descriptions appear in Traub et al. (1997) and Whittington et al. (1997). Do not describe Wang & Buzsáki 1996 as the PING source.

---

### Destexhe et al. 2003 — High-conductance state

> Destexhe A, Rudolph M, Paré D.
> **"The high-conductance state of neocortical neurons in vivo"**
> *Nature Reviews Neuroscience*, 4:739–751, 2003.
> DOI: 10.1038/nrn1198

**Provides:** Framework for the point-conductance (OU) noise model used in Feng Table 7. (Year corrected from earlier 2001 listings; a different Destexhe 2001 paper exists with different co-authors.)

**Key insight:** In vivo high-conductance state lowers effective membrane resistance and time constant. Conductance-based noise captures this; pure current injection does not.
