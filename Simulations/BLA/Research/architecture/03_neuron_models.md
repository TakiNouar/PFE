# 03 — Neuron Models

## Rule

The reference level uses Feng's cell templates from ModelDB 247968 **unchanged**. The main level uses the same FSI template unchanged, plus **Feng's PN rebuilt on a coarser grid** (6 segments instead of 16, section below). Do not mix in ModelDB 150288 (Kim 2013): Feng revised Kim's principal-cell model, and only the FSI model is unchanged from Kim (Feng 2019, Methods).

| Population | Template file (ModelDB 247968) | Template |
|------------|--------------------------------|----------|
| PN-A | `BLcells_template_LFP_segconsider_all_Iinject_recordingimembrane.hoc` | `Cell_A` |
| PN-C | same file | `Cell_C` |
| FSI | `interneuron_template_gj_LFP_Iinject_recordingimembrane.hoc` | the FSI template in that file |

`Cell_B` in the PN file is never used by Feng's own network and is not used here.

## What the templates contain (for reference, read from the code)

These values are **not** set by us. They are listed so the thesis can describe the cells and so Gate 2 results can be checked. Source: the template files, verified October 2026 (`Research/Sources/01_primary_bla_references.md`).

**Principal cell (PN-A and PN-C):**

- **Shape:** soma (L 25 µm, diam 24.75 µm, 1 segment), apical dendrite `dend` (L 270 µm, diam 3 µm, 8 segments), distal dendrite `p_dend` (L 555 µm, diam 5 µm, 7 segments). **16 segments.**
- **Channels:** fast Na (`na3`), delayed-rectifier K (`kdr`), A-type K (`kap`), M-current (`im`), h-current (`hd`), high-threshold Ca (`cadyn`), persistent Na (`nap`), Ca pool (`capool`, τ = 1,000 ms), slow Ca-dependent K (`sAHP`), leak.
- **Where the adaptation brake sits:** the sAHP and its Ca pool are in the **soma only**; the dendrites have sAHP = 0.
- **PN-A vs PN-C:** sAHP density 0.05 S/cm² (A) vs 0.0002 S/cm² (C). The code also differs in persistent Na (0.000559 vs 0.000555 S/cm²), which the paper does not mention.
- **Passive:** Cm 2.4 µF/cm², Ra 150 Ω·cm, leak 2.5e-5 S/cm² (soma) and 4.71e-5 S/cm² (dendrites), **E_leak −72 mV**. The paper text says Rm 55 kΩ·cm² and E_L −75 mV; its own Table 2 and the code disagree with that text. The code is used (DEV-002).
- **Reversal potentials:** Na +45, K −80, h −45, Ca +120 mV.

**FSI:**

- **Shape:** soma (15 × 15 µm) + one dendrite (150 × 10 µm), 1 segment each. **2 segments.**
- **Channels:** Na (`nainter`), K (`kdrinter`), leak (`leakinter`).
- **Passive:** Rm 20 kΩ·cm², Cm 1.0 µF/cm², dendrite Ra 150 Ω·cm, soma Ra 3,375 Ω·cm, **E_leak −70 mV**. The template overrides the `leakinter.mod` default of −75 mV.

**Both:** temperature 31 °C, v_init −70 mV (set in `BL_main.hoc`; we set the same values).

## Heterogeneity

None added. Every cell of a type is identical. Variety comes only from what Feng's model already has: lognormal synaptic weights, distance-dependent delays, independent noise, and random wiring.

## The LFP mechanism

Feng's templates insert `extracellular` and `xtraimemrec` (his LFP recorder) in every section. They stay in the reference level, because the templates are used unchanged, but Run 1 does not compute an LFP. Measured cost: about 0.3 µs per segment per step for `extracellular`, and about 6 % of the PN's cost for `xtraimemrec`. The reduced PNs leave both out: a rebuild of Feng's cell on his own grid without them reproduces his cell exactly (latencies and spike counts identical, 2026-10-14), so they do not affect the dynamics. Feng's FSI template keeps them in both levels.

## Measured cost (2026-10-14, project laptop, one process)

