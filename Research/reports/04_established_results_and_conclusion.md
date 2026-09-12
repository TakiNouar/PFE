## 5. What Has Been Established (Summary)

| Criterion | Status | Details |
|---|---|---|
| Graded desynchronized activity during stimulus | ✅ Achieved | At N=25–75, private drive, NMDA baseline. Syn < 0.5, CV > 0.3 |
| Synchrony < 0.5, CV > 0.3 | ✅ Achieved | Consistently from Run 3 onward |
| PV and SOM suppression functional | ✅ Confirmed | ~4× suppression in mean rate at 1.0× |
| Reproducibility (calibration = sweep) | ✅ Fixed | Run 3 onward, bit-identical |
| Large-N collapse explanation | ✅ Identified | Structural E/I asymmetry under fixed in-degree; partially mitigated by NMDA |
| After-discharge ≥ 10 ms | ❌ Not achieved | Inhibitory overshoot at stimulus offset; also a design problem |

**Confirmed BLA parameters for full-network use (pending literature correction):**

```
K_Pyr→Pyr = 3 (fixed in-degree)
g_AMPA = 0.08 μS  [NOTE: literature value should be re-derived from Feng et al.]
g_NMDA = 0.04 μS, τ_NMDA = 120 ms  [NOTE: no Mg²+ block — simplification]
g_GABA_PV = 0.70 μS
g_GABA_SOM = 0.40 μS
Private drive fraction = 0.75
σ_noise = 1.2 μA/cm²
GLOBAL_SEED = 20260909
```

---

## 6. Design-Level Conclusion

### The simulation is running correctly. The results are not meeting the biological target. These are not the same problem.

After-discharge — emotional inertia, the persistence of state after a stimulus ends — was the primary dynamic target for BLA. Five runs failed to produce it. The reason is not a bug, not a parameter problem, and not a fixable simulation issue within the isolated BLA framework. **It is a design problem.**

In the real brain, BLA does not maintain post-stimulus activity by itself. It is held active by a network of regions:

- **VTA** releases dopamine onto BLA, raising baseline excitability after a salient event
- **HYP** drives CeA and PAG when PFC suppression weakens
- **HIP** provides contextual reactivation
- **BLA→CeA→PAG feedback loop** sustains reverberatory activity across regions

The isolated BLA receives a step input, fires, and returns to baseline when the input drops — exactly as it should when isolated. Emotional inertia is a **network-level emergent property**, not a single-region property.

The five runs established clean parameters for BLA's internal dynamics — graded response, desynchronized firing, functional interneuron suppression. That is what an isolated characterization is supposed to deliver.
