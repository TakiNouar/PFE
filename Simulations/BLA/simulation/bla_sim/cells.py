"""Cell builders for both levels (architecture/03).

Reference level ("full"): Feng's templates, unchanged.
Main level: PN-A / PN-C reduced from Feng's full cell, parameters in
mechanisms_run1/reduced_pn.json (DEV-006):
  "onepiece": one compartment;
  "twopiece": Feng's soma, exactly, plus one lumped dendrite.
FSI is Feng's template at every level.
"""
import json
import math

from .nrn import OURS_DIR

KINDS = ("PN_A", "PN_C", "FSI")
REDUCED_LEVELS = ("onepiece", "twopiece")
REDUCED_PATH = OURS_DIR / "reduced_pn.json"


def _fill(h, sec, comp):
    sec.nseg = 1
    sec.L = comp["L_um"]
    sec.diam = comp["diam_um"]
    sec.cm = comp["cm_uF_cm2"]
    sec.Ra = comp["Ra_ohm_cm"]
    seg = sec(0.5)
    for mech, values in comp["mechanisms"].items():
        sec.insert(mech)
        for pname, val in values.items():
            setattr(seg, pname, val)
    for attr, val in comp["reversal_mV"].items():
        setattr(sec, attr, val)


class ReducedPN:
    """Principal cell with one ("onepiece") or two ("twopiece") compartments.

    `soma` always exists. `dend` exists only in the two-piece cell; in the one-piece
    cell it is the soma itself, so callers can place excitatory synapses on `dend`
    (Feng: dend(0.9)) and inhibitory ones on `soma` at either level.
    """

    def __init__(self, h, params, name):
        self.h = h
        self.soma = h.Section(name=f"{name}_soma")
        _fill(h, self.soma, params["soma"])
        if "dend" in params:
            self.dend = h.Section(name=f"{name}_dend")
            _fill(h, self.dend, params["dend"])
            self.dend.connect(self.soma(1), 0)
        else:
            self.dend = self.soma

    def connect2target(self, target=None):
        nc = self.h.NetCon(self.soma(0.5)._ref_v, target, sec=self.soma)
        nc.threshold = 0          # same detector as Feng's templates
        return nc


def load_reduced_params():
    with open(REDUCED_PATH, encoding="utf-8") as f:
        return json.load(f)


_counter = [0]


def make_cell(h, kind, level="full", reduced=None):
    if kind not in KINDS:
        raise ValueError(kind)
    if level == "full" or kind == "FSI":
        return {"PN_A": h.Cell_A, "PN_C": h.Cell_C, "FSI": h.InterneuronCell}[kind]()
    if level in REDUCED_LEVELS:
        reduced = reduced or load_reduced_params()
        _counter[0] += 1
        return ReducedPN(h, reduced[level][kind], f"{kind}_{level}_{_counter[0]}")
    raise ValueError(level)


def spike_detector(h, cell):
    vec = h.Vector()
    nc = cell.connect2target(None)
    nc.record(vec)
    return nc, vec


def attach_noise(h, cell, kind, gid, n_total, cfg):
    """Feng's point-conductance noise at soma(0.5), set up as in BL_main.hoc.

    Returns the objects that must stay referenced for the noise to keep running.
    """
    p = cfg["noise"]["FSI" if kind == "FSI" else "PN"]
    off = cfg["noise"]["random123_offset"]
    r_e = h.Random()
    r_e.Random123(gid + off)
    r_e.normal(0, 1)
    exc = h.Gfluct2_exc(cell.soma(0.5))
    exc.g_e0 = p["g_e0_uS"]
    exc.std_e = p["std_e_uS"]
    exc.setRandObj(r_e)
    r_i = h.Random()
    r_i.Random123(gid + off + n_total)
    r_i.normal(0, 1)
    inh = h.Gfluct2_inh(cell.soma(0.5))
    inh.g_i0 = p["g_i0_uS"]
    inh.std_i = p["std_i_uS"]
    inh.setRandObj(r_i)
    return [exc, inh, r_e, r_i]
