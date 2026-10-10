# 12 — Sources Map (Architecture ↔ Literature)

**Authority:** Every number in this architecture must resolve to an entry under `Research/Sources/` (primary: `01_primary_bla_references.md`).

If a value is not listed there, implementation **stops** and the gap is written to `deviations.md`.

---

## Master models

| Architecture need | Source document | Paper |
|-------------------|-----------------|-------|
| Tables 1–7, Mg block, scale, composition | `Research/Sources/01_primary_bla_references.md` | Feng et al. 2019 eNeuro; ModelDB **247968** |
| PN / FSI single-cell mechanisms | same + Kim entry | Kim et al. 2013 Learn Mem; ModelDB **150288** |
| Reading order for implementation | `Research/Sources/07_reading_priority.md` | — |
| Index of all Sources files | `Research/Sources/README.md` | — |
| Provenance audits | `Research/reports/literature_provenance_audit_sep2026.md`, `Research/reports/consistency_and_source_verification_oct2026.md` | — |
| Open items (U-numbers) | `Research/reports/open_uncertainties.md` | — |

---

## Parameter → source (Run 1)

### Synaptic kinetics (`04_synaptic_models.md`)

| Parameter | Value | Feng locus | Upstream (do not omit) | Sources file |
|-----------|-------|------------|------------------------|--------------|
| PN→PN AMPA | 0.3 / **6.9** ms, 1.0 nS | Table 3 | Mahanty & Sah **1998**; Guzman et al. **2016** | `01_primary_bla_references.md` |
| PN→FSI AMPA | 0.1 / 2.4 ms, 1.0 nS | Table 3 | same | same |
| PN→PN / PN→FSI NMDA | 3.7 / **125** ms, 0.5 nS | Table 3 | **Weisskopf, Bauer & LeDoux 1999** (Feng ref. [115], confirmed) | same |
| FSI→PN GABA-A | 0.5 / **6.8** ms, 0.6 nS, E=−75 mV | Table 3 | **Galarreta & Hestrin 1997** | same |
| FSI→FSI GABA-A | 0.5 / 6.8 ms, 0.2 nS | Table 3 | Galarreta & Hestrin 1997 | same |
| Weight multipliers W | lognormal; Table 3 mean/var PN→PN AMPA 5/3, NMDA 2/1; PN→FSI 7/2; FSI→PN 12/2; FSI→FSI 20/10 | Table 3 + ModelDB connect hoc | — (U20: paper vs code) | same |
| Synaptic delay | d/(1 mm/ms) + 0.8 ms + U(±0.1) + dt | Methods + ModelDB | — | same |
| Synapse formalism | Destexhe 1994 kinetic scheme (AlphaTmax/Beta/Cdur) | ModelDB `.mod` | Destexhe et al. 1994 | `05_computational_neuroscience.md` |
| Mg²⁺ block | s(V)=[1+0.33exp(−0.06V)]⁻¹ | Methods | **Zador et al. 1990** | `02_supporting_biological.md` |
| Gap junctions FSI–FSI | 8 % of pairs, coupling ≈ 0.05 | Tables 3, 6 | Woodruff & Sah 2007 | `01_primary_bla_references.md` |

### Short-term depression (`04_synaptic_models.md`)

“D_max” is a floor on the release factor F·D1·D2 (ModelDB). d1/d2 pairing with τ is open (U21).

| Connection | D_max | d1/d2 | τ (ms) | Upstream | Sources file |
|------------|-------|-------|--------|----------|--------------|
| FSI→PN | **0.6** | 0.9/0.95 | 40/70 | Woodruff & Sah **2007** (BLA) | `01_primary_bla_references.md` |
| PN→FSI | **0.7** | 0.9/0.95 | 40/70 | Woodruff & Sah 2007 (BLA) | same |
| PN→PN | **0.5** | 0.9/0.95 | 40/70 | **Silberberg et al. 2004 (neocortex)** — not BLA-measured | same |

### Connectivity (`05_connectivity.md`)

