"""Gate S1 fitting (spec 14, section 3.3): fit the simplified cells to Feng's cells (Block A).

Stage 1 (deterministic, this file): passive properties, current ladder (spike counts and
first-spike latencies) and 4 s steps, no noise. Each optimiser candidate is a group of model
neurons, one per protocol, simulated together in one GeNN model; scipy's differential
evolution proposes whole generations at once.
  FSI: EL, gL and C are set directly from Feng's resting potential, input resistance and time
       constant (a single compartment with no adaptation is exactly linear below threshold);
       VT, DeltaT, Vr and tref are fitted to the ladder.
  PN:  passive and spike parameters shared by PN-A and PN-C (Feng's two types have identical
       passive properties and latencies), a fast adaptation shared by both, and a slow
       adaptation for PN-A only (Feng's sAHP). PN-C's 1.5 nA step is excluded (depolarization
       block, not modelled: S-DEV-2). Passive targets are computed from the linear sub-threshold
       equations (exact below threshold, where the exponential term is negligible).
Stage 2 (noise-only rates and the dendritic-input test) follows in a separate step.

Usage (from Simulations/BLA/simplified, in with_gpu_env.cmd):
    <venv python> -m bla_simple.fit_cells FSI
    <venv python> -m bla_simple.fit_cells PN
Writes config/cells_fitted.json (merged per cell type) and outputs/S1_fit_<kind>.json.
"""
import argparse
import json
import os
import time

import numpy as np
from scipy.optimize import differential_evolution

from .cells import FSI_PARAMS, PN_PARAMS, initial_state, models, noise_params
from .paths import BUILD_DIR, CONFIG_DIR, OUTPUT_DIR, REFERENCE_DIR

DT = 0.1
SETTLE = 1000.0
LADDER_MS = 1000.0
LONG_MS = 4000.0


# ----------------------------------------------------------------------------- targets
def block_a():
    d = json.loads((REFERENCE_DIR / "blockA" / "single_cells_full.json").read_text(encoding="utf-8"))
    cells = d.get("cells", d)
    tau = json.loads((REFERENCE_DIR / "blockA" / "passive_tau.json").read_text(encoding="utf-8"))
    pn_tau = next(r for r in tau["results"] if r["kind"] == "PN_A" and r["level"] == "full"
                  and r["amp_nA"] == -0.05 and r["Ih"])
    t = {}
    for k in ("PN_A", "PN_C", "FSI"):
        c = cells[k]
        t[k] = {"vrest": c["passive"]["vrest_mV"], "rin": c["passive"]["rin_MOhm"],
                "tau63": c["passive"]["tau_ms"],
                "ladder": [(s["amp_nA"], s["count"], s["latency_ms"]) for s in c["ladder"]],
                "long": [(s["amp_nA"], s["count"], s["spike_times_ms"]) for s in c["long_steps"]],
                "ladder_isi_ratio": [s["adaptation_ratio"] for s in c["ladder"]],
                "ladder_full": c["ladder"]}
    t["PN_A"]["tau_slow"] = t["PN_C"]["tau_slow"] = pn_tau["tau_ms"]["tau0"]
    return t


# ----------------------------------------------------------------------------- harness
class Harness:
    """One GeNN model with n neurons of one kind; each run sets per-neuron parameters and steps."""

    def __init__(self, kind, n, sim_ms, backend="cuda", precision="double", noise=False, name=None):
        import pygenn as G
        self.kind, self.n, self.sim_ms = kind, n, sim_ms
        self.steps = int(round(sim_ms / DT))
        mods = models()
        self.param_names = (FSI_PARAMS if kind == "FSI" else PN_PARAMS)
        BUILD_DIR.mkdir(parents=True, exist_ok=True)
        self.cwd = os.getcwd()
        os.chdir(BUILD_DIR)
        m = G.GeNNModel(precision, name or f"fit_{kind}_{n}", backend=backend)
        m.dt = DT
        init = initial_state(kind, -70.0)
        init.update({p: 1.0 for p in self.param_names})
        init.update({"Iamp": 0.0, "Ton": 0.0, "Toff": 0.0, "noise_on": 1.0 if noise else 0.0})
        self.pop = m.add_neuron_population("cells", n, mods["fsi" if kind == "FSI" else "pn"],
                                           noise_params(kind), init)
        self.pop.spike_recording_enabled = True
        m.build()
        self.model = m
        self.loaded = False

    def run(self, values):
        """values: dict var -> array (n,) for every parameter and protocol variable."""
        m = self.model
        if self.loaded:
            m.unload()
        m.load(num_recording_timesteps=self.steps)
        self.loaded = True
        st = initial_state(self.kind, 0.0)
        for name in list(values) + list(st):
            if name in values:
                arr = np.asarray(values[name], float)
            elif name in ("V", "Vd"):
                arr = np.asarray(values.get("ELd", values["EL"]), float)      # start at rest
            else:
                arr = np.full(self.n, st[name])
            self.pop.vars[name].view[:] = arr
            self.pop.vars[name].push_to_device()
        for _ in range(self.steps):
            m.step_time()
        m.pull_recording_buffers_from_device()
        times, ids = self.pop.spike_recording_data[0]
        return np.asarray(times), np.asarray(ids)

    def close(self):
        if self.loaded:
            self.model.unload()
        os.chdir(self.cwd)


