# Supporting Biological References — BLA

### Abatis et al. 2017 — PN→PN connectivity in BLA

> Abatis M, et al.
> **"Distance-dependent connectivity of BLA principal neurons"**
> 2017.

**What it provides:** Distance-dependent PN→PN connection probabilities in BLA: 3% at <50 μm, 2% at 50–100 μm, 1% at 100–200 μm, 0.5% at 200–600 μm. Source for Feng et al. Table 5. The simulation used a flat K=3 fixed in-degree (~6% at baseline scale) — substantially over-dense at all distance ranges.

---

### Paré et al. 1995, Samson and Paré 2006 — Recurrent connections in BLA

> Paré D, et al. 1995. *Journal of Neurophysiology.*
> Samson RD, Paré D. 2006.

**What these provide:** Evidence for recurrent connections within BLA (cited in Feng et al. Introduction). Establishes that the BLA is not a purely feedforward network — recurrent connectivity is a key feature, and the model must account for it. These connections enable the reverberatory activity (after-discharge / emotional inertia) that the thesis requires.

---

### Rainnie et al. 1993 — BLA neuron electrophysiology

> Rainnie DG, et al.
> **"Adenosine inhibition of mesolimbic dopamine release and motor activity"**
> *Journal of Neurophysiology*, 1993.

**What it provides:** Electrophysiological characterization of BLA neurons in vitro, including the two PN subtypes (adapting vs. continuous spiking) and FSI properties. Used by Feng et al. to set the adaptation ratio cutoff (1.5) for classifying PN types. The sAHP magnitude difference (50 mS/cm² for adapting vs. 0.2 mS/cm² for continuous) comes from this work.

---

### Zador et al. 1990 — NMDA Mg²⁺ block

> Zador A, Koch C, Brown TH.
> **"Biophysical model of a Hebbian synapse"**
> *PNAS*, 87(17), 1990.

**What it provides:** The voltage-dependent Mg²⁺ block function for NMDA receptors: s(V) = [1 + 0.33 × exp(−0.06V)]⁻¹. This function gates NMDA conductance by membrane voltage — at resting potential (~−70 mV), NMDA is largely blocked; it opens as the membrane depolarizes. This was completely absent from Runs 1–5, causing NMDA to behave as a constant current source at all voltages.
