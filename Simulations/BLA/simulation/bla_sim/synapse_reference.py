"""Reference conductance traces of Feng's synapse files, for the simplified model (spec 14, gate S2).

Same protocols as synapse_test.py: each receiving compartment voltage-clamped at -70 mV, one
connection driven by isolated spikes, 5 / 20 / 50 Hz trains, 1 ms doublets and Poisson 20 Hz.
Two physiological trains are added (random, but no two spikes closer than 5 ms, as no BLA cell
fires faster than ~220 Hz in Block A): 20 Hz and 50 Hz. Only Feng's files are simulated here.

Usage (from Simulations/BLA/simulation): python -m bla_sim.synapse_reference
Writes outputs/blockA/synapse_reference.npz: for each pathway, receptor and protocol the
conductance trace (uS, already multiplied by the connection weight W), the spike times and W,
sampled every dt (0.05 ms). Index file synapse_reference.json lists the keys and parameters.
"""
import json

import numpy as np

from .nrn import OUTPUT_DIR, load_config, setup
from .provenance import run_metadata
from .synapse_test import PATHWAYS, _compartment, spike_trains


def record(h, pw, times, W, t_end):
    sec, clamp = _compartment(h, "ref_target")
    vs, tv = h.VecStim(), h.Vector(times)
    vs.play(tv)
    syn = getattr(h, pw["feng"])(sec(0.5))
    syn.initW = W
    nc = h.NetCon(vs, syn, 0, 1.0, 1.0)
    vecs = {name: h.Vector().record(getattr(syn, f"_ref_{gf}")) for name, gf, _ in pw["receptors"]}
    h.finitialize(-70)
    h.continuerun(t_end)
    out = {name: np.array(v) * W for name, v in vecs.items()}      # Feng: current = W * g
    h.delete_section(sec=sec)
    del nc, vs, tv, syn, clamp
    return out


def main():
    cfg = load_config()
    h = setup(cfg)
    rng = np.random.default_rng(1)
    trains = spike_trains(rng)
    rng2 = np.random.default_rng(2)
    for rate, t_max in ((20, 3000.0), (50, 2000.0)):
        isi = 5.0 + rng2.exponential(1000.0 / rate - 5.0, size=400)
        times = 100.0 + np.cumsum(isi)
        trains[f"Poisson {rate} Hz, >=5 ms"] = [float(t) for t in times if t < t_max]
    arrays, index = {}, {"meta": run_metadata(h), "dt_ms": h.dt, "clamp_mV": -70.0, "entries": []}
    for pname, pw in PATHWAYS.items():
        W = pw["W"][0]
        for tname, times in trains.items():
            t_end = max(times) + 600.0
            traces = record(h, pw, times, W, t_end)
            for rec_name, g in traces.items():
                key = f"{pname}|{rec_name}|{tname}"
                arrays[key + "|g"] = g
                arrays[key + "|spikes"] = np.array(times)
                index["entries"].append({"key": key, "pathway": pname, "receptor": rec_name, "protocol": tname,
                                         "W": W, "feng_file": pw["feng"], "overrides": pw["set"],
                                         "peak_uS": float(np.abs(g).max())})
    d = OUTPUT_DIR / "blockA"
    np.savez_compressed(d / "synapse_reference.npz", **arrays)
    (d / "synapse_reference.json").write_text(json.dumps(index, indent=1), encoding="utf-8")
    print(f"{len(index['entries'])} traces -> {d / 'synapse_reference.npz'}")


if __name__ == "__main__":
    main()
