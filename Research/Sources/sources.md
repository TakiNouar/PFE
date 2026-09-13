# Research Sources — Emotionally Grounded Conversational AI (PFE)

> **Prefer the split modules** `01_primary_bla_references.md` … `07_reading_priority.md` for current, verified provenance.  
> This monolithic copy was re-synced September 2026 after an accidental empty push.

**Project:** BLA Isolated Population Simulation / Full Limbic Network  
**Author:** Mohamed Takieddine Nouar  
**Last updated:** September 2026

---

## Provenance rules (strict)

1. Feng Table 3/4 upstream citations win over secondary summaries.
2. AMPA 6.9/2.4 ms: Feng cites **Mahanty & Sah 1998 + Guzman et al. 2016** — not Mahanty & Sah 1999 as the τ source.
3. GABA-A 0.5/6.8 ms: **Galarreta & Hestrin 1997**.
4. STP: FSI→PN D=0.6, PN→FSI D=0.7 (Woodruff & Sah 2007); PN→PN D=**0.5** (Silberberg et al. 2004, neocortex).
5. Noise equations: **Destexhe et al. 2001** (*Neuroscience* 107); 2003 Nat Rev Neurosci = review only.
6. Full detail: `01_primary_bla_references.md`, `ACCURACY_VERIFICATION_CORRECTIONS.md`, `Research/reports/literature_provenance_audit_sep2026.md`.

---

## Primary (must-read)

### Feng et al. 2019
Feng F, Headley DB, Amir A, Kanta V, Chen Z, Paré D, Nair SS. *eNeuro* 6(1), 2019. DOI 10.1523/ENEURO.0388-18.2018. ModelDB **247968**.

### Kim et al. 2013
Kim D, Paré D, Nair SS. **"Mechanisms contributing to the induction and storage of Pavlovian fear memories in the lateral amygdala"** *Learning & Memory* 20:421–430, 2013. ModelDB **150288**.

### Mahanty & Sah 1998
Nature 394:683–687. Co-cited by Feng for AMPA kinetics (with Guzman 2016).

### Mahanty & Sah 1999
Eur J Neurosci 11:1217–1222. Companion LA pyramidal inputs paper — **supporting only**, not Feng’s Table 3 τ attribution.

### Guzman et al. 2016
Science 353:1117–1123 (CA3; best match for Feng’s Guzman 2016 — confirm ref list).

### Galarreta & Hestrin 1997
GABA-A kinetics upstream for Feng Table 3.

### Woodruff & Sah 2007
FSI connectivity and FSI-related STP (not PN→PN D_max).

### Silberberg et al. 2004
Neocortical source of PN→PN D_max=0.5 in Feng Table 4.

### Destexhe et al. 2001
*Neuroscience* 107:13–24 — OU / point-conductance **methods** source Feng cites.

### Destexhe et al. 2003
*Nat Rev Neurosci* 4:739–751 — high-conductance **review only**.

### Weisskopf, Bauer & LeDoux 1999
J Neurosci 19:10512–10519 — LTP / L-type Ca at thalamic inputs. **Not confirmed** as τ_NMDA=125 ms measurement source.

### Rainnie et al. 1993
**"Intracellular recordings from morphologically identified neurons of the basolateral amygdala"** J Neurophysiol 69:1350–1362. DOI 10.1152/jn.1993.69.4.1350. PMID 8492168.

### Headley et al. 2021
Headley DB, **Kyriazi P**, Feng F, Nair SS, Paré D. J Neurosci 41:6087–6101.

### Cattani et al. 2024
Cattani A, Arnold DB, McCarthy M, Kopell N. eLife 12:RP89519. DOI 10.7554/eLife.89519.4.

### Zador et al. 1990
Mg block formula used by Feng.

### McDonald series (cell types)
- McDonald & Betette 2001 — PV ~50% of INs  
- McDonald & Mascagni 2002 — SOM 11–18%  
- Mascagni & McDonald 2003 — CCK only (not blanket taxonomy source)

---

## Computational

- Hodgkin & Huxley 1952  
- Destexhe et al. 1994 dual-exponential synapses  
- Wang & Buzsáki 1996 = **ING** (not PING); BLA gamma in Feng is **PING** (Traub/Whittington 1997 framework)

---

For tables, footnotes, and architecture binding see split Sources files and `Simulation tests/BLA/Research/architecture/12_sources_map.md`.
