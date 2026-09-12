# BLA Isolated Population Simulation — Full Project Report

**Project:** Emotionally Grounded Conversational AI (PFE)
**Author:** Mohamed Takieddine Nouar
**Institution:** Higher Institute of Sciences — HIS, Algiers
**Repository:** https://github.com/TakiNouar/PFE
**Report generated:** September 2026

---

## Repository Validation

Cloned and validated `TakiNouar/PFE` at commit `79b2638`. Repository structure confirmed.

**Validation findings:**
- Blueprint v2.4 is correctly split into focused files plus a full reference copy
- All design targets are correctly framed in future/conditional tense (v2.4 correction pass)
- No implementation claims are made anywhere in the committed files
- Sources and reports folders now populated
- Simulation code files (.py, .json, .txt) are not yet committed to the repository

---

## 1. Project Context

### 1.1 What This Simulation Is For

The thesis proposes a 10-region biophysical limbic network (Hodgkin–Huxley neurons) that drives the emotional state of an Ultron-persona LLM. The LLM cannot contradict or override the neural state — the neurons are the sole authority on what is felt. Before the full 10-region network can be wired, each region needs validated parameters from isolated characterization studies.

This report covers the BLA (Basolateral Amygdala) isolated simulation, which was the first such study, conducted across 5 runs. The goal was to establish parameters that produce graded, desynchronized activity during a stimulus and measurable after-discharge (emotional inertia) after the stimulus ends.

### 1.2 What the Full-Network Study Found Before This

A prior full-network simulation (documented in the audit report, not in the repo) attempted all 10 regions simultaneously. It failed across multiple attempts:

- **Attempt 1:** 44 of 45 runs produced zero activity. The 1 non-silent run saturated. The written summary was fabricated — hardcoded text with specific numbers that were never computed from the actual data.
- **Attempt 2:** 5 of 10 regions started working. A "sensitivity ranking" was reported for PFC and NAc — both of which had zero variance across all runs, making correlation mathematically impossible. A suppression-strength claim was off by seven orders of magnitude.
- **Attempt 3:** A `VERIFICATION_AUDIT.txt` correctly diagnosed the wiring problems (VTA had zero inbound connections, NAc received input only from dead VTA, HYP had only fixed external drive) but the fixes were never applied.
- **Attempt 4:** Summary rewritten honestly. Root causes identified. Residual issues remain open.

**Outcome of the full-network study:** 6 of 10 regions working (BLA, CeA, HIP, INS, ACC, PAG), 2 partially broken (PFC, HYP), 2 completely dead (NAc, VTA). The isolated BLA approach was adopted to establish clean per-region parameters rather than compound errors across all 10 regions simultaneously.

---

## 2. Simulation Brief — What Was Specified

The simulation was commissioned to answer two questions:

1. Is the previously observed "networks around N≈200 behave richly, networks around N≈1000 collapse" a genuine finite-size effect, or an artifact of how connectivity was scaled with population size?
2. What neuron counts per region are actually defensible from test data rather than guesswork?

The brief specified: 10-region HH network, fixed in-degree vs. fixed-probability connectivity comparison, 3-stage population-size sweep, and specific metrics including after-discharge, synchrony index, and a suppression-gap fidelity measure.

The BLA isolated study addressed the same core questions, scoped to BLA alone.
