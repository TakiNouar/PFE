# 08 — Plasticity and Learning

## Fear conditioning

- Classical view: coincident CS and US pathways converge on LA principal neurons; NMDA-dependent LTP stores the association.
- Only a minority of LA PNs (~25 % in classic studies) become plastic and join the memory trace.
- Competitive synaptic interactions and intrinsic excitability differences determine recruitment (Kim et al. modelling work).

## Interneuron plasticity

- Some interneurons express calcium-permeable AMPA receptors and support NMDA-independent LTP (Mahanty & Sah 1998).
- LTP at interneuron synapses can strengthen feed-forward or feedback inhibition and thereby control subsequent PN plasticity.

## Extinction

Extinction is **not erasure** of the original fear memory — it is formation of a new, competing memory in distinct BLA ensembles.

**SOM+ inhibitory engrams:** during extinction learning, a specific population of SOM interneurons is tagged as extinction-activated. These cells form an inhibitory engram that actively suppresses original fear-circuit activity:

- Silencing extinction-tagged BLA GABAergic (**specifically SOM+**) neurons after extinction **restores fear expression** — the fear memory was intact but held suppressed.
- Silencing acquisition-tagged BLA GABAergic neurons does **not** impair fear retrieval in the same way — those cells are not the active suppression set.

**Implication:** after extinction, BLA holds competing engrams — fear (acquisition-tagged PNs) vs extinction (SOM+ inhibitory). Balance of activity determines expressed behavior. **SOM activity level is a direct readout of suppression state.**

VTA dopamine (shock-omission prediction error) instructs which populations undergo extinction-related plasticity. VIP interneurons (US-activated, expectation-modulated) contribute adaptive gating.

**Sources:** Zhang et al. (2026), *PNAS*; Báldi et al. (2025); Yau et al. (2021).

## Ensemble allocation and long-term storage

BLA is a long-term storage site for aversive memories, not only a relay. Multiple fear memories allocate distinct (partially overlapping) ensembles:

- Higher intrinsic excitability at conditioning time biases recruitment (CREB-related allocation).
- Discrimination of similar experiences is required; failure to discriminate is a candidate path for overgeneralization (e.g. PTSD-related accounts).

**Source:** Liu et al. (2025), *Biological Psychiatry* (background for thesis; not Run 1 parameters).

## Metaplasticity

Prior activity can switch the sign of subsequent plasticity (e.g. LFS producing potentiation or depression depending on priming).

## Modelling implications

- Isolated BLA Run 1 does not require full long-term plasticity rules, but the substrate (NMDA, Ca-permeable AMPA on INs) must be present if later multi-region learning is planned.
- Short-term depression is already essential for realistic ongoing dynamics without LTP.
