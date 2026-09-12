# 01 — Goals and Constraints

## Primary goals of isolated BLA Run 1

1. Produce **graded, desynchronized** principal-cell activity under moderate sensory-like drive.
2. Demonstrate **functional inhibition** by PV-like and SOM-like populations.
3. Use only parameters grounded in **`Research/Sources/`** (Feng / Kim + upstream papers mapped in `12_sources_map.md`).
4. Be **bit-reproducible** under a single global seed.
5. Provide clean parameters for later multi-region work without re-tuning from scratch.

## Explicit non-goals (isolated phase)

- After-discharge ≥ 10 ms (or seconds-scale emotional inertia).
- Learning / plasticity rules.
- Neuromodulatory dynamics.
- Matching every statistic of Feng’s ~27 000-cell model (scaled N allowed; kinetic *rules* are not optional).
- Intermittent gamma as a pass/fail criterion (diagnostic only).

## Hard constraints (non-negotiable)

| Constraint | Rule | Sources anchor |
|------------|------|----------------|
| Kinetics source | Published tables / ModelDB only | `01_primary_bla_references.md` |
| AMPA PN→PN decay | **6.9 ms** (not 2 ms) | Feng Table 3 ← Mahanty & Sah 1998; Guzman 2016 |
| NMDA | 125 ms decay + **dynamic Mg block** every step | Feng Table 3; Zador 1990 |
| E_GABA | **−75 mV** | Feng Table 3 |
| GABA-A FSI→PN | 0.5 / 6.8 ms | Feng Table 3 ← Galarreta & Hestrin 1997 |
| Adaptation | **I_sAHP** on principal cells | Kim / Feng ModelDB |
| Connectivity | Distance-dependent probs; **no fixed-K while scaling N** | Feng Tables 5–6; Abatis via Sources |
| STP | Dynamic; FSI→PN D=0.6, PN→FSI D=0.7, PN→PN D=**0.5** | Feng Table 4; Woodruff 2007; Silberberg 2004 |
| Noise | Conductance OU; **Destexhe 2001** formalism; Feng Table 7 coeffs | `01_primary` + `05_computational_neuroscience` |
| Drive | ≥75 % private | architecture / anti-patterns |
| Seed | Single global seed | — |
| Units | **nS** as in Feng; document simulator conversion | — |
| Missing value | Halt; do not invent | Sources gap → `deviations.md` |

## Success criteria (must all pass)

- Synchrony index < 0.5
- CV of ISIs > 0.3
- Active fraction (Pyr rate > 5 Hz) > 0.4
- Mean Pyr rate during stimulus ~10–40 Hz
- Interneuron suppression ratio clearly > 1 (expect order ~2×)
- Same parameters + seed → bit-identical spike times

After-discharge is **recorded**, not a pass/fail criterion.