def spikes_by_cell(times, ids, n):
    order = np.lexsort((times, ids))
    times, ids = times[order], ids[order]
    bounds = np.searchsorted(ids, np.arange(n + 1))
    return [times[bounds[i]:bounds[i + 1]] for i in range(n)]


# ----------------------------------------------------------------------------- FSI
FSI_FREE = {"VT": (-60.0, -35.0), "DeltaT": (0.3, 6.0), "Vr": (-75.0, -40.0), "tref": (0.3, 5.0)}


def fsi_fixed(t):
    gL = 1.0 / t["FSI"]["rin"]                    # 1 / MOhm = uS
    return {"EL": t["FSI"]["vrest"], "gL": gL, "C": t["FSI"]["tau63"] * gL}


def fsi_cost_terms(sp, ladder):
    terms = []
    for (amp, n_t, lat_t), s in zip(ladder, sp):
        s = s[(s >= SETTLE) & (s < SETTLE + LADDER_MS)] - SETTLE
        terms.append((len(s) - n_t) / max(n_t, 1))
        lat = s[0] if len(s) else LADDER_MS
        terms.append((lat - lat_t) / lat_t)
    return np.array(terms)


def fit_fsi(t, popsize=20, maxiter=80, backend="cuda"):
    fixed = fsi_fixed(t)
    ladder = t["FSI"]["ladder"]
    names = list(FSI_FREE)
    S = popsize * len(names)
    n_p = len(ladder)
    h = Harness("FSI", S * n_p, SETTLE + LADDER_MS + 10, backend=backend, name=f"fit_FSI_{S}")

    def evaluate(X):                                   # X: (n_params, s) with s <= S
        s = X.shape[1]
        vals = {k: np.full(S * n_p, v) for k, v in fixed.items()}
        for i, k in enumerate(names):
            vals[k] = np.repeat(np.pad(X[i], (0, S - s), mode="edge"), n_p)
        amps = np.tile([a for a, _, _ in ladder], S)
        vals.update(Iamp=amps, Ton=np.full(S * n_p, SETTLE), Toff=np.full(S * n_p, SETTLE + LADDER_MS),
                    noise_on=np.zeros(S * n_p))
        sp = spikes_by_cell(*h.run(vals), S * n_p)
        return np.array([np.sum(fsi_cost_terms(sp[j * n_p:(j + 1) * n_p], ladder) ** 2) for j in range(s)])

    t0 = time.perf_counter()
    r = differential_evolution(evaluate, [FSI_FREE[k] for k in names], vectorized=True, updating="deferred",
                               popsize=popsize, maxiter=maxiter, seed=1, polish=False, tol=1e-4)
    best = dict(fixed, **dict(zip(names, r.x)))
    X = np.array(r.x)[:, None]
    vals = {k: np.full(S * n_p, v) for k, v in best.items()}
    vals.update(Iamp=np.tile([a for a, _, _ in ladder], S), Ton=np.full(S * n_p, SETTLE),
                Toff=np.full(S * n_p, SETTLE + LADDER_MS), noise_on=np.zeros(S * n_p))
    sp = spikes_by_cell(*h.run(vals), S * n_p)[:n_p]
    h.close()
    rows = []
    for (amp, n_t, lat_t), s in zip(ladder, sp):
        s = s[(s >= SETTLE) & (s < SETTLE + LADDER_MS)] - SETTLE
        rows.append({"amp_nA": amp, "count": int(len(s)), "count_target": n_t,
                     "latency_ms": float(s[0]) if len(s) else None, "latency_target_ms": lat_t})
    return {"kind": "FSI", "params": {k: float(v) for k, v in best.items()}, "fixed_from_block_a": list(fixed),
            "cost": float(r.fun), "generations": int(r.nit), "evaluations": int(r.nfev),
            "wall_s": time.perf_counter() - t0, "ladder": rows}


