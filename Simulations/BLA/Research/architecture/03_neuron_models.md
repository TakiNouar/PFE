# 03 — Neuron Models

## Rule

The reference level uses Feng's cell templates from ModelDB 247968 **unchanged**. The main level uses the same FSI template unchanged, plus a **two-piece PN** built from Feng's full PN (section below). Do not mix in ModelDB 150288 (Kim 2013): Feng revised Kim's principal-cell model, and only the FSI model is unchanged from Kim (Feng 2019, Methods).

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

Feng's templates insert `extracellular` and `xtraimemrec` (his LFP recorder) in every section. They stay in the reference level, because the templates are used unchanged, but Run 1 does not compute an LFP. Measured cost: about 0.3 µs per segment per step for `extracellular`, and about 6 % of the PN's cost for `xtraimemrec`. The two-piece PN leaves both out; Feng's FSI template keeps them in both levels.

## Measured cost (2026-10-14, project laptop, one process)

| Cell | Cost per cell per 0.05 ms step |
|---|---|
| Feng's full PN (16 segments, 11 mechanisms each) | 77.6 µs (~5 µs per segment; NEURON's `hh` is 0.13 µs) |
| **Two-piece PN (main level)** | **8.5 µs** |
| One-piece PN (tested, not used) | 4.4 µs |
| Feng's FSI (2 segments) | 4.3 µs |

## Two-piece PN (main level)

**Decision (2026-10-14, M. T. Nouar):** the main level uses the two-piece PN. A one-piece version was built and tested the same way and rejected: its first spike was 15–60 % late at every current (Gate R1: 29/46 checks).

**Where:** parameters in `Simulations/BLA/simulation/mechanisms_run1/reduced_pn.json`, written by `bla_sim/reduce_pn.py`; the cell is built by `bla_sim/cells.py`. Feng's files are not edited.

**Construction (no fitted values):**
1. **Soma: Feng's soma, copied exactly:** 25 × 24.75 µm, every mechanism (`cadyn`, `capool`, `hd`, `im`, `kap`, `kdr`, `leak`, `na3`, `nap`, `sAHP`) with Feng's values, the same reversal potentials, Cm and Ra. Feng's LFP recorders (`extracellular`, `xtraimemrec`) are left out; they only record and do not drive the cell.
2. **Dendrite: Feng's two dendrites merged into one compartment.** Its membrane area is their total (11,263 µm²). Each channel's **total** conductance is their total, summed segment by segment, so channels Feng places only in the first dendritic segment (`nap`, `im`) keep their real amount.
3. **Coupling:** the dendrite's diameter and length are chosen so that its area matches and the soma-to-dendrite axial resistance equals the half-length resistances of Feng's two dendrites in parallel (12.18 MΩ): diameter 6.55 µm, length 547.3 µm.
4. **PN-C** is built the same way from Feng's `Cell_C`.

**Synapses:** excitatory synapses on the dendrite (Feng: `dend(0.9)`); inhibitory synapses and background noise on the soma (as Feng).

**Gate R1 result (2026-10-14):** matches Feng's full cell on resting potential (−70.2 vs −70.2 mV), input resistance (138 vs 136 MΩ), time constant (34.4 vs 34.9 ms), spike counts at every level up to 1.0 nA and in the 4 s steps, first-spike latency up to 0.4 nA, and firing under noise alone (PN-A 0.35 vs 0.35 Hz; PN-C 1.45 vs 1.65 Hz). Two strong-current differences were **approved as exceptions** by M. T. Nouar (DEV-006, `10_validation_gates.md`):
- first-spike latency about 1 ms shorter at 0.6–1.5 nA (2.4 vs 3.3 ms at 1.5 nA);
- at 1.5 nA, Feng's PN-C stops firing early (depolarization block: 9 spikes in 1 s), the two-piece does not (39).

Gate R2 (network level) decides whether they matter in the network.

## The live engine

Run 1 does not decide the live engine's cell model (U26). The measured costs show that real time needs cells cheaper than even the one-piece PN, plus several cores. The two-piece PN and its Gate R1 recordings are the reference such a cell must match.
