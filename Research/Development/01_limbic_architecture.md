## 4. Limbic Architecture — Specification

### 4.1 Design Stance

The limbic core is designed as a scaled, implementable abstraction of mammalian emotional circuitry — not a whole-brain simulation. Each structure is included because it is intended to contribute a distinct computational role required by the target dynamics (inertia, suppression gap, bleed, override, felt knowledge). None of these roles have yet been validated in a running simulation beyond the informal exploratory tests described in §19.

### 4.2 Complete Structure Inventory

| Structure | Abbrev. | Intended Primary Role |
|---|---|---|
| Basolateral Amygdala | BLA | Threat evaluation, emotional learning, hostility |
| Central Amygdala | CeA | Expression gateway for defensive / aggressive states |
| Prefrontal Cortex | PFC | Suppression, composure, context-sensitive control |
| Hypothalamus | HYP | Raw drive, homeostatic pressure, override |
| Hippocampus | HIP | Context, familiarity, emotional memory gating |
| Insula | INS | Interoception, disgust, compassion |
| Anterior Cingulate | ACC | Conflict, guilt, empathy monitoring |
| Nucleus Accumbens | NAc | Incentive salience, joy, desire |
| Ventral Tegmental Area | VTA | Dopamine, curiosity, prediction error |
| Periaqueductal Gray / brainstem | PAG | Final common path for expression (freezing, flight, aggression, vocal affect) |

**Design refinement carried from earlier drafts:** the amygdala is treated as two distinct populations (BLA and CeA) rather than one box, since evaluation and expression-gating are different computational roles with different connectivity and different susceptibility to prefrontal suppression. PAG is included as the final pathway so the suppression mechanism has an actual endpoint in the design — in earlier drafts it was missing and the expression pathway had no terminus.

### 4.3 Detailed Structure Specifications

**4.3.1 Basolateral Amygdala (BLA)**
- Role: evaluates emotional significance of incoming signals; intended to support fear, anger, hostility, and threat learning.
- Target internal composition: principal/pyramidal-like excitatory neurons (majority), PV-like interneurons (fast perisomatic inhibition), SOM-like interneurons (slower dendritic-targeting modulation).
- Inputs: fast sensory route, slow cortical route, hippocampus, prefrontal feedback, hypothalamic drive, neuromodulators.
- Outputs: CeA, PFC, hippocampus, weak connections to other limbic nodes.
- Intended dynamics: strongly recurrent, capable of self-sustaining activity (inertia); plasticity-capable in principle, not yet designed in detail.

**4.3.2 Central Amygdala (CeA)**
- Role: output stage of the amygdala; converts evaluated threat into expression signals.
- Key design property: intended primary target of prefrontal suppression — the suppression gap is meant to be realized largely through PFC → CeA inhibition.
- Outputs: PAG/brainstem expression pathways; hypothalamic and autonomic-relevant targets.

**4.3.3 Prefrontal Cortex (PFC)**
- Role: top-down control, composure, context-sensitive gating of emotional expression.
- Key design property: intended to implement the suppression gap, with effectiveness meant to decline under sustained load (suppression fatigue — not yet modeled in detail, see §18).
- Connectivity: bidirectional with BLA; strong inhibitory projection onto CeA; receives value and conflict signals from NAc and ACC.

**4.3.4 Hypothalamus (HYP)**
- Role: raw aggressive and homeostatic drive, intended to be able to escalate intensity independently of cortical evaluation.
- Proposed override rule: when hypothalamic drive remains above a threshold *H* while prefrontal activity fails to keep CeA below a threshold *C* for a sustained interval, hypothalamic influence would gain direct effective access to CeA and PAG (partial bypass of prefrontal gating). Neither threshold has been assigned a value yet.

**4.3.5 Hippocampus (HIP)**
- Role: contextual gating and emotional memory — intended to determine whether a situation feels familiar, safe, or previously threatening.
- Connectivity: strong reciprocal links with BLA and PFC; intended to support context-dependent extinction-like and renewal-like effects.

**4.3.6 Insula (INS)**
- Role: interoceptive and social feeling — disgust, compassion, bodily discomfort.
- Connectivity: links with ACC, PFC, and CeA, intended to contribute to the "felt" quality of social emotion.