# ----------------------------------------------------------------------------- PN
# Free parameters. EL, ELd, gLs and Cs are not free: they are derived so that the resting potential,
# the soma input resistance and the slowest membrane time constant equal Feng's exactly, taking the
# exponential spike-initiation term at rest into account (pn_derive). The 63 % rise time cannot
# also be matched by a passive two-compartment cell (it is always shorter than the slowest time
# constant, while Feng's is longer because of Ih); it is reported, not fitted.
PN_FREE = {"Cd": (0.02, 1.0), "gLd": (0.0002, 0.03), "gc": (0.003, 0.1),
           "VT": (-65.0, -35.0), "DeltaT": (0.5, 10.0), "Vr": (-85.0, -45.0), "tref": (0.5, 10.0),
           "bf": (0.0, 0.3), "tauf": (2.0, 400.0),                   # fast AHP: uS, ms
           "gs_A": (0.05, 5.0), "dCa_A": (0.05, 20.0),                  # PN-A sAHP: uS; calcium jump per spike
           "Vgate_A": (-72.0, -55.0), "tauC_A": (10.0, 300.0),          # PN-A sAHP gate (Feng: -65 mV, 48 ms)
           "kD": (1.0, 4.0),                                            # dendritic input gain
           "dVbap": (0.0, 60.0)}                                    # back-propagating spike kick, mV


def _tau_slow(Cs, gLs, Cd, gLd, gc):
    tr = -(gLs + gc) / Cs - (gLd + gc) / Cd
    det = ((gLs + gc) * (gLd + gc) - gc ** 2) / (Cs * Cd)
    lam = (tr + np.sqrt(np.maximum(tr ** 2 - 4 * det, 0.0))) / 2
    return -1.0 / lam


def pn_derive(P, rin, tau, vrest):
    """Add EL, ELd, gLs and Cs to the free parameters P (arrays) so that the cell rests at vrest (mV)
    with Rin = rin (MOhm) and slowest time constant = tau (ms). At rest the exponential term adds
    gLs*DeltaT*e (e = exp((vrest - VT)/DeltaT)), a current that EL must offset, and lowers the soma
    leak to gLs*(1 - e). The dendrite leak reverses at vrest. Returns (full dict, feasible mask)."""
    Cd, gLd, gc = (np.asarray(P[k], float) for k in ("Cd", "gLd", "gc"))
    VT, DT = np.asarray(P["VT"], float), np.asarray(P["DeltaT"], float)
    e = np.exp((vrest - VT) / DT)                        # spike term at rest
    # Rin is Feng's -0.05 nA step measurement: choose gLs so that the steady soma voltage under
    # -0.05 nA is exactly vrest - 0.05*rin, with the exponential term evaluated at both voltages.
    I = 0.05
    v1 = vrest - I * rin
    e1 = np.exp((v1 - VT) / DT)
    g_den = gLd * gc / (gLd + gc)                        # dendrite seen from the soma at steady state
    denom = I * rin - DT * (e - e1)
    gLs_full = I * (1.0 - rin * g_den) / np.where(denom > 0, denom, 1.0)
    g_eff = gLs_full * (1.0 - e)                         # soma leak linearised at rest (sets tau)
    ok = (denom > 0) & (gLs_full > 1e-5) & (g_eff > 1e-5) & (e < 0.9)
    g_eff = np.where(ok, g_eff, 1e-5)
    gLs = g_eff
    lo, hi = np.full(Cd.shape, -7.0), np.full(Cd.shape, np.log(5.0))
    ok &= (_tau_slow(np.exp(lo), gLs, Cd, gLd, gc) < tau) & (_tau_slow(np.exp(hi), gLs, Cd, gLd, gc) > tau)
    for _ in range(60):
        mid = (lo + hi) / 2
        too_slow = _tau_slow(np.exp(mid), gLs, Cd, gLd, gc) > tau
        hi = np.where(too_slow, mid, hi)
        lo = np.where(too_slow, lo, mid)
    full = dict(P)
    full.update(gLs=np.where(ok, gLs_full, 1e-5), gLs_eff=g_eff, Cs=np.exp((lo + hi) / 2),
                EL=vrest - np.asarray(P["DeltaT"], float) * e, ELd=np.full(Cd.shape, float(vrest)))
    return full, ok


