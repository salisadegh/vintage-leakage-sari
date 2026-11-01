"""Run every analysis from the pinned data and write tables, figures and a summary.

Usage:  python run_all.py --data-dir data --out results [--jobs 2]
Optional: --first-delay N (timely-report threshold, weeks), --eps X (log offset), --max-restatement X
(inclusion threshold) and --only main,age_65plus (subset of analyses). Sensitivity runs write to their own --out.

This script computes forecast errors (MAE, excess error, gap closed, bias, bootstrap intervals). Surge-alert
metrics (sensitivity, false-alert rate, AUROC) are computed from its saved forecasts by alerts.py, and the
forecast-horizon audit by horizon_audit.py. reproduce.py runs every step in order.
"""
import argparse
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

# One thread per process: avoids oversubscription when analyses run in parallel,
# and keeps gradient-boosting results identical across machines.
os.environ.setdefault("OMP_NUM_THREADS", "1")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import config as C  # noqa: E402
import vl_data  # noqa: E402
import vl_evaluate  # noqa: E402
import vl_figures  # noqa: E402
import vl_forecast  # noqa: E402
import vl_revisions  # noqa: E402

ANALYSES = [  # name, country set, age group, truth window (weeks)
    ("main", "included", "total", 8),
    ("age_65plus", "included", "65+", 8),
    ("age_0to4", "included", "0-4", 8),
    ("truth_12wk", "included", "total", 12),
    ("all_series", "sensitivity_set", "total", 8),
    ("with_scale_breaks", "nonstale", "total", 8),
]


