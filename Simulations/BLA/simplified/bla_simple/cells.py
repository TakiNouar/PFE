"""Cells of the simplified model (spec 14, section 3; S-DEV-1, S-DEV-2).

Units: mV, ms, nF, uS, nA. Every cell parameter is a per-neuron read-only variable, so one
compiled model serves both fitting (each neuron a different candidate) and the network (all
neurons equal). Each neuron also has its own injected current step (Iamp from Ton to Toff).

PN (PN-A and PN-C): soma with exponential spike initiation and two spike-triggered potassium
conductances (after-hyperpolarisation, AHP), plus one passive dendrite that receives the
excitatory synapses (IsynD):
    Cs dV/dt  = -gLs (V - EL) + gLs DeltaT exp((V - VT)/DeltaT) + gc (Vd - V)
                - (wf + gs*cs)(V - EK) + I_noise + Isyn + I_inject
    Cd dVd/dt = -gLd (Vd - ELd) + gc (V - Vd) + kD IsynD
    tauf dwf/dt = -wf                                    (fast AHP conductance, both types)
    slow AHP (PN-A), Feng's sahp.mod gating:  tauC dcs/dt = cinf - cs,
        cinf = ca^nH / (ca^nH + 1) if V >= Vgate else 0;   tauCa dca/dt = -ca
    spike when V > VT + 5 DeltaT: V -> Vr, wf -> wf + bf, ca -> ca + dCa, Vd -> Vd + dVbap,
    V held at Vr for tref.  EK = -80 mV (Feng's PN template).
ca is calcium in units of the sAHP half-activation level (Feng: ~0.59 uM). Feng's constants kept:
nH = 3.04 (his rate functions give a Hill curve of exponent 7/ln 10), tauCa = 1000 ms (capool).
Fitted per cell, starting from Feng's values: gs (uS), dCa, Vgate (Feng -65 mV) and tauC (Feng 48 ms);
the gate constants compensate for the missing spike shape (the voltage path after a spike differs).
kD: gain on the synaptic current reaching the dendrite (fitted to the dendritic-input test), standing
in for the amplification by the Na channels of Feng's apical dendrite, which a passive lumped
dendrite lacks.
dVbap is the back-propagating action potential: Feng's apical dendrite carries Na, K and Ca
channels, so each somatic spike depolarises it and unblocks its NMDA receptors. The reset cell has
no spike shape, so the dendrite gets this kick explicitly (fitted to the dendritic-input test).
wf: fast AHP, both types; ws: slow AHP, PN-A only (Feng's Ca2+-dependent sAHP). Conductances
rather than fixed currents: the AHP grows with depolarisation, which flattens the firing curve
at strong currents as in Feng's PN-C (a fixed-current AHP could not, fit of 2026-10-15).
FSI: one compartment, same spike rule, no adaptation, no depolarization block (decision 2026-10-15).
Background noise: Feng's point-conductance noise at the soma (Gfluct2_exc / Gfluct2_inh):
two independent Ornstein-Uhlenbeck conductances, exact update, clipped at 0,
I_noise = gE (Ee - V) + gI (Ei - V), scaled by the per-neuron switch noise_on (0 or 1).
Integration: forward Euler for V, Vd, w (derivatives from the values at the start of the
step); exact update for the noise.
"""
import math

_MODELS = {}

PN_PARAMS = ["Cs", "gLs", "Cd", "gLd", "gc", "EL", "ELd", "VT", "DeltaT", "Vr", "tref",
             "bf", "tauf", "gs", "dCa", "Vgate", "tauC", "dVbap", "kD"]
EK = -80.0                       # Feng's PN template: ek = -80 mV
SAHP = {"nH": 7.0 / math.log(10.0), "tauCa": 1000.0}          # Feng's sahp.mod, capool.mod (Vgate, tauC fitted)
FSI_PARAMS = ["C", "gL", "EL", "VT", "DeltaT", "Vr", "tref"]
PROTOCOL_VARS = ["Iamp", "Ton", "Toff", "noise_on"]

# Feng's noise (BL_main.hoc via config run1.json "noise"; tau and reversal from Gfluct defaults).
NOISE = {"PN": {"ge0": 0.0032, "std_e": 0.003, "gi0": 0.021, "std_i": 0.008},
         "FSI": {"ge0": 0.00121, "std_e": 0.00012, "gi0": 0.00573, "std_i": 0.00264}}
NOISE_KINETICS = {"tau_e": 2.728, "tau_i": 10.49, "Ee": 0.0, "Ei": -75.0}

