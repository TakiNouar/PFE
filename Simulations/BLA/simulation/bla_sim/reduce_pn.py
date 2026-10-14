"""Block A2: reduce Feng's full PN and check the reductions (Gate R1, DEV-006).

Two reductions are built from Feng's full cell, with no fitted values:
  onepiece: one compartment holding the whole cell's membrane area and channel totals;
  twopiece: Feng's soma exactly, plus one lumped dendrite holding both dendrites'
            area and channel totals, coupled to the soma through the parallel
            half-length axial resistances of Feng's two dendrites.

Usage (from Simulations/BLA/simulation), after `python -m bla_sim.single_cell --level full`:
    python -m bla_sim.reduce_pn
Writes mechanisms_run1/reduced_pn.json and, per reduction, outputs/blockA/
single_cells_<level>.json, reduction_R1_<level>.json and single_cells_<level>_vs_full.png.
"""
import json
import math

import numpy as np

from . import cells as C
from .nrn import OURS_DIR, OUTPUT_DIR, load_config, setup
from .provenance import run_metadata
from .single_cell import run_protocol

SKIP = {"extracellular", "xtraimemrec"}   # Feng's LFP recorders: they only record (03)
FENG_TEMPLATE = {"PN_A": "Cell_A", "PN_C": "Cell_C"}


def _parameter_names(h, mech):
    ms = h.MechanismStandard(mech, 1)      # vartype 1 = PARAMETER range variables
    name = h.ref("")
    names = []
    for i in range(int(ms.count())):
        ms.name(name, i)
        names.append(name[0])
    return names


def _is_conductance(pname, mech):
    base = pname[: -(len(mech) + 1)] if pname.endswith("_" + mech) else pname
    return base.startswith("g") and base.endswith("bar")


def lump(h, segs):
    """Merge segments into one compartment: conductance totals kept, densities = total / area."""
    area = np.array([seg.area() for seg in segs])
    A = float(area.sum())
    present = [{m.name() for m in seg} for seg in segs]
    mechs = sorted(set().union(*present) - SKIP)
    params, totals, differing = {}, {}, {}
    for mech in mechs:
        vals = {}
        for p in _parameter_names(h, mech):
            per_seg = np.array([getattr(seg, p) if mech in pres else np.nan
                                for seg, pres in zip(segs, present)], dtype=float)
            have = ~np.isnan(per_seg)
            if _is_conductance(p, mech):
                g = np.nan_to_num(per_seg)                       # absent = 0 conductance
                totals[p] = float((g * area).sum() * 1e-8 * 1e6)  # S/cm2 * um2 -> uS
                vals[p] = float((g * area).sum() / A)
            else:
                v = per_seg[have]
                vals[p] = float(v[0]) if np.allclose(v, v[0]) else float((v * area[have]).sum() / area[have].sum())
                if not np.allclose(v, v[0]):
                    differing[p] = {"min": float(v.min()), "max": float(v.max()), "used_area_mean": vals[p]}
        params[mech] = vals
    reversal = {}
    for ion in ("ena", "ek", "eca"):
        v = [getattr(seg, ion) for seg in segs if hasattr(seg, ion)]
        if v:
            if not np.allclose(v, v[0]):
                differing[ion] = {"min": float(min(v)), "max": float(max(v))}
            reversal[ion] = float(v[0])
    return {
        "area_um2": A,
        "segments_merged": len(segs),
        "cm_uF_cm2": float((np.array([seg.cm for seg in segs]) * area).sum() / A),
        "Ra_ohm_cm": float(segs[0].sec.Ra),
        "mechanisms": params,
        "reversal_mV": reversal,
        "total_conductance_uS": totals,
        "parameters_that_differ_across_segments": differing,
    }


def _half_resistance_ohm(sec):
    """Axial resistance from a section's start to its midpoint (Ohm)."""
    L, d = sec.L * 1e-4, sec.diam * 1e-4
    return sec.Ra * (L / 2) / (math.pi * d * d / 4)


def reduce(h, kind):
    cell = C.make_cell(h, kind, "full")
    secs = (cell.soma, cell.dend, cell.p_dend)
    all_segs = [seg for sec in secs for seg in sec]
    src = f"Feng's {FENG_TEMPLATE[kind]} (ModelDB 247968); DEV-006"

    one = lump(h, all_segs)
    d1 = math.sqrt(one["area_um2"] / math.pi)
    one.update(L_um=d1, diam_um=d1)

    soma = lump(h, list(cell.soma))
    soma.update(L_um=cell.soma.L, diam_um=cell.soma.diam)
    dend = lump(h, [seg for sec in (cell.dend, cell.p_dend) for seg in sec])
    r_couple = 1.0 / sum(1.0 / _half_resistance_ohm(s) for s in (cell.dend, cell.p_dend))
    A_cm2 = dend["area_um2"] * 1e-8
    d_cm = (2 * dend["Ra_ohm_cm"] * A_cm2 / (math.pi ** 2 * r_couple)) ** (1 / 3)
    dend.update(diam_um=d_cm * 1e4, L_um=A_cm2 / (math.pi * d_cm) * 1e4,
                coupling_MOhm=r_couple / 1e6,
                coupling_rule="parallel half-length axial resistances of Feng's dend and p_dend")
    return ({"source": f"All 16 segments of {src}", "soma": one},
            {"source": f"Soma copied exactly; both dendrites lumped; {src}", "soma": soma, "dend": dend})


def _rel(a, b):
    return abs(a - b) / abs(b) if b else float("inf")


