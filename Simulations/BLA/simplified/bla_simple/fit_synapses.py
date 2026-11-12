"""Fit the rise-and-decay synapses to Feng's unitary conductance waveforms (spec 14 S-1 b, gate S2).

Reference: simulation/outputs/blockA/synapse_reference.npz (Feng's files in NEURON, written by
`python -m bla_sim.synapse_reference`). The first response of the "isolated (1 s apart)"
protocol, divided by the connection weight W, is the unitary waveform. Its onset is the spike
time + 1 ms (the NetCon delay of that protocol).

Usage (from Simulations/BLA/simplified): <venv python> -m bla_simple.fit_synapses
Writes config/synapses_fitted.json: A (uS per unit weight), tau_r, tau_d per pathway and
receptor, with the fit errors (peak, time to peak, charge, worst point relative to the peak).
"""
import json

import numpy as np
from scipy.optimize import brentq

from .paths import CONFIG_DIR, REFERENCE_DIR
from .synapses import unitary

DELAY_MS = 1.0
WINDOW_MS = 900.0


def load_reference():
    idx = json.loads((REFERENCE_DIR / "blockA" / "synapse_reference.json").read_text(encoding="utf-8"))
    data = np.load(REFERENCE_DIR / "blockA" / "synapse_reference.npz")
    return idx, data


def unitary_waveform(idx, data, pathway, receptor):
    e = next(e for e in idx["entries"] if e["pathway"] == pathway and e["receptor"] == receptor
             and e["protocol"].startswith("isolated"))
    dt = idx["dt_ms"]
    g = data[e["key"] + "|g"] / e["W"]
    t0 = data[e["key"] + "|spikes"][0] + DELAY_MS
    t = np.arange(len(g)) * dt - t0
    sel = (t >= -1.0) & (t < WINDOW_MS)
    return t[sel], g[sel], e


def fit(t, g):
    """Decay time from the tail of Feng's waveform (log-linear fit between 30 % and 5 % of the
    peak); then tau_r and A chosen so that the peak and the charge equal Feng's exactly."""
    dt = t[1] - t[0]
    peak = g.max()
    i_peak = int(np.argmax(g))
    t_peak = t[i_peak]
    charge = g.sum() * dt
    tail = (np.arange(len(g)) > i_peak) & (g < 0.30 * peak) & (g > 0.05 * peak)
    td = float(-1.0 / np.polyfit(t[tail], np.log(g[tail]), 1)[0])

    def peak_of(tr):
        A = charge / (td - tr)
        tp = np.log(td / tr) * tr * td / (td - tr)
        return A * (np.exp(-tp / td) - np.exp(-tp / tr))

    tr = float(brentq(lambda x: peak_of(x) - peak, 1e-4, 0.999 * td))
    A = charge / (td - tr)
    model = unitary(t, A, tr, td)
    return {"A_uS": float(A), "tau_r_ms": float(tr), "tau_d_ms": float(td),
            "errors": {"peak_rel": float(model.max() / peak - 1),
                       "time_to_peak_ms": float(t[np.argmax(model)] - t_peak),
                       "charge_rel": float(model.sum() * dt / (g.sum() * dt) - 1),
                       "worst_point_rel_peak": float(np.abs(model - g).max() / peak)},
            "feng": {"peak_uS_per_W": float(peak), "time_to_peak_ms": float(t_peak),
                     "charge_uS_ms_per_W": float(g.sum() * dt)}}


def main():
    idx, data = load_reference()
    pairs = sorted({(e["pathway"], e["receptor"]) for e in idx["entries"]})
    out = {"source": "Feng's synapse files (ModelDB 247968) in NEURON, voltage clamp -70 mV, "
                     "simulation/outputs/blockA/synapse_reference.npz", "form": "A*(exp(-t/tau_d) - exp(-t/tau_r)) per unit weight",
           "fits": {}}
    for pathway, receptor in pairs:
        t, g, e = unitary_waveform(idx, data, pathway, receptor)
        f = fit(t, g)
        out["fits"][f"{pathway}|{receptor}"] = f
        er = f["errors"]
        print(f"{pathway:10s} {receptor:5s} A {f['A_uS']:.5f} uS  tau_r {f['tau_r_ms']:6.3f}  tau_d {f['tau_d_ms']:7.2f} ms | "
              f"peak {100*er['peak_rel']:+.1f}%  t_peak {er['time_to_peak_ms']:+.2f} ms  charge {100*er['charge_rel']:+.1f}%  "
              f"worst {100*er['worst_point_rel_peak']:.1f}% of peak")
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    (CONFIG_DIR / "synapses_fitted.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"-> {CONFIG_DIR / 'synapses_fitted.json'}")


if __name__ == "__main__":
    main()
