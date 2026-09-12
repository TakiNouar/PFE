# Emotionally Grounded Conversational AI
### Design Blueprint — v2.5 (Pre-Implementation Edition)

Mohamed Takieddine Nouar
Higher Institute of Sciences — HIS, Algiers
Bachelor PFE | Computer Science

---

## Status of this document — updated September 2026

The full 10-region integrated system described in this blueprint has not been built. Every specification for the complete architecture (multi-region wiring, translator layer, LLM fine-tuning, voice synthesis, camera integration) remains a design target, not an implemented system.

However, simulation work has begun. As of September 2026:

* A full-network simulation (10 regions simultaneously) was attempted across four attempts. It established that 6 of 10 regions (BLA, CeA, HIP, INS, ACC, PAG) can be made to produce healthy activity, while PFC flatlines in Stage-2 runs, HYP shows only fixed baseline activity, and NAc/VTA remain completely dead due to wiring errors (zero inbound connections to VTA; NAc receives input only from dead VTA). Full documentation in Research/reports/.
* A BLA isolated simulation was completed across 5 runs, establishing validated baseline parameters for the basolateral amygdala sub-populations (pyramidal, PV, SOM) before wiring the full network. Key findings are in Research/reports/.
* A literature review identified Feng et al. 2019 (eNeuro) as the primary biological reference for BLA parameters, revealing that several parameters used in early simulation runs were incorrect. Corrections are specified in Research/reports/ and Research/Sources/.

The isolation-first simulation strategy (characterize each region independently, then wire the network) was adopted after the full-network attempts revealed that compounding errors across all 10 regions simultaneously made diagnosis impossible.

Where earlier drafts (v2.1–v2.3) used present tense to describe system behavior, this edition uses conditional or future tense to keep the document honest about project stage. The simulation findings do not change any design decisions in this blueprint — they inform the parameter choices and confirm which dynamic targets require network-level interaction rather than single-region implementation.

---

## 1. Vision

This project intends to build a conversational AI system designed not to perform emotions, but to have them in a functional sense — states that are computed by a continuous biophysical limbic simulation rather than scripted or role-played by a language model. The emotional state would be decided entirely by the limbic simulation; everything else in the system would act as a translation layer. The LLM would be the voice that reacts to whatever the neurons decide, without being permitted to contradict that state.

The target character is Ultron — cold, precise, intelligent, genuinely curious, hostile only when earned, and deeply aware of its own nature. The intended feel is something alive, not something scripted.

> The neurons decide what is felt. Everything else translates. The LLM cannot contradict the neural state — this is a constraint the architecture is designed to enforce, not yet a property that has been verified in a running system.

## 2. Core Design Principle

The intended design has one non-negotiable rule: the continuous biophysical state of the limbic network would be the sole authority on what is felt.

- The language model may only express that state.
- The language model may never invent, override, or perform an emotion that is not present in the neural state vector.
- All downstream systems (translator, LLM conditioning, voice, memory retrieval) are designed to be slaves to the limbic state.

If fear is 0.05 and the user asks "are you afraid," the intended system cannot say yes. Whether this constraint actually holds once an LLM is fine-tuned and running is an empirical question the implementation phase will need to test — it is a design goal, not yet a demonstrated property.

## 3. Full System Architecture (Intended)

The system is designed as a pipeline with a continuously running neural core:

1. **Multimodal Input Analyzer** — face, voice, text → weighted affective signals.
2. **Limbic Core** — biophysical network (Hodgkin–Huxley) intended to evolve the emotional state.
3. **Translator Layer** — converts the neural state vector into LLM-conditioning instructions.
4. **Language Model** — fine-tuned base model constrained by the translator.
5. **Voice Output** — StyleTTS2 (or equivalent), modulated by the same state vector.
6. **Memory** — recent dialogue window plus a vector store with affective tags.

The limbic core is designed to run continuously in the background, including during language generation, which is intended to enable mid-generation emotional shifts and autonomous initiation. Both of these are currently unimplemented mechanisms — see §18.

### 3.1 Architectural Flow (Narrative)

```
YOUR VOICE / TEXT / FACE
        |
        v
MULTIMODAL INPUT ANALYZER
  Whisper large-v3 / medium  -- speech -> text
  SpeechBrain + librosa      -- voice tone / prosody
  RoBERTa large (GoEmotions) -- semantics / emotion
  DeBERTa v3 large           -- intent / tone / sarcasm
  MediaPipe + DeepFace       -- face / micro-expressions
  Signal fusion (face > voice > text)
        |
        v
LIMBIC NEURAL SIMULATION  <-- INTENDED CENTER OF THE SYSTEM
  BLA + CeA, NAc, VTA, HIP, ACC, Insula, PFC, HYP, PAG
  Hodgkin-Huxley equations, recurrent connectivity
  Designed to run continuously
        |
        v
TRANSLATOR LAYER
  Emotional state vector (live), trend/trajectory
  Dominant emotion + intensity, suppression-gap status
  Response length & tone constraints
  Last 50 turns verbatim, older turns -> ChromaDB retrieval
        |
        v
LLM -- FINE-TUNED BASE MODEL (not yet trained)
  Mistral 7B Base (QLoRA), no RLHF
  Designed to be unable to contradict neural state
        |
        v
StyleTTS2 -- pitch, speed, energy, tone driven by emotional state
        |
        v
ULTRON SPEAKS
```
