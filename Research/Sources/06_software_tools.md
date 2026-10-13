# Software and Tools

**Simulator for BLA Run 1: NEURON 9.0.2 with Feng's ModelDB 247968 files unchanged (U13 resolved, 2026-10-13).** The simulator for the live engine is decided after the Run 1 speed benchmark (U26). See `Simulations/BLA/Research/architecture/03_neuron_models.md` and `07_simulation_protocol.md`.

---

### NEURON — Reference simulator for Feng et al. (preferred)

> Carnevale NT, Hines ML.
> **"The NEURON Book"**
> Cambridge University Press, 2006.
> https://neuron.yale.edu

**What it provides:** The simulator used by Feng et al. 2019. The ModelDB code for their model is in NEURON `.hoc` / `.mod` files. Running those files directly keeps every coefficient faithful to the paper. Python-compatible via the `neuron` package.

**Installing on Windows (checked October 2026):** NEURON 9.0.2 (2026-08-10, Python 3.10–3.14) ships PyPI wheels for Linux and macOS only, so `pip install neuron` fails on native Windows. Use the official installer `nrn-9.0.2.w64-mingw-py-310-311-312-313-314-setup.exe` from github.com/neuronsimulator/nrn/releases with a python.org CPython, or WSL2 Ubuntu + `pip install neuron==9.0.2`. The archived blocker (`import neuron` failed; pip 502 from an internal mirror; a `libnrnmech.so` on disk) came from a Linux sandbox's network, not from NEURON. Feng's mod files were updated in 2022 for NEURON 8.2/9.0. Keep build paths free of spaces; this is why the repo folder is named `Simulations/`.

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
