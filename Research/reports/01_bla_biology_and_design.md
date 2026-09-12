## 3. BLA Biology and Design

### 3.1 Blueprint Specification

From Design Blueprint v2.4 (`02_biophysical_substrate.md`):

| Sub-population | Proposed N | Role |
|---|---|---|
| BLA pyramidal (excitatory) | 50 | Principal cells — carry the main signal |
| BLA PV-like (fast inhibitory) | 12 | Fast perisomatic inhibition |
| BLA SOM-like (slow inhibitory) | 8 | Slower dendritic-targeting modulation |
| **Total BLA** | **70** | |

External inputs: fast sensory route (thalamic-like, low latency) targeting BLA primarily; slow cortical route (higher latency, higher detail) targeting BLA, INS, and ACC. Neither route was implemented in isolation — only step-current approximations were used.

### 3.2 What the Literature Actually Specifies

Research conducted after the 5 runs revealed that validated, literature-grounded parameters already exist for BLA and were not used. The primary reference is **Feng et al. 2019** (eNeuro), the first large-scale biophysically and anatomically realistic model of the basolateral amygdala nucleus, with all parameters constrained by published in vitro and in vivo electrophysiology.

**Key parameters from Feng et al. 2019 (Table 3) — not used in any of Runs 1–5:**

| Connection | Receptor | Rise τ (ms) | Decay τ (ms) | Conductance (nS) |
|---|---|---|---|---|
| PN → PN | AMPA | 0.3 | **6.9** | 1.0 |
| PN → PN | NMDA | 3.7 | **125** | 0.5 |
| PN → FSI | AMPA | 0.1 | 2.4 | 1.0 |
| FSI → PN | GABA-A | 0.5 | **6.8** | 0.6 |

**Critical discrepancies with what was used:**

| Parameter | Runs 1–5 (guessed) | Literature value | Impact |
|---|---|---|---|
| AMPA τ_decay (PN→PN) | 2 ms | **6.9 ms** | Too fast — AMPA decayed between spikes, no sustained recurrent drive |
| NMDA τ_decay | 80–120 ms (guessed) | **125 ms** | Close but still wrong, and missing Mg²⁺ block |
| NMDA Mg²⁺ block | None | **s(V) = [1+0.33e^{−0.06V}]⁻¹** | NMDA was open at all voltages — became a constant current source |
| E_GABA | −70 mV | **−75 mV** | Inhibitory driving force underestimated |
| PN→PN connectivity | Fixed K=3 (~6%) | **Distance-dependent 0.5–3%** | Over-dense recurrent excitation |
| Noise model | Current injection (Gaussian) | **Conductance-based OU (separate E/I)** | Current noise doesn't change membrane conductance |
| Short-term depression | None | **D_max=0.6, τ_D1=40ms, τ_D2=70ms** | No fatigue mechanism |
| sAHP current | None | **Required for spike adaptation** | Neurons couldn't slow firing during sustained drive |