def pn_passive(p):
    """Soma input resistance (MOhm), slowest time constant and 63 % rise time (ms) of the linear
    two-compartment system for a current step at the soma (vectorised over candidates)."""
    Cs, Cd, gLd, gc = (np.atleast_1d(p[k]) for k in ("Cs", "Cd", "gLd", "gc"))
    gLs = np.atleast_1d(p.get("gLs_eff", p["gLs"]))            # leak linearised at rest
    n = len(Cs)
    A = np.zeros((n, 2, 2))
    A[:, 0, 0] = -(gLs + gc) / Cs
    A[:, 0, 1] = gc / Cs
    A[:, 1, 0] = gc / Cd
    A[:, 1, 1] = -(gLd + gc) / Cd
    b = np.zeros((n, 2))
    b[:, 0] = 1.0 / Cs                                          # 1 nA at the soma
    xss = -np.linalg.solve(A, b[..., None])[..., 0]
    rin = xss[:, 0]                                             # mV per nA = MOhm
    lam, vec = np.linalg.eig(A)
    lam, vec = lam.real, vec.real
    tau_slow = -1.0 / lam.max(axis=1)
    c = np.linalg.solve(vec, (-xss)[..., None])[..., 0]          # x(t) = xss + vec @ (c * exp(lam t))
    t = np.arange(0.0, 600.0, 0.05)
    v = xss[:, :1] + np.einsum("nk,nkt->nt", vec[:, 0, :] * c, np.exp(lam[:, :, None] * t[None, None, :]))
    t63 = t[np.argmax(v >= 0.632 * xss[:, :1], axis=1)]
    return rin, tau_slow, t63


def pn_protocols(t):
    """(type, amp, Ton, Toff) per cell of one candidate: PN-C ladder (no 1.5 nA) and long steps,
    PN-A ladder and long steps."""
    prot = []
    for kind in ("PN_C", "PN_A"):
        for amp, _, _ in t[kind]["ladder"]:
            if kind == "PN_C" and amp >= 1.5:
                continue
            prot.append((kind, amp, SETTLE, SETTLE + LADDER_MS))
        for amp, _, _ in t[kind]["long"]:
            prot.append((kind, amp, SETTLE, SETTLE + LONG_MS))
    return prot


def pn_cost_terms(sp, prot, t, params=None):
    """Relative errors against Feng's cells: PN-C counts, latencies and first and last ISI on the
    ladder; PN-A counts, latencies and the gaps of the 4 s steps; long-step counts. A reset at or
    above threshold is penalised (it makes the cell burst)."""
    terms = []
    for (kind, amp, on, off), s in zip(prot, sp):
        s = s[(s >= on) & (s < off)] - on
        if off - on == LADDER_MS:
            ref = next(x for x in t[kind]["ladder_full"] if x["amp_nA"] == amp)
            n_t, lat_t, times_t = ref["count"], ref["latency_ms"], np.array(ref["spike_times_ms"])
            terms.append((len(s) - n_t) / (max(n_t, 1) if kind == "PN_C" else 1.0))
            terms.append(((s[0] if len(s) else LADDER_MS) - lat_t) / lat_t)
            if kind == "PN_C" and n_t >= 2:
                isi_t = np.diff(times_t)
                isi = np.diff(s) if len(s) >= 2 else np.array([LADDER_MS, LADDER_MS])
                terms.append((isi[0] - isi_t[0]) / isi_t[0])
                terms.append((isi[-1] - isi_t[-1]) / isi_t[-1])
        else:
            _, n_t, times_t = next(x for x in t[kind]["long"] if x[0] == amp)
            terms.append((len(s) - n_t) / (max(n_t, 1) if kind == "PN_C" else 1.0))
            if kind == "PN_A":
                gaps_t = np.diff(times_t)
                gaps = np.diff(s)
                for i, g_t in enumerate(gaps_t):
                    g = gaps[i] if i < len(gaps) else LONG_MS
                    terms.append((g - g_t) / g_t)
    if params is not None and params["Vr"] >= params["VT"] - 1.0:
        terms.append(10.0)
    return np.array(terms)


