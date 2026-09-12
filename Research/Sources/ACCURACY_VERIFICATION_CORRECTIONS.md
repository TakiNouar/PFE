# Research Folder — Accuracy Verification Corrections Log

**Last updated:** September 2026 (strict primary-source verification against Feng Methods/Tables)

## Strict verification pass (this document set)

Checked directly against Feng et al. 2019 (Methods + Tables 1–7), not against prior repo “corrections” alone.

| # | Issue | Correction applied |
|---|-------|--------------------|
| 1 | AMPA 6.9/2.4 ms attributed to Mahanty & Sah **1999** | Restored to **Mahanty & Sah 1998 + Guzman et al. 2016** (as Feng Table 3). 1999 paper = supporting only, not the τ source. Guzman 2016 = Science CA3 paper (best match; confirm Feng ref #). |
| 2 | GABA-A 0.5/6.8 ms had no upstream citation | **Galarreta & Hestrin 1997** added (Feng Table 3). |
| 3 | STP: D_max=0.6 for both FSI→PN and PN→PN; both to Woodruff & Sah | **FSI→PN 0.6**, **PN→FSI 0.7** (Woodruff & Sah 2007, BLA); **PN→PN 0.5** (**Silberberg et al. 2004, neocortex** — Feng’s explicit approximation). |
| 4 | Noise model cited as Destexhe 2003 Nat Rev Neurosci | Reverted to **Destexhe, Rudolph, Fellous, Sejnowski 2001**, *Neuroscience* 107:13–24 (what Feng Methods cite). 2003 = review only. |
| 5 | Population 150/112/108 vs 50/12/8 | Locked to **50/12/8** for clean Run 1; 150/112/108 archive-only, not interchangeable E/I. |

## Items verified accurate (no change)

- Feng 2019 identity, DOI, ModelDB 247968, scale 27k, composition 64/26/10
- Table 3 numeric kinetics and E_GABA = −75 mV
- Mg block formula → Zador et al. 1990
- Connectivity % and distance bands → Abatis via Feng Tables 5–6
- Kim 2013 DOI / ModelDB 150288
- Headley 2021 second author Kyriazi P
- Cattani et al. 2024 eLife
- Weisskopf 1999 hedge on τ_NMDA source

## Still open before thesis citation

1. Exact Feng footnote for τ_NMDA = 125 ms.
2. Confirm Guzman et al. 2016 against Feng’s numbered reference list (CA3 paper is best match, not amygdala).
3. Full bibliographic line for Silberberg et al. 2004 from Feng’s reference list.
4. Full DOI for Abatis et al. 2017 if cited independently of Feng.

**Numeric kinetic targets used by the architecture are unchanged.** This pass corrects **provenance** so every number can be defended.

Full write-up: `Research/reports/literature_provenance_audit_sep2026.md`
