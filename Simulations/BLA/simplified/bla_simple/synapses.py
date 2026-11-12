"""Synapses of the simplified model (spec 14, section 4; choice S-1 b; S-DEV-3).

Each receptor is a rise-and-decay conductance fitted to the unitary waveform of Feng's pulse
scheme (fit_synapses.py), summed per receiving cell:
    on an arriving spike:   x += scale * W * fac * amp     (fac: depression, amp: saturation, below)
    every step (exact):     g <- g*ed + x*c*(ed - er) ;  x <- x*er
    current:                I = g * (E - V) [* B(V) for NMDA]
with ed = exp(-dt/tau_d), er = exp(-dt/tau_r), c = tau_r/(tau_d - tau_r), scale = A*(tau_d - tau_r)/tau_r,
so that one spike of weight 1 gives g(t) = A*(exp(-t/tau_d) - exp(-t/tau_r)).

Saturation: in Feng's pulse scheme, open receptors cannot open again, so a spike arriving while
the response of earlier spikes is still large adds less. Each presynaptic cell keeps its own
normalised response u (same rise-and-decay kinetics, 1 = single-spike peak); a spike adds
a = max(0, 1 - u/u_sat), where u_sat = 1 / (1 - exp(-Cdur (alpha + beta))) is Feng's saturation
level relative to one pulse (Rinf over the single-pulse peak), from his kinetic constants.

Depression (Feng's d1, tauD1, d2, tauD2 and floor) is applied per spike to the new response, as in
Varela et al. 1997, the source Feng cites. Feng's file also rescales the conductance still active
from earlier spikes; that difference matters only at high rates per connection (gate S2).
Saturation and depression depend only on the presynaptic spike train, so both are kept once per
presynaptic cell (pre variables), which keeps the cost per connection unchanged.
NMDA Mg2+ block: Feng's form B(V) = 1 / (1 + 0.33 exp(-0.06 V)).
"""
import math

_MODELS = {}

# Depression parameters from Feng's files (exc_ev.mod / inh_ev.mod, DEV-004).
DEPRESSION = {"PN_PN": 0.5, "PN_FSI": 0.7, "FSI_PN": 0.7, "FSI_FSI": 0.7}     # floors
D_PARAMS = {"d1": 0.95, "tauD1": 40.0, "d2": 0.9, "tauD2": 70.0}
# Feng's pulse kinetics (Cdur ms, alpha*Tmax /ms, beta /ms): pyrD2pyrD_STFD_new.mod, pyrD2interD_STFD.mod
# (AMPA overrides from config event_synapses), interD2pyrD_STFD_new.mod, interD2interD_STFD_new.mod.
FENG_KINETICS = {"PN_PN|AMPA": (1.421, 3.8142, 0.1429), "PN_PN|NMDA": (16.765, 0.2659, 0.008),
                 "PN_FSI|AMPA": (0.713, 10.1571, 0.4167), "PN_FSI|NMDA": (16.765, 0.2659, 0.008),
                 "FSI_PN|GABA": (0.7254, 1.52, 0.14), "FSI_FSI|GABA": (0.7254, 1.853, 0.147)}


def u_sat(pathway, receptor):
    cdur, alpha, beta = FENG_KINETICS[f"{pathway}|{receptor}"]
    return 1.0 / (1.0 - math.exp(-cdur * (alpha + beta)))


def peak_norm(tau_r, tau_d):
    tp = math.log(tau_d / tau_r) * tau_r * tau_d / (tau_d - tau_r)
    return math.exp(-tp / tau_d) - math.exp(-tp / tau_r)


