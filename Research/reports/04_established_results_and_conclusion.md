# Established Results and Design-Level Conclusion (BLA Isolated Runs 1–5)

## What has been established

| Criterion | Status | Details |
|---|---|---|
| Graded desynchronized activity during stimulus | ✅ Achieved | At N=25–75, private drive, NMDA baseline. Syn < 0.5, CV > 0.3 |
| Synchrony < 0.5, CV > 0.3 | ✅ Achieved | Consistently from Run 3 onward |
| PV and SOM suppression functional | ✅ Confirmed | **~2× suppression** (effectiveness ratio 0.51) at 1.0× |
| Reproducibility (calibration = sweep) | ✅ Fixed | Run 3 onward, bit-identical |
| Large-N collapse explanation | ✅ Identified | Structural E/I asymmetry under fixed in-degree; partially mitigated by NMDA |
| After-discharge ≥ 10 ms | ❌ Not achieved | Inhibitory overshoot at stimulus offset; also a design problem |

**Note on suppression factor:** Earlier draft summaries that stated “~4×” were inconsistent with the measured effectiveness ratio of 0.51 (1/0.51 ≈ 2). All documents now use the ~2× figure derived from the ratio.

## Design-level conclusion

The simulation is running correctly. The results are not meeting the biological target of isolated after-discharge. These are not the same problem.

Emotional inertia is a **network-level emergent property**, not a single-region property. An isolated BLA correctly returns to baseline when its only input ends. Persistence in the intact system depends on VTA dopamine, HIP contextual reactivation, BLA↔CeA↔PAG loops, and HYP bypass routes when prefrontal suppression weakens.

Isolated characterization delivered what it should: graded response, desynchronized firing, functional interneuron suppression, and a clear diagnosis of the kinetic errors that must be fixed before the next implementation.
