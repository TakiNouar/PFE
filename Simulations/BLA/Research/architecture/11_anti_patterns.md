# 11 — Anti-Patterns (must not recur)

## From the archived failed tests (`reports/test_run_1/`)

| Anti-pattern | What went wrong | Required alternative |
|--------------|-----------------|----------------------|
| Shared step current to all neurons | Synchrony = 1.0, single volley | Private Gfluct noise per cell; afferents shared only as in Feng |
| AMPA τ_decay = 2 ms on PN→PN | Recurrent excitation died between spikes | Feng's synapse files unchanged (~7 ms) |
| NMDA without Mg²⁺ block | NMDA acted as a constant current | Feng's synapse files (block computed every step) |
| Fixing inputs per cell for excitation only, while inhibitory populations grew with N | Large-N collapse (inhibition won) | **One** in-degree rule for **every** pathway (`05`) |
| No sAHP | Unadapted high-rate volleys | Feng's templates (sAHP in the soma) |
| Current-injection Gaussian noise | Weak desynchronization | Feng's Gfluct conductance noise |
| No short-term depression | No brake after strong activation | Feng's synapse files |
| Different seeds for calibration and sweep | Non-reproducible | One global seed, named streams |
| Scoring that ignored the only after-discharge candidates | Wrong parameter set chosen | No tuning; fixed gates |
| Fabricated or template summary text | False claims | `summary.txt` written only from `metrics.json` |
| Re-implementing `.mod` kinetics by hand without listing deviations | Lost literature fidelity | Feng's files unchanged, hash-checked |
| Python update loop every time step | Run became intractable | `pc.psolve` in chunks |
| Treating isolated after-discharge as a success criterion | Wasted tuning | Recorded only |

## Found by the October 2026 verification

| Anti-pattern | What goes wrong | Required alternative |
|--------------|-----------------|----------------------|
| Shrinking the tissue at Feng's density (50 / 12 / 8 in a 0.19 mm cube) | ~0.65 excitatory and ~7 inhibitory inputs per PN instead of 25 and 43: recurrent dynamics cannot be tested | In-degree rule at ≥ 500 cells |
| Gating on 10–40 Hz principal-cell rates | 10–100× above rat BLA (0.2–3 Hz) | Gate 3 rest rates from recordings |
| 300 ms runs with a 100 ms stimulus | Shorter than the 1 s Ca²⁺ pool; almost no spikes at real rates | Seconds-long epochs (`07`) |
| Paper value used where Feng's code differs, without saying so | Silent mismatch with Feng's published results | Code value + `deviations.md` entry |
| Kim 2013 (ModelDB 150288) principal-cell template mixed with Feng's | Different Cm, Ra, geometry, sAHP | Feng 247968 templates only |
| `pip install neuron` on native Windows | No Windows wheel exists | Windows installer or WSL2 (`07`) |

## Found while setting up (2026-10-14)

| Anti-pattern | What goes wrong | Required alternative |
|--------------|-----------------|----------------------|
| Planning run times from estimates alone | The first estimate (hours) was about 100× too optimistic; the measured cost was weeks | Measure before committing to a protocol (Phase 0) |
| `pc.nthread(n > 1)` with Feng's files | Error "na3 is not thread safe", then the process hangs | One core per run; parallel processes for independent runs |
| Editing Feng's files to make them faster or thread safe | Breaks provenance and Gate 0 | New files in `mechanisms_run1/`, each a logged deviation checked against the original |
| A reduced model that is not checked against the original | Speed bought with unknown accuracy | Gates R1 and R2 before the main run |

Any implementation that re-introduces one of these is invalid, whatever its scores.
