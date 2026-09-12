# Software and Tools

### Brian2 — Neural simulation framework

> Stimberg M, Brette R, Goodman DF.
> **"Brian 2, an intuitive and efficient neural simulator"**
> *eLife*, 8, e47314, 2019.
> https://elifesciences.org/articles/47314

**What it provides:** The Python-based neural simulation framework used in Runs 1–5. Conductance-based synapses with axonal delays are well-supported. Recommended for Run 6 onward. The Feng et al. model was built in NEURON — parameters should be ported to Brian2 rather than switching simulators.

---

### NEURON — Reference simulator for Feng et al.

> Carnevale NT, Hines ML.
> **"The NEURON Book"**
> Cambridge University Press, 2006.
> https://neuron.yale.edu

**What it provides:** The simulator used by Feng et al. 2019. The ModelDB code for their model is in NEURON `.hoc` files. Reading these files extracts the exact parameter values used in their simulation. Python-compatible via the `neuron` Python package.

---

### ModelDB — Computational neuroscience model repository

> Hines ML, et al.
> **"ModelDB: A Database to Support Computational Neuroscience"**
> *Journal of Computational Neuroscience*, 2004.
> https://modeldb.science

**What it provides:** The repository hosting the Feng et al. 2019 BLA model code (accession 247968) and thousands of other published neural models. All models are freely downloadable. The BLA model code at https://github.com/ModelDBRepository/247968 contains the complete parameter set in runnable form.
