# Simplified BLA Model — Synapses and Cells (Gates S2 and S1) — October–November 2026

**Dates:** 2026-10-15 (synapses, first cell fits), 2026-10-21 (cell model completed, gate S1 run). Report written 2026-11-12.
**Spec:** `Research/architecture/14_simplified_model.md`. **Deviations:** `simplified/deviations.md` (S-DEV-1 to S-DEV-3).
**Code:** `Simulations/BLA/simplified/bla_simple/`. **Results:** `Simulations/BLA/simplified/outputs/` (S2_synapses, S1_cells, S1_fit_*). **Fitted values:** `simplified/config/`.

---

## 1. Synapses — gate S2: PASS with 1 approved exception

Each of Feng's five synapse types is a rise-and-decay conductance whose peak, charge and decay equal Feng's exactly (`config/synapses_fitted.json`). Two more ingredients make trains match:
- **Saturation:** Feng's pulse scheme cannot reopen receptors that are already open. A spike adds only what the presynaptic cell's own response is not already headed for, up to Feng's saturation level computed from his kinetic constants (NMDA 1.01, AMPA 1.00, GABA 1.31–1.43 times one pulse).
- **Depression:** Feng's d1, d2, time constants and floors, applied per spike as in Varela et al. 1997 (the source Feng cites).

Both are kept once per presynaptic cell, so they cost nothing per connection. The comparison is against Feng's own files, run in NEURON with the receiving compartment clamped at −70 mV:

| Spike pattern | Largest difference (peak or charge) |
|---|---|
| Single spikes, 5 Hz | ≤ 2.4 % |
| Physiological random trains (no interval < 5 ms), 20 and 50 Hz | ≤ 2.8 % |
| Regular 20 and 50 Hz (reported) | ≤ 5.1 % |
| 1 ms doublets (reported; no BLA cell fires that fast) | NMDA +17 %, others ≤ 9 % |

**Approved exception** (M. T. Nouar, 2026-10-15; `config/gate_exceptions.json`): FSI→PN GABA-A on the reference Poisson 20 Hz train, peak +5.9 %. That train has no refractory period and contains intervals of 1.5–3 ms, which an FSI cannot produce.

## 2. Cells — gate S1: 69 of 71 checks pass (2 open, decision pending)

### The cell model as it stands

- **FSI:** one compartment with an exponential spike onset and a refractory period; no adaptation; no depolarization block (S-DEV-2).
- **PN, PN-A and PN-C:** soma plus one passive dendrite.
  - **Soma:** exponential spike onset, refractory period, and a fast spike-triggered potassium conductance (E_K = −80 mV, Feng's template).
  - **PN-A only:** Feng's slow AHP, copied from his `sahp.mod`. It opens with calcium along a Hill curve (exponent 3.04 from his rate functions; calcium decay 1,000 ms from his pool), but only while the soma is above a gate voltage. The gate voltage (−64.2 mV; Feng −65) and gate time (163 ms; Feng 48) are fitted, because the reset cell has no spike shape.
  - **Dendrite:** receives all excitatory synapses. It gets a back-propagating spike kick of 35 mV at each somatic spike, and a dendritic input gain kD = 3.3 standing in for the sodium channels of Feng's apical dendrite.
- **Passive values are set exactly, not fitted:** resting potential, input resistance (over Feng's −0.05 nA step, with the spike-onset term included) and slowest time constant.
- **Everything else was fitted with differential evolution in GeNN:**
  - **Stage 1:** current ladder, latencies, PN-C spike intervals, 4 s steps, PN-A silences.
  - **Stage 2:** the stage-1 targets plus firing under Feng's noise and the dendritic-input test.

### Why the model took this form (each step forced by a measurement)

| Problem found | Fix |
|---|---|
| PN-C burst (reset above threshold) | Reset bounded below threshold; PN-C spike intervals added as targets |
| PN-C firing curve too steep (+21 % at 1 nA) with fixed adaptation currents | Adaptation as potassium conductances (±6 %) |
| Resting potential and input resistance off by up to 4 mV and 12 % | The spike-onset term is included when the passive values are derived |
| Dendritic input too weak in both types (−30 % to −57 %) | Back-propagating spike kick; dendritic gain kD |
| PN-A's pauses barely shortened under input (Feng's: intervals down to 340 ms, no bursts) | Feng's calcium- and voltage-gated sAHP, with gate voltage and time fitted |

### Results (exact CPU mode, double precision, dt 0.1 ms)

| Check | Simplified | Feng | Result |
|---|---|---|---|
| Resting potential (PN / FSI) | −70.2 / −70.0 mV | −70.2 / −70.0 mV | pass |
| Input resistance (PN / FSI) | 136.2 / 371.8 MΩ | 136.2 / 371 MΩ | pass |
| Time constant (PN slowest / FSI) | 29.1 / 20.0 ms | 30.9 / 19.9 ms | pass |
| 63 % rise time, PN (reported only) | 23.5 ms | 34.9 ms | not gated: Feng's is longer than his own slowest time constant because of Ih; no passive two-compartment cell can do that |
| PN-C spikes, 0.1–1.0 nA | 10 / 14 / 17 / 19 / 23 / 26 / 29 | 10 / 15 / 18 / 20 / 22 / 25 / 28 | pass |
| PN-C, 4 s steps | 76 and 114 | 78 and 110 | pass |
| FSI spikes, 0.1–1.5 nA | 25 / 61 / 89 / 111 / 145 / 169 / 189 / 222 | 24 / 61 / 89 / 111 / 144 / 168 / 187 / 221 | pass |
| Latencies (all types, all currents) | within 10 % except one | | **1 fail:** PN-A at 1.5 nA, 3.7 vs 3.3 ms |
| PN-A: one spike per 1 s step | 1 at every current | 1 | pass |
| PN-A 4 s gaps | 1,953 / 1,675 / 1,847 ms | 2,095 / 1,657 / 1,639 ms | pass (≤ 15 %) |
| Noise only, PN-A | 0.34 Hz, CV 0.23 | 0.345 Hz, CV 0.21 | pass |
| Noise only, PN-C | 1.52 Hz, CV 0.86 | 1.54 Hz, CV 0.79 | pass |
| Noise only, FSI | silent | silent | pass |
| Dendritic input, PN-C | 3.66 Hz | 3.19 Hz | pass (+14.7 %) |
| Dendritic input, PN-A | **0.50 Hz** | **0.70 Hz** | **fail (−28 %)** |

Feng's references: Block A (`single_cells_full.json`, `passive_tau.json`), the sharper stage-2 reference (`simulation/outputs/blockA/stage2_reference.json`: 10 cells × 60 s of noise; dendritic input over 3 noise seeds) and Feng's PN-A spike times under input (`drive_spike_times_seed1.json`).

### Decision pending (M. T. Nouar)

- **(a) Recommended:** approve both failures as recorded exceptions and build the network. Gates S3 and S4 will show whether PN-A's weaker response to dendritic input matters at network level. Feng's network PN-A (0.51 Hz in Block B) already fires above rat type-1 cells (0.21 Hz).
- **(b)** One more targeted PN-A attempt first (for example, its calcium decay time). About 30–45 min, with no guarantee.

## 3. Environment note

Windows 11 **Smart App Control** switched itself from evaluation to enforcing between 2026-10-15 and 2026-10-21, and blocked the locally built GeNN library. M. T. Nouar turned it off on 2026-10-21. NEURON with Feng's compiled files was not affected.
