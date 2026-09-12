# Runs 1–3 — Synchrony, Private Drive, Large-N Collapse

## Run 1 — Synchrony artifact / fabricated summary

**Parameters:** K=3, g_AMPA=0.025, σ=0.15, shared step current, no heterogeneity.

**Result:** All 8 runs reported identical peak rate 66.67 Hz. Every neuron fired simultaneously then went silent. Synchrony index = 1.0.

**Root causes:**
- Shared uniform step current → all neurons crossed threshold together.
- Noise too weak to desynchronize.
- K=3 too weak to sustain ongoing activity.
- Written summary claimed healthy graded responses — **false** (hardcoded template, not derived from data).

**Valid runs:** 0/8. After-discharge not measured.

---

## Run 2 — Synchrony partially broken, reproducibility broken

**Changes:** σ=1.5, per-neuron heterogeneity (C_m, g_L, E_L), SOM given external drive.

**Result:** 7/8 runs still failed synchrony (syn > 0.5). Only one fixed-probability run passed. Calibration and main sweep used different seeds → results not reproducible. Synchrony *increased* with population size under fixed in-degree.

**Root cause:** External drive was still a shared common signal. Heterogeneity and higher noise could not overcome a perfectly synchronous input clock.

**Valid runs:** 1/8. After-discharge = 0.

---

## Run 3 — Private drive architecture, first genuine passes

**Changes:**
- Ornstein–Uhlenbeck private drive (75 % independent per neuron, τ_OU=3 ms).
- Single global seed fixed → bit-identical reproducibility.
- Mean rate + active_frac metrics added.

**Result:** 5/8 runs passed (syn < 0.5, CV > 0.3, active_frac > 0.4). First clean audit.

**New structural finding — large-N collapse under fixed in-degree:**

| Scale | N_pyr | Mean rate | Active frac | Status |
|-------|-------|-----------|-------------|--------|
| 0.5×  | 25    | 36.0 Hz   | 0.65        | PASS |
| 1.0×  | 50    | 19.4 Hz   | 0.65        | PASS |
| 1.5×  | 75    | 10.4 Hz   | 0.35        | borderline |
| 3.0×  | 150   | 0.7 Hz    | 0.05        | LOW ACTIVITY |

**Cause:** Fixed K=3 keeps recurrent excitation per neuron constant while inhibitory populations scale with N → inhibition wins at large N.

**Interneuron effectiveness ratio (1.0×):** 0.51 → **~2× suppression** of peak rate when inhibitory synapses are active vs silenced. (Earlier summary tables that said “~4×” were inconsistent with this measured ratio and have been corrected.)

**After-discharge:** Zero across all fixed-indegree runs.

**What was established:** Graded desynchronized activity is achievable once shared drive is broken. Reproducibility is achievable with a single global seed.
