"""Figures for Block A (display only; numbers come from the JSON files)."""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

COLOURS = {"PN_A": "#1D9E75", "PN_C": "#378ADD", "FSI": "#D85A30"}
LABELS = {"PN_A": "PN-A", "PN_C": "PN-C", "FSI": "FSI"}


def _time(trace, dt):
    return np.arange(len(trace)) * dt / 1000.0


def single_cell_figure(out, traces, path, dt, overlay=None):
    """One column per cell type: 1 s step, 4 s step, 5 s of noise, f-I curve.

    overlay: optional (results, traces, label) drawn in grey underneath (Gate R1 view).
    """
    kinds = list(out["cells"].keys())
    fig, axes = plt.subplots(4, len(kinds), figsize=(4.2 * len(kinds), 10), squeeze=False)
    settle = out["protocol"]["settle_ms"] / 1000.0
    for j, k in enumerate(kinds):
        c = COLOURS[k]
        rows = [("ladder", 0.4, "0.4 nA for 1 s"), ("long", 0.4, "0.4 nA for 4 s"),
                ("noise", 0, "Background noise only (5 s)")]
        for i, (part, amp, title) in enumerate(rows):
            ax = axes[i][j]
            if overlay is not None and k in overlay[1]:
                ref = overlay[1][k][part] if part == "noise" else overlay[1][k][part].get(amp)
                if ref is not None:
                    ax.plot(_time(ref, dt), ref, color="0.7", lw=0.8, label=overlay[2])
            tr = traces[k][part] if part == "noise" else traces[k][part][amp]
            ax.plot(_time(tr, dt), tr, color=c, lw=0.8, label=out["level"])
            ax.set_title(f"{LABELS[k]} · {title}", fontsize=10)
            ax.set_ylim(-95, 50)
            if part != "noise":
                ax.axvspan(settle, settle + (1 if part == "ladder" else 4), color=c, alpha=0.06)
            if j == 0:
                ax.set_ylabel("mV")
            if overlay is not None and i == 0:
                ax.legend(fontsize=8, loc="upper right")
        ax = axes[3][j]
        amps = [s["amp_nA"] for s in out["cells"][k]["ladder"]]
        counts = [s["count"] for s in out["cells"][k]["ladder"]]
        if overlay is not None and k in overlay[0]:
            ax.plot([s["amp_nA"] for s in overlay[0][k]["ladder"]],
                    [s["count"] for s in overlay[0][k]["ladder"]], "o-", color="0.7", label=overlay[2])
        ax.plot(amps, counts, "o-", color=c, label=out["level"])
        ax.set_ylim(bottom=0, top=max(counts + [2]) * 1.15)
        ax.set_title(f"{LABELS[k]} · spikes in a 1 s step", fontsize=10)
        ax.set_xlabel("injected current (nA)")
        if j == 0:
            ax.set_ylabel("spikes")
        for row in axes[:3]:
            row[j].set_xlabel("s")
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
