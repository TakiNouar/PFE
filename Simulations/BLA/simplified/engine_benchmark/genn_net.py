"""The benchmark network in PyGeNN 5 (GPU). Same equations as brian2_net.py.

Same forward-Euler updates and the same order within a time step as Brian2: synaptic
increments from step t are used from step t+1; conductances decay by (1 - dt/tau).
Each excitatory connection drives AMPA and NMDA through one postsynaptic model (as one
Brian2 Synapses object increments both), so both engines process the same number of
synaptic events. Needs the MSVC + CUDA environment (run from vcvars64).

run_genn(n, sim_ms, precision) builds, loads and runs one network and returns the
wall-clock time of the stepping loop only (not code generation or compilation).
"""
import os
import time

from . import model as M

_MODELS = {}


def _models():
    if _MODELS:
        return _MODELS
    import pygenn as G
    _MODELS["pn"] = G.create_neuron_model(
        "pn_two_compartment",
        params=["Cs", "gLs", "Cd", "gLd", "gc", "EL", "VT", "DeltaT", "Vcut", "Vr", "a", "b", "tauw",
                "I0", "sigma", "taun"],
        vars=[("V", "scalar"), ("Vd", "scalar"), ("W", "scalar"), ("Iext", "scalar")],
        additional_input_vars=[("IsynD", "scalar", 0.0)],
        sim_code="""
        const scalar dV = (-gLs*(V-EL) + gLs*DeltaT*exp((V-VT)/DeltaT) + gc*(Vd-V) - W + Iext + Isyn) / Cs;
        const scalar dVd = (-gLd*(Vd-EL) + gc*(V-Vd) + IsynD) / Cd;
        const scalar dW = (a*(V-EL) - W) / tauw;
        const scalar noise = sigma*sqrt(2.0*dt/taun)*gennrand_normal();
        V += dt*dV; Vd += dt*dVd; W += dt*dW;
        Iext += dt*(I0 - Iext)/taun + noise;
        """,
        threshold_condition_code="V > Vcut",
        reset_code="V = Vr; W += b;")
    _MODELS["fsi"] = G.create_neuron_model(
        "fsi_point",
        params=["C", "gL", "EL", "VT", "DeltaT", "Vcut", "Vr", "I0", "sigma", "taun"],
        vars=[("V", "scalar"), ("Iext", "scalar")],
        sim_code="""
        const scalar dV = (-gL*(V-EL) + gL*DeltaT*exp((V-VT)/DeltaT) + Iext + Isyn) / C;
        const scalar noise = sigma*sqrt(2.0*dt/taun)*gennrand_normal();
        V += dt*dV;
        Iext += dt*(I0 - Iext)/taun + noise;
        """,
        threshold_condition_code="V > Vcut",
        reset_code="V = Vr;")
    # AMPA + NMDA (Mg block) from one connection; NMDA increment = ratioN x AMPA increment.
    _MODELS["exc"] = G.create_postsynaptic_model(
        "ampa_nmda_euler",
        params=["tauE", "tauN", "E", "Mg", "ratioN"],
        vars=[("gA", "scalar"), ("gN", "scalar")],
        neuron_var_refs=[("V", "scalar", G.VarAccessMode.READ_ONLY)],
        sim_code="""
        gA += inSyn; gN += ratioN*inSyn; inSyn = 0.0;
        injectCurrent(gA*(E - V) + gN*(E - V)/(1.0 + Mg/3.57*exp(-0.062*V)));
        gA *= (1.0 - dt/tauE); gN *= (1.0 - dt/tauN);
        """)
    _MODELS["inh"] = G.create_postsynaptic_model(
        "gaba_euler",
        params=["tauI", "E"],
        vars=[("g", "scalar")],
        neuron_var_refs=[("V", "scalar", G.VarAccessMode.READ_ONLY)],
        sim_code="""
        g += inSyn; inSyn = 0.0;
        injectCurrent(g*(E - V));
        g *= (1.0 - dt/tauI);
        """)
    return _MODELS


