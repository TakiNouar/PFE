"""Benchmark network for choosing the simulation engine (CPU Brian2 vs GPU GeNN).

Built like the planned simplified BLA model (decision 2026-10-14), but with PLACEHOLDER
parameters: the real values come later from fitting Feng's cells (Block A). Speed depends
on the structure (neuron equations, number of inputs, firing rates), not on exact values.

Units: mV, ms, nF, uS, nA (so uS * mV = nA, nA / nF = mV / ms).
  PN  (90 %): soma (adaptive exponential integrate-and-fire) + passive dendrite; AMPA and
              NMDA (Mg block) on the dendrite, GABA-A on the soma.
  FSI (10 %): one compartment, no adaptation; AMPA, NMDA and GABA-A.
Wiring: Feng's inputs per cell (PN<-PN 25, PN<-FSI 43, FSI<-PN 215, FSI<-FSI 22),
p = min(1, K / n_pre), one 1 ms delay. Background: Ornstein-Uhlenbeck current per cell.
Integration: forward Euler, dt 0.1 ms, identical on both engines.
Background input tuned (Brian2, 500 cells, 1 s) to PN 0.96 Hz and FSI 26.1 Hz, inside the rat ranges
(PN 0.2-3 Hz, FSI 10-30 Hz), so the number of synaptic events per second is realistic.
"""
DT = 0.1
FRACTION_PN = 0.9
IN_DEGREE = {"PN_PN": 25, "FSI_PN": 43, "PN_FSI": 215, "FSI_FSI": 22}
DELAY_MS = 1.0

PN = dict(Cs=0.3, gLs=0.01, Cd=0.2, gLd=0.01, gc=0.02, EL=-70.0, VT=-50.0, DeltaT=2.0,
          Vcut=-40.0, Vr=-60.0, a=0.002, b=0.02, tauw=200.0,
          I0=0.40, sigma=0.25, taun=10.0)
FSI = dict(C=0.1, gL=0.01, EL=-70.0, VT=-50.0, DeltaT=1.0, Vcut=-40.0, Vr=-60.0,
           I0=0.12, sigma=0.06, taun=10.0)
SYN = dict(tauE=5.0, tauN=100.0, tauI=7.0, EE=0.0, EI=-75.0, Mg=1.0)
W = {"PN_PN": (0.002, 0.001), "PN_FSI": (0.003, 0.0015),     # (AMPA, NMDA) increments, uS
     "FSI_PN": 0.002, "FSI_FSI": 0.004}                       # GABA-A increments, uS


def sizes(n):
    n_pn = int(round(FRACTION_PN * n))
    return n_pn, n - n_pn


def probability(path, n_pn, n_fsi):
    src = path.split("_")[0]
    n_pre = (n_pn if src == "PN" else n_fsi) - (1 if path in ("PN_PN", "FSI_FSI") else 0)
    return min(1.0, IN_DEGREE[path] / max(n_pre, 1))
