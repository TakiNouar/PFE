# Open Uncertainties — BLA / Research Track

**Date:** September 2026  
**Purpose:** Single place for unresolved provenance, implementation, and design questions. Not a list of known errors (those are fixed or logged in `ACCURACY_VERIFICATION_CORRECTIONS.md`).

**Authority while open:** Prefer Feng Table numbers + `Simulation tests/BLA/Research/architecture/`. Do not invent fill-ins. Record any temporary choice in `simulation/deviations.md`.

---

## 1. Literature provenance (thesis-blocking if cited wrongly)

| ID | Uncertainty | Why it matters | Suggested resolution |
|----|-------------|----------------|----------------------|
| **U1** | Exact Feng Table 3 / Methods **footnote for τ_NMDA = 125 ms** | Weisskopf et al. 1999 is *not* confirmed as the measurement source; wrong attribution in a thesis is a citation failure | Open Feng 2019 PDF reference list + Table 3 footnotes; record paper + page |
| **U2** | **Guzman et al. 2016** vs Feng’s numbered reference | Best match is Guzman, Schlögl, Frotscher, Jonas *Science* 353:1117–1123 (hippocampal **CA3**, not BLA). Feng co-cites it with Mahanty & Sah 1998 for AMPA kinetics | Confirm Feng ref number; if different Guzman 2016, replace; if same, keep CA3 caveat in every citation |
| **U3** | Full bibliographic line for **Silberberg et al. 2004** | Source of PN→PN D_max = 0.5 (neocortex); Feng flags no BLA-specific data | Copy exact entry from Feng reference list |
| **U4** | Full **Abatis et al. 2017** citation (journal, DOI, pages) | Distance-dependent PN→PN probabilities (3/2/1/0.5%) | Find DOI or state explicitly “cited only via Feng Tables 5–6 / unpublished” |
| **U5** | Primary paper for **VIP/CR interneuron %** in rat BLA | Taxonomy table left VIP row open; not Mascagni & McDonald 2003 | McDonald/Mascagni series or later quantitative review; one primary paper |
| **U6** | Exact title/pages for **Galarreta & Hestrin 1997** as Feng cites it | GABA-A 0.5/6.8 ms upstream | Match Feng ref list entry character-for-character |
| **U7** | **Mahanty & Sah 1999** role | Companion LA pyramidal paper exists; Feng Table 3 attributes AMPA τs to 1998 + Guzman 2016, not 1999 | Keep 1999 as supporting only unless Feng footnote says otherwise |

**Settled (do not re-open without new primary evidence):**

- AMPA 6.9 / 2.4 ms attribution in repo follows **Feng Table 3** (1998 + Guzman 2016), not the older “1999 for PN” secondary guess.
- Noise **methods** paper = Destexhe et al. **2001** (*Neuroscience* 107); 2003 *Nat Rev Neurosci* = review only.
- Headley 2021 second author = **Kyriazi P** (not Kanta V).
- Kim 2013 = *Learn Mem* 20:421–430, ModelDB 150288.
- Rainnie 1993 = intracellular BLA morphology paper (not the adenosine title).
- Wang & Buzsáki 1996 = **ING**; Feng BLA gamma = **PING**.

---

## 2. Architecture / Run 1 implementation

| ID | Uncertainty | Default until resolved |
|----|-------------|------------------------|
| **U8** | FSI OU τ_e, τ_i, E_e, E_i exact Table 7 / ModelDB values | Copy from ModelDB 247968 into `full_parameters.json` before first run; do not leave “as in ModelDB” blank |
| **U9** | Synaptic delay 1.5 ms vs any per-type ModelDB delays | Use 1.5 ms unless ModelDB differs; document in `full_parameters.json` |
| **U10** | SOM = PV kinetics for Run 1 | Allowed only with `deviations.md` entry; real SOM needs NaP/H (Cattani et al. 2024) later |
| **U11** | `P_SOM_PN = 0.34` | Approximation (same as PV→PN); not a Feng Table value — must stay in `deviations.md` |
| **U12** | Passive parameters (C_m, R_m, …) “typical ranges” | Prefer exact Kim/Feng template values; no invented ±10% heterogeneity |
| **U13** | Simulator: NEURON+ModelDB vs Brian2 re-implementation | Prefer NEURON; Brian2 only with full coefficient table + deviations |
| **U14** | Intermittent gamma at N=70 | Diagnostic only, not a pass/fail gate |

---

## 3. Design / blueprint (non-blocking for isolated Run 1)

| ID | Uncertainty | Notes |
|----|-------------|-------|
| **U15** | Mid-generation LLM state injection mechanism | Open question [4]; llama.cpp / vLLM callbacks may reduce need for a fully custom loop — still unproven for this stack |
| **U16** | Computational definition of face `neutral` for autonomous initiation | Placeholder in camera section; needs explicit vector/threshold rule before implementation |
| **U17** | Suppression-gap constant *k* and prefrontal fatigue law | Still open design [1] |
| **U18** | Population / connectivity scaling for **non-BLA** regions | Q[2] partially resolved for BLA only |
| **U19** | Whether 50/12/8 remains optimal after Feng-faithful Run 1 | Architecture default; revise only with measured gates + written decision |

---

## 4. Conflicting secondary reports (how to read them)

An older “Full Accuracy Verification Report” recommended some changes that **conflict** with direct Feng Table/Methods checks:

| Topic | Older report said | Current repo stance |
|-------|-------------------|---------------------|
| AMPA 6.9 ms | Prefer Mahanty & Sah **1999** for PN | **Feng Table 3:** 1998 + Guzman 2016 |
| Destexhe noise | Change citations to **2003** | **2001** methods; 2003 review only |

When secondary audits disagree, **primary source text (Feng) wins**. See `literature_provenance_audit_sep2026.md`.

---

## 5. Housekeeping

- Update this file when U1–U7 close (cite PDF page / ref number).
- Do not delete closed items; move them to a “Resolved” section with date and evidence.
- Blueprint remains a living outline; closing U18–U19 may trigger a blueprint bump, not the reverse.

---

*Related:* `ACCURACY_VERIFICATION_CORRECTIONS.md` · `literature_provenance_audit_sep2026.md` · `cell_type_taxonomy_citation_check.md` · `architecture/12_sources_map.md`
