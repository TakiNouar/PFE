# Reading Priority for Next Implementation (clean BLA Run 1)

| Priority | Paper / code | Specific sections to read |
|---|---|---|
| ⭐⭐⭐ | Feng et al. 2019 | Methods (Model Implementation, synaptic equations, delay rule, extrinsic inputs), Tables 1–7 |
| ⭐⭐⭐ | Feng et al. 2019 ModelDB 247968 | `pyrD2pyrD_STFD_new.mod` and the other `*_STFD*.mod` files (kinetics, weights, STP), `function_ConnectInternal_simplify_online_op.hoc` (weights, delays), cell templates, `sahp.mod`, `Gfluct_new_*.mod` |
| ⭐⭐ | Kim et al. 2013 (*Learn Mem*) + ModelDB 150288 | Single-cell PN/FSI models, I_sAHP |
| ⭐⭐ | Mahanty & Sah 1998 (*Nature*) | AMPA kinetics; Feng cites it (with Guzman 2016) for **both** PN→PN and PN→FSI |
| ⭐⭐ | Woodruff & Sah 2007 (*J Neurosci* 27:553–563) | FSI connectivity, gap junctions, FSI↔PN short-term depression |
| ⭐⭐ | Destexhe, Rudolph, Fellous & Sejnowski 2001 (*Neuroscience* 107:13–24) | Point-conductance / OU noise equations (the methods source Feng cites) |
| ⭐ | Weisskopf, Bauer & LeDoux 1999 (*J Neurosci* 19:10512–10519) | Feng’s cited source for NMDA 3.7 / 125 ms (ref. [115], confirmed) |
| ⭐ | Galarreta & Hestrin 1997 (*J Neurosci* 17:7220–7227) | GABA-A 0.5 / 6.8 ms |
| ⭐ | Silberberg, Wu & Markram 2004 (*J Physiol* 556:19–27) | PN→PN depression (neocortical; imported by Feng) |
| ⭐ | Cattani et al. 2024 (*eLife*) | SOM & VIP additional currents (NaP, H, D); PING support of fear learning |
| background | Mahanty & Sah 1999 (*Eur J Neurosci*) | LA principal-cell glutamatergic inputs — supporting only, not Feng’s Table 3 source |
| background | Destexhe, Rudolph & Paré 2003 (*Nat Rev Neurosci*) | High-conductance state review — conceptual only, not the noise-methods source |

---

*Updated October 2026 after the consistency pass and verification against Feng’s full text and the ModelDB code. This list will be revised for CeA characterization and the multi-region network.*