_NOISE_DERIVED = [("exp_e", lambda p, dt: math.exp(-dt / p["tau_e"])),
                  ("amp_e", lambda p, dt: p["std_e"] * math.sqrt(1 - math.exp(-2 * dt / p["tau_e"]))),
                  ("exp_i", lambda p, dt: math.exp(-dt / p["tau_i"])),
                  ("amp_i", lambda p, dt: p["std_i"] * math.sqrt(1 - math.exp(-2 * dt / p["tau_i"])))]
_NOISE_CODE = """
        const scalar gEn = noise_on*fmax(0.0, ge0 + ge1);
        const scalar gIn = noise_on*fmax(0.0, gi0 + gi1);
        const scalar Inoise = gEn*(Ee - V) + gIn*(Ei - V);
        const scalar Iinj = (t >= Ton && t < Toff) ? Iamp : 0.0;
"""
_NOISE_UPDATE = """
        ge1 = ge1*exp_e + amp_e*gennrand_normal();
        gi1 = gi1*exp_i + amp_i*gennrand_normal();
"""


def models():
    if _MODELS:
        return _MODELS
    import pygenn as G
    ro = G.VarAccess.READ_ONLY
    noise_params = ["ge0", "std_e", "gi0", "std_i", "tau_e", "tau_i", "Ee", "Ei"]
    pn_params = noise_params + ["EK", "nH", "tauCa"]
    state = [("V", "scalar"), ("RefracTime", "scalar"), ("ge1", "scalar"), ("gi1", "scalar")]
    _MODELS["pn"] = G.create_neuron_model(
        "pn_two_compartment",
        params=pn_params,
        derived_params=_NOISE_DERIVED,
        vars=state + [("Vd", "scalar"), ("wf", "scalar"), ("cs", "scalar"), ("ca", "scalar")]
             + [(p, "scalar", ro) for p in PN_PARAMS + PROTOCOL_VARS],
        additional_input_vars=[("IsynD", "scalar", 0.0)],
        sim_code=_NOISE_CODE + """
        const scalar expo = gLs*DeltaT*exp(fmin((V - VT)/DeltaT, 30.0));
        const scalar dV = (-gLs*(V - EL) + expo + gc*(Vd - V) - (wf + gs*cs)*(V - EK) + Inoise + Isyn + Iinj) / Cs;
        const scalar dVd = (-gLd*(Vd - ELd) + gc*(V - Vd) + kD*IsynD) / Cd;
        const scalar can = pow(fmax(ca, 0.0), nH);
        const scalar cinf = (V >= Vgate) ? can / (can + 1.0) : 0.0;
        if (RefracTime > 0.0) { RefracTime -= dt; } else { V += dt*dV; }
        Vd += dt*dVd;
        wf *= exp(-dt/tauf);
        cs = cinf + (cs - cinf)*exp(-dt/tauC);
        ca *= exp(-dt/tauCa);
        """ + _NOISE_UPDATE,
        threshold_condition_code="RefracTime <= 0.0 && V > VT + 5.0*DeltaT",
        reset_code="V = Vr; wf += bf; ca += dCa; Vd += dVbap; RefracTime = tref;")
    _MODELS["fsi"] = G.create_neuron_model(
        "fsi_point",
        params=noise_params,
        derived_params=_NOISE_DERIVED,
        vars=state + [(p, "scalar", ro) for p in FSI_PARAMS + PROTOCOL_VARS],
        sim_code=_NOISE_CODE + """
        const scalar expo = gL*DeltaT*exp(fmin((V - VT)/DeltaT, 30.0));
        const scalar dV = (-gL*(V - EL) + expo + Inoise + Isyn + Iinj) / C;
        if (RefracTime > 0.0) { RefracTime -= dt; } else { V += dt*dV; }
        """ + _NOISE_UPDATE,
        threshold_condition_code="RefracTime <= 0.0 && V > VT + 5.0*DeltaT",
        reset_code="V = Vr; RefracTime = tref;")
    return _MODELS


def noise_params(kind):
    """Population-wide constants: Feng's noise (both kinds) and EK (PN)."""
    p = dict(NOISE["FSI" if kind == "FSI" else "PN"], **NOISE_KINETICS)
    if kind != "FSI":
        p["EK"] = EK
        p.update(SAHP)
    return p


def initial_state(kind, EL):
    s = {"V": EL, "RefracTime": 0.0, "ge1": 0.0, "gi1": 0.0}
    if kind != "FSI":
        s.update(Vd=EL, wf=0.0, cs=0.0, ca=0.0)
    return s