def pn_values(P_full, prot, S, extra_kinds=()):
    """Per-neuron values for S candidates x (protocol cells + extra noisy cells of the given kinds)."""
    kinds = [k for k, _, _, _ in prot] + list(extra_kinds)
    C = len(kinds)
    n = S * C
    vals = {}
    for k in ("EL", "ELd", "Cs", "gLs", "Cd", "gLd", "gc", "VT", "DeltaT", "Vr", "tref", "bf", "tauf", "dVbap"):
        vals[k] = np.repeat(P_full[k], C)
    is_a = np.tile([k == "PN_A" for k in kinds], S)
    vals["gs"] = np.where(is_a, np.repeat(P_full["gs_A"], C), 0.0)
    vals["dCa"] = np.repeat(P_full["dCa_A"], C)
    vals["Vgate"] = np.repeat(P_full["Vgate_A"], C)
    vals["tauC"] = np.repeat(P_full["tauC_A"], C)
    vals["kD"] = np.repeat(P_full["kD"], C)
    z = np.zeros(C)
    amp, ton, toff, non = z.copy(), z.copy(), z.copy(), np.ones(C)
    n_p = len(prot)
    amp[:n_p] = [a for _, a, _, _ in prot]
    ton[:n_p] = [o for _, _, o, _ in prot]
    toff[:n_p] = [f for _, _, _, f in prot]
    non[:n_p] = 0.0                                   # protocol cells without noise, as in Block A
    vals.update(Iamp=np.tile(amp, S), Ton=np.tile(ton, S), Toff=np.tile(toff, S), noise_on=np.tile(non, S))
    return vals


def pn_report(best, prot, sp_cand):
    rin, tau_slow, t63 = (float(x[0]) for x in pn_passive({k: np.array([v]) for k, v in best.items()}))
    rows = []
    for (kind, amp, on, off), s in zip(prot, sp_cand):
        s = s[(s >= on) & (s < off)] - on
        rows.append({"type": kind, "amp_nA": amp, "dur_ms": off - on, "count": int(len(s)),
                     "spike_times_ms": [round(float(x), 1) for x in s[:6]]})
    params = {k: float(v) for k, v in best.items() if not k.endswith("_A")}
    sahp = {k[:-2]: float(best[k]) for k in ("gs_A", "dCa_A", "Vgate_A", "tauC_A")}
    return ({"shared": params, "PN_A": sahp, "PN_C": dict(sahp, gs=0.0)},
            {"rin_MOhm": rin, "tau_slow_ms": tau_slow, "t63_ms": t63}, rows)


def fit_pn(t, popsize=15, maxiter=200, backend="cuda"):
    names = [k for k in PN_FREE if k != "kD"]            # no synaptic input in stage 1: kD has no effect
    prot = pn_protocols(t)
    n_p = len(prot)
    S = popsize * len(names)
    h = Harness("PN", S * n_p, SETTLE + LONG_MS + 10, backend=backend, name=f"fit_PN_{S}")
    EL, rin, tau = t["PN_C"]["vrest"], t["PN_C"]["rin"], t["PN_C"]["tau_slow"]

    def full(Xp):
        P, ok = pn_derive(dict(zip(names, Xp)), rin, tau, EL)
        P["kD"] = np.ones(Xp.shape[1])
        return P, ok

    def evaluate(X):
        s = X.shape[1]
        Xp = np.pad(X, ((0, 0), (0, S - s)), mode="edge")
        P, ok = full(Xp)
        sp = spikes_by_cell(*h.run(pn_values(P, prot, S)), S * n_p)
        iv, it = names.index("Vr"), names.index("VT")
        return np.array([np.sum(pn_cost_terms(sp[j * n_p:(j + 1) * n_p], prot, t,
                                              {"Vr": Xp[iv, j], "VT": Xp[it, j]}) ** 2) if ok[j] else 1e3
                         for j in range(s)])

    t0 = time.perf_counter()
    r = differential_evolution(evaluate, [PN_FREE[k] for k in names], vectorized=True, updating="deferred",
                               popsize=popsize, maxiter=maxiter, seed=1, polish=False, tol=1e-6)
    Xb = np.repeat(np.array(r.x)[:, None], S, axis=1)
    P, _ = full(Xb)
    sp = spikes_by_cell(*h.run(pn_values(P, prot, S)), S * n_p)[:n_p]
    h.close()
    best = {k: float(np.atleast_1d(v)[0]) for k, v in P.items()}
    params, passive, rows = pn_report(best, prot, sp)
    return {"kind": "PN", "stage": 1, "params": params, "passive": passive,
            "cost": float(r.fun), "generations": int(r.nit), "evaluations": int(r.nfev),
            "wall_s": time.perf_counter() - t0, "protocols": rows}


# ----------------------------------------------------------------------------- PN stage 2
NOISE_CELLS = 10                 # per PN type and candidate
S2_SETTLE, S2_RUN = 2000.0, 20000.0


def stage2_reference():
    r = json.loads((REFERENCE_DIR / "blockA" / "stage2_reference.json").read_text(encoding="utf-8"))
    d = np.load(REFERENCE_DIR / "blockA" / "drive_test_inputs.npz")
    return r, d


