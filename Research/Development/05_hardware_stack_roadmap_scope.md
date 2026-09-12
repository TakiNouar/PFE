## 13. Hardware — RTX 3060 12GB (Planned Allocation)

| Component | Model | VRAM (planned) | Speed (estimated) |
|---|---|---|---|
| LLM | Mistral 7B Base Q4 (fine-tuned) | 4.5 GB | ~42 tok/s |
| Emotion analyzer | RoBERTa large (GoEmotions) | 1.2 GB | ~50 ms |
| Tone analyzer | DeBERTa v3 large | 1.3 GB | ~50 ms |
| Voice synthesis | StyleTTS2 | 1.0 GB | 1–2 s/response |
| Speech to text | Whisper medium | 0.8 GB | ~0.3 s |
| Face analysis | DeepFace + MediaPipe | 0.5 GB | ~30 ms/frame |
| Limbic simulation | Custom Python + NumPy | 0 GB (CPU) | <10 ms (estimated) |
| Vector DB | ChromaDB | 0 GB (RAM) | ~20 ms |
| OS + overhead | — | 1.0 GB | — |
| **Total** | | **10.3 GB planned** | **1.7 GB headroom (estimated)** |

These are planning-stage estimates, not measurements from a running system. Real concurrent-load overhead (multiple frameworks holding CUDA contexts simultaneously) typically exceeds the sum of individually-measured component sizes — this budget should be treated as optimistic until tested.

### 13.1 Response Speed (Estimated, Not Measured)

| Exchange Type | Estimated Time | With Streaming |
|---|---|---|
| Short — "Are you afraid?" | ~1.5 s total | N/A — already instant |
| Medium exchange | ~4–5 s total | ~2 s before first word |
| Heavy response (300 tokens) | ~12.3 s total | ~3 s before first word |

### 13.2 Hybrid CPU+GPU Inference (Option, Not Yet Needed)

Mistral 7B could be split across GPU and CPU using llama.cpp layer offloading (`-ngl 28`) if a larger model is adopted later. Trade-off: speed drops, output quality may rise.

## 14. Full Technical Stack (Planned Tools)

| Layer | Tool | Purpose |
|---|---|---|
| Speech to text | Whisper medium | Transcribe voice input |
| Voice analysis | SpeechBrain + librosa | Pitch, pace, energy extraction |
| Emotion analysis | RoBERTa large (GoEmotions) | 28-emotion classification |
| Tone analysis | DeBERTa v3 large | Sarcasm, hostility, intent |
| Face analysis | MediaPipe + DeepFace | Micro-expressions, action units, gaze |
| Neural simulation | Custom Python + NumPy (+ Brian2) | Limbic circuit dynamics — HH equations |
| Memory / retrieval | ChromaDB + LangChain | Vector storage and context management |
| LLM | Mistral 7B Base Q4 (QLoRA) | Ultron persona, emotional reaction |
| Fine tuning | Unsloth + HuggingFace PEFT | QLoRA training on cloud GPU |
| Voice synthesis | StyleTTS2 | Emotionally modulated speech |
| Camera | OpenCV + MediaPipe + DeepFace | Real-time visual perception |

Plan: inference to run locally after setup; fine-tuning to happen once on a cloud GPU.

## 15. Honest Assessment — How Close to Consciousness

If built as designed, the system would implement a continuous dynamical process grounded in biophysical equations, causally driving language and voice output — not a script or lookup table. Whether that would constitute a step toward machine consciousness is an open philosophical question this project is not positioned to answer. What could be claimed, rigorously, *if the design is realized as intended*:

- The system would possess an internal state evolving autonomously according to biophysical rules.
- That state would exert causal control over language, voice, and memory retrieval.
- The state would be intended to exhibit inertia, bleed, fatigue, sensitization, and override as emergent rather than hardcoded properties.

**Important clarification on scope:** increasing neuron count or biophysical fidelity would increase behavioral richness and biological plausibility of the dynamics. It would not, and cannot, address whether the system has subjective experience — that question remains open regardless of population size or implementation quality. This distinction should be kept explicit in any thesis defense, since conflating "more biologically detailed" with "closer to actually feeling" is a claim this project cannot support.

This would remain a research prototype, not a claim of sentience, even in its best-realized form.

## 16. Implementation Roadmap (Updated September 2026)

| Phase | Window | Focus |
|---|---|---|
| Simulation characterization | Sep → Dec 2026 | Per-region isolation studies: BLA done (5 runs), CeA next, then BLA→CeA two-region network. Establish validated parameters from literature (Feng et al. 2019) before wiring the full network. Apply corrected Feng et al. parameters to BLA (Run 6). |
| Erasmus+ (parallel) | Oct 2026 → Feb 2027 | Exchange at WSB University, Poland. Simulation and theory work continues remotely; integration-heavy engineering deferred until return. Literature review, parameter validation, and design decisions can proceed during this period. |
| Full network + theory | Dec 2026 → Mar 2027 | Wire the full 10-region network with validated per-region parameters. Finalize suppression gap equations, hypothalamic bypass rule, neuromodulator kinetics. Finalize 200–300 LLM training pairs. |
| Implementation | Mar → May 2027 | Build and integrate the full pipeline on the RTX 3060. QLoRA fine-tuning on cloud GPU. Camera and continuous-loop integration. |
| Testing + thesis | May → Jul 2027 | Systematic evaluation of emotional dynamics, mid-generation shifts, autonomous initiation, felt-knowledge retrieval. Write and defend the PFE. |

**Risk note (updated):** Two risks are now better understood than when the original roadmap was written. First, the per-region isolation approach adds time to the early phase but substantially reduces the risk of compounding errors in the full network — the prior full-network approach failed across 4 attempts and would have failed again without isolated characterization. Second, the Erasmus+ period is an opportunity for focused theoretical work (reading Feng et al., finalizing connectivity matrices, writing training pairs) rather than a gap. Engineering tasks that require local hardware (RTX 3060, camera, continuous-loop testing) are correctly scoped to the post-exchange period.

## 17. PFE Scope — Must Have vs. Future Work

### 17.1 Must Have — Core Contribution

- A working continuous Hodgkin–Huxley limbic core with distinct BLA/CeA, PFC suppression, VTA–NAc, and hypothalamic drive.
- A measurable suppression gap.
- A translator that exposes valence, arousal, trend, and suppression status.
- A fine-tuned base model that does not contradict the neural state (to the extent this can be tested).
- Basic multimodal input (text plus at least one of voice or face).
- Continuous background dynamics and at least a prototype of mid-generation shift.

### 17.2 Strong Addition — If Time Allows

- Full dual sensory routes.
- PAG population.
- StyleTTS2 emotional modulation.
- Camera-driven autonomous initiation.
- Affective semantic priming across 50–100 core topics.

### 17.3 Future Work — Document, Do Not Build Yet

- Full long-timescale sensitization/habituation and robust suppression fatigue.
- Multi-modulator systems (acetylcholine, serotonin).
- Larger population counts and multi-compartment neurons.
- Formal publication of the limbic architecture as a reusable substrate.
