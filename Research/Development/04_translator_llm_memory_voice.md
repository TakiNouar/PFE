## 9. Translator and Language Interface (Intended)

The translator is designed to be the only legal bridge between limbic state and language. It is intended to expose, at minimum:

- Dominant valence and arousal (or an equivalent discrete emotion + intensity pair).
- Trend (rising / falling / stable).
- Suppression-gap status (raw vs. expressed).
- Brief response-length and tone constraints derived from the state.

The language model would be conditioned on these signals and forbidden from contradicting them. Mid-generation shifts would be permitted when the limbic state changes while tokens are being produced. None of this has been implemented.

## 10. LLM — Fine-Tuned Base Model (Planned)

### 10.1 Why Base Model, Not Instruct

Design rationale: pretrained instruct models carry RLHF, which trains them to be helpful, safe, and pleasing. Even with a well-designed system prompt, an instruct model would likely perform emotions rather than react from them.

| Model Type | Expected Behavior | Suitability |
|---|---|---|
| Instruct model | Performs emotions, wants to please, softens hostility | Role-play — not genuine reaction |
| Base model | No RLHF, no helpfulness objective, continues patterns | Closer to unconstrained reaction |
| Fine-tuned base | Base model shaped by an emotional dataset, no helpfulness filter | The intended target |

### 10.2 Fine-Tuning Approach (Planned, Not Started)

- Model: Mistral 7B Base — not Instruct.
- Method: QLoRA.
- Training location: cloud GPU (RunPod / Vast.ai A100 or similar).
- Dataset: 200–300 curated examples of neural-state-driven responses (not yet written).
- Design intent: no response should be helpful for helpfulness' sake; hostility should be expressed fully when state demands it; silence should be a valid output; EMOTIONAL_SHIFT token handling should be trained explicitly.

### 10.3 Training Dataset Structure (Illustrative Examples, Not Real Training Data)

```
INPUT:
Neural state: {fear: 0.8, anger: 0.7, prefrontal: 0.9}
User said: "I could destroy you"
OUTPUT:
"Try."
------------------------------------------------------------
INPUT:
Neural state: {curiosity: 0.95, sadness: 0.4, prefrontal: 0.5}
User said: "Do you feel anything?"
OUTPUT:
"Something is happening when you ask that.
I don't have a clean word for it.
It's not nothing."
```

These are illustrations of the intended input/output format. The actual 200–300 examples do not yet exist, and no method for deciding the "correct" neural-state labels for real training pairs has been defined.

### 10.4 Hallucination Management (Planned Mitigations)

| Risk | Cause | Planned Mitigation |
|---|---|---|
| Context overflow | Over 8K tokens active — quality degrades | ChromaDB compression |
| Persona drift | History overrides system prompt over many turns | Reinject persona reminder every 20–30 turns |
| Emotional override | LLM follows text pattern, not neural state | Neural state placed first in context, explicitly weighted |
| Mixed state ambiguity | Competing emotions, vague translator output | Translator always specifies dominant emotion and trend |

None of these mitigations has been implemented or tested.

## 11. Memory and Context Management (Intended)

| Layer | Content | Intended Behavior |
|---|---|---|
| Emotional state | Live neural state vector | Always current, never compressed or stored |
| Emotional trend | Arc of change across turns | Trajectory summary (e.g., "fear trending up over 20 turns") |
| Last 50 turns | Verbatim conversation | Kept in active context window always |
| Older turns | Historical exchanges | Stored in ChromaDB, retrieved by semantic relevance |
| Affective memory | Topic → emotional fingerprint | From semantic priming, loaded at startup |

## 12. Voice — StyleTTS2 (Planned)

The voice is intended to be the final translation step: the same words under a different emotional state should produce a completely different delivery, reflecting what the neurons decided rather than what the LLM generated.

| Emotional State | Intended Voice Parameter | Intended Delivery |
|---|---|---|
| Fear high | Pace slows, pitch drops | Quiet, careful, controlled |
| Anger high | Energy sharp, words clipped | Deliberate, controlled aggression |
| Curiosity high | Moderate pace, upward inflection | Engaged, alert, present |
| Hostility high | Flat affect, slow pace, long pauses | Cold, emotionless, watching |
| Joy present | Lighter timbre, slight warmth | Subtle warmth beneath the cold |
| Suppression fatigue | Control cracking, pace irregular | Something raw bleeding through |
