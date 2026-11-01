"""Figure 1 of the paper: completeness of first reports (a) and real-time error relative to
retrospective error per country (b).

Usage:  python make_paper_figure.py --data-dir data --results results
Reads the per-country table written by run_all.py and recomputes first-report completeness.
Countries are ordered by median completeness (least complete at the top) in both panels.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import vl_data  # noqa: E402
import vl_revisions  # noqa: E402

GREY, INK, DOT = "#8c8c8c", "#1a1a1a", "#2a78d6"
ARMS = [("B", "B real time", "#2a78d6", "o", "#2a78d6"),          # key, label, colour, marker, face
        ("C", "C real time + correction", "#eb6834", "D", "white"),
        ("D", "D vintage-trained", "#1baf7a", "^", "#1baf7a")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data")
    ap.add_argument("--results", default="results")
    a = ap.parse_args()
    v, latest = vl_data.load(a.data_dir)
    vk, first = vl_data.first_reports(v)
    vt, lt = vk[vk.age == "total"], latest[latest.age == "total"]
    _, e = vl_revisions.revision_summary(vl_revisions.clean_first(vt, first, lt))
    pc = pd.read_csv(os.path.join(a.results, "tables", "per_country_gbm_h1_all_analyses.csv"))
    pc = pc[pc.analysis == "main"].set_index("countryname")
    e = e[e.countryname.isin(pc.index)].assign(ratio=lambda x: x.v0 / x.v8)
    order = e.groupby("countryname").ratio.median().sort_values().index.tolist()   # least complete first
    e = e.assign(ratio=e.ratio.clip(upper=1.2))

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7, "axes.linewidth": 0.6})
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(4.88, 1.85), sharey=True,
                                   gridspec_kw={"width_ratios": [1, 1.3], "wspace": 0.22})
    rng = np.random.default_rng(0)
    y = np.arange(len(order))
    for i, c in enumerate(order):
        r = e[e.countryname == c].ratio.values
        ax1.scatter(r, i + rng.uniform(-0.22, 0.22, len(r)), s=5, color=DOT, alpha=0.6, lw=0)
        ax1.plot([np.median(r)] * 2, [i - 0.34, i + 0.34], color=INK, lw=1.4)
    ax1.axvline(1, color=GREY, lw=0.6, ls="--")
    ax1.set_xlim(0, 1.2)
    ax1.set_xticks([0, 0.25, 0.5, 0.75, 1], ["0", "0.25", "0.5", "0.75", "1"])
    ax1.set_yticks(y, order)
    ax1.invert_yaxis()
    ax1.set_xlabel("First report ÷ value 8 weeks later")
    ax1.set_title("(a) First-report completeness", loc="left", fontsize=7, fontweight="bold")

    for j, (k, lab, col, mk, face) in enumerate(ARMS):
        yy = y + (j - 1) * 0.25
        r, lo, hi = (pc.loc[order, f"ratio_{k}{s}"].values for s in ("", "_lo", "_hi"))
        ok = pc.loc[order, "ci_reliable"].astype(bool).values      # no interval below MIN_ORIGINS_CI origins
        ax2.hlines(yy[ok], lo[ok], hi[ok], color=col, lw=0.9, zorder=2)
        ax2.scatter(r, yy, s=14, marker=mk, facecolor=face, edgecolor=col, lw=0.9, zorder=3, label=lab)
    ax2.axvline(1, color=GREY, lw=0.6, ls="--", zorder=1)
    ax2.set_xscale("log")
    ax2.set_xlim(0.6, 18)
    ticks = [1, 2, 4, 8, 16]
    ax2.set_xticks(ticks, [f"{t:g}" for t in ticks])
    ax2.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax2.set_xlabel("MAE ÷ MAE of setting A (log axis)")
    ax2.set_title("(b) Real-time / retrospective error", loc="left", fontsize=7, fontweight="bold")
    for ax in (ax1, ax2):
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        ax.tick_params(length=2, width=0.6)
        ax.grid(axis="x", color="#eeeeee", lw=0.5, zorder=0)
    ax2.tick_params(axis="y", length=0)
    h, lab = ax2.get_legend_handles_labels()
    fig.legend(h, lab, frameon=False, fontsize=7, loc="lower center", bbox_to_anchor=(0.5, -0.16), ncol=3,
               handletextpad=0.2, columnspacing=1.2)
    out = os.path.join(a.results, "figures", "fig1_paper")
    fig.savefig(out + ".png", dpi=600, bbox_inches="tight")
    fig.savefig(out + ".pdf", bbox_inches="tight")
    print("wrote", out + ".png/.pdf")


if __name__ == "__main__":
    main()
