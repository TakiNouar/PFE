# Runs 1–3 — Synchrony, Private Drive, Large-N Collapse

## Run 1 — Synchrony artifact / fabricated summary

**Parameters:** K=3, g_AMPA=0.025 µS, σ=0.15 µA/cm², shared uniform step current, no heterogeneity, no SOM external drive.

**Result:** All 8 runs reported an identical peak rate of 66.67 Hz. Every neuron fired simultaneously, then went silent. Synchrony index = 1.0 in all fixed-indegree runs.

**Root causes:**
- A shared uniform step current made all neurons cross threshold together.
- Noise was too weak to desynchronize.
- K=3 was too weak to sustain ongoing activity between volleys.
- The written summary claimed healthy graded responses. This was **false**: it came from hardcoded template text, not from the data.

**Valid runs:** 0/8. After-discharge not measured (results invalid).

**Lesson:** Uniform shared drive is the primary synchronizing force. Any BLA simulation must break it at the source.

---

## Run 2 — Synchrony partially broken, reproducibility broken

**Changes:** σ=1.5 µA/cm², per-neuron heterogeneity (C_m, g_L, E_L), SOM given direct external drive at 0.2× I_stim_slow.

**Result:** 7/8 runs still failed synchrony (syn > 0.5). Only one fixed-probability run passed. Calibration and main sweep used different random seeds, so results were not reproducible. Synchrony *increased* with population size under fixed in-degree. SOM was silent at 0.5×.

**Root cause:** External drive was still a shared common signal. Heterogeneity and higher noise could not overcome a perfectly synchronous input clock.

**Valid runs:** 1/8. After-discharge = 0.

---

## Run 3 — Private drive architecture, first genuine passes

**Changes:**
- Ornstein–Uhlenbeck private drive: 75 % independent per neuron, 25 % shared, τ_OU=3 ms.
- Single global seed (GLOBAL_SEED=20260909), giving bit-identical reproducibility.
- Mean rate and active_frac metrics added.

**Result:** 5/8 runs passed (syn < 0.5, CV > 0.3, active_frac > 0.4). First clean audit.

| Scale | N_pyr | Connectivity | Mean (Hz) | Active frac | Syn | CV | Status |
|-------|-------|--------------|-----------|-------------|-----|----|--------|
| 0.5× | 25 | fixed_indegree | 36.0 | 0.65 | 0.194 | 0.45 | PASS |
| 0.5× | 25 | fixed_prob | 40.4 | 0.80 | 0.299 | 0.61 | PASS |
| 1.0× | 50 | fixed_indegree | 19.4 | 0.65 | 0.248 | 0.51 | PASS |
| 1.0× | 50 | fixed_prob | 25.2 | 0.60 | 0.239 | 0.60 | PASS |
| 1.5× | 75 | fixed_indegree | 10.4 | 0.35 | 0.296 | 0.38 | borderline |
| 1.5× | 75 | fixed_prob | 11.9 | 0.55 | 0.106 | 0.47 | PASS |
| 3.0× | 150 | fixed_indegree | 0.7 | 0.05 | 0.251 | 0.00 | LOW ACTIVITY |
| 3.0× | 150 | fixed_prob | 9.6 | 0.40 | 0.167 | 0.40 | PASS |

**New structural finding — large-N collapse under fixed in-degree:** the mean rate drops 36.0 → 19.4 → 10.4 → 0.7 Hz. Fixed K=3 keeps recurrent excitation per neuron constant while inhibitory populations scale with N, so inhibition wins at large N.

**Interneuron effectiveness ratio (1.0×):** 0.51, i.e. **~2× suppression** of peak rate with inhibitory synapses active versus silenced. Earlier summary tables that said “~4×” were inconsistent with this measured ratio and have been corrected.

**After-discharge:** Zero across all fixed-indegree runs.

**What was established:** Graded desynchronized activity is achievable once shared drive is broken. Reproducibility is achievable with a single global seed.