class Stage2Harness:
    """Per candidate: the stage-1 protocol cells, NOISE_CELLS noise-only cells of each PN type, and
    the 16 dendritic-input cells driven by Feng's 48 afferent trains through the fitted PN->PN
    synapses (AMPA + NMDA, on the dendrite), all in one GeNN model."""

    def __init__(self, t, S, backend="cuda", precision="double", noise_cells=NOISE_CELLS, drive_reps=1,
                 noise_ms=S2_RUN, name=None):
        import pygenn as G
        from .synapses import PRE_INIT, models as syn_models, psm_params, wu_params
        self.prot = pn_protocols(t)
        self.ref, inp = stage2_reference()
        n_drive = len(inp["kinds"])
        self.drive_kinds = list(inp["kinds"]) * drive_reps
        self.noise_ms = noise_ms
        npc = len(self.prot)
        self.layout = {"prot": (0, npc), "noise_A": (npc, noise_cells), "noise_C": (npc + noise_cells, noise_cells),
                       "drive": (npc + 2 * noise_cells, n_drive * drive_reps)}
        self.noise_kinds = ["PN_A"] * noise_cells + ["PN_C"] * noise_cells
        self.C = npc + 2 * noise_cells + n_drive * drive_reps
        self.S, self.n = S, S * self.C
        self.steps = int(round((S2_SETTLE + max(S2_RUN, noise_ms)) / DT))
        fits = json.loads((CONFIG_DIR / "synapses_fitted.json").read_text(encoding="utf-8"))["fits"]
        BUILD_DIR.mkdir(parents=True, exist_ok=True)
        self.cwd = os.getcwd()
        os.chdir(BUILD_DIR)
        m = G.GeNNModel(precision, name or f"fit2_PN_{S}", backend=backend)
        m.dt = DT
        m.seed = 20261015                       # same noise in every generation (common random numbers)
        init = initial_state("PN", -70.0)
        init.update({p: 1.0 for p in PN_PARAMS})
        init.update({"Iamp": 0.0, "Ton": 0.0, "Toff": 0.0, "noise_on": 0.0})
        self.pop = m.add_neuron_population("cells", self.n, models()["pn"], noise_params("PN"), init)
        self.pop.spike_recording_enabled = True
        off = inp["offsets"]
        n_tr = len(off) - 1
        src = m.add_neuron_population("trains", n_tr, "SpikeSourceArray", {},
                                      {"startSpike": off[:-1].astype(int), "endSpike": off[1:].astype(int)})
        src.extra_global_params["spikeTimes"].set_init_values(np.asarray(inp["times"], float))
        d0 = self.layout["drive"][0]
        pre = np.tile(np.arange(n_tr), S * drive_reps)
        post = np.concatenate([s * self.C + d0 + r * n_drive + np.asarray(inp["cell"])
                               for s in range(S) for r in range(drive_reps)])
        w = np.tile(np.asarray(inp["weight"], float), S * drive_reps)
        dly = np.tile(np.round(np.asarray(inp["delay_ms"]) / DT).astype(int), S * drive_reps)
        order = np.lexsort((post, pre))                  # GeNN stores connections sorted by (pre, post)
        self.syn_vals = {"W": w[order], "delay": dly[order]}
        sm = syn_models()
        self.groups = []
        for rec in ("AMPA", "NMDA"):
            fit = fits[f"PN_to_PN|{rec}"]
            psm = G.init_postsynaptic(sm["psm_nmda" if rec == "NMDA" else "psm"], psm_params(fit, 0.0),
                                      {"x": 0.0, "g": 0.0}, var_refs={"V": G.create_var_ref(self.pop, "Vd")})
            wu = G.init_weight_update(sm["wu"], wu_params("PN_PN", rec, fit), {"W": 0.0, "delay": 0},
                                      pre_vars=dict(PRE_INIT))
            sg = m.add_synapse_population(f"aff_{rec}", "SPARSE", src, self.pop, wu, psm)
            sg.set_sparse_connections(pre[order], post[order])
            sg.post_target_var = "IsynD"
            sg.max_dendritic_delay_timesteps = int(dly.max()) + 1
            self.groups.append(sg)
        m.build()
        self.model = m
        self.loaded = False

    def run(self, cell_values):
        m = self.model
        if self.loaded:
            m.unload()
        m.load(num_recording_timesteps=self.steps)
        self.loaded = True
        st = initial_state("PN", 0.0)
        for name in list(cell_values) + list(st):
            arr = (np.asarray(cell_values[name], float) if name in cell_values else
                   np.asarray(cell_values.get("ELd", cell_values["EL"]), float) if name in ("V", "Vd")
                   else np.full(self.n, st[name]))
            self.pop.vars[name].view[:] = arr
            self.pop.vars[name].push_to_device()
        for sg in self.groups:
            for k, v in self.syn_vals.items():
                sg.vars[k].values = v
                sg.vars[k].push_to_device()
        for _ in range(self.steps):
            m.step_time()
        m.pull_recording_buffers_from_device()
        times, ids = self.pop.spike_recording_data[0]
        return spikes_by_cell(np.asarray(times), np.asarray(ids), self.n)

    def close(self):
        if self.loaded:
            self.model.unload()
        os.chdir(self.cwd)


