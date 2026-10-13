## 18. Open Design Questions

These are not implementation gaps in an existing system — they are unresolved design decisions that need to be settled before or during implementation. Numbering is kept consistent with the architecture diagram.

**[1] Suppression gap scaling.** `expressed = raw × (1 − prefrontal_strength × k)` — the constant *k* (0.7 in the illustrative example) and the decay function for `prefrontal_strength` under sustained load have not been derived or justified.

**[2] Population size and synaptic weight scaling.** Open for all regions, BLA included. BLA has a concrete plan.

For BLA, the archived first campaign (Runs 1–5, September 2026; now classed as failed tests) suggested that the large-N collapse is a structural E/I asymmetry, not a resonance effect: under fixed in-degree, recurrent excitation per neuron stays constant while inhibitory populations grow. Those runs used wrong kinetics, so this is a **hypothesis**, not a result. Standard network-scaling theory (van Vreeswijk & Sompolinsky 1996; Brunel 2000; van Albada et al. 2015) explains it the same way: changing N with an inconsistent scaling rule shifts the E/I balance.

**Update 2026-10-13:** the clean Run 1 now wires **every** pathway to Feng's realised inputs per cell (PN→PN 25, FSI→PN 43, PN→FSI 215, FSI→FSI 22) at Feng's reduced size of 1,000 cells (640 / 260 / 100). The old plan (50 / 12 / 8 with Feng's distance probabilities) gave under one recurrent input per principal cell. Run 1's 500-vs-1,000 size check (Gate 5) tests whether rates are independent of N under this rule. See `Simulations/BLA/Research/architecture/`, `Simulations/BLA/reports/04_run1_redesign_oct2026.md` and `Research/reports/open_uncertainties.md` (U19, U23, U26).

For all other regions (CeA, PFC, HIP, INS, ACC, NAc, VTA, PAG, HYP), the population size and connectivity question remains open. Each region will be characterized in isolation before the full network is wired.

**[3] Emergent dynamics validation.** Whether inertia, bleed, sensitization, habituation, and refractory dynamics actually emerge robustly — and at what timescale — from the chosen population sizes and connectivity has not been tested at the multi-structure level.

**[4] Continuous limbic–LLM coupling.** Real-time synchronization between a continuously-running limbic thread and an LLM's token generation loop is an open engineering question. This likely requires a custom generation loop, since standard inference APIs do not support mid-stream state injection.

**[5] Affective-tag retrieval threshold.** No function has been defined for how similarity between the current limbic state and a stored affective tag should gate memory retrieval.

**[6] Arousal calibration.** No method has been defined for calibrating the noradrenaline-like arousal dimension independently of valence.

**[7] Autonomous initiation thresholds.** The trigger values in §8.2 (curiosity > 0.75, silence > 15s, prefrontal > 0.60) are placeholders with no calibration method attached.

**[8] Fine-tuning label provenance.** For the 200–300 training examples in §10.3, no method has been defined for deciding what the "correct" neural-state numbers are for a given exchange — this is a hidden research question, not just a data-collection task.

**[9] Validation of "genuine" vs. "performed" emotion.** No metric has been proposed for distinguishing genuine emotional dynamics from a system that merely produces plausible-looking outputs, beyond informal human judgment.

**[10] Scalability of affective priming.** Whether 50–100 topics is sufficient for meaningful "felt knowledge," and whether priming at larger scale would degrade retrieval discrimination, is untested.

## 19. Preliminary Simulation Notes (Informal, Exploratory Only)

**Note (updated October 2026):** The simulation history has grown substantially since this section was written. Tests 1 and 2 below were early informal checks during the design phase. They have since been followed by:

* A full-network simulation (10 regions simultaneously, 4 attempts), archived as failed. See `Simulations/Neurons_Connected/reports/full_network_attempts_1_to_4.md`.
* A first BLA isolated campaign (5 runs), archived as failed because it used guessed kinetics. It produced a plausible explanation of the collapse mechanism but validated no parameters. See `Simulations/BLA/reports/test_run_1/`.

The two tests below are preserved because they motivated open question [2] and the isolation-first simulation strategy. They are not the current state of the simulation work.

**Test 1 — independent neurons, shared drive, no internal coupling.** A population of Hodgkin–Huxley neurons was driven by a shared external step input (simulating a threat signal) with independent per-neuron noise, but with no synaptic connections between neurons in the population. Comparing N = 20, 500, and 2000: the population-averaged activation signal was nearly identical in shape across all three sizes. This is expected — without internal connectivity, population size only improves signal resolution (finer gradations of the reported intensity value), not response dynamics. Resolution scales as 1/N: a 20-neuron population can only report ~21 distinguishable intensity levels; a 500-neuron population, ~501.

**Test 2 — recurrent, conductance-based synapses with axonal delays.** A second population was built with actual excitatory/inhibitory synaptic connections between neurons (conductance-based, with transmission delays), tested across several regimes (weak/strong recurrence, high heterogeneity, drive-dominated, longer delays) at N = 20, 200, and 1000. Result: in strong-recurrence regimes, **N = 200 produced higher firing rates and dramatically stronger after-discharge (reverberation after the stimulus ended) than either N = 20 or N = 1000.** N = 1000 in particular showed near-total collapse of activity in the strongest-recurrence regime tested.

**Open interpretation question:** this collapse at N = 1000 could mean either (a) a genuine resonance effect, where intermediate population sizes support the richest reverberatory dynamics, or (b) an artifact of how connectivity was scaled — if connection probability (rather than a fixed number of inputs per neuron) was held constant, larger populations would receive proportionally more total synaptic drive unless weights were rescaled to compensate. Which of these explanations is correct has not been determined, and it materially changes the conclusion: a genuine resonance effect would argue for deliberately targeting population sizes near the observed sweet spot; a scaling artifact would mean the "collapse" says nothing about population size and would disappear once weights are corrected.

**Practical implication for §5.2.1:** the proposed population counts (BLA ≈ 70 combined, CeA = 20, PFC = 30) are smaller than the N ≈ 200 region where the exploratory test found the strongest reverberatory behavior in the most recurrent regime. This does not mean the proposed counts are wrong, but it means they have not been justified against this finding either, and should not be treated as settled until the scaling question above is resolved.

**Update — October 2026 (supersedes the September 2026 update):** The archived BLA campaign points toward interpretation (b), a connectivity-scaling artifact, rather than a genuine resonance effect. Under fixed in-degree, inhibitory populations scaled with N while recurrent excitation per neuron stayed constant, so inhibition won at large N. That is a different mechanism from the original fixed-probability N≈1000 collapse, and those runs used guessed kinetics (AMPA 2 ms, no Mg²⁺ block). The question is therefore **not yet settled** by simulation. Run 1's size check under a single in-degree rule for every pathway is the test (update 2026-10-13).

The practical implication for §5.2.1: the 50 / 12 / 8 BLA default was dropped on 2026-10-13. Run 1 uses Feng's 640 / 260 / 100; the BLA size in the live network is decided after the Run 1 speed benchmark (U26). An earlier version of this section said 50 / 12 / 8 had been tested "with literature-grounded parameters". That was incorrect: the archived runs used fixed K=3 and guessed kinetics, not Feng parameters.

Full simulation history: `Simulations/BLA/reports/test_run_1/` and `Simulations/Neurons_Connected/reports/`.