def run_one(args):
    name, countries, age, kmax, data_dir, first_delay, eps = args
    C.MAX_FIRST_DELAY = first_delay   # set inside each worker (spawned processes re-import config)
    C.EPS = eps
    v, latest = vl_data.load(data_dir)
    vk, _ = vl_data.first_reports(v)
    truth = vl_data.truth_table(vk, latest, kmax)
    pred = vl_forecast.run_arms(vk, latest, countries, age, kmax)
    ev = vl_evaluate.evaluate(pred, truth, age)
    return name, pred, ev


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data")
    ap.add_argument("--out", default="results")
    ap.add_argument("--jobs", type=int, default=1)
    ap.add_argument("--first-delay", type=int, default=C.MAX_FIRST_DELAY)
    ap.add_argument("--eps", type=float, default=C.EPS)
    ap.add_argument("--max-restatement", type=float, default=C.MAX_RESTATEMENT)
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    C.MAX_FIRST_DELAY, C.EPS, C.MAX_RESTATEMENT = a.first_delay, a.eps, a.max_restatement
    t0 = time.time()
    here = os.path.dirname(os.path.abspath(__file__))
    n = vl_data.verify(a.data_dir, os.path.join(here, C.MANIFEST))
    print(f"Verified {n} files against the manifest (commit {C.COMMIT[:7]}).")
    tab, fig = os.path.join(a.out, "tables"), os.path.join(a.out, "figures")
    os.makedirs(tab, exist_ok=True)
    os.makedirs(fig, exist_ok=True)

    # RQ1: revisions and inclusion rule (all-age series)
    v, latest = vl_data.load(a.data_dir)
    vk, first = vl_data.first_reports(v)
    vt, lt = vk[vk.age == "total"], latest[latest.age == "total"]
    cf = vl_revisions.clean_first(vt, first, lt)
    summ, e = vl_revisions.revision_summary(cf)
    summ = summ.astype(object)  # holds numbers and date strings
    pcr = vl_revisions.by_country(cf, e)
    rule = vl_revisions.inclusion_rule(vt, lt, pcr)
    conv = vl_revisions.convergence(vt, lt)
    late = vl_revisions.late_uploads(first)
    late.to_csv(os.path.join(tab, "rq1_late_historical_uploads.csv"))
    summ["first_publications_after_first_snapshot"] = int(late.first_publications.sum())
    summ["late_historical_uploads"] = int(late.late_historical.sum())
    summ["reporting_lag_median_weeks"] = vl_revisions.reporting_lag(vt)
    summ["n_vintages"] = v.vintage.nunique()
    summ["first_vintage"], summ["last_vintage"] = str(v.vintage.min().date()), str(v.vintage.max().date())
    summ.to_csv(os.path.join(tab, "rq1_revision_summary.csv"), header=["value"])
    pcr.to_csv(os.path.join(tab, "rq1_revisions_by_country.csv"))
    conv.to_csv(os.path.join(tab, "rq1_convergence_by_report_age.csv"))
    rule.to_csv(os.path.join(tab, "inclusion_rule.csv"))
    sets = {"included": sorted(rule.index[rule.included]), "sensitivity_set": sorted(rule.index[rule.sensitivity_set]),
            "nonstale": sorted(rule.index[rule.nonstale])}
    print("Included:", ", ".join(sets["included"]))
    print("Sensitivity set:", ", ".join(sets["sensitivity_set"]))
    print("Non-stale (incl. scale breaks):", ", ".join(sets["nonstale"]))
    vl_figures.backfill_shape(e, sets["included"], os.path.join(fig, "fig_backfill_shape"))

    # RQ2-RQ3: forecasting under arms A-D
    only = set(filter(None, a.only.split(",")))
    jobs = [(nm, sets[s], age, k, a.data_dir, a.first_delay, a.eps) for nm, s, age, k in ANALYSES
            if not only or nm in only]
    results = {}
    if not jobs:
        return
    if a.jobs > 1:
        with ProcessPoolExecutor(max_workers=a.jobs) as ex:
            for nm, pred, ev in ex.map(run_one, jobs):
                results[nm] = (pred, ev)
                print(f"  finished {nm}")
    else:
        for j in jobs:
            nm, pred, ev = run_one(j)
            results[nm] = (pred, ev)
            print(f"  finished {nm}")

    gaps, gaps_lt, pcs = [], [], []
    for nm, (pred, ev) in results.items():
        pred.to_csv(os.path.join(a.out, f"predictions_{nm}.csv.gz"), index=False)
        gaps.append(ev["gap"].assign(analysis=nm))
        gaps_lt.append(ev["gap_latest_truth"].assign(analysis=nm))
        pcs.append(ev["per_country"].join(ev["per_country_ci"].drop(columns="n_origins")).assign(analysis=nm))
        if nm == "main":
            ev["bias"].to_csv(os.path.join(tab, "main_bias_by_arm.csv"))
            ev["rankings"].to_csv(os.path.join(tab, "main_model_rankings.csv"), index=False)
            ev["leave_one_out"].to_csv(os.path.join(tab, "main_leave_one_country_out.csv"), index=False)
            ev["gap_latest_truth"].to_csv(os.path.join(tab, "main_gap_latest_file_truth.csv"), index=False)
            ev["country_cluster"].to_csv(os.path.join(tab, "main_country_cluster_bootstrap.csv"), index=False)
            ev["n_train"].to_csv(os.path.join(tab, "main_training_rows_by_origin.csv"))
            ev["n_dropped"].to_csv(os.path.join(tab, "main_screened_training_pairs_by_origin.csv"))
            ev["bias_by_country"].to_csv(os.path.join(tab, "main_bias_by_country_gbm_h1.csv"))
            ev["gap_share"].to_csv(os.path.join(tab, "main_gap_share_by_country.csv"), header=["share"])
            ev["drop_two"] = vl_evaluate.leave_set_out(ev["panel"], np.random.default_rng(C.SEED + 4),
                                                       ["Estonia", "Austria"])
            pd.Series(ev["drop_two"]).to_csv(os.path.join(tab, "main_without_estonia_austria.csv"), header=["value"])
    pd.concat(gaps_lt, ignore_index=True).to_csv(os.path.join(tab, "gap_by_arm_latest_file_truth_all_analyses.csv"),
                                                 index=False)
    gaps_lt = pd.concat(gaps_lt, ignore_index=True)
    gaps = pd.concat(gaps, ignore_index=True)
    pcs = pd.concat(pcs)
    gaps.to_csv(os.path.join(tab, "gap_by_arm_all_analyses.csv"), index=False)
    pcs.to_csv(os.path.join(tab, "per_country_gbm_h1_all_analyses.csv"))

    if "main" not in results:
        print(f"Done in {time.time() - t0:.0f} s (no main analysis requested).")
        return
    main_ev = results["main"][1]
    g = main_ev["gap"].set_index(["model", "h"])
    pooled = g.loc[("gbm", 1), "MAE_B"] / g.loc[("gbm", 1), "MAE_A"]
    vl_figures.gap_by_country(main_ev["per_country"], pooled, os.path.join(fig, "fig_gap_by_country"))
    extra = context_stats(v, e, sets, pcr, main_ev)
    write_summary(a.out, summ, rule, sets, gaps, gaps_lt, main_ev, conv, a, extra)
    print(f"Done in {time.time() - t0:.0f} s. See {os.path.join(a.out, 'summary.md')}")