def stage2_measures(sp, h):
    """Noise-only and dendritic-input rates (Hz) and noise-only ISI CVs of one candidate."""
    def window(s, run=S2_RUN):
        return s[(s >= S2_SETTLE) & (s < S2_SETTLE + run)]
    out = {}
    for key, kind in (("noise_A", "PN_A"), ("noise_C", "PN_C")):
        a, n = h.layout[key]
        rates, cvs = [], []
        for s in sp[a:a + n]:
            w = window(s, h.noise_ms)
            rates.append(len(w) / (h.noise_ms / 1000.0))
            if len(w) >= 3:
                d = np.diff(w)
                cvs.append(d.std() / d.mean())
        out[f"noise_{kind}_Hz"] = float(np.mean(rates))
        out[f"noise_{kind}_cv"] = float(np.mean(cvs)) if cvs else 0.0
    a, n = h.layout["drive"]
    r = np.array([len(window(s)) / (S2_RUN / 1000.0) for s in sp[a:a + n]])
    k = np.array(h.drive_kinds)
    out["drive_PN_A_Hz"] = float(r[k == "PN_A"].mean())
    out["drive_PN_C_Hz"] = float(r[k == "PN_C"].mean())
    return out


def stage2_terms(m, ref):
    no, dr = ref["noise_only"], ref["drive_summary"]
    return np.array([(m["noise_PN_A_Hz"] - no["PN_A"]["mean_Hz"]) / no["PN_A"]["mean_Hz"],
                     (m["noise_PN_C_Hz"] - no["PN_C"]["mean_Hz"]) / no["PN_C"]["mean_Hz"],
                     0.5 * (m["noise_PN_A_cv"] - no["PN_A"]["isi_cv_mean"]),
                     0.5 * (m["noise_PN_C_cv"] - no["PN_C"]["isi_cv_mean"]),
                     (m["drive_PN_A_Hz"] - dr["PN_A"]["mean_Hz"]) / dr["PN_A"]["mean_Hz"],
                     (m["drive_PN_C_Hz"] - dr["PN_C"]["mean_Hz"]) / dr["PN_C"]["mean_Hz"]])