def gate_r1(full, red, tol):
    checks = []

    def add(kind, what, f, o, ok, rule):
        checks.append({"cell": kind, "measure": what, "full": f, "reduced": o, "rule": rule, "pass": bool(ok)})

    for kind in ("PN_A", "PN_C"):
        F, O = full[kind], red[kind]
        add(kind, "vrest_mV", F["passive"]["vrest_mV"], O["passive"]["vrest_mV"],
            abs(F["passive"]["vrest_mV"] - O["passive"]["vrest_mV"]) <= tol["vrest_mV"], "±1 mV")
        for key, rule in (("rin_MOhm", "rin_rel"), ("tau_ms", "tau_rel")):
            add(kind, key, F["passive"][key], O["passive"][key],
                _rel(O["passive"][key], F["passive"][key]) <= tol[rule], f"±{tol[rule]:.0%}")
        one_s = F["ladder"][0]["dur_ms"]
        for fs, os_ in zip(F["ladder"] + F["long_steps"], O["ladder"] + O["long_steps"]):
            fc, oc = fs["count"], os_["count"]
            ok = abs(fc - oc) <= tol["count_abs_below_10"] if fc < 10 else _rel(oc, fc) <= tol["count_rel"]
            add(kind, f"count {fs['amp_nA']} nA / {fs['dur_ms'] / 1000:g} s", fc, oc, ok,
                "±1 spike" if fc < 10 else f"±{tol['count_rel']:.0%}")
            if fs["latency_ms"] is not None and fs["dur_ms"] == one_s:
                ol = os_["latency_ms"]
                add(kind, f"latency {fs['amp_nA']} nA", round(fs["latency_ms"], 2),
                    None if ol is None else round(ol, 2),
                    ol is not None and _rel(ol, fs["latency_ms"]) <= tol["latency_rel"],
                    f"±{tol['latency_rel']:.0%}")
        Fn, On = F["noise_only"], O["noise_only"]
        add(kind, "noise rate_Hz", Fn["rate_Hz"], On["rate_Hz"],
            _rel(On["rate_Hz"], Fn["rate_Hz"]) <= tol["noise_rate_rel"], f"±{tol['noise_rate_rel']:.0%}")
        if Fn["count"] >= tol["noise_cv_min_spikes"] and On["isi_cv"] is not None:
            add(kind, "noise isi_cv", round(Fn["isi_cv"], 3), round(On["isi_cv"], 3),
                abs(Fn["isi_cv"] - On["isi_cv"]) <= tol["noise_cv_abs"], f"±{tol['noise_cv_abs']}")
    return checks


def _load_full_traces(d):
    traces = {}
    npz = np.load(d / "traces_full.npz")
    for key in npz.files:
        k, part, a = key.split("|")
        slot = traces.setdefault(k, {"ladder": {}, "long": {}, "noise": None})
        if part == "noise":
            slot["noise"] = npz[key]
        else:
            slot[part][float(a)] = npz[key]
    return traces


def main():
    cfg = load_config()
    h = setup(cfg)
    meta = run_metadata(h)
    reduced = {"onepiece": {}, "twopiece": {}}
    for kind in ("PN_A", "PN_C"):
        reduced["onepiece"][kind], reduced["twopiece"][kind] = reduce(h, kind)
    OURS_DIR.mkdir(exist_ok=True)
    C.REDUCED_PATH.write_text(json.dumps(reduced, indent=1), encoding="utf-8")
    tp = reduced["twopiece"]["PN_A"]["dend"]
    print(f"two-piece dendrite: area {tp['area_um2']:.0f} um2, diam {tp['diam_um']:.2f} um, "
          f"L {tp['L_um']:.1f} um, coupling {tp['coupling_MOhm']:.2f} MOhm")

    d = OUTPUT_DIR / "blockA"
    full = json.loads((d / "single_cells_full.json").read_text(encoding="utf-8"))
    full_traces = _load_full_traces(d)
    from .plots import single_cell_figure
    for level in C.REDUCED_LEVELS:
        results, traces = run_protocol(h, level, cfg, ("PN_A", "PN_C"))
        out = {"meta": meta, "level": level, "protocol": cfg["single_cell_protocol"], "cells": results}
        (d / f"single_cells_{level}.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
        checks = gate_r1(full["cells"], results, cfg["gate_R1_tolerances"])
        exc = cfg.get("gate_R1_accepted_exceptions", {})
        accepted = {tuple(x) for x in exc.get("checks", [])} if exc.get("level") == level else set()
        for c in checks:
            c["accepted_exception"] = (not c["pass"]) and (c["cell"], c["measure"]) in accepted
        n_ok = sum(c["pass"] for c in checks)
        n_exc = sum(c["accepted_exception"] for c in checks)
        unexplained = [c for c in checks if not c["pass"] and not c["accepted_exception"]]
        status = "FAIL" if unexplained else ("PASS" if n_exc == 0 else f"PASS with {n_exc} approved exceptions")
        report = {"meta": meta, "gate": "R1", "level": level, "status": status,
                  "passed_outright": n_ok, "checks_total": len(checks), "checks": checks}
        if n_exc:
            report["exceptions_approved"] = {k: exc[k] for k in ("approved", "reason")}
        (d / f"reduction_R1_{level}.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
        for c in checks:
            if not c["pass"]:
                tag = "accepted" if c["accepted_exception"] else "FAIL"
                print(f"  {tag:8s} {c['cell']} {c['measure']}: full {c['full']} vs {level} {c['reduced']} ({c['rule']})")
        print(f"Gate R1 [{level}]: {status} ({n_ok}/{len(checks)} checks pass outright)")
        single_cell_figure(out, traces, d / f"single_cells_{level}_vs_full.png",
                           cfg["single_cell_protocol"]["trace_interval_ms"],
                           overlay=(full["cells"], full_traces, "full (Feng)"))


if __name__ == "__main__":
    main()
