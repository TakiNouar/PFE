"""NEURON setup: Feng's compiled mechanisms and templates, plus Feng's global settings.

Run scripts from Simulations/BLA/simulation (not from a mechanisms folder):
NEURON auto-loads an nrnmech.dll found in the current directory, and loading
it a second time fails.
"""
import json
from pathlib import Path

SIM_DIR = Path(__file__).resolve().parents[1]
FENG_DIR = SIM_DIR / "mechanisms"          # ModelDB 247968, unchanged (Gate 0)
OURS_DIR = SIM_DIR / "mechanisms_run1"     # our additions (DEV-006, DEV-007)
OUTPUT_DIR = SIM_DIR / "outputs"
CONFIG_PATH = Path(__file__).resolve().parent / "config" / "run1.json"

PN_TEMPLATE = "BLcells_template_LFP_segconsider_all_Iinject_recordingimembrane.hoc"
FSI_TEMPLATE = "interneuron_template_gj_LFP_Iinject_recordingimembrane.hoc"

_h = None


def load_config():
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)


def setup(cfg=None):
    """Load NEURON once and return h, with Feng's templates and settings applied."""
    global _h
    if _h is not None:
        return _h
    if (Path.cwd() / "nrnmech.dll").exists():
        raise RuntimeError("Run from a folder without nrnmech.dll (NEURON auto-loads it).")
    cfg = cfg or load_config()

    from neuron import h, load_mechanisms

    load_mechanisms(str(FENG_DIR))
    if (OURS_DIR / "nrnmech.dll").exists():
        load_mechanisms(str(OURS_DIR))
    h.load_file("stdrun.hoc")
    # The templates read the global tstop when a cell is built (drv.dur = tstop; drv.amp = 0).
    h.tstop = 1e9
    h.load_file((FENG_DIR / PN_TEMPLATE).as_posix())
    h.load_file((FENG_DIR / FSI_TEMPLATE).as_posix())

    sim = cfg["simulation"]
    h.celsius = sim["celsius"]
    h.dt = sim["dt_ms"]
    h.steps_per_ms = 1.0 / sim["dt_ms"]
    h.v_init = sim["v_init_mV"]
    _h = h
    return h
