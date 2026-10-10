# Software and Tools

**Simulator decision for clean BLA Run 1 is still open (U13).** The architecture prefers NEURON + ModelDB mechanisms (strict path), with Brian2 as a documented fallback (pragmatic path). See `Simulations/BLA/Research/architecture/03_neuron_models.md`. Do not mix the two silently.

---

### NEURON — Reference simulator for Feng et al. (preferred)

> Carnevale NT, Hines ML.
> **"The NEURON Book"**
> Cambridge University Press, 2006.
> https://neuron.yale.edu

**What it provides:** The simulator used by Feng et al. 2019. The ModelDB code for their model is in NEURON `.hoc` / `.mod` files. Running those files directly keeps every coefficient faithful to the paper. Python-compatible via the `neuron` package.

**Known blocker from the archived campaign:** `import neuron` failed and `pip install neuron` returned 502 from a mirror. Before Run 1, verify a working install and that `nrnivmodl` can compile the ModelDB `.mod` files. Keep build paths free of spaces; this is why the repo folder is named `Simulations/`.

---

### Brian2 — Python simulator (fallback)

> Stimberg M, Brette R, Goodman DF.
> **"Brian 2, an intuitive and efficient neural simulator"**
> *eLife*, 8, e47314, 2019.
> https://elifesciences.org/articles/47314

**What it provides:** Python-based simulator used in the archived Runs 1–5. Suitable for the pragmatic path only if every coefficient is copied from Feng tables / ModelDB `.mod` files and every approximation is logged in `deviations.md`. Known approximations include dual-exponential versus the kinetic synapse scheme, and analytic OU versus `Gfluct`.

---

### ModelDB — Computational neuroscience model repository

> Hines ML, et al.
> **"ModelDB: A Database to Support Computational Neuroscience"**
> *Journal of Computational Neuroscience*, 2004.
> https://modeldb.science

**What it provides:** Hosts the Feng et al. 2019 BLA model (accession **247968**, mirror https://github.com/ModelDBRepository/247968) and Kim et al. 2013 (accession **150288**). The file map for 247968 is in `01_primary_bla_references.md`.
