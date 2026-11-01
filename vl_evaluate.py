"""Scoring: error against the stable truth, circular block bootstrap, rankings, robustness checks.

MAE is averaged over countries within each origin, then over origins. A circular block bootstrap
resamples blocks of BLOCK consecutive origins (wrapping at the end, so every origin has equal weight).
Surge-alert metrics (sensitivity, false-alert rate, AUROC) are in alerts.py, which reuses scored_panel,
attach_truth and _block_samples from this module.
"""
import numpy as np
import pandas as pd

import config as C

A, B, Cc, D = C.ARMS


def attach_truth(pred, truth, age):
    t = truth[truth.age == age][["countryname", "week", "t1", "t2"]]
    p = pred.merge(t.rename(columns={"week": "target_week"}), on=["countryname", "target_week"])
    p["err"] = (p.pred - np.log(p.t2 + C.EPS)).abs()
    p["bias"] = p.pred - np.log(p.t2 + C.EPS)
    p["err_latest"] = (p.pred - np.log(p.t1 + C.EPS)).abs()
    return p.dropna(subset=["t2"])


def scored_panel(p, col="err"):
    """Rows (model, h, origin, country) with all four arms present; persistence D = persistence B."""
    p = p[p.h.isin(C.TRAIN_HORIZONS)]
    pers_d = p[(p.arm == B) & (p.model == "persistence")].assign(arm=D)
    p = pd.concat([p, pers_d], ignore_index=True)
    return p.pivot_table(index=["model", "h", "origin", "countryname"], columns="arm", values=col).dropna()


def _block_samples(n, rng):
    starts = rng.integers(0, n, (C.N_BOOT, int(np.ceil(n / C.BLOCK))))
    idx = ((starts[:, :, None] + np.arange(C.BLOCK)[None, None, :]) % n).reshape(C.N_BOOT, -1)[:, :n]
    return idx


def gap_table(panel, rng):
    by_o = panel.groupby(level=["model", "h", "origin"]).mean()
    rows = []
    for (m, h), g in by_o.groupby(level=["model", "h"]):
        g = g.droplevel(["model", "h"])
        X = g[C.ARMS].values
        idx = _block_samples(len(X), rng)
        boot = X[idx].mean(axis=1)                       # N_BOOT x 4
        pt = X.mean(axis=0)
        rec = {"model": m, "h": h, "n_origins": len(X),
               "n_forecasts": int(panel.loc[(m, h)].shape[0])}
        for i, a in enumerate(C.ARMS):
            rec[f"MAE_{a[0]}"] = pt[i]
        for i, a in enumerate(C.ARMS[1:], start=1):
            r = 100 * (boot[:, i] / boot[:, 0] - 1)
            rec[f"{a[0]}_excess_pct"] = 100 * (pt[i] / pt[0] - 1)
            rec[f"{a[0]}_lo"], rec[f"{a[0]}_hi"] = np.quantile(r, [.025, .975])
        gap_pt, gap_bs = pt[1] - pt[0], boot[:, 1] - boot[:, 0]
        for i, a in ((2, "C"), (3, "D")):
            rec[f"gap_closed_{a}_pct"] = 100 * (pt[1] - pt[i]) / gap_pt
            cl = 100 * (boot[:, 1] - boot[:, i]) / gap_bs
            rec[f"gap_closed_{a}_lo"], rec[f"gap_closed_{a}_hi"] = np.quantile(cl, [.025, .975])
        rows.append(rec)
    return pd.DataFrame(rows)


def per_country(panel, model="gbm", h=1):
    pc = panel.loc[(model, h)].groupby(level="countryname").mean()
    for a in C.ARMS[1:]:
        pc[f"{a[0]}_excess_pct"] = 100 * (pc[a] / pc[A] - 1)
    pc["ratio_B_over_A"] = pc[B] / pc[A]
    pc["ratio_C_over_A"] = pc[Cc] / pc[A]
    return pc.sort_values("ratio_B_over_A", ascending=False)


