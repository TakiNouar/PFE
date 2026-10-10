# Accuracy Verification Corrections Log (archive documents)

**Date:** September 2026; updated October 2026
**Source:** Internal accuracy verification against literature and cross-document consistency.

## Confirmed fixes applied

| Priority | Issue | Action taken |
|----------|-------|--------------|
| High | Rainnie et al. 1993 wrong title | Corrected to “Intracellular recordings from morphologically identified neurons of the basolateral amygdala”, *J Neurophysiol* 69:1350–62, 1993. |
| High | Weisskopf & LeDoux 1999 wrong title | Corrected to the 1999 paper on L-type VGCC-mediated NMDA-independent LTP. **Oct 2026:** Feng’s reference list confirms this paper (ref. [115]) is Feng’s cited source for τ_NMDA = 125 ms. |
| High | 2× vs 4× suppression contradiction | All documents now report ~2× suppression from the measured effectiveness ratio 0.51. |
| Medium | “3 attempts” vs 4 listed attempts | Corrected to 4 attempts. |
| Medium | Destexhe noise-model year | A September pass wrongly changed 2001 → 2003. **Reverted:** the correct methods source is Destexhe, Rudolph, Fellous & Sejnowski **2001**, *Neuroscience* 107:13–24. The 2003 *Nat Rev Neurosci* paper is a review only. |
| Medium | Abatis 2017 incomplete citation | **Resolved Oct 2026:** it is an SfN 2017 poster with no DOI. Cite Feng et al. 2019 for the numbers. |
| Low | ISI 22.9 ms vs 1000/46.4 ≈ 21.6 ms | Clarifying note added: ISI is measured from active neurons, while the population mean rate includes silent cells. |
| Low | PN→FSI NMDA missing from some tables | Added in the corrected primary sources table. |
| Low | PV/SOM vs Feng single FSI class | Explicit note that distinct SOM kinetics come from post-Feng extensions. |
| Low | Duplicate archive copies | **Oct 2026:** `Research/reports/00_`–`05_`, the monolithic report and its CORRECTIONS overlay were merged into this folder. |

## Remaining open item

1. The 0.852 NMDA current fraction (Run 5) cannot be re-verified from traces, because the simulation code and outputs were never committed. Treat it as reported, not reproduced.

None of the corrections change the scientific conclusions of the archived study.