def fit_pn_stage2(t, popsize=10, maxiter=60, spread=None, backend="cuda"):
    """Refine all PN parameters, adding noise-only and dendritic-input targets to the stage-1 targets.
    Bounds: the full PN_FREE ranges (spread=None), or stage-1 value -+ spread (relative). The stage-1
    result is one member of the first generation. The dendrite needs the full range: stage 1 does not
    constrain it, and only the dendritic-input test does."""
    names = list(PN_FREE)
    s1 = json.loads((OUTPUT_DIR / "S1_fit_PN.json").read_text(encoding="utf-8"))["params"]
    mid = {k: (PN_FREE[k][0] + PN_FREE[k][1]) / 2 for k in names}
    x1 = np.array([s1["PN_A"].get(k[:-2], mid[k]) if k.endswith("_A") else s1["shared"].get(k, mid[k]) for k in names])
    lo = np.array([PN_FREE[k][0] for k in names], float)
    hi = np.array([PN_FREE[k][1] for k in names], float)
    if spread is not None:
        lo, hi = np.maximum(lo, x1 - spread * np.abs(x1)), np.minimum(hi, x1 + spread * np.abs(x1))
    S = popsize * len(names)
    h = Stage2Harness(t, S, backend=backend)
    EL, rin, tau = t["PN_C"]["vrest"], t["PN_C"]["rin"], t["PN_C"]["tau_slow"]
    n_p = len(h.prot)
    extra = h.noise_kinds + h.drive_kinds

    def full(Xp):
        return pn_derive(dict(zip(names, Xp)), rin, tau, EL)

    def evaluate(X):
        s = X.shape[1]
        Xp = np.pad(X, ((0, 0), (0, S - s)), mode="edge")
        P, ok = full(Xp)
        sp = h.run(pn_values(P, h.prot, S, extra))
        iv, it = names.index("Vr"), names.index("VT")
        costs = []
        for j in range(s):
            if not ok[j]:
                costs.append(1e3)
                continue
            cs = sp[j * h.C:(j + 1) * h.C]
            t1 = pn_cost_terms(cs[:n_p], h.prot, t, {"Vr": Xp[iv, j], "VT": Xp[it, j]})
            t2 = stage2_terms(stage2_measures(cs, h), h.ref)
            costs.append(np.sum(t1 ** 2) + np.sum(t2 ** 2))
        return np.array(costs)

    rng = np.random.default_rng(2)
    init = lo + (hi - lo) * rng.random((S, len(names)))
    init[0] = x1                                          # keep the stage-1 result in the first generation
    t0 = time.perf_counter()
    r = differential_evolution(evaluate, list(zip(lo, hi)), vectorized=True, updating="deferred", init=init,
                               maxiter=maxiter, seed=1, polish=False, tol=1e-6)
    Xb = np.repeat(np.array(r.x)[:, None], S, axis=1)
    P, _ = full(Xb)
    sp = h.run(pn_values(P, h.prot, S, extra))
    h.close()
    best = {k: float(np.atleast_1d(v)[0]) for k, v in P.items()}
    cs = sp[:h.C]
    params, passive, rows = pn_report(best, h.prot, cs[:n_p])
    return {"kind": "PN", "stage": 2, "params": params, "passive": passive, "stage2": stage2_measures(cs, h),
            "stage2_reference": {"noise_only": {k: (v["mean_Hz"], v["isi_cv_mean"]) for k, v in h.ref["noise_only"].items()},
                                 "drive": {k: v["mean_Hz"] for k, v in h.ref["drive_summary"].items()}},
            "cost": float(r.fun), "generations": int(r.nit), "evaluations": int(r.nfev),
            "wall_s": time.perf_counter() - t0, "protocols": rows}


# ----------------------------------------------------------------------------- main
def save(result):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    path = CONFIG_DIR / "cells_fitted.json"
    allp = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {
        "_about": "Simplified cells fitted to Feng's cells (Block A); units mV, ms, nF, uS, nA. Written by fit_cells.py."}
    allp[result["kind"]] = {"params": result["params"], "stage": result.get("stage", 1), "cost": result["cost"]}
    path.write_text(json.dumps(allp, indent=1), encoding="utf-8")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    suffix = "" if result.get("stage", 1) == 1 else f"_stage{result['stage']}"
    (OUTPUT_DIR / f"S1_fit_{result['kind']}{suffix}.json").write_text(json.dumps(result, indent=1), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kind", choices=("FSI", "PN", "PN2"))
    ap.add_argument("--backend", default="cuda")
    args = ap.parse_args()
    t = block_a()
    if args.kind in ("PN", "PN2"):
        r = fit_pn(t, backend=args.backend) if args.kind == "PN" else fit_pn_stage2(t, backend=args.backend)
        save(r)
        print(f"PN: cost {r['cost']:.4f} after {r['generations']} generations ({r['wall_s']:.0f} s)")
        print("  params:", json.dumps(r["params"]))
        print("  passive:", {k: round(v, 1) for k, v in r["passive"].items()},
              f"(Feng: Rin {t['PN_C']['rin']:.0f}, tau_slow {t['PN_C']['tau_slow']:.1f}, t63 {t['PN_C']['tau63']:.1f})")
        if "stage2" in r:
            print("  stage 2:", {k: round(v, 3) for k, v in r["stage2"].items()}, "| Feng:", r["stage2_reference"])
        for row in r["protocols"]:
            print(f"  {row['type']} {row['amp_nA']:.1f} nA {row['dur_ms']/1000:.0f} s: {row['count']:3d} spikes, first {row['spike_times_ms']}")
        return
    r = fit_fsi(t, backend=args.backend)
    save(r)
    print(f"{r['kind']}: cost {r['cost']:.4f} after {r['generations']} generations ({r['wall_s']:.0f} s)")
    print("  params:", {k: round(v, 5) for k, v in r["params"].items()})
    for row in r["ladder"]:
        print(f"  {row['amp_nA']:.1f} nA: {row['count']:3d} spikes (Feng {row['count_target']:3d}), "
              f"latency {row['latency_ms'] if row['latency_ms'] is None else round(row['latency_ms'], 1)} ms "
              f"(Feng {row['latency_target_ms']:.1f})")


if __name__ == "__main__":
    main()