def run_genn(n, sim_ms, precision="float", build_root=".", warmup_steps=200):
    import pygenn as G
    mods = _models()
    n_pn, n_fsi = M.sizes(n)
    name = f"bench_n{n}_{precision}"
    os.makedirs(build_root, exist_ok=True)
    cwd = os.getcwd()
    os.chdir(build_root)
    try:
        model = G.GeNNModel(precision, name, backend="cuda")
        model.dt = M.DT
        pn_par = {k: M.PN[k] for k in ("Cs", "gLs", "Cd", "gLd", "gc", "EL", "VT", "DeltaT", "Vcut", "Vr",
                                       "a", "b", "tauw", "I0", "sigma", "taun")}
        fsi_par = {k: M.FSI[k] for k in ("C", "gL", "EL", "VT", "DeltaT", "Vcut", "Vr", "I0", "sigma", "taun")}
        unif = lambda el: G.init_var("Uniform", {"min": el - 5.0, "max": el + 5.0})
        pn = model.add_neuron_population("PN", n_pn, mods["pn"], pn_par,
                                         {"V": unif(M.PN["EL"]), "Vd": M.PN["EL"], "W": 0.0, "Iext": M.PN["I0"]})
        fsi = model.add_neuron_population("FSI", n_fsi, mods["fsi"], fsi_par,
                                          {"V": unif(M.FSI["EL"]), "Iext": M.FSI["I0"]})
        pn.spike_recording_enabled = True
        fsi.spike_recording_enabled = True
        S = M.SYN
        n_syn = 0
        for path, pre, post in (("PN_PN", pn, pn), ("PN_FSI", pn, fsi), ("FSI_PN", fsi, pn), ("FSI_FSI", fsi, fsi)):
            p = M.probability(path, n_pn, n_fsi)
            conn = G.init_sparse_connectivity("FixedProbabilityNoAutapse" if pre is post else "FixedProbability",
                                              {"prob": p})
            if path.startswith("PN"):
                w_a, w_n = M.W[path]
                target_v = "Vd" if post is pn else "V"
                psm = G.init_postsynaptic(mods["exc"], {"tauE": S["tauE"], "tauN": S["tauN"], "E": S["EE"],
                                                        "Mg": S["Mg"], "ratioN": w_n / w_a},
                                          {"gA": 0.0, "gN": 0.0}, var_refs={"V": G.create_var_ref(post, target_v)})
                wu = G.init_weight_update("StaticPulseConstantWeight", {"g": w_a})
            else:
                psm = G.init_postsynaptic(mods["inh"], {"tauI": S["tauI"], "E": S["EI"]}, {"g": 0.0},
                                          var_refs={"V": G.create_var_ref(post, "V")})
                wu = G.init_weight_update("StaticPulseConstantWeight", {"g": M.W[path]})
            sg = model.add_synapse_population(path, "SPARSE", pre, post, wu, psm, conn)
            sg.axonal_delay_steps = int(round(M.DELAY_MS / M.DT))
            if path == "PN_PN":
                sg.post_target_var = "IsynD"           # excitatory input to the PN dendrite
        steps = int(round(sim_ms / M.DT))
        t_build = time.perf_counter()
        model.build()
        model.load(num_recording_timesteps=steps + warmup_steps)
        build_s = time.perf_counter() - t_build
        for path in ("PN_PN", "PN_FSI", "FSI_PN", "FSI_FSI"):
            sg = model.synapse_populations[path]
            sg.pull_connectivity_from_device()
            n_syn += len(sg.get_sparse_pre_inds())
        for _ in range(warmup_steps):
            model.step_time()
        t0 = time.perf_counter()
        for _ in range(steps):
            model.step_time()
        model.pull_recording_buffers_from_device()     # waits for the GPU to finish
        wall = time.perf_counter() - t0
        sim_s = sim_ms / 1000.0

        def count(pop):
            times, _ids = pop.spike_recording_data[0]
            return int((times >= warmup_steps * M.DT).sum())
        out = {"engine": f"genn-cuda-{precision}", "threads": 1, "n": n, "sim_ms": sim_ms, "wall_s": wall,
               "real_time_factor": wall / sim_s, "rate_PN_Hz": count(pn) / n_pn / sim_s,
               "rate_FSI_Hz": count(fsi) / n_fsi / sim_s, "synapses": n_syn, "build_s": build_s}
        model.unload()
        return out
    finally:
        os.chdir(cwd)
