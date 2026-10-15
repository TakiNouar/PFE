# Block B — Reference Behaviour of Feng's Network — October 2026

**Date:** 2026-10-15
**Role:** the network-level reference for the simplified model (decision of 2026-10-14, `04_run1_redesign_oct2026.md`).
**Data:** `Simulations/BLA/simulation/outputs/B_full_n200/seed1..3/`. Summary (mean ± SD across seeds, per-seed values): `outputs/blockB/reference_summary.json`, written by `python -m bla_sim.blockb_summary`.

---

## What was run

Feng's cells and synapse files unchanged (ModelDB 247968), 200 cells (128 PN-A, 52 PN-C, 20 FSI):
- wiring by Feng's inputs per cell (DEV-001);
- Feng's background noise and afferent trains;
- settle 3 s, rest 30 s, then one 2 s threat each at ×2, ×4 and ×8 afferent rate (2 s before, 4 s after);
- 3 seeds.

Each seed took 11.6 h (731× slower than real time), run in parallel from 2026-10-14 16:40 to 2026-10-15 04:18. No failures.

## Results

**Rest (30 s):**

| Measure | Feng's network (mean ± SD, 3 seeds) | Rat BLA |
|---|---|---|
| PN-A rate | 0.51 ± 0.01 Hz | 0.21 Hz (type 1, Amir et al. 2018) |
| PN-C rate | 0.97 ± 0.03 Hz | 1.55 Hz (type 2, Amir et al. 2018) |
| All PNs | 0.64 Hz | 0.2–3 Hz (Gate 3) |
| FSI rate | **35.1 ± 0.4 Hz** | 22–27 Hz (Amir et al. 2018); Gate 3 range 10–30 Hz |
| Synchrony index | 0.03–0.07 | Gate 3: < 0.5 |
| ISI CV (PNs) | 0.71–0.73 (irregular) | — |
| PN rest range (mean ± 2 SD over 2 s windows) | 0.47–0.81 Hz | — |

**Threat (one trial per dose per seed):**

| Dose | PN before → during | FSI before → during | Back in rest range afterwards |
|---|---|---|---|
| ×2 | 0.64 → **0.84 ± 0.07** Hz | 33 → **50 ± 4** Hz | 2 of 3 seeds (seed 3 undershoots: 0.46 vs 0.49) |
| ×4 | 0.62 → **1.00 ± 0.02** Hz | 32 → **62 ± 2** Hz | 3 of 3 |
| ×8 | 0.65 → **1.37 ± 0.39** Hz | 35 → **70 ± 3** Hz | 3 of 3 |

- The PN response grows with dose in every seed (×2 < ×4 < ×8), and FSIs follow.
- The response is modest: an 8× stronger afferent input roughly doubles PN firing, because the FSIs (inhibition) rise with it.

**FSI depolarization block:** in seed 3, at the end of the ×8 threat (51.0–53.0 s):
- **all 20 FSIs fell silent** for 250–500 ms;
- the probe FSI's soma sat near −12 mV, compared with −53 to −56 mV in ordinary pauses;
- PNs burst to 6.1 Hz while inhibition was gone, then everything recovered.

Seeds 1 and 2 showed no block. Other FSI silences of 250 ms or more in all seeds were ordinary pauses below threshold.

## What it means

1. **U30, FSI rate:** with a 30 s rest, FSIs fire 35 Hz in Feng's own cells under our wiring. That's lower than the 1 s samples (~42 Hz), but still above rat data (22–27 Hz) and above Gate 3's 30 Hz. Since the cells are Feng's, unchanged, the difference comes from our network setup, not from the cells. Candidates:
   - **Not the network size:** in the Phase 0 benchmark (1 s samples) FSIs fired about the same at 200, 500 and 1,000 cells (42.7 / 43.0 / 41.8 Hz), although only at 200 cells does every FSI receive all PNs (p = 1, weights ×1.19). So the shared, scaled input at 200 cells is not the main cause.
   - **Remaining candidates:** how afferent trains reach FSIs at our sizes (Feng: 3.4 trains per FSI, FSIs within 300 µm sharing a train with 0.3 % probability); the missing distance structure (Feng's PN→FSI connections are local); and Feng's in-degree values having been read from his realised 27,000-cell connectivity. Open (U30).

   For the simplified model, the FSI target comes from the rat data and Feng's paper (FSIs tuned to in vivo rates). Block B's 35 Hz is a known difference, not a target.
2. **Depolarization block is a property of Feng's FSI model** under strong drive, at 200 cells too, not only the 100-cell artifact suspected on 2026-10-14. Whether real BLA FSIs do this is not documented in Feng's paper. The simplified FSI can reproduce or omit it, but the choice must be stated (open).
3. **Targets for the simplified network:**
   - PN rest rates per class;
   - an FSI rest rate in the rat range;
   - low synchrony and irregular firing;
   - a dose-dependent PN and FSI threat response of about these sizes;
   - recovery to the rest range within 4 s.
