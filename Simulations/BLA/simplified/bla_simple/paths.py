"""Folders used by the simplified model."""
from pathlib import Path

SIMPLE_DIR = Path(__file__).resolve().parents[1]           # Simulations/BLA/simplified
CONFIG_DIR = SIMPLE_DIR / "config"
OUTPUT_DIR = SIMPLE_DIR / "outputs"
BUILD_DIR = OUTPUT_DIR / "build_genn"                      # GeNN code generation (gitignored)
REFERENCE_DIR = SIMPLE_DIR.parent / "simulation" / "outputs"   # Feng's reference results (Blocks A, B)
