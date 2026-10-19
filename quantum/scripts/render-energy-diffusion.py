#!/usr/bin/env python3
"""Render responsive energy-diffusion plots from Kalra et al. (2023), Table S5.

Source: Kalra et al., “Electronic Energy Migration in Microtubules,” ACS Central
Science 9 (2023), DOI: 10.1021/acscentsci.2c01114, Supplementary Information,
Table S5. Values are the reported estimated diffusion lengths (nm) and
propagated errors for isolated 13-protofilament microtubules, and the same
microtubules with 50 μM etomidate or isoflurane. The errors are reported
propagated errors, not confidence intervals.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parents[1] / "assets"

# Table S5: estimated energy-diffusion length, not directly tracked travel or
# coherence length. No values are derived or altered here.
LABELS = ["Microtubules", "+ etomidate", "+ isoflurane"]
VALUES = [6.64, 5.61, 5.81]
ERRORS = [0.10, 0.10, 0.20]
VALUE_LABELS = ["6.64 ± 0.10", "5.61 ± 0.10", "5.81 ± 0.20"]

BG = "#111411"
FG = "#efeee7"
MUTED = "#a7ada1"
AMBER = "#deb97f"
GRID = "#33382f"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Liberation Sans", "DejaVu Sans"],
    "font.size": 10,
    "text.color": FG,
    "axes.labelcolor": MUTED,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "svg.fonttype": "none",  # Keep labels selectable in SVG output.
    "savefig.facecolor": BG,
})


def style_axis(ax):
    ax.set_facecolor(BG)
    ax.set_xlim(0, 8)
    ax.set_xticks([0, 2, 4, 6, 8])
    ax.set_ylim(-0.5, 2.5)
    ax.set_yticks([])
    ax.grid(axis="x", color=GRID, linewidth=0.65, zorder=0)
    ax.tick_params(axis="x", labelsize=9.5, length=0, pad=7)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.errorbar(
        VALUES, [2, 1, 0], xerr=ERRORS, fmt="o",
        color=AMBER, ecolor=AMBER, markersize=6.2,
        elinewidth=1.5, capsize=4, capthick=1.4, zorder=3,
    )


def render_desktop():
    fig = plt.figure(figsize=(6.8, 3.0), dpi=100, facecolor=BG)
    ax = fig.add_axes([0.30, 0.235, 0.54, 0.58])
    style_axis(ax)

    # Stable label and value columns keep the actual readings easy to scan.
    for label, value, y in zip(LABELS, VALUE_LABELS, [2, 1, 0]):
        ax.text(-0.48, y, label, transform=ax.get_yaxis_transform(),
                ha="left", va="center", color=MUTED, fontsize=9.8,
                clip_on=False)
        ax.text(8.16, y, value, ha="left", va="center", color=FG,
                fontsize=9.5, clip_on=False)

    fig.text(0.04, 0.925, "Estimated energy-diffusion length",
             ha="left", va="center", color=FG, fontsize=12)
    fig.text(0.57, 0.105, "Nanometers", ha="center", va="center",
             color=MUTED, fontsize=9.5)
    fig.text(0.04, 0.035,
             "Anesthetics: 50 μM · reported propagated error",
             ha="left", va="center", color=MUTED, fontsize=8.9)
    fig.savefig(OUT / "energy-diffusion.svg", format="svg", transparent=False)
    fig.savefig(OUT / "energy-diffusion.png", format="png", dpi=160,
                transparent=False)
    plt.close(fig)


def render_mobile():
    fig = plt.figure(figsize=(3.46, 3.9), dpi=100, facecolor=BG)
    ax = fig.add_axes([0.085, 0.205, 0.83, 0.605])
    style_axis(ax)

    # Each label/value pair gets a dedicated band above its whisker row.
    for label, value, y in zip(LABELS, VALUE_LABELS, [2, 1, 0]):
        ax.text(0, y + 0.29, label, ha="left", va="center",
                color=MUTED, fontsize=9.5, clip_on=False)
        ax.text(8, y + 0.29, value, ha="right", va="center",
                color=FG, fontsize=9.5, clip_on=False)

    fig.text(0.06, 0.94, "Estimated energy-diffusion length",
             ha="left", va="center", color=FG, fontsize=10.5)
    fig.text(0.50, 0.105, "Nanometers", ha="center", va="center",
             color=MUTED, fontsize=9.5)
    fig.text(0.06, 0.035,
             "Anesthetics: 50 μM · reported propagated error",
             ha="left", va="center", color=MUTED, fontsize=8.2)
    fig.savefig(OUT / "energy-diffusion-mobile.svg", format="svg",
                transparent=False)
    plt.close(fig)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    render_desktop()
    render_mobile()