def models():
    """GeNN model definitions (created once per process)."""
    if _MODELS:
        return _MODELS
    import pygenn as G
    _MODELS["wu"] = G.create_weight_update_model(
        "saturating_depressing",
        params=["d1", "tauD1", "d2", "tauD2", "floor", "tau_r", "tau_d", "usat", "pnorm"],
        vars=[("W", "scalar", G.VarAccess.READ_ONLY), ("delay", "uint8_t", G.VarAccess.READ_ONLY)],
        pre_vars=[("D1", "scalar"), ("D2", "scalar"), ("tlast", "scalar"), ("fac", "scalar"),
                  ("ux", "scalar"), ("ug", "scalar"), ("amp", "scalar")],
        pre_spike_code="""
        const scalar dtl = t - tlast;
        D1 = 1.0 - (1.0 - D1)*exp(-dtl/tauD1);
        D2 = 1.0 - (1.0 - D2)*exp(-dtl/tauD2);
        const scalar er_ = exp(-dtl/tau_r);
        const scalar ed_ = exp(-dtl/tau_d);
        ug = ug*ed_ + ux*(tau_r/(tau_d - tau_r))*(ed_ - er_);
        ux = ux*er_;
        // level the response is already headed for: the peak of g(s) = (ug + xg) e^(-s/tau_d) - xg e^(-s/tau_r)
        const scalar xg = ux*tau_r/(tau_d - tau_r);
        scalar upk = ug;
        if (xg > 0.0) {
            const scalar arg = (xg/tau_r) / ((ug + xg)/tau_d);
            if (arg > 1.0) {
                const scalar ts = log(arg) / (1.0/tau_r - 1.0/tau_d);
                upk = (ug + xg)*exp(-ts/tau_d) - xg*exp(-ts/tau_r);
            }
        }
        amp = fmax(0.0, 1.0 - upk/(pnorm*usat));
        ux += amp*(tau_d - tau_r)/tau_r;
        tlast = t;
        fac = fmax(floor, D1*D2);
        D1 *= d1; D2 *= d2;
        """,
        pre_spike_syn_code="addToPostDelay(W*fac*amp, delay);")
    common = dict(
        params=["tau_r", "tau_d", "E", "scale"],
        vars=[("x", "scalar"), ("g", "scalar")],
        neuron_var_refs=[("V", "scalar", G.VarAccessMode.READ_ONLY)],
        derived_params=[("er", lambda p, dt: math.exp(-dt / p["tau_r"])),
                        ("ed", lambda p, dt: math.exp(-dt / p["tau_d"])),
                        ("c", lambda p, dt: p["tau_r"] / (p["tau_d"] - p["tau_r"]))])
    update = "g = g*ed + x*c*(ed - er); x = x*er;"
    _MODELS["psm"] = G.create_postsynaptic_model(
        "dualexp_cond", **common,
        sim_code="x += scale*inSyn; inSyn = 0.0;\ninjectCurrent(g*(E - V));\n" + update)
    _MODELS["psm_nmda"] = G.create_postsynaptic_model(
        "dualexp_cond_nmda", **common,
        sim_code="x += scale*inSyn; inSyn = 0.0;\ninjectCurrent(g*(E - V)/(1.0 + 0.33*exp(-0.06*V)));\n" + update)
    return _MODELS


def psm_params(fit, E):
    """Postsynaptic parameters from one fitted receptor {A_uS, tau_r_ms, tau_d_ms}."""
    tr, td = fit["tau_r_ms"], fit["tau_d_ms"]
    return {"tau_r": tr, "tau_d": td, "E": E, "scale": fit["A_uS"] * (td - tr) / tr}


def wu_params(pathway, receptor, fit):
    tr, td = fit["tau_r_ms"], fit["tau_d_ms"]
    return dict(D_PARAMS, floor=DEPRESSION[pathway], tau_r=tr, tau_d=td,
                usat=u_sat(pathway, receptor), pnorm=peak_norm(tr, td))


PRE_INIT = {"D1": 1.0, "D2": 1.0, "tlast": 0.0, "fac": 1.0, "ux": 0.0, "ug": 0.0, "amp": 1.0}


def unitary(t, A, tau_r, tau_d):
    """Conductance after one spike of weight 1 at t = 0 (t in ms, array)."""
    import numpy as np
    t = np.asarray(t, float)
    return np.where(t >= 0, A * (np.exp(-np.clip(t, 0, None) / tau_d) - np.exp(-np.clip(t, 0, None) / tau_r)), 0.0)
