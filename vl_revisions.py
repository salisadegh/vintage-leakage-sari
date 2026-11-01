"""RQ1: size and type of post-publication revisions, and the data-quality inclusion rule."""
import numpy as np
import pandas as pd

import config as C

KEY = ["countryname", "age", "week"]


def late_uploads(first):
    """Weeks first published after the first snapshot but more than MAX_FIRST_DELAY weeks late."""
    f = first[(first.age == "total") & (first.d0 > first.d0.min())]
    return f.assign(late=~f.timely).groupby("countryname").late.agg(first_publications="size", late_historical="sum")


def clean_first(vk, first, latest):
    """Timely first reports (published after the first snapshot, within MAX_FIRST_DELAY weeks),
    with first, week-8 and latest values."""
    f0 = vk[(vk.k == 0) & vk.timely][KEY + ["value"]].rename(columns={"value": "v0"})
    v8 = (vk[vk.k.between(C.TRUTH_WEEKS, C.TRUTH_WEEKS + 1)].sort_values("k")
          .groupby(KEY, as_index=False).value.first().rename(columns={"value": "v8"}))
    out = f0.merge(latest.rename(columns={"value": "vlatest"}), on=KEY, how="left")
    return out.merge(v8, on=KEY, how="left")


def revision_summary(cf):
    """Overall revision sizes (first report vs latest) and backfill vs restatement split."""
    d = cf[(cf.v0 > 0) & cf.vlatest.notna()].copy()
    d["rel"] = d.vlatest / d.v0 - 1
    rows = {"clean_first_reports_nonzero": len(d), "countries": d.countryname.nunique()}
    for th in (0.01, 0.05, 0.10, 0.25):
        rows[f"share_abs_rev_gt_{int(th * 100)}pct"] = (d.rel.abs() > th).mean()
    rows["upward_share_of_revised_gt_1pct"] = (d.rel[d.rel.abs() > .01] > 0).mean()
    e = cf[(cf.v0 > 0) & (cf.v8 > 0) & cf.vlatest.notna()].copy()
    e["backfill"] = e.v8 / e.v0 - 1
    e["restatement"] = e.vlatest / e.v8 - 1
    rows["weeks_with_8wk_followup"] = len(e)
    rows["backfill_share_gt_10pct"] = (e.backfill.abs() > .10).mean()
    rows["backfill_upward_share"] = (e.backfill[e.backfill.abs() > .01] > 0).mean()
    rows["backfill_median_when_revised"] = e.backfill[e.backfill.abs() > .01].median()
    rows["restatement_share_gt_10pct"] = (e.restatement.abs() > .10).mean()
    return pd.Series(rows), e


def by_country(cf, e):
    d = cf[(cf.v0 > 0) & cf.vlatest.notna()].assign(rel=lambda x: x.vlatest / x.v0 - 1)
    g1 = d.groupby("countryname").rel.agg(n_clean="size", share_rev_gt_10=lambda s: (s.abs() > .1).mean())
    e = e.assign(ratio=e.v0 / e.v8)
    g2 = e.groupby("countryname").agg(
        backfill_gt_10=("backfill", lambda s: (s.abs() > .1).mean()),
        restatement_gt_10=("restatement", lambda s: (s.abs() > .1).mean()),
        first_over_stable_median=("ratio", "median"),
        first_over_stable_p10=("ratio", lambda s: s.quantile(.1)),
        first_over_stable_q25=("ratio", lambda s: s.quantile(.25)),
        first_over_stable_q75=("ratio", lambda s: s.quantile(.75)),
        share_complete_first=("ratio", lambda s: (s >= .95).mean()),
        share_first_below_half=("ratio", lambda s: (s < .5).mean()))
    z = cf.groupby("countryname").agg(n_first=("v0", "size"), zero_first_share=("v0", lambda s: (s == 0).mean()))
    return g1.join(g2, how="outer").join(z, how="outer")


def convergence(vk, latest):
    """Median and IQR of (as published / latest) by weeks since first report, clean weeks only."""
    d = vk[vk.timely].merge(latest.rename(columns={"value": "vlatest"}), on=KEY)
    d = d[(d.vlatest > 0) & (d.k <= 12)]
    d["ratio"] = d.value / d.vlatest
    return d.groupby("k").ratio.agg(median="median", q25=lambda s: s.quantile(.25),
                                    q75=lambda s: s.quantile(.75), n="size")


def reporting_lag(v):
    lat = v.groupby(["vintage", "countryname"]).week.max().reset_index()
    lag = (lat.vintage - (lat.week + pd.Timedelta(days=6))).dt.days / 7
    return float(lag.median())


def inclusion_rule(v, latest, per_country):
    """Apply the four data-quality criteria; returns a table with the decision per country."""
    med = v[v.value > 0].groupby(["countryname", "vintage"]).value.median()
    shift = med.groupby(level=0).agg(lambda s: s.max() / s.min())
    final_vintage = v.vintage.max()
    last = latest.groupby("countryname").week.max()
    stale = ((final_vintage - last).dt.days / 7)
    t = pd.DataFrame({"level_shift": shift, "weeks_since_last_report": stale})
    t = t.join(per_country[["restatement_gt_10", "zero_first_share"]], how="left")
    t["fail_level_shift"] = t.level_shift >= C.MAX_LEVEL_SHIFT
    t["fail_restatement"] = t.restatement_gt_10.fillna(0) >= C.MAX_RESTATEMENT
    t["fail_zero_first"] = t.zero_first_share.fillna(0) >= C.MAX_ZERO_FIRST
    t["fail_stale"] = t.weeks_since_last_report > C.MAX_STALE_WEEKS
    t["included"] = ~(t.fail_level_shift | t.fail_restatement | t.fail_zero_first | t.fail_stale)
    t["sensitivity_set"] = ~(t.fail_level_shift | t.fail_stale)
    t["nonstale"] = ~t.fail_stale
    return t