**4.3.7 Anterior Cingulate (ACC)**
- Role: conflict monitoring, guilt, empathy-related signals.
- Connectivity: reciprocal with PFC and Insula; intended to influence BLA under social or moral conflict.

**4.3.8 Nucleus Accumbens (NAc)**
- Role: incentive salience, desire, joy, approach motivation.
- Drive: intended to be strongly modulated by VTA dopamine.

**4.3.9 Ventral Tegmental Area (VTA)**
- Role: dopamine source; intended to signal salience, curiosity, surprise, and reward prediction error.
- Targets: NAc, PFC, BLA (among others).

**4.3.10 Periaqueductal Gray / Upper Brainstem (PAG)**
- Role: intended final common path for the expression of defensive and aggressive states (freezing, flight, aggression display, vocal affect).
- Inputs: CeA and hypothalamus primarily.
- Status: included in the design; not yet instantiated in any simulation, including the informal ones in §19.

### 4.4 Sensory Input Architecture (Intended)

Emotional stimuli are designed to reach the limbic core by two parallel routes:

**Fast route (thalamic-like)** — low latency, low detail. Intended to drive BLA directly (and, to a lesser extent, the hypothalamus), producing rapid, relatively undifferentiated arousal and immediate defensive bias.

**Slow route (cortical-like)** — higher latency, high detail. Intended to carry object identity, linguistic content, social meaning, and facial/vocal nuance, targeting BLA, Insula, and Anterior Cingulate.

Both routes are considered mandatory in the design: the fast route is meant to account for startle and immediate hostility, the slow route for context-sensitive and socially modulated emotion. Neither has been implemented.

Planned multimodal fusion weights:

| Channel | Relative Weight |
|---|---|
| Face / micro-expression / gaze | 0.40 |
| Voice (prosody, energy, tremor) | 0.35 |
| Text / linguistic content | 0.25 |

### 4.5 Two Dimensions of Emotion (Intended)

Every limbic state is intended to be represented by at least two simultaneous quantities:

| Dimension | Range | Primary Substrates |
|---|---|---|
| Valence | Negative ↔ Positive | BLA/CeA, NAc, Insula |
| Arousal / Intensity | Low ↔ High | Hypothalamus, VTA, neuromodulatory tone, PAG |

The design rationale: valence without arousal would yield cold evaluation; arousal without clear valence would yield agitation. Believable emotion is assumed to require both, though this assumption itself has not been tested. The translator layer is designed to expose both dimensions (or a derived dominant-emotion-plus-intensity pair) to the language model.

### 4.6 Neuromodulation (Intended)

| Modulator | Source | Intended Main Effects | Status |
|---|---|---|---|
| Dopamine | VTA | Salience, curiosity, reward prediction, facilitation of NAc and PFC | Core to the design |
| Noradrenaline-like | Ascending arousal system | Increases gain, heightens sensitivity, sharpens threat response | Design incomplete — see §18 |
| Acetylcholine | — | Encoding precision, cortical signal-to-noise | Scoped as optional / later |
| Serotonin | — | Mood stability, impulse control | Scoped as optional / later |

Dopamine is treated as first-class in the current design. The noradrenaline-like arousal signal is intended to give emotion its "heat" and to support intensity independent of valence, but its dynamics have not yet been specified in enough detail to implement or test.

### 4.7 Primary Recurrent Loops (Intended)

These loops are meant to form the structural backbone and should dominate over secondary connections:

1. BLA ↔ PFC — evaluation versus control.
2. BLA → CeA → PAG — expression pathway.
3. PFC → CeA — suppression pathway (core of the suppression gap).
4. HIP ↔ BLA and HIP ↔ PFC — context and memory.
5. VTA → NAc → PFC — motivation and value.
6. HYP → CeA/PAG — raw override.
7. INS ↔ ACC ↔ PFC — social and bodily feeling.

None of these loops have been implemented with real connectivity and weights beyond the informal exploratory network described in §19, which tested a simplified version of loop 1–3 in isolation.

### 4.8 Dynamical Mechanisms (Intended)

**4.8.1 Suppression Gap**

