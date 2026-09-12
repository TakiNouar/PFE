# Run-by-Run Results (Runs 1–3)

### Run 1 — Synchrony Artifact / Fabricated Summary

**Parameters:** K=3, g_AMPA=0.025 μS, σ=0.15 μA/cm², shared uniform step current, no heterogeneity, no SOM external drive

**Results:**

| Metric | Value |
|---|---|
| Valid runs | 0 / 8 |
| Peak rate (all runs) | 66.67 Hz (identical) |
| Synchrony index | 1.0 (all fixed-indegree runs) |
| After-discharge | Not measured — results invalid |

**Root causes:**
- All neurons received identical step current at the same time → simultaneous threshold crossing → single synchronous volley
- Noise too weak (σ=0.15) to desynchronize anything
- K=3 recurrent connections insufficient to sustain ongoing activity between volleys
- Written summary reported "healthy graded responses" — this was false, generated from hardcoded template text not derived from data

**What was learned:** Uniform shared drive is the primary synchronizing force. Any BLA simulation must break this at the source.

---

### Run 2 — Synchrony Partially Broken, Reproducibility Broken

**Changes from Run 1:** Noise raised to σ=1.5 μA/cm², per-neuron heterogeneity added, SOM given direct external drive at 0.2× I_stim_slow

**Results:** 1 / 8 valid. Synchrony increased with population size under fixed in-degree. Calibration and main sweep used different random seeds — not reproducible. SOM silent at 0.5×.

---

### Run 3 — Private Drive Architecture, Genuine Pass for 5 Runs

**Changes from Run 2:** Ornstein-Uhlenbeck private drive — 75% independent per-neuron OU; 25% shared. Single global seed (GLOBAL_SEED=20260909). Mean rate and active_frac metrics added.

**Results:**

| Scale | Conn | Mean (Hz) | Active frac | Syn | CV | Status |
|---|---|---|---|---|---|---|
| 0.5× | fixed_indegree | 36.0 | 0.65 | 0.194 | 0.45 | **PASS** |
| 0.5× | fixed_prob | 40.4 | 0.80 | 0.299 | 0.61 | **PASS** |
| 1.0× | fixed_indegree | 19.4 | 0.65 | 0.248 | 0.51 | **PASS** |
| 1.0× | fixed_prob | 25.2 | 0.60 | 0.239 | 0.60 | **PASS** |
| 1.5× | fixed_indegree | 10.4 | 0.35 | 0.296 | 0.38 | borderline |
| 1.5× | fixed_prob | 11.9 | 0.55 | 0.106 | 0.47 | **PASS** |
| 3.0× | fixed_indegree | 0.7 | 0.05 | 0.251 | 0.00 | **LOW ACTIVITY** |
| 3.0× | fixed_prob | 9.6 | 0.40 | 0.167 | 0.40 | **PASS** |

**Valid runs:** 5 / 8. First clean audit. Reproducibility confirmed.

**Large-N collapse under fixed in-degree:** Mean rate drops 36.0 → 19.4 → 10.4 → 0.7 Hz. Fixed K=3 means recurrent excitation per neuron stays constant while inhibition scales with N — inhibition wins at large N.

**After-discharge:** Zero across all fixed-indegree runs.
