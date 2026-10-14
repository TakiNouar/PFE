"""Provenance checks (Gate 0) and run metadata."""
import datetime
import hashlib
import platform
import shutil
import subprocess

from .nrn import FENG_DIR, SIM_DIR


def check_feng_hashes():
    """Verify every Feng file matches mechanisms/HASHES.txt. Raises on any mismatch."""
    listing = FENG_DIR / "HASHES.txt"
    bad = []
    n = 0
    for line in listing.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        digest, name = line.split(maxsplit=1)
        name = name.lstrip("*")
        path = FENG_DIR / name
        n += 1
        if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            bad.append(name)
    if bad:
        raise RuntimeError(f"Feng files changed or missing (Gate 0): {bad}")
    return n


def _git_commit():
    git = shutil.which("git") or r"C:\Program Files\Git\cmd\git.exe"
    try:
        out = subprocess.run([git, "rev-parse", "--short", "HEAD"], cwd=SIM_DIR,
                             capture_output=True, text=True, timeout=10)
        dirty = subprocess.run([git, "status", "--porcelain", "--", "bla_sim"], cwd=SIM_DIR,
                               capture_output=True, text=True, timeout=10).stdout.strip()
        return out.stdout.strip() + ("+uncommitted" if dirty else "")
    except Exception:
        return "unknown"


def run_metadata(h):
    return {
        "date": datetime.datetime.now().isoformat(timespec="seconds"),
        "neuron_version": h.nrnversion(5),
        "python": platform.python_version(),
        "machine": platform.processor() or platform.machine(),
        "repo_commit": _git_commit(),
        "feng_files_checked": check_feng_hashes(),
        "dt_ms": h.dt,
        "celsius": h.celsius,
    }
