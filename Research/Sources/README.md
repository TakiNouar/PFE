# Research Sources

Literature and parameter references for the biophysical limbic simulation. This folder holds **literature only**. Correction logs and audits live in `Research/reports/`.

## Structure

| File | Content |
|------|---------|
| [01_primary_bla_references.md](01_primary_bla_references.md) | ⭐ Feng et al. 2019 (Tables 3–7, delays, inputs, ModelDB file map) + Kim, Mahanty, Guzman, Galarreta, Woodruff, Silberberg, Destexhe 2001, Weisskopf |
| [02_supporting_biological.md](02_supporting_biological.md) | Abatis (SfN poster), Samson & Paré, Rainnie, Zador, McDonald/Mascagni cell types |
| [03_extended_models.md](03_extended_models.md) | Cattani 2024, Headley 2021, related |
| [04_fear_memory_dynamics.md](04_fear_memory_dynamics.md) | Fear consolidation, amygdala–HIP |
| [05_computational_neuroscience.md](05_computational_neuroscience.md) | HH, Destexhe kinetic synapses, Destexhe 2001 noise, W&B ING vs PING |
| [06_software_tools.md](06_software_tools.md) | NEURON (preferred), Brian2 (fallback), ModelDB |
| [07_reading_priority.md](07_reading_priority.md) | Ordered reading for implementation |
| [08_bla_2026_paper_batch.md](08_bla_2026_paper_batch.md) | **2026 assessment batch** (Báldi, Perumal & Sah, Zhang, Yau, astrocytes, …) |

## Provenance rules (strict)

1. Feng Table 3/4 upstream citations win over secondary summaries.
2. AMPA 6.9 / 2.4 ms: Feng cites **Mahanty & Sah 1998 + Guzman et al. 2016**, not Mahanty & Sah 1999.
3. NMDA 3.7 / 125 ms: Feng cites **Weisskopf, Bauer & LeDoux 1999** (ref. [115]).
4. GABA-A 0.5 / 6.8 ms: **Galarreta & Hestrin 1997**.
5. STP: FSI→PN 0.6, PN→FSI 0.7 (Woodruff & Sah 2007); PN→PN **0.5** (Silberberg et al. 2004, neocortex).
6. Noise equations: **Destexhe et al. 2001** (*Neuroscience* 107). The 2003 *Nat Rev Neurosci* paper is a review only.
7. PN→PN distance bands: cite **Feng 2019** (its basis, Abatis 2017, is an unpublished SfN poster).

Audit trail: `Research/reports/literature_provenance_audit_sep2026.md` and `Research/reports/consistency_and_source_verification_oct2026.md`.

**Quick start for Run 1:** `01_primary_bla_references.md` + `Simulations/BLA/Research/architecture/12_sources_map.md`.
**Biology beyond kinetics:** dossier under `Simulations/BLA/Research/` + the `08_` batch index.
