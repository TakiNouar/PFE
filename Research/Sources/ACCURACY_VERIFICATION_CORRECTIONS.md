# Research Folder — Accuracy Verification Corrections Log

**Last updated:** September 2026 (provenance correction pass)

## High-priority provenance fixes (this pass)

| Issue | Correction |
|-------|------------|
| AMPA source | Feng Table 3 cites **Mahanty & Sah 1998 + Guzman et al. 2016**, not Mahanty & Sah 1999. 1999 paper remains a real companion study but is not Feng’s cited source for the 6.9 ms value. |
| GABA-A source | Feng Table 3 attributes 0.5/6.8 ms to **Galarreta & Hestrin 1997**. Added. |
| STP PN→PN | D_max = **0.5** (not 0.6); source = **Silberberg et al. 2004 (neocortex)**. Woodruff & Sah 2007 covers FSI-related connections only. |
| Destexhe noise model | Methods source = **Destexhe, Rudolph, Fellous, Sejnowski 2001**, *Neuroscience* 107:13–24. The 2003 *Nat Rev Neurosci* paper is a different review. |
| Population counts | Locked to blueprint **50 Pyr / 12 PV / 8 SOM**. 150/112/108 is historical only and not biologically interchangeable. |

## Previously applied fixes (still valid)

- Rainnie 1993 title corrected
- Weisskopf 1999 title corrected + hedged on τ_NMDA source
- Headley 2021 second author = Kyriazi P
- Kim 2013 title/journal corrected
- eLife 2024 authors = Cattani, Arnold, McCarthy, Kopell
- Wang & Buzsáki = ING, not PING
- Suppression ratio unified to ~2×
- Full-network attempts = 4

## Still open

1. Exact Feng footnote for τ_NMDA = 125 ms.
2. Full bibliographic line for Guzman et al. 2016 and Silberberg et al. 2004 from Feng’s reference list.
3. Full DOI for Abatis et al. 2017 if cited independently of Feng.

None of these corrections change the numerical kinetic targets used by the architecture; they correct **provenance** so the thesis can defend every number.
