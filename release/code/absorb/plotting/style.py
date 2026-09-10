"""Shared matplotlib style for the paper figures.

Serif text at the document's size, 300 dpi, colour-blind-safe palette, no
titles inside the axes (captions carry that information).  Figures are written
as PDF (vector, for the paper) and PNG (for quick inspection).
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt

FIG_DIR = Path(__file__).resolve().parents[3] / "paper" / "figures"

# Column widths of the article class at 11pt, a4paper, 2.5 cm margins.
WIDTH_FULL = 6.3      # inches, = \textwidth
WIDTH_HALF = 3.05     # inches, two side-by-side panels

#: Colour-blind-safe qualitative palette (Okabe & Ito 2008).
COLORS = {
    "model":   "#0072B2",   # blue      - the absorption model
    "lcdm":    "#000000",   # black     - LambdaCDM reference
    "alt":     "#D55E00",   # vermilion - competing parametrization (CPL, RVM)
    "data":    "#009E73",   # green     - measurements
    "accent":  "#CC79A7",   # purple
    "warn":    "#E69F00",   # orange
    "muted":   "#56B4E9",   # sky blue
    "grey":    "#666666",
}
BAND_ALPHA = (0.30, 0.15)   # 68% and 95% credible bands


def setup_style() -> None:
    """Apply the paper style to the global matplotlib state."""
    matplotlib.rcParams.update({
        "figure.dpi": 120,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.03,
        "font.family": "serif",
        "font.serif": ["DejaVu Serif", "Computer Modern Roman", "Times"],
        "mathtext.fontset": "dejavuserif",
        "font.size": 9,
        "axes.labelsize": 10,
        "axes.titlesize": 10,
        "xtick.labelsize": 8.5,
        "ytick.labelsize": 8.5,
        "legend.fontsize": 8.5,
        "legend.frameon": False,
        "axes.grid": True,
        "grid.linestyle": ":",
        "grid.alpha": 0.35,
        "grid.linewidth": 0.6,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 0.8,
        "lines.linewidth": 1.5,
        "errorbar.capsize": 2.0,
        "figure.autolayout": False,
    })


def save_figure(fig, name: str, directory: Path | None = None) -> Path:
    """Write ``name``.pdf and ``name``.png; return the PDF path."""
    directory = Path(directory) if directory is not None else FIG_DIR
    directory.mkdir(parents=True, exist_ok=True)
    pdf = directory / f"{name}.pdf"
    fig.savefig(pdf)
    fig.savefig(directory / f"{name}.png", dpi=150)
    plt.close(fig)
    return pdf