| Parameter | Value | Upstream | Sources file |
|-----------|-------|----------|--------------|
| PN→PN distance bands | 3/2/1/0.5 % at <50 / 50–100 / 100–200 / 200–600 µm | Feng Tables 5–6 ← Abatis et al. 2017 (SfN poster; cite Feng) | `01_primary…` + `02_supporting_biological.md` |
| PV→PN | P = 0.34 | Woodruff & Sah 2007 / Feng | `01_primary_bla_references.md` |
| PN→PV | 0.12 uni / 0.16 reciprocal | Woodruff & Sah 2007 / Feng | same |
| PV→PV chemical | 0.26 (0.20 uni + 0.03 bi), conditioned on gap-junction coupling | Woodruff & Sah 2007 / Feng Table 6 | same |
| Interneuron distance limit | ~300 µm | Feng Methods | same |
| P_SOM_PN | 0.34 (Run 1 approx.) | **Approximation** — not a Feng Table value; must appear in `deviations.md` | architecture only |

### Noise (`06_noise_and_drive.md`)

| Parameter | Value | Upstream | Sources file |
|-----------|-------|----------|--------------|
| Point-conductance / OU formalism | equations | **Destexhe, Rudolph, Fellous, Sejnowski 2001**, *Neuroscience* 107:13–24 | `01_primary…` + `05_computational_neuroscience.md` |
| PN Table 7 coeffs | g_e0=3.2, σ_e=3, τ_e=2.728, E_e=0, g_i0=21, σ_i=8, τ_i=10.49, E_i=−75 (nS, ms, mV) | Feng Table 7 (adapted from Destexhe 2001) | `01_primary_bla_references.md` |
| FSI Table 7 coeffs | g_e0=1.2, σ_e=0.1, τ_e=2.728, E_e=0, g_i0=5.7, σ_i=2.6, τ_i=10.49, E_i=−75 | Feng Table 7 (verified Oct 2026) | same |
| Extrinsic input | Feng: Poisson surrogate trains, ≈3 per PN; Run 1 uses OU stimulus instead (U25) | Feng Methods | same |
| Destexhe 2003 Nat Rev Neurosci | — | **Review only** — not the methods source | listed separately in Sources |

### Neuron models (`03_neuron_models.md`)

| Need | Source |
|------|--------|
| Multi-compartment PN + I_sAHP | Kim 2013 + Feng 2019 ModelDB templates |
| PN / FSI passive params | Feng Methods (verified; see `01_primary_bla_references.md`) |
| FSI kinetics | Kim / Feng FSI templates |
| Time step | dt = 0.05 ms (Feng Methods) |
| SOM = PV kinetics (Run 1) | Temporary; document in `deviations.md`; later Cattani et al. 2024 | `01_primary` / extended models |

---

## Forbidden substitutions (from Sources audit)

| Do not use | Instead |
|------------|---------|
| Mahanty & Sah **1999** as source of 6.9 ms AMPA | **1998** + Guzman 2016 |
| Woodruff & Sah for PN→PN D_max | Silberberg 2004; D_max=**0.5** |
| Destexhe **2003** as OU methods paper | Destexhe **2001** |
| Fixed K while scaling N | Distance-dependent probabilities |
| Invented ±10% heterogeneity | Source ranges only, else 0% |
| Fixed 1.5 ms delay | Feng distance-dependent delay rule |
| Bare g without weight multiplier | g × W (Table 3 strength) |
| Abatis 2017 as a standalone citation | Feng et al. 2019 (Abatis is an SfN poster) |

---

## Implementation checklist

Before coding Run 1:

1. Open `Research/Sources/01_primary_bla_references.md` and copy Table 3 / 4 / 7 numbers into `full_parameters.json` with citation keys.
2. Open this map and tick every row used in the run.
3. Any row marked approximation (e.g. P_SOM_PN, SOM=PV kinetics) goes into `simulation/deviations.md`.
4. Do not invent values that are absent from Sources.
