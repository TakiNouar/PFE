# BLA Research Dossier — Overview

**Location:** `Simulation tests/BLA/Research/`  
**Scope:** Exhaustive reference on the basolateral amygdala (BLA) for the Emotionally Grounded Conversational AI PFE.  
**Sources:** Peer-reviewed literature (Feng et al. 2019, Kim et al. 2013, Woodruff & Sah 2007, McDonald series, Sah reviews, recent interneuron and dopamine papers) + ModelDB implementations.

---

## File index

| File | Topic |
|------|-------|
| `00_overview.md` | This file |
| `01_anatomy_and_subdivisions.md` | Gross anatomy, LA / BA / BM, density, species notes |
| `02_cell_types.md` | Principal neurons + full interneuron taxonomy (PV, SOM, CCK, VIP, etc.) |
| `03_local_connectivity.md` | Intrinsic microcircuit: who synapses on whom, probabilities, targets |
| `04_extrinsic_inputs_outputs.md` | Afferents (thalamus, cortex, HIP, VTA…) and efferents (CeA, PFC, NAc, vHPC…) |
| `05_synaptic_physiology.md` | AMPA / NMDA / GABA kinetics, Mg block, short-term plasticity |
| `06_intrinsic_physiology.md` | Currents, adaptation (sAHP), firing phenotypes |
| `07_oscillations_and_dynamics.md` | Gamma, theta, PING mechanism, spatial properties |
| `08_plasticity_and_learning.md` | Fear conditioning, LTP/LTD, interneuron plasticity |
| `09_neuromodulation.md` | Dopamine, noradrenaline, acetylcholine, serotonin |
| `10_computational_models.md` | Feng 2019, Kim 2013, later extensions — parameters and limitations |
| `11_functional_roles.md` | Threat evaluation, valence, extinction, projection-defined ensembles |
| `12_implications_for_simulation.md` | Direct mapping to the PFE isolated-BLA and multi-region design |

---

## Core identity of the BLA

The basolateral complex is the main sensory gateway and associative core of the amygdala. It evaluates the emotional significance of stimuli, supports fear and reward learning, and routes valence-specific signals to downstream effectors (CeA, NAc, PFC, hippocampus, brainstem). It is cortex-like in cellular composition (glutamatergic principal cells + diverse GABAergic interneurons) yet deeply embedded in limbic loops.

Everything that follows is organized so that a simulation can be built from published numbers rather than guesses.