| Cell | Segments | Cost per cell per 0.05 ms step |
|---|---|---|
| Feng's full PN | 16 (+ LFP recorders) | 83 µs (~5 µs per segment; NEURON's `hh` is 0.13 µs) |
| **Coarse PN, apical 2 + basal 3 (main level)** | **6** | **25 µs** |
| Coarse PN, apical 2 + basal 7 | 10 | 41 µs |
| Coarse PN, apical 2 + basal 1 | 4 | 17 µs |
| Two-piece PN (rejected) | 2 | 8.4 µs |
| One-piece PN (rejected) | 1 | 4.4 µs |
| Feng's FSI | 2 | 4.3 µs |

## Main-level PN: Feng's cell on a coarser grid ("coarse_d2_p3")

**Decision (2026-10-14, M. T. Nouar):** the main level uses Feng's PN rebuilt with his own geometry and topology on a coarser grid: soma 1 segment, apical dendrite 2 segments (Feng: 8), basal dendrite 3 segments (Feng: 7). Total 6 segments instead of 16.

**Where:** parameters in `Simulations/BLA/simulation/mechanisms_run1/reduced_pn.json` (key `coarse_d2_p3`), written by `bla_sim/reduce_pn.py`; built by `bla_sim/cells.py`; selected in `bla_sim/config/run1.json` (`main_level_cell`). Feng's files are not edited.

**Construction (no fitted values):**
1. **Soma:** Feng's soma copied exactly (25 × 24.75 µm; `cadyn`, `capool`, `hd`, `im`, `kap`, `kdr`, `leak`, `na3`, `nap`, `sAHP` with Feng's values; same reversal potentials, Cm, Ra).
2. **Dendrites:** Feng's apical (`dend`, 270 × 3 µm, attached at soma(0)) and basal (`p_dend`, 555 × 5 µm, attached at soma(1)) sections with their real geometry, on fewer segments. Values that are uniform along a section are copied. `nap` and `im`, which Feng puts only in a section's first segment, keep their total and go in the new first segment. Any other pattern stops the build.
3. **Left out:** the LFP recorders (see above).
4. **PN-C** is built the same way from Feng's `Cell_C`.

**Synapses:** excitatory synapses at `dend(0.9)`, as Feng; inhibitory synapses and background noise on the soma, as Feng.

**Why this grid:** two things were found by testing (2026-10-14):
- The **basal dendrite** must keep at least 3 segments. With 1 segment, its single node sits 277 µm from the soma, the soma is under-loaded at fast timescales, and the first spike comes about 1 ms early at strong currents.
- The **apical dendrite** must stay a thin separate section, because excitatory input lands at its tip and depolarizes it enough to relieve the NMDA Mg²⁺ block. Lumping it into a fat compartment (the two-piece cell) made the cell respond about 35 % too weakly to synaptic input.

**Gate R1 result (2026-10-14):** 45 of 46 current-injection checks pass. Resting potential −70.2 vs −70.2 mV, input resistance 136.6 vs 136.2 MΩ, time constant 34.8 vs 34.9 ms, latency 3.2 vs 3.3 ms at 1.5 nA, firing under noise PN-A 0.35 vs 0.35 Hz and PN-C 1.62 vs 1.65 Hz. Under Feng's afferent trains on the dendrite (`bla_sim/drive_test.py`): PN-A 0.66 vs 0.69 Hz, PN-C 3.36 vs 3.25 Hz. One exception was **approved by M. T. Nouar** (DEV-006): at the strongest step (1.5 nA), PN-C fires 6 spikes before depolarization block instead of Feng's 9; the block itself is reproduced.

**Rejected alternatives** (same tests, `outputs/blockA/`):

| Cell | Result |
|---|---|
| One-piece | First spike 15–60 % late at every current |
| Two-piece | ~1 ms early at strong current; 35 % too weak under dendritic synaptic input (2–3× too few spikes in a 100-cell network) |
| Apical 2 + basal 1 | ~1 ms early at strong current |
| Apical 2 + basal 7 | Passes every check, but 1.6× the cost of the chosen cell |

## The live engine

Run 1 does not decide the live engine's cell model (U26). The measured costs show that real time needs cells far cheaper than any of these, plus several cores. The chosen cell and its Gate R1 recordings are the reference a live-engine cell must match, including the dendritic-input test.
