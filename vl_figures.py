"""Figures for the paper (PNG at 300 dpi and PDF)."""
import matplotlib
import matplotlib.ticker

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

GREY, BLUE, INK, QUIET = "#9a9a9a", "#2b6cb0", "#1a1a1a", "#666666"


def _save(fig, path):
    fig.savefig(path + ".png", dpi=300, bbox_inches="tight")
    fig.savefig(path + ".pdf", bbox_inches="tight")
    plt.close(fig)


def gap_by_country(pc, pooled_ratio, path):
    """Dumbbell: retrospective (A) vs real-time (B) error per country, log axis."""
    pc = pc.sort_values("ratio_B_over_A", ascending=True)
    fig, ax = plt.subplots(figsize=(6.5, 0.42 * len(pc) + 1.3))
    y = np.arange(len(pc))
    ax.hlines(y, pc["A_retrospective"], pc["B_realtime"], color="#dddddd", lw=3, zorder=1)
    ax.scatter(pc["A_retrospective"], y, color=GREY, s=36, zorder=2, label="Retrospective (A)")
    ax.scatter(pc["B_realtime"], y, color=BLUE, s=36, zorder=3, label="Real-time (B)")
    ax.set_xscale("log")
    ax.set_yticks(y, pc.index)
    xmax = max(pc["B_realtime"].max(), pc["A_retrospective"].max()) * 1.9
    xmin = min(pc["A_retrospective"].min(), pc["B_realtime"].min()) * 0.7
    ax.set_xlim(xmin, xmax)
    ticks = [t for t in (0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5) if xmin <= t <= xmax]
    ax.set_xticks(ticks, [f"{t:g}" for t in ticks])
    ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    for yi, r in zip(y, pc["ratio_B_over_A"]):
        ax.text(xmax * 0.97, yi, f"×{r:.1f}", va="center", ha="right", fontsize=9,
                color=INK if r >= 2 else QUIET, fontweight="bold" if r >= 2 else "normal")
    ax.set_xlabel("Mean absolute error of the log SARI rate, 1 week ahead (log axis)", fontsize=9, color=QUIET)
    ax.set_title(f"Real-time error is {pooled_ratio:.1f}× the retrospective error", fontsize=11, loc="left")
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color="#eeeeee", zorder=0)
    ax.legend(frameon=False, fontsize=8.5, loc="upper center", bbox_to_anchor=(0.45, -0.16), ncol=2)
    _save(fig, path)


def backfill_shape(e, countries, path, rng_seed=0):
    """First report divided by the value 8 weeks later, one dot per country-week."""
    rng = np.random.default_rng(rng_seed)
    d = e[e.countryname.isin(countries)].assign(ratio=lambda x: (x.v0 / x.v8).clip(upper=1.5))
    order = d.groupby("countryname").ratio.median().sort_values().index
    fig, ax = plt.subplots(figsize=(6.5, 0.42 * len(order) + 1.2))
    for i, c in enumerate(order):
        r = d[d.countryname == c].ratio.values
        ax.scatter(r, i + rng.uniform(-0.18, 0.18, len(r)), s=7, color=BLUE, alpha=0.35, lw=0)
        ax.plot([np.median(r)] * 2, [i - 0.3, i + 0.3], color=INK, lw=1.5)
    ax.axvline(1.0, color=GREY, lw=0.8, ls="--")
    ax.set_yticks(range(len(order)), order)
    ax.set_xlabel("Timely first report / value 8 weeks later (1 = complete at first report)", fontsize=9, color=QUIET)
    ax.set_title("How complete is a week when ECDC first publishes it?", fontsize=11, loc="left")
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(axis="y", length=0)
    _save(fig, path)
