# Literature Mismatches — Parameters Used vs Feng et al. 2019 / Kim et al. 2013

**Primary source:** Feng et al. (2019) eNeuro, ModelDB 247968  
**Single-cell kinetics:** Kim et al. (2013), ModelDB 150288  
**Synaptic kinetics sources:** Mahanty & Sah (1998), Weisskopf et al. (1999), Woodruff & Sah (2007)

Every numerical value below that is marked “Literature” must be treated as the target for the next implementation. Values used in Runs 1–5 were guessed or inherited from generic HH defaults.

---

## Synaptic kinetics

| Connection | Receptor | Runs 1–5 | Literature (Feng Table 3) |
|------------|----------|----------|---------------------------|
| PN → PN    | AMPA     | τ_decay ≈ 2 ms, g arbitrary | rise 0.3 ms, **decay 6.9 ms**, g ≈ 1.0 nS |
| PN → PN    | NMDA     | τ 80–120 ms, **no Mg block** | rise 3.7 ms, **decay 125 ms**, g ≈ 0.5 nS, **s(V)=1/(1+0.33·exp(−0.06V))** |
| PN → FSI   | AMPA/NMDA| similar simplifications | AMPA rise 0.1 / decay 2.4 ms; NMDA same as above |
| FSI → PN   | GABA-A   | τ ≈ 5 ms, E = −70 mV | rise 0.5 ms, **decay 6.8 ms**, g ≈ 0.6 nS, **E = −75 mV** |
| FSI → FSI  | GABA-A   | — | rise 0.5 / decay 6.8 ms, g ≈ 0.2 nS |

**Impact of the AMPA error:** At typical BLA rates (ISI ~20–25 ms) a 2 ms AMPA conductance is gone long before the next spike. Recurrent excitation could not bridge volleys. This single error is the main reason after-discharge was unreachable with AMPA-only kinetics.

**Impact of missing Mg²⁺ block:** NMDA opened at all voltages and behaved like a constant current source, producing the observed ~85 % NMDA current fraction.

---

## Connectivity

| Projection | Runs 1–5 | Literature |
|------------|----------|------------|
| PN → PN    | Fixed in-degree K=3 (~6 % at N=50) | Distance-dependent: 3 % (<50 µm), 2 % (50–100), 1 % (100–200), 0.5 % (200–600) |
| FSI → PN   | Fixed K ~35 % | **34 %** unidirectional (matches) |
| PN → FSI   | approximate | 12 % uni + 16 % reciprocal |
| FSI → FSI  | approximate | 26 % total (includes gap junctions at ~8 %) |

Fixed-K over-dense excitation + scaling inhibition is the structural cause of the large-N collapse observed in Run 3.

---

## Neuron models & currents

| Item | Runs 1–5 | Literature |
|------|----------|------------|
| PN morphology | Single-compartment | **3-compartment** (soma + apical + passive dendrite) |
| Adaptation | None | **I_sAHP** (Ca-dependent slow AHP) required for spike-frequency adaptation |
| Other currents | Basic HH (Na, K, leak) | I_Na, I_Kdr, I_M, I_H, I_Ca, I_NaP, I_A, I_sAHP |
| FSI model | Generic HH | Specific fast-spiking kinetics (Kim et al.) |

Without I_sAHP the model neurons cannot slow their firing during sustained drive — they produce unadapted volleys.

---

## Noise & short-term plasticity

| Item | Runs 1–5 | Literature |
|------|----------|------------|
| Noise | Current injection (Gaussian) | **Conductance-based OU**, separate E and I components (Feng Table 7 / Destexhe-style) |
| Short-term depression | Absent | Present on all synapses (D_max≈0.6, τ_D1≈40 ms, τ_D2≈70 ms) |

Conductance noise changes effective membrane time constant and produces more realistic desynchronization. Short-term depression naturally reduces drive as cells fire and helps the network return toward baseline after stimulus offset.

---

## Bottom line for the next implementation

Any new BLA simulation that does not start from the Feng/Kim numbers (especially AMPA 6.9 ms, NMDA 125 ms + Mg block, multi-compartment + sAHP, conductance noise, distance-dependent connectivity, and dynamic STP) will re-create the same structural failures.
