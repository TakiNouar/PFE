# Corrections Overlay for `BLA_isolated_simulation_report.md`

**Apply these corrections when reading the full report.** The split files under `Simulation tests/BLA/reports/test_run_1/` and `Research/reports/04_established_results_and_conclusion.md` already incorporate them.

## 1. Full-network attempt count (§1.2)

**Wrong:** “failed across 3 attempts”  
**Correct:** “failed across **4** attempts”

(The same section already lists Attempt 1–4.)

## 2. Suppression factor (§5 summary table)

**Wrong:** “~4× suppression in mean rate at 1.0×”  
**Correct:** “**~2×** suppression (effectiveness ratio 0.51) at 1.0×”

The Run 3 narrative ratio of 0.51 is the measured value; 1/0.51 ≈ 2. All other documents now use ~2×.

## 3. ISI clarification (Run 5)

Reported mean ISI = 22.9 ms at mean rate 46.4 Hz.  
1000/46.4 ≈ 21.6 ms. Difference is expected: ISI is computed only from active neurons; population mean rate includes silent cells.

## 4. Authoritative locations after the accuracy pass

| Topic | Use this file |
|-------|---------------|
| Runs 1–3 narrative | `Simulation tests/BLA/reports/test_run_1/01_runs_1_to_3.md` |
| Runs 4–5 + ISI note | `Simulation tests/BLA/reports/test_run_1/02_runs_4_to_5.md` |
| Established results table | `Research/reports/04_established_results_and_conclusion.md` |
| Citation fixes (Rainnie, Weisskopf, Destexhe, Abatis) | `Research/Sources/01_primary_bla_references.md` and `02_supporting_biological.md` |
| Full verification log | `Simulation tests/BLA/reports/test_run_1/06_accuracy_verification_corrections.md` |

None of these corrections change the scientific conclusions of the isolated BLA study.
