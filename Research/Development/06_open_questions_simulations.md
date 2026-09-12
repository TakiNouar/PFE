## 18. Open Design Questions

These are not implementation gaps in an existing system — they are unresolved design decisions that need to be settled before or during implementation. Numbering is kept consistent with the architecture diagram.

**[1] Suppression gap scaling.** `expressed = raw × (1 − prefrontal_strength × k)` — the constant *k* (0.7 in the illustrative example) and the decay function for `prefrontal_strength` under sustained load have not been derived or justified.

**[2] Population size and synaptic weight scaling.** How many neurons per structure, and under what connectivity rule? Informal simulation (§19) suggests this interacts with whether connectivity uses fixed in-degree or fixed connection probability — these two choices predict different outcomes as population size grows, and this has not been resolved.

**[3] Emergent dynamics validation.** Whether inertia, bleed, sensitization, habituation, and refractory dynamics actually emerge robustly — and at what timescale — from the chosen population sizes and connectivity has not been tested at the multi-structure level.

**[4] Continuous limbic–LLM coupling.** Real-time synchronization between a continuously-running limbic thread and an LLM's token generation loop is an open engineering question. This likely requires a custom generation loop, since standard inference APIs do not support mid-stream state injection.

**[5] Affective-tag retrieval threshold.** No function has been defined for how similarity between the current limbic state and a stored affective tag should gate memory retrieval.

**[6] Arousal calibration.** No method has been defined for calibrating the noradrenaline-like arousal dimension independently of valence.

**[7] Autonomous initiation thresholds.** The trigger values in §8.2 (curiosity > 0.75, silence > 15s, prefrontal > 0.60) are placeholders with no calibration method attached.

**[8] Fine-tuning label provenance.** For the 200–300 training examples in §10.3, no method has been defined for deciding what the "correct" neural-state numbers are for a given exchange — this is a hidden research question, not just a data-collection task.

**[9] Validation of "genuine" vs. "performed" emotion.** No metric has been proposed for distinguishing genuine emotional dynamics from a system that merely produces plausible-looking outputs, beyond informal human judgment.

**[10] Scalability of affective priming.** Whether 50–100 topics is sufficient for meaningful "felt knowledge," and whether priming at larger scale would degrade retrieval discrimination, is untested.

## 19. Preliminary Simulation Notes (Informal, Exploratory Only)

**These are not part of the PFE's formal evidence base.** They were run as quick exploratory checks during the design phase, on simplified single-region models, not the full multi-structure architecture. They are recorded here so the reasoning behind open question [2] is not lost.

**Test 1 — independent neurons, shared drive, no internal coupling.** A population of Hodgkin–Huxley neurons was driven by a shared external step input (simulating a threat signal) with independent per-neuron noise, but with no synaptic connections between neurons in the population. Comparing N = 20, 500, and 2000: the population-averaged activation signal was nearly identical in shape across all three sizes. This is expected — without internal connectivity, population size only improves signal resolution (finer gradations of the reported intensity value), not response dynamics. Resolution scales as 1/N: a 20-neuron population can only report ~21 distinguishable intensity levels; a 500-neuron population, ~501.

**Test 2 — recurrent, conductance-based synapses with axonal delays.** A second population was built with actual excitatory/inhibitory synaptic connections between neurons (conductance-based, with transmission delays), tested across several regimes (weak/strong recurrence, high heterogeneity, drive-dominated, longer delays) at N = 20, 200, and 1000. Result: in strong-recurrence regimes, **N = 200 produced higher firing rates and dramatically stronger after-discharge (reverberation after the stimulus ended) than either N = 20 or N = 1000.** N = 1000 in particular showed near-total collapse of activity in the strongest-recurrence regime tested.

**Open interpretation question:** this collapse at N = 1000 could mean either (a) a genuine resonance effect, where intermediate population sizes support the richest reverberatory dynamics, or (b) an artifact of how connectivity was scaled — if connection probability (rather than a fixed number of inputs per neuron) was held constant, larger populations would receive proportionally more total synaptic drive unless weights were rescaled to compensate. Which of these explanations is correct has not been determined, and it materially changes the conclusion: a genuine resonance effect would argue for deliberately targeting population sizes near the observed sweet spot; a scaling artifact would mean the "collapse" says nothing about population size and would disappear once weights are corrected.

**Practical implication for §5.2.1:** the proposed population counts (BLA ≈ 70 combined, CeA = 20, PFC = 30) are smaller than the N ≈ 200 region where the exploratory test found the strongest reverberatory behavior in the most recurrent regime. This does not mean the proposed counts are wrong, but it means they have not been justified against this finding either, and should not be treated as settled until the scaling question above is resolved.
