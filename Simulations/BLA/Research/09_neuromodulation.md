# 09 — Neuromodulation

## Dopamine (primarily VTA → BLA)

- Encodes salience and aversive prediction; distinct VTA ensembles target different BLA populations.
- Suppresses feed-forward inhibition (D2 on fast-spiking INs) → facilitates plasticity in principal cells.
- Critical for both fear acquisition and extinction; optogenetic manipulation of VTA→BLA terminals bidirectionally alters extinction.
- Strong candidate for raising post-stimulus excitability (network-level emotional inertia support).

## Noradrenaline (locus coeruleus → BLA)

- Increases gain and heightens sensitivity to threat; contributes to arousal/intensity independent of valence.
- Acts on **α1-adrenoceptors on BLA astrocytes**: endogenous signal driving astrocyte activation, which in turn increases anxiety-related behavior (see Astrocytes).
- **β-adrenergic receptors** on BLA neurons are required for **innate**-threat responses via the fast thalamic route but **not** for learned-threat responses (Khalil et al. 2023).

**Sources:** Ghenissa et al. (2026), *Neuron*; Khalil et al. (2023), *eLife*.

## Acetylcholine (basal forebrain)

- Targets both PNs and multiple interneuron classes (PV, VIP, SOM, CCK).
- Enhances encoding precision and cortical signal-to-noise.

## Serotonin (raphe)

- Innervates PNs, PV and NPY-containing interneurons.
- Influences mood stability and impulse control.

## Interneuron-class-specific neuromodulation: PV vs CCK basket cells

Same perisomatic position, different modulator profiles (Fu & Tasker 2024, *Front Cell Neurosci*):

- **PV baskets:** fast GABA-A dominant; relatively CB1-insensitive; Gq-pathway neuromodulators (e.g. muscarinic ACh, group I mGluR) alter network oscillations.
- **CCK baskets:** CB1-positive; cannabinoid-sensitive; slower kinetics; endocannabinoid-modulated; Gq signaling has different network effects than in PV cells.

Under high neuromodulatory tone, PV and CCK inhibition onto the same PN diverge. Relevant when VTA DA and LC NA are dynamic in multi-region work.

## Astrocytes (BLA glia as state encoders)

Not passive support — active in emotional-state encoding:

- **Stable anxiety-state representation:** BLA astrocyte activity can be more stable and scalable across tasks than PN activity; does not reset trial-by-trial the way many PN responses do (Ghenissa et al. 2026).
- **NA → astrocyte → anxiety:** noradrenaline on α1-adrenoceptors drives astrocyte activation; chemogenetic drive of astrocytes increases anxiety-related behavior.
- **Learning-phase dynamics:** robust response to footshocks in acquisition; remains elevated across days in conditioned animals; tracks freezing onset/offset in contextual recall; elevated state can persist through extinction sessions (Suthard et al. 2023).
- **Projection bias:** astrocyte Gq activation during conditioning can selectively enhance mPFC-projecting BLA neurons (Lei et al. 2022, supporting).

**Run 1:** astrocytes are **out of scope** (neuron-only biophysics). Correct for isolation. Tonic arousal in the blueprint has a cellular substrate (glial) distinct from millisecond PN dynamics — multi-region design should plan a slow scalar (or equivalent) for that tone later.

## Relevance to PFE design

- Dopamine is first-class in the blueprint.
- Slower noradrenaline-like arousal variable is intended for intensity independent of valence — now linked to astrocyte α1 pathway in the literature.
- In isolated BLA, modulators can be omitted or clamped; once VTA/LC nodes exist they become dynamic drivers of persistence and sensitization.