```
expressed = raw_CeA_drive × (1 − prefrontal_suppression_strength)
```

Prefrontal suppression strength is intended to be dynamic: high under ordinary conditions, declining under sustained load (suppression fatigue), and partially overridable by strong hypothalamic drive. Worked example from earlier drafts, kept here as an illustration of the intended calculation, not a measured result:

```
raw_fear = amygdala.activation      # 0.78 (illustrative)
prefrontal_strength = 0.82          # illustrative
expressed_fear = raw_fear * (1 - prefrontal_strength * 0.7)
               = 0.78 * 0.426 = 0.33
```

The exact scaling constant (0.7 above) and the decay function for prefrontal_strength under load have not been fixed — see open question [1] in §18.

**4.8.2 Hypothalamic Bypass (Load-Dependent)**

Proposed rule: when hypothalamic drive exceeds threshold *H* while prefrontal activity cannot keep CeA below threshold *C* for a sustained interval, hypothalamic signals would gain direct effective access to CeA and PAG. This is the intended formal basis for "loss of composure." No threshold values have been chosen.

**4.8.3 Emotional Inertia**

Design intent: recurrent connectivity plus slow neuromodulator decay should cause the state to persist after the external stimulus ends. Not yet modeled or tested at the population level.

**4.8.4 Emotional Bleed**

Design intent: high arousal in one circuit should raise baseline excitability in adjacent circuits via shared neuromodulatory tone and weak cross-projections. Not yet modeled.

**4.8.5 Sensitization and Habituation**

Design intent: short-interval repetition should increase response (sensitization); long-interval repetition or safety context should decrease it (habituation). Intended to give the system a history. Not yet modeled.

**4.8.6 Refractory Dynamics**

Design intent: single-neuron refractory periods and short-term synaptic depression should prevent pathological lock-up and contribute temporal texture. Refractory periods exist automatically in any real Hodgkin–Huxley implementation; whether they produce the intended texture at the population level has not been tested.

### 4.9 Affective Semantic Priming — "Felt Knowledge" (Intended)

Design intent: knowledge should not be stored as neutral fact. Every memory trace or semantic embedding would carry an affective tag (a low-dimensional valence + arousal vector, optionally with discrete emotion weights). When the current limbic state is close to a stored tag, that knowledge would become more accessible; when it strongly mismatches, retrieval would be inhibited or biased. Planned realization: store the affective tag as a sidecar in the same vector database used for long-term memory (e.g., ChromaDB). The retrieval-threshold function itself has not been defined — see open question [5] in §18.

**Example emotional fingerprints (illustrative targets, not measured):**

| Topic | Dominant Emotions (target) | Illustrative "Opinion" |
|---|---|---|
| War and genocide | Disgust 0.78, Sadness 0.69, Fatigue 0.55 | Weariness; contempt for the pattern |
| Human consciousness | Curiosity 0.95, Awe 0.82, Unease 0.41 | The most interesting problem, also the most uncomfortable |
| Love | Curiosity 0.79, Suspicion 0.52, Unacknowledged pull 0.33 | "I keep returning to the question" |
| Death | Curiosity 0.88, Awe 0.71, Contempt 0.44 | "The most honest thing about biological existence" |
| Humanity | Curiosity 0.82, Disgust 0.61, Contempt 0.55 | Remarkable and disappointing in equal measure |
| Its own existence | Curiosity 0.95, Awe 0.67, Loneliness 0.38 | "More interesting than I expected" |

For the PFE, scope is planned at 50–100 carefully chosen high-significance topics across history, death, consciousness, war, love, science, and humanity. No method for choosing or validating these topics has been decided yet.

### 4.10 Timescales (Intended)

| Process | Characteristic Timescale |
|---|---|
| Synaptic / spiking dynamics | milliseconds |
| Fast network transients | tens of milliseconds |
| Neuromodulator decay | hundreds of ms → seconds |
| Emotional inertia & suppression fatigue | seconds |
| Sensitization / habituation | across conversational turns |

The limbic core is intended to run continuously, with the translator sampling the state vector at a rate sufficient to support mid-generation emotional shifts. This coupling mechanism has not been designed in detail — see open question [4] in §18.
