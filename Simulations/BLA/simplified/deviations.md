# Deviations of the Simplified BLA Model from Feng et al. 2019

Spec: `Simulations/BLA/Research/architecture/14_simplified_model.md`. The detailed model's own deviations (DEV-001 to DEV-007: wiring, code values, inputs) are in `Simulations/BLA/simulation/deviations.md` and apply here too.

Each entry: what differs, why, the source of the substitute, and the gate that checks it.

## S-DEV-3 — Synapse kinetics: fitted rise-and-decay conductances (implemented 2026-10-15)

- **What:**
  - **Shape:** each receptor (PN→PN AMPA and NMDA, PN→FSI AMPA and NMDA, FSI→PN GABA-A, FSI→FSI GABA-A) is a rise-and-decay conductance A (e^(−t/τd) − e^(−t/τr)) instead of Feng's transmitter-pulse kinetic scheme. τd is taken from the tail of Feng's response, and τr and A are set so that the peak and the charge equal Feng's exactly (`config/synapses_fitted.json`).
  - **Saturation:** a spike adds a = max(0, 1 − u/u_sat). Here u is the level the presynaptic cell's own response is already headed for, and u_sat = 1/(1 − e^(−Cdur(α+β))) is Feng's saturation level, from his kinetic constants.
  - **Depression:** Feng's d1, τD1, d2, τD2 and floors, applied per spike to the new response.
- **Why:** choice S-1 (b), decided by M. T. Nouar on 2026-10-15. Feng's pulse scheme needs per-connection timing state and end-of-pulse events, which GeNN does not provide cheaply. Saturation and depression depend only on the presynaptic spike train, so both are kept once per presynaptic cell.
- **Source of the substitute:**
  - The fits use Feng's own files run in NEURON (`simulation/outputs/blockA/synapse_reference.npz`).
  - Per-spike depression follows Varela et al. 1997, the source Feng cites. Feng's file also rescales the conductance still active from earlier spikes; that is the remaining difference, visible as an instant drop of Feng's NMDA conductance at each spike.
- **Impact, gate S2** (`outputs/S2_synapses.json`, `.png`): **PASS with 1 approved exception.**
  - Single spikes and 5 Hz: within 0.1–2.4 %.
  - Physiological random trains (no interval below 5 ms), 20 and 50 Hz: within 2.8 %.
  - 20 and 50 Hz regular trains: within 5.1 % (reported).
  - 1 ms doublets: up to +17 % (NMDA), reported. No BLA cell fires that fast.
  - Exception approved by M. T. Nouar, 2026-10-15 (`config/gate_exceptions.json`): FSI→PN GABA-A on the Poisson 20 Hz train without refractory period, peak +5.9 %, caused by 1.5–3 ms intervals an FSI cannot produce.

## S-DEV-1 — Simplified cells (implemented 2026-10-15 to 2026-10-21; gate S1: 69 of 71, 2 pending)

- **What:**
  - **FSI:** one compartment with an exponential spike onset and a refractory period; no adaptation.
  - **PN (PN-A and PN-C):** soma plus one passive dendrite.
    - **Soma:** exponential spike onset, refractory period, and a fast spike-triggered potassium conductance (E_K = −80 mV, Feng's PN template) for both types.
    - **PN-A only:** Feng's slow AHP from `sahp.mod`. The conductance follows a gate cs that relaxes towards cinf = ca^nH/(ca^nH + 1) while V ≥ Vgate and towards 0 otherwise. Kept from Feng: Hill exponent nH = 3.04 (from his rate functions) and calcium decay 1,000 ms (his `capool`). The calcium jump per spike, the maximal conductance, Vgate (−64.2 mV; Feng −65) and the gate time (163 ms; Feng 48) are fitted.
    - **Dendrite:** passive, its leak reversing at rest; it receives all excitatory synapses. Each somatic spike adds a back-propagating kick (dVbap = 35 mV), and dendritic synaptic current is multiplied by kD = 3.3.
  - **Not modelled:** Ih, spike shape, depolarization block (S-DEV-2).
  - **Fixed by construction, not fitted:**
    - **Resting potential:** −70.2 mV (PN) and −70.0 mV (FSI).
    - **PN input resistance:** 136.2 MΩ over Feng's −0.05 nA step, with the spike-onset term included.
    - **PN slowest time constant:** 30.9 ms.
    - **FSI passive values:** input resistance 371 MΩ, time constant 19.9 ms.
  - **Everything else is fitted** with differential evolution in GeNN (`config/cells_fitted.json`).
- **Why each choice** (`reports/08` section 2):
  - **Potassium conductances:** with fixed adaptation currents, PN-C's firing curve stayed too steep at strong currents.
  - **Spike-onset term included at rest:** the fitted cells have a soft spike onset, so the term is not negligible at rest.
  - **Back-propagating kick and kD:** Feng's apical dendrite carries Na, K and Ca channels. A passive lumped dendrite gives too little response to dendritic input (−30 % to −57 % before these two were added).
  - **Feng's calcium- and voltage-gated sAHP:** his PN-A shortens its pauses under input (intervals down to 340 ms, no bursts), and an exponentially fading brake could not. The gate constants are fitted because the reset cell has no spike shape, so its voltage path after a spike differs from Feng's.
- **What a passive two-compartment cell cannot do:** reproduce Feng's 63 % rise time (34.9 ms), which is longer than his slowest time constant because of Ih. Ours is 23.5 ms. Reported, not gated.
- **Gate S1** (`outputs/S1_cells.json`, exact CPU mode): **69 of 71 checks pass.**
  - **Open 1:** PN-A first-spike latency at 1.5 nA, 3.7 vs 3.3 ms.
  - **Open 2:** PN-A dendritic-input rate, 0.50 vs 0.70 Hz (U31).
  - **Decision pending (M. T. Nouar):** approve both as exceptions (recommended) or try once more on PN-A.
- **Source of targets:** Block A (`simulation/outputs/blockA/single_cells_full.json`, `passive_tau.json`), the stage-2 reference (`stage2_reference.json`) and Feng's PN-A spike times under input (`drive_spike_times_seed1.json`).

## S-DEV-2 — No depolarization block (decided 2026-10-15)

- **What:** neither the simplified FSI nor the PN enters depolarization block. Feng's PN-C does at 1.5 nA (9 spikes, then silence), and his FSIs did once at ×8 threat in Block B (U30).
- **Why:** decision by M. T. Nouar on 2026-10-15. The block is not reported by Feng and not documented for the BLA, and it would make the engine's response unpredictable. It is kept as a documented option.
- **Impact:** the PN-C 1.5 nA step is excluded from gate S1.