def leave_one_out(panel, model="gbm", h=1):
    """Pooled excess error of B and C over A when each country is left out in turn."""
    g = panel.loc[(model, h)]
    rows = []
    for c in sorted(g.index.get_level_values("countryname").unique()):
        k = g[g.index.get_level_values("countryname") != c].groupby(level="origin").mean().mean()
        rows.append({"left_out": c, "B_excess_pct": 100 * (k[B] / k[A] - 1), "C_excess_pct": 100 * (k[Cc] / k[A] - 1),
                     "gap_closed_C_pct": 100 * (k[B] - k[Cc]) / (k[B] - k[A])})
    return pd.DataFrame(rows)


def _pooled(g):
    """Origin-averaged MAE per arm from a (origin, country) x arm panel slice."""
    return g.groupby(level="origin").mean().mean()


def country_cluster(panel, rng, model="gbm", h=1):
    """Treat countries as the sampling unit: resample countries with replacement (N_BOOT times)
    and recompute the pooled excess error of B, C and D over A and the share of the gap closed."""
    g = panel.loc[(model, h)]
    cs = np.array(sorted(g.index.get_level_values("countryname").unique()))
    by_c = {c: g[g.index.get_level_values("countryname") == c] for c in cs}
    rec = []
    for _ in range(C.N_BOOT):
        pick = rng.choice(cs, len(cs), replace=True)
        parts = [by_c[c].assign(_rep=i).set_index("_rep", append=True) for i, c in enumerate(pick)]
        k = pd.concat(parts).groupby(level="origin").mean().mean()
        rec.append([100 * (k[B] / k[A] - 1), 100 * (k[Cc] / k[A] - 1), 100 * (k[D] / k[A] - 1),
                    100 * (k[B] - k[Cc]) / (k[B] - k[A]) if k[B] != k[A] else np.nan])
    r = np.array(rec)
    q = np.nanquantile(r, [.025, .975], axis=0)
    return pd.DataFrame({"quantity": ["B_excess_pct", "C_excess_pct", "D_excess_pct", "gap_closed_C_pct"],
                         "lo": q[0], "hi": q[1]})


def leave_set_out(panel, rng, drop, model="gbm", h=1):
    """Pooled excess (origin block bootstrap CI) with a set of countries removed from scoring."""
    g = panel.loc[(model, h)]
    g = g[~g.index.get_level_values("countryname").isin(drop)]
    X = g.groupby(level="origin").mean()[C.ARMS].values
    idx = _block_samples(len(X), rng)
    boot, pt = X[idx].mean(axis=1), X.mean(axis=0)
    out = {"dropped": "+".join(drop), "n_origins": len(X)}
    for i, a in enumerate(C.ARMS[1:], start=1):
        out[f"{a[0]}_excess_pct"] = 100 * (pt[i] / pt[0] - 1)
        out[f"{a[0]}_lo"], out[f"{a[0]}_hi"] = np.quantile(100 * (boot[:, i] / boot[:, 0] - 1), [.025, .975])
    out["gap_closed_C_pct"] = 100 * (pt[1] - pt[2]) / (pt[1] - pt[0])
    return out


def per_country_ci(panel, rng, model="gbm", h=1):
    """Per-country error ratios to A with block-bootstrap CIs over that country's origins."""
    g = panel.loc[(model, h)]
    rows = []
    for c in sorted(g.index.get_level_values("countryname").unique()):
        X = g[g.index.get_level_values("countryname") == c][C.ARMS].values
        n = len(X)
        rec = {"countryname": c, "n_origins": n, "ci_reliable": n >= C.MIN_ORIGINS_CI}
        idx = _block_samples(n, rng)
        boot, pt = X[idx].mean(axis=1), X.mean(axis=0)
        for i, a in enumerate(C.ARMS[1:], start=1):
            rec[f"ratio_{a[0]}"] = pt[i] / pt[0]
            rec[f"ratio_{a[0]}_lo"], rec[f"ratio_{a[0]}_hi"] = np.quantile(boot[:, i] / boot[:, 0], [.025, .975])
        rows.append(rec)
    return pd.DataFrame(rows).set_index("countryname")


