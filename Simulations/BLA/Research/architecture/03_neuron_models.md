# 03 — Neuron Models

## Rule

Use Feng's cell templates from ModelDB 247968 **unchanged**. Do not copy their numbers into new code, and do not mix in ModelDB 150288 (Kim 2013): Feng revised Kim's principal-cell model, and only the FSI model is unchanged from Kim (Feng 2019, Methods).

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

The templates insert `xtraimemrec` (Feng's LFP recorder). It must stay, because the templates are used unchanged, but Run 1 does not compute an LFP. It costs some speed; the benchmark measures that.

## What the live engine may change later

Run 1 does not decide the live engine's cell model. If the benchmark shows Feng's full cells cannot run fast enough beside the LLM, the live engine may use a reduced cell. Run 1's single-cell recordings (Gate 2) then become the reference that a reduced cell must match.
