# Established Results and Design-Level Conclusion (archived Runs 1–5)

These results came from runs with **wrong kinetics** (see `03_literature_mismatches.md`). They are lessons, not validated parameters. Nothing here is inherited by the clean Run 1 except as an anti-pattern or a hypothesis to re-test.

## What the archived runs showed

| Criterion | Status | Details |
|---|---|---|
| Graded desynchronized activity during stimulus | Achieved | At N=25–75, private drive, NMDA baseline. Syn < 0.5, CV > 0.3 |
| Synchrony < 0.5, CV > 0.3 | Achieved | Consistently from Run 3 onward |
| PV and SOM suppression functional | Achieved | **~2× suppression** (effectiveness ratio 0.51) at 1.0× |
| Reproducibility (calibration = sweep) | Achieved | Run 3 onward, bit-identical with a single global seed |
| Large-N collapse explanation | Hypothesis | Structural E/I asymmetry under fixed in-degree, partially mitigated by NMDA. Re-test in clean Run 1 (Gate 4 scale sweep) |
| After-discharge ≥ 10 ms | Not achieved | Inhibitory overshoot at stimulus offset; also out of scope for an isolated region |

**Note on suppression factor:** Earlier draft summaries that said “~4×” were inconsistent with the measured effectiveness ratio of 0.51 (1/0.51 ≈ 2). All documents now use ~2×.

## Design-level conclusion

The simulation engine was functioning. The biological target (isolated after-discharge) was out of scope. These are not the same problem.

Emotional inertia is a **network-level emergent property**, not a single-region one. An isolated BLA correctly returns to baseline when its only input ends. In the intact system, persistence depends on VTA dopamine, HIP contextual reactivation, BLA↔CeA↔PAG loops, and HYP bypass routes when prefrontal suppression weakens.

Isolated characterization should only be required to deliver:

- graded desynchronized activity,
- functional interneuron suppression,
- reproducible parameters.

The archived campaign showed these are reachable even with wrong kinetics. The clean Run 1 must reach them with literature kinetics. After-discharge belongs to the multi-region phase.