def gap_share(panel, model="gbm", h=1):
    """Each country's share of the pooled B-A gap, using the same weights as the pooled MAE
    (countries averaged within an origin, then origins averaged)."""
    g = panel.loc[(model, h)]
    d = (g[B] - g[A]).to_frame("d")
    n = d.groupby(level="origin").d.transform("size")
    w = (d.d / n) / d.index.get_level_values("origin").nunique()
    return w.groupby(level="countryname").sum() / w.sum()


def publication_week_share(p):
    """Share of scored 1-week forecasts whose target ISO week contains the origin (publication) date."""
    q = p[(p.h == 1) & (p.arm == B) & (p.model == "gbm")]
    t, o = q.target_week.dt.isocalendar(), q.origin.dt.isocalendar()
    same = pd.Series((t.week.values == o.week.values) & (t.year.values == o.year.values), index=q.index)
    return float(same.mean()), same.groupby(q.countryname).mean()


def bias_table(p, panel_index):
    q = p[p.h.isin(C.TRAIN_HORIZONS)].set_index(["model", "h", "origin", "countryname"])
    q = q[q.index.isin(panel_index)]
    return q.groupby(["model", "h", "arm"]).bias.mean().unstack()


def rankings(panel, rng):
    by_o = panel.groupby(level=["model", "h", "origin"]).mean()
    rows = []
    for h in C.TRAIN_HORIZONS:
        mats = {m: by_o.loc[(m, h)] for m in C.MODELS}
        origins = mats["gbm"].index
        mats = {m: x.reindex(origins) for m, x in mats.items()}
        idx = _block_samples(len(origins), rng)
        for a in C.ARMS:
            means = {m: mats[m][a].mean() for m in C.MODELS}
            order = sorted(means, key=means.get)
            rows.append({"h": h, "arm": a, "order": " < ".join(order),
                         **{f"MAE_{m}": means[m] for m in C.MODELS}})
        best = {}
        for a in (A, B):
            M = np.stack([mats[m][a].values for m in C.MODELS], axis=1)  # origins x models
            bm = np.nanmean(M[idx], axis=1)                               # N_BOOT x models
            best[a] = bm.argmin(axis=1)
        rows.append({"h": h, "arm": "P(leader under A differs from leader under B)",
                     "order": f"{(best[A] != best[B]).mean():.3f}"})
    return pd.DataFrame(rows)


def evaluate(pred, truth, age, seed=C.SEED):
    rng = np.random.default_rng(seed)
    p = attach_truth(pred, truth, age)
    panel = scored_panel(p)
    out = {"scored": p, "panel": panel, "gap": gap_table(panel, rng), "per_country": per_country(panel),
           "bias": bias_table(p, panel.index), "rankings": rankings(panel, rng),
           "leave_one_out": leave_one_out(panel)}
    # robustness: score every arm against the latest file instead of the week-8 value
    out["gap_latest_truth"] = gap_table(scored_panel(p, "err_latest"), np.random.default_rng(seed + 1))
    out["per_country_ci"] = per_country_ci(panel, np.random.default_rng(seed + 2))
    out["gap_share"] = gap_share(panel)
    out["country_cluster"] = country_cluster(panel, np.random.default_rng(seed + 3))
    out["pub_week_share"], out["pub_week_share_by_country"] = publication_week_share(p[p.set_index(
        ["model", "h", "origin", "countryname"]).index.isin(panel.index)])
    d = p[(p.model == "gbm") & (p.h == 1)]
    out["n_train"] = d.groupby(["arm", "origin"]).n_train.first().unstack(0)
    out["n_dropped"] = d.groupby(["arm", "origin"]).n_dropped.first().unstack(0)
    q = p[p.set_index(["model", "h", "origin", "countryname"]).index.isin(panel.index)]
    out["bias_by_country"] = q[(q.model == "gbm") & (q.h == 1)].groupby(["countryname", "arm"]).bias.mean().unstack()
    return out
