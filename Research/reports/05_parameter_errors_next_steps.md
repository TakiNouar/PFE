## 7. Parameter Errors That Must Be Fixed Before Run 6

| Parameter | Runs 1–5 (wrong) | Correct literature value | Source |
|---|---|---|---|
| AMPA τ_decay (PN→PN) | 2 ms | **6.9 ms** | Mahanty & Sah 1998 |
| NMDA τ_decay | 80–120 ms | **125 ms** | Weisskopf et al. 1999 |
| NMDA Mg²⁺ block | None | **s(V) = [1 + 0.33 e^{−0.06V}]⁻¹** | Zador et al. 1990 / Feng et al. 2019 |
| E_GABA | −70 mV | **−75 mV** | Feng et al. 2019 |
| PN→PN connectivity | Fixed K=3 (~6%) | **Distance-dependent: 3% at <50μm, 2% at 50–100μm, 1% at 100–200μm, 0.5% at 200–600μm** | Abatis et al. 2017 |
| Noise model | Gaussian current injection | **Conductance-based OU (separate E + I)** | Destexhe et al. 2001 |
| Short-term depression | None | **D_max=0.6, d1=0.9, d2=0.95, τ_D1=40ms, τ_D2=70ms** | Woodruff & Sah 2007 |
| sAHP current (Pyr) | None | **Ca²⁺-dependent slow AHP** | Kim et al. 2013 |
| PN neuron model | Single-compartment | **3-compartment (soma + apical dendrite + passive dendrite)** | Feng et al. 2019 |

---

## 8. What Comes Next

### 8.1 Immediate: Re-run BLA with Feng et al. Parameters

Run 6 must implement the correct literature parameters. Port Feng et al. 2019 into Brian2, citing the paper. Acknowledge single-compartment vs multi-compartment simplification.

### 8.2 CeA Isolation Study

Once BLA parameters are clean, characterize CeA in isolation.

### 8.3 BLA → CeA Two-Region Network

Wire BLA → CeA and test whether the two-region network shows after-discharge that neither showed in isolation. This is where the suppression-gap mechanism (PFC → CeA inhibition) can be first tested.

### 8.4 Primary Reference

**Feng et al. 2019** (eNeuro) — https://pmc.ncbi.nlm.nih.gov/articles/PMC6361623/  
**Code:** https://github.com/ModelDBRepository/247968

---

## 9. Full-Network Study Open Items (Carried Forward)

1. Confirm what the design brief actually says about HYP/VTA connectivity.
2. Fix VTA wiring (zero inbound connections) and NAc wiring (input only from dead VTA).
3. Investigate why PFC Stage-2 output is invariant to its own varied inputs.
4. Correct "eight orders of magnitude" → "seven" in the k-value discussion.
5. Re-run the INS→CeA enable/disable comparison under the current working parameter regime.

---

*Report covers the full history of the BLA isolated study (Runs 1–5) plus the pre-existing full-network study findings.*
