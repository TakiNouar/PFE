"""The benchmark network in Brian2 (CPU). Same equations as genn_net.py.

run_brian2(n, sim_ms, target, threads) builds and runs one network and returns the
wall-clock time of the simulation loop only (not code generation or compilation).
target: "numpy" (no compiler, slow, for tuning), "cpp_standalone" (compiled C++, OpenMP).
"""
import time

import numpy as np

from . import model as M


def _equations():
    from brian2 import Equations
    pn = Equations("""
        dv/dt = (-gLs*(v-EL) + gLs*DeltaT*exp((v-VT)/DeltaT) + gc*(vd-v) - w + Iext
                 + gI*(EI-v)) / Cs : 1
        dvd/dt = (-gLd*(vd-EL) + gc*(v-vd) + gE*(EE-vd)
                  + gN*(EE-vd)/(1 + Mg/3.57*exp(-0.062*vd))) / Cd : 1
        dw/dt = (a*(v-EL) - w) / tauw : 1
        dIext/dt = (I0 - Iext)/taun + sigma*sqrt(2/taun)*xi_n : 1
        dgE/dt = -gE/tauE : 1
        dgN/dt = -gN/tauN : 1
        dgI/dt = -gI/tauI : 1
    """)
    fsi = Equations("""
        dv/dt = (-gL*(v-EL) + gL*DeltaT*exp((v-VT)/DeltaT) + Iext + gE*(EE-v)
                 + gN*(EE-v)/(1 + Mg/3.57*exp(-0.062*v)) + gI*(EI-v)) / C : 1
        dIext/dt = (I0 - Iext)/taun + sigma*sqrt(2/taun)*xi_n : 1
        dgE/dt = -gE/tauE : 1
        dgN/dt = -gN/tauN : 1
        dgI/dt = -gI/tauI : 1
    """)
    return pn, fsi


def run_brian2(n, sim_ms, target="numpy", threads=1, seed=1, build_dir=None):
    import brian2 as b2
    b2.start_scope()
    if target == "cpp_standalone":
        b2.set_device("cpp_standalone", directory=build_dir, build_on_run=False)
        b2.prefs.devices.cpp_standalone.openmp_threads = threads
    else:
        b2.prefs.codegen.target = target
    b2.defaultclock.dt = M.DT * b2.ms
    b2.seed(seed)
    n_pn, n_fsi = M.sizes(n)
    pn_eq, fsi_eq = _equations()
    # Dimensionless model in mV / ms / nF / uS / nA: time constants carry ms so Brian2's clock fits.
    ms = b2.ms
    ns_pn = dict(M.PN, **M.SYN)
    ns_pn.update(Cs=M.PN["Cs"] * ms, Cd=M.PN["Cd"] * ms, tauw=M.PN["tauw"] * ms, taun=M.PN["taun"] * ms,
                 tauE=M.SYN["tauE"] * ms, tauN=M.SYN["tauN"] * ms, tauI=M.SYN["tauI"] * ms)
    ns_fsi = dict(M.FSI, **M.SYN)
    ns_fsi.update(C=M.FSI["C"] * ms, taun=M.FSI["taun"] * ms, tauE=M.SYN["tauE"] * ms,
                  tauN=M.SYN["tauN"] * ms, tauI=M.SYN["tauI"] * ms)
    pn = b2.NeuronGroup(n_pn, pn_eq, threshold="v > Vcut", reset="v = Vr; w += b",
                        method="euler", namespace=ns_pn, name="pn")
    fsi = b2.NeuronGroup(n_fsi, fsi_eq, threshold="v > Vcut", reset="v = Vr",
                         method="euler", namespace=ns_fsi, name="fsi")
    for g, p in ((pn, M.PN), (fsi, M.FSI)):
        g.v = "EL + 10*rand() - 5"
        g.Iext = p["I0"]
    pn.vd = M.PN["EL"]
    syns = []
    for path, pre, post in (("PN_PN", pn, pn), ("PN_FSI", pn, fsi), ("FSI_PN", fsi, pn), ("FSI_FSI", fsi, fsi)):
        w = M.W[path]
        code = f"gE_post += {w[0]}; gN_post += {w[1]}" if path.startswith("PN") else f"gI_post += {w}"
        s = b2.Synapses(pre, post, on_pre=code, delay=M.DELAY_MS * ms, name=path.lower())
        s.connect(condition="i != j" if pre is post else None, p=M.probability(path, n_pn, n_fsi))
        syns.append(s)
    mon_pn, mon_fsi = b2.SpikeMonitor(pn), b2.SpikeMonitor(fsi)
    net = b2.Network(b2.collect())
    net.add(syns)
    if target == "cpp_standalone":
        import os
        # Brian2 starts the compiled program as "main" from inside build_dir. Where Windows is set
        # not to search the current folder (NoDefaultCurrentDirectoryInExePath), put build_dir on
        # this process's PATH so the program is found.
        os.environ["PATH"] = os.path.abspath(build_dir) + os.pathsep + os.environ["PATH"]
        net.run(sim_ms * ms)
        b2.device.build(directory=build_dir, compile=True, run=True, debug=False)
        wall = b2.device._last_run_time
    else:
        t0 = time.perf_counter()
        net.run(sim_ms * ms)
        wall = time.perf_counter() - t0
    out = {"engine": f"brian2-{target}", "threads": threads, "n": n, "sim_ms": sim_ms, "wall_s": wall,
           "real_time_factor": wall / (sim_ms / 1000.0),
           "rate_PN_Hz": mon_pn.num_spikes / n_pn / (sim_ms / 1000.0),
           "rate_FSI_Hz": mon_fsi.num_spikes / n_fsi / (sim_ms / 1000.0),
           "synapses": int(sum(len(s) for s in syns))}
    if target == "cpp_standalone":
        b2.device.reinit()
        b2.device.activate()
        b2.set_device("runtime")
    return out


if __name__ == "__main__":
    import sys
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 500
    print(run_brian2(n, 1000.0, target="numpy"))
