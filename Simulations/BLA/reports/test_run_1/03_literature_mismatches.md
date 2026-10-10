# Literature Mismatches — Parameters Used vs Feng et al. 2019 / Kim et al. 2013

**Primary source:** Feng et al. (2019) eNeuro, ModelDB 247968
**Single-cell kinetics:** Kim et al. (2013), ModelDB 150288
**Upstream sources Feng cites:** Mahanty & Sah 1998 + Guzman et al. 2016 (AMPA); Weisskopf et al. 1999 (NMDA); Galarreta & Hestrin 1997 (GABA-A); Woodruff & Sah 2007 (FSI connectivity, FSI↔PN depression); Silberberg et al. 2004 (PN→PN depression); Destexhe et al. 2001 (noise); Zador et al. 1990 (Mg block); Abatis et al. 2017 SfN poster (PN→PN distance bands).

Values used in Runs 1–5 were guessed or taken from generic HH defaults. The current numeric targets (with full provenance) live in `Research/Sources/01_primary_bla_references.md` and `Simulations/BLA/Research/architecture/`. This file records what was **wrong**.

---

## Synaptic kinetics

| Connection | Receptor | Runs 1–5 | Literature (Feng Table 3) |
|------------|----------|----------|---------------------------|
| PN → PN    | AMPA     | τ_decay ≈ 2 ms, g arbitrary | rise 0.3 ms, **decay 6.9 ms**, g 1.0 nS × weight |
| PN → PN    | NMDA     | τ 80–120 ms, **no Mg block** | rise 3.7 ms, **decay 125 ms**, g 0.5 nS × weight, **s(V)=1/(1+0.33·exp(−0.06V))** |
| PN → FSI   | AMPA/NMDA| similar simplifications | AMPA rise 0.1 / decay 2.4 ms; NMDA as above |
| FSI → PN   | GABA-A   | τ ≈ 5 ms, E = −70 mV | rise 0.5 ms, **decay 6.8 ms**, g 0.6 nS × weight, **E = −75 mV** |
| FSI → FSI  | GABA-A   | — | rise 0.5 / decay 6.8 ms, g 0.2 nS × weight |
| all        | weights  | single fixed value | per-synapse lognormal multiplier (Table 3 “strength”) |
| all        | delay    | fixed | distance-dependent: d / (1 mm/ms) + 0.8 ms ± 0.1 ms |

**Impact of the AMPA error:** At typical BLA rates (ISI ~20–25 ms) a 2 ms AMPA conductance is gone long before the next spike, so recurrent excitation could not bridge volleys. This single error is the main reason after-discharge was unreachable with AMPA-only kinetics.

**Impact of missing Mg²⁺ block:** NMDA was open at all voltages and behaved like a constant current source, producing the observed ~85 % NMDA current fraction.

---

## Connectivity

| Projection | Runs 1–5 | Literature |
|------------|----------|------------|
| PN → PN    | Fixed in-degree K=3 (~6 % at N=50) | Distance-dependent: 3 % (<50 µm), 2 % (50–100), 1 % (100–200), 0.5 % (200–600) |
| FSI → PN   | Fixed K ~35 % | **34 %** unidirectional (close) |
| PN → FSI   | approximate | 12 % uni + 16 % reciprocal |
| FSI → FSI  | approximate | 26 % chemical; separately, gap junctions in 8 % of pairs |

Fixed-K over-dense excitation plus scaling inhibition is the structural cause of the large-N collapse observed in Run 3.

---

## Neuron models & currents

| Item | Runs 1–5 | Literature |
|------|----------|------------|
| PN morphology | Single-compartment | **3-compartment** (soma + apical + passive dendrite) |
| Adaptation | None | **I_sAHP** (Ca-dependent slow AHP) required for spike-frequency adaptation |
| Other currents | Basic HH (Na, K, leak) | I_Na, I_Kdr, I_M, I_H, I_Ca, I_NaP, I_A, I_sAHP |
| FSI model | Generic HH | Specific fast-spiking kinetics (Kim et al.) |

Without I_sAHP, model neurons cannot slow their firing during sustained drive, so they produce unadapted volleys.

---

## Noise & short-term plasticity

| Item | Runs 1–5 | Literature |
|------|----------|------------|
| Noise | Current injection (Gaussian) | **Conductance-based OU**, separate E and I (Feng Table 7, Destexhe et al. 2001 formalism) |
| Short-term depression | Absent | Present, per connection (Feng Table 4): FSI→PN floor 0.6, PN→FSI 0.7, PN→PN 0.5; d1/d2 0.9/0.95; τ 40/70 ms |

Conductance noise changes the effective membrane time constant and desynchronizes more realistically. Short-term depression reduces drive as cells fire and helps the network return toward baseline after stimulus offset.

---

## Bottom line for the next implementation

Any new BLA simulation that does not start from the Feng/Kim numbers will re-create the same structural failures. The key ones are AMPA 6.9 ms, NMDA 125 ms with Mg block, multi-compartment PNs with sAHP, conductance noise, distance-dependent connectivity, weight multipliers and dynamic STP.
