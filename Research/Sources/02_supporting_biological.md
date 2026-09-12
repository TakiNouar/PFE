# Supporting Biological References — BLA

### Abatis et al. 2017 — PN→PN connectivity in BLA

> Abatis M, et al.
> **"Distance-dependent connectivity of BLA principal neurons"**
> 2017.

**Status:** Full journal citation (volume, pages, DOI) could not be located at the time of this verification pass. The distance-dependent probabilities (3 % <50 µm, 2 % 50–100 µm, 1 % 100–200 µm, 0.5 % 200–600 µm) appear in Feng et al. 2019 Tables 5–6 and are attributed there to anatomical measurements. Treat the numbers as coming from Feng et al.; do not cite a free-standing “Abatis 2017” paper in the thesis until a DOI/PMID is confirmed.

**What the numbers provide:** Distance-dependent PN→PN connection probabilities used by Feng et al. The earlier simulation used a flat K=3 fixed in-degree (~6 % at baseline scale) — substantially over-dense relative to these values.

---

### Paré et al. 1995, Samson and Paré 2006 — Recurrent connections in BLA

> Paré D, et al. 1995. *Journal of Neurophysiology.*
> Samson RD, Paré D. 2006.

**What these provide:** Evidence for recurrent connections within BLA (cited in Feng et al. Introduction). Establishes that the BLA is not a purely feedforward network — recurrent connectivity is a key feature.

---

### Rainnie et al. 1993 — BLA neuron electrophysiology

> Rainnie DG, Asprodini EK, Shinnick-Gallagher P.
> **"Intracellular recordings from morphologically identified neurons of the basolateral amygdala."**
> *Journal of Neurophysiology*, 69(4):1350–1362, 1993.
> DOI: 10.1152/jn.1993.69.4.1350 · PMID: 8492168

**What it provides:** Electrophysiological characterization of BLA neurons in vitro, including adapting vs continuous-spiking principal-cell subtypes and FSI properties. Used by Feng et al. / Kim et al. for adaptation classification and sAHP magnitude differences. (Previous draft incorrectly listed an unrelated adenosine/dopamine title; corrected here.)

---

### Zador et al. 1990 — NMDA Mg²⁺ block

> Zador A, Koch C, Brown TH.
> **"Biophysical model of a Hebbian synapse"**
> *PNAS*, 87(17), 1990.

**What it provides:** The voltage-dependent Mg²⁺ block function for NMDA receptors: s(V) = [1 + 0.33 × exp(−0.06V)]⁻¹. This function gates NMDA conductance by membrane voltage — at resting potential (~−70 mV), NMDA is largely blocked; it opens as the membrane depolarizes. This was completely absent from Runs 1–5, causing NMDA to behave as a constant current source at all voltages.