def context_stats(v, e, sets, pcr, ev):
    """Snapshot spacing, post-week-8 restatement in the scored countries, completeness vs gap."""
    vint = pd.Series(sorted(v.vintage.unique()))
    gaps = vint.diff().dt.days.dropna().astype(int).value_counts().sort_index()
    inc = e[e.countryname.isin(sets["included"])]
    gr = ~e.countryname.isin(["Greece", "Latvia"])
    pc = ev["per_country"]
    comp = pcr.loc[pc.index, "first_over_stable_median"]
    rho = pd.Series(comp.values).corr(pd.Series(pc["ratio_B_over_A"].values), method="spearman")
    return {"snapshot_spacing_days": ", ".join(f"{d} d x{n}" for d, n in gaps.items()),
            "restatement_gt10_included": f"{(inc.restatement.abs() > .10).mean():.3f} of {len(inc)} weeks",
            "restatement_gt10_without_gr_lv": f"{(e[gr].restatement.abs() > .10).mean():.3f} of {gr.sum()} weeks",
            "spearman_completeness_vs_B_over_A": f"{rho:.2f} ({len(pc)} countries)",
            "last_origin_scored": str(ev["panel"].index.get_level_values("origin").max().date()),
            "origins_scored_before_2026-03-21": int((ev["panel"].loc[("gbm", 1)].index.get_level_values("origin")
                                                     .unique() < pd.Timestamp("2026-03-21")).sum())}


def _ci(r, arm):
    return f"{r[f'{arm}_excess_pct']:+.0f}% (95% CI {r[f'{arm}_lo']:.0f} to {r[f'{arm}_hi']:.0f})"


