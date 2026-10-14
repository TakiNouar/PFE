# 03 — Neuron Models

## Rule

The reference level uses Feng's cell templates from ModelDB 247968 **unchanged**. The main level uses the same FSI template unchanged, plus a **one-piece PN** built from Feng's full PN (section below). Do not mix in ModelDB 150288 (Kim 2013): Feng revised Kim's principal-cell model, and only the FSI model is unchanged from Kim (Feng 2019, Methods).

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

Feng's templates insert `extracellular` and `xtraimemrec` (his LFP recorder) in every section. They stay in the reference level, because the templates are used unchanged, but Run 1 does not compute an LFP. Measured cost: about 0.3 µs per segment per step for `extracellular`, and about 6 % of the PN's cost for `xtraimemrec`. The one-piece PN leaves both out; Feng's FSI template keeps them in both levels.

## Measured cost (2026-10-14, project laptop, one process)

Feng's PN costs about **5.2 µs per segment per time step**, about 40× NEURON's built-in `hh` (0.13 µs). The cost is spread over its 11 mechanisms per segment; `extracellular` alone adds about 0.3 µs. At 16 segments that is about 83 µs per PN per step, the main reason the full-detail network takes about an hour per simulated second at 1,000 cells.

## One-piece PN (main level only)

**Why:** one segment instead of 16 makes each PN about 16× cheaper.

**Where:** a new template file in `Simulations/BLA/simulation/mechanisms_run1/` (templates for PN-A and PN-C). Feng's files are not edited.

**Construction:**
1. **One section, one segment**, with the same mechanisms as Feng's soma: `cadyn`, `capool`, `hd`, `im`, `kap`, `kdr`, `leak`, `na3`, `nap`, `sAHP`. Feng's LFP recorders (`extracellular`, `xtraimemrec`) are left out; they only record and do not drive the cell.
2. **Starting point, computed from Feng's full cell, not chosen by us:**
   - Membrane area = the full cell's total membrane area.
   - Each channel's **total** conductance = its total in Feng's full cell, summed segment by segment (so channels Feng places only in part of the cell, such as `nap` and `im` in the first dendritic segment, keep their real amount).
   - `sAHP` keeps its somatic total (it is somatic in Feng).
   - Cm, E_leak, reversal potentials, Ca²⁺-pool settings and temperature are Feng's code values.
3. **Fit only if the starting point fails Gate R1:** scale factors on four totals (Na `na3`, K `kdr`, `sAHP`, leak), fitted by least squares to **Feng's full cell's** Gate R1 measures. Nothing else is adjusted, and no biological target is used. The fitted factors and the remaining errors go in `full_parameters.json` and DEV-006.
4. **PN-C** is built the same way from Feng's `Cell_C` (sAHP 0.0002 S/cm² at the soma; NaP 0.000555 S/cm²).

**Synapses on the one-piece cell:** Feng places excitatory synapses on the apical dendrite (`dend(0.9)`) and inhibitory ones on the soma. In one compartment all of them sit on the same section, so dendritic filtering is lost. This is part of DEV-006 and is exactly what Gate R2 (network-level comparison) checks.

**Check (Gate R1):** the one-piece cell must match Feng's full cell on resting potential, input resistance, membrane time constant, spike counts across a current ladder, first-spike latency, and firing under Feng's background noise alone (`10_validation_gates.md`).

## The live engine

Run 1 does not decide the live engine's cell model (U26). The measured costs show that real time needs cells cheaper than even the one-piece PN, plus several cores. The one-piece PN and its Gate R1 recordings are the reference such a cell must match.