def write_summary(out, summ, rule, sets, gaps, gaps_lt, ev, conv, a, extra):
    L = ["# Results summary", "", f"Data: {C.REPO} @ {C.COMMIT}",
         f"Timely first report: within {a.first_delay} weeks; log offset {a.eps}; "
         f"restatement threshold {a.max_restatement}", ""]
    L += ["## RQ1 revisions (all ages, clean first reports)", ""]
    for k in ["n_vintages", "first_vintage", "last_vintage", "first_publications_after_first_snapshot",
              "late_historical_uploads", "clean_first_reports_nonzero", "countries",
              "share_abs_rev_gt_10pct", "upward_share_of_revised_gt_1pct", "weeks_with_8wk_followup",
              "backfill_share_gt_10pct", "backfill_upward_share", "backfill_median_when_revised",
              "restatement_share_gt_10pct", "reporting_lag_median_weeks"]:
        val = summ[k]
        if isinstance(val, (float, np.floating)) and not float(val).is_integer():
            L.append(f"- {k}: {val:.3f}")
        else:
            L.append(f"- {k}: {int(val) if isinstance(val, (float, np.floating)) else val}")
    L.append(f"- convergence: IQR at week 8 = [{conv.loc[8, 'q25']:.3f}, {conv.loc[8, 'q75']:.3f}]")
    L += ["", "## Inclusion rule", "", f"- Included ({len(sets['included'])}): {', '.join(sets['included'])}",
          f"- Sensitivity set ({len(sets['sensitivity_set'])}): {', '.join(sets['sensitivity_set'])}",
          f"- Non-stale incl. scale breaks ({len(sets['nonstale'])}): {', '.join(sets['nonstale'])}", ""]
    for c, r in rule.iterrows():
        why = [w for w, f in [("level shift", r.fail_level_shift), ("restatement", r.fail_restatement),
                              ("zero first reports", r.fail_zero_first), ("stale", r.fail_stale)] if f]
        L.append(f"- {c}: {'included' if r.included else 'excluded (' + ', '.join(why) + ')'}")
    L += ["", "## Context", ""] + [f"- {k}: {val}" for k, val in extra.items()]
    L += ["", "## Leakage gap by analysis (circular block bootstrap over origins)", ""]
    for nm, gg in gaps.groupby("analysis", sort=False):
        L.append(f"### {nm}")
        for r in gg.to_dict("records"):
            L.append(f"- {r['model']} h={r['h']} (origins {r['n_origins']}, forecasts {r['n_forecasts']}): "
                     f"MAE A {r['MAE_A']:.3f}, B {r['MAE_B']:.3f}, C {r['MAE_C']:.3f}, D {r['MAE_D']:.3f}; "
                     f"B {_ci(r, 'B')}; C {_ci(r, 'C')}; D {_ci(r, 'D')}; "
                     f"gap closed C {r['gap_closed_C_pct']:.0f}% ({r['gap_closed_C_lo']:.0f} to {r['gap_closed_C_hi']:.0f}), "
                     f"D {r['gap_closed_D_pct']:.0f}% ({r['gap_closed_D_lo']:.0f} to {r['gap_closed_D_hi']:.0f})")
        L.append("")
    L += ["## Scored against the latest file (all analyses)", ""]
    for nm, gg in gaps_lt.groupby("analysis", sort=False):
        for r in gg[gg.model == "gbm"].to_dict("records"):
            L.append(f"- {nm} gbm h={r['h']}: MAE A {r['MAE_A']:.3f}, B {r['MAE_B']:.3f}, C {r['MAE_C']:.3f}; "
                     f"B {_ci(r, 'B')}; C {_ci(r, 'C')}; gap closed C {r['gap_closed_C_pct']:.0f}% "
                     f"({r['gap_closed_C_lo']:.0f} to {r['gap_closed_C_hi']:.0f})")
    L.append("")
    pc = ev["per_country"].join(ev["per_country_ci"].drop(columns="n_origins"))
    L += ["## Main analysis detail", "", "Per country (gbm, 1 week; ratio to A with 95% block-bootstrap CI over that country's origins):"]
    for c, r in pc.iterrows():
        L.append(f"- {c} ({ev['per_country_ci'].loc[c, 'n_origins']} origins): A {r['A_retrospective']:.3f}, "
                 f"B {r['B_realtime']:.3f} x{r['ratio_B']:.2f} ({r['ratio_B_lo']:.2f}-{r['ratio_B_hi']:.2f}), "
                 f"C x{r['ratio_C']:.2f} ({r['ratio_C_lo']:.2f}-{r['ratio_C_hi']:.2f}), "
                 f"D x{r['ratio_D']:.2f} ({r['ratio_D_lo']:.2f}-{r['ratio_D_hi']:.2f})")
    cc = ev["country_cluster"].set_index("quantity")
    L += ["", "Country-cluster bootstrap (countries resampled; gbm, 1 week): " + "; ".join(
        f"{q} {r.lo:.0f} to {r.hi:.0f}" for q, r in cc.iterrows())]
    gs = ev["gap_share"]
    L.append("Share of the pooled B-A gap (origin-averaged MAE) by country: "
             + ", ".join(f"{c} {100 * x:.1f}%" for c, x in gs.sort_values(ascending=False).items()))
    d2 = ev["drop_two"]
    L.append(f"Without Estonia and Austria ({d2['n_origins']} origins): B {d2['B_excess_pct']:+.0f}% "
             f"({d2['B_lo']:.0f} to {d2['B_hi']:.0f}), C {d2['C_excess_pct']:+.0f}% ({d2['C_lo']:.0f} to {d2['C_hi']:.0f}), "
             f"D {d2['D_excess_pct']:+.0f}% ({d2['D_lo']:.0f} to {d2['D_hi']:.0f}); gap closed C {d2['gap_closed_C_pct']:.0f}%")
    L.append(f"1-week targets in the ISO week of publication: {ev['pub_week_share']:.3f}; by country: "
             + ", ".join(f"{c} {x:.2f}" for c, x in ev["pub_week_share_by_country"].items()))
    nt = ev["n_train"]
    scored = ev["panel"].loc[("gbm", 1)].index.get_level_values("origin").unique()
    L.append("Training rows (gbm) at first / median / last scored origin: " + "; ".join(
        f"{c[0]} {int(nt[c].dropna().iloc[0])} / {int(nt[c].median())} / {int(nt[c].reindex(scored).dropna().iloc[-1])}"
        for c in nt.columns))
    L.append("Training pairs dropped by the gross-error screen (max over origins): " + "; ".join(
        f"{c[0]} {int(ev['n_dropped'][c].max())}" for c in ev["n_dropped"].columns))
    bc = ev["bias_by_country"]
    L.append("Bias by country (gbm, 1 week; mean log error): " + "; ".join(
        f"{c}: " + ", ".join(f"{a[0]} {bc.loc[c, a]:+.2f}" for a in bc.columns) for c in bc.index))
    L.append(f"- median per-country excess B {pc['B_excess_pct'].median():.0f}%, C {pc['C_excess_pct'].median():.0f}%, "
             f"D {pc['D_excess_pct'].median():.0f}%; countries with B excess >10%: {(pc['B_excess_pct'] > 10).sum()} of {len(pc)}")
    lo = ev["leave_one_out"]
    L += ["", "Leave one country out (gbm, 1 week):", "", lo.round(1).to_string(index=False), "",
          "Scored against the latest file instead of the week-8 value (gbm/ridge/persistence):", ""]
    for r in ev["gap_latest_truth"].to_dict("records"):
        L.append(f"- {r['model']} h={r['h']}: MAE A {r['MAE_A']:.3f}, B {r['MAE_B']:.3f}, C {r['MAE_C']:.3f}; "
                 f"B {_ci(r, 'B')}; C {_ci(r, 'C')}")
    L += ["", "Bias (log) by arm:", "", ev["bias"].round(3).to_string(), "", "Rankings:", "",
          ev["rankings"].to_string(index=False), ""]
    with open(os.path.join(out, "summary.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L))


if __name__ == "__main__":
    main()
