"""Surge alerts: does retrospective evaluation overstate how many high-activity weeks a forecast would flag?

Usage:  python alerts.py --data-dir data --results results [--quantile 0.9]
Reads results/predictions_main.csv.gz written by run_all.py; writes results/tables/main_alerts.csv and
results/alerts_summary.md.

Definitions (config.py, fixed before results were seen):
- threshold T(country, origin): the ALERT_QUANTILE of the country's all-age values in the ALERT_WINDOW weeks
  starting at least ALERT_LAG weeks before the origin, as published in the snapshot of the origin (no look-ahead);
- high-activity week: the week-8 value (the truth used throughout) of the target week exceeds T;
- alert: the forecast, back-transformed from log(rate + EPS), exceeds T.
Sensitivity = alerts among high-activity weeks; false-alert rate = alerts among other weeks; AUROC uses
log(forecast + EPS) - log(T + EPS) as the score. CIs: circular block bootstrap over origins.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from sklearn.metrics import roc_auc_score  # noqa: E402

import config as C  # noqa: E402
import vl_data  # noqa: E402
import vl_evaluate  # noqa: E402


def thresholds(vk, origins, countries):
    rows = []
    for o in origins:
        snap = vk[(vk.vintage == o) & (vk.age == "total") & vk.countryname.isin(countries)]
        hi = o - pd.Timedelta(weeks=C.ALERT_LAG)
        lo = hi - pd.Timedelta(weeks=C.ALERT_WINDOW)
        w = snap[(snap.week > lo) & (snap.week <= hi)]
        for c, g in w.groupby("countryname"):
            if len(g) >= C.ALERT_MIN_WEEKS:
                rows.append({"origin": o, "countryname": c, "T": g.value.quantile(C.ALERT_QUANTILE)})
    return pd.DataFrame(rows)


def metrics(d, arms):
    out = {}
    ev = d.event.values
    for a in arms:
        al = d[f"alert_{a}"].values
        out[f"sens_{a}"] = al[ev].mean() if ev.any() else np.nan
        out[f"far_{a}"] = al[~ev].mean() if (~ev).any() else np.nan
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data")
    ap.add_argument("--results", default="results")
    ap.add_argument("--quantile", type=float, default=C.ALERT_QUANTILE,
                    help="threshold quantile; values other than the default write to results/sensitivity/")
    a = ap.parse_args()
    out = a.results
    if a.quantile != C.ALERT_QUANTILE:
        out = os.path.join(a.results, "sensitivity", f"alerts_q{round(100 * a.quantile)}")
        C.ALERT_QUANTILE = a.quantile
    v, latest = vl_data.load(a.data_dir)
    vk, _ = vl_data.first_reports(v)
    truth = vl_data.truth_table(vk, latest, C.TRUTH_WEEKS)
    pred = pd.read_csv(os.path.join(a.results, "predictions_main.csv.gz"),
                       parse_dates=["origin", "target_week", "ow"])
    p = vl_evaluate.attach_truth(pred, truth, "total")
    fc = vl_evaluate.scored_panel(p, "pred")              # forecasts (log scale) by arm, rows with all arms
    t2 = p.drop_duplicates(["model", "h", "origin", "countryname"]).set_index(
        ["model", "h", "origin", "countryname"]).t2
    fc = fc.join(t2, how="left")
    th = thresholds(vk, fc.index.get_level_values("origin").unique(),
                    fc.index.get_level_values("countryname").unique())
    fc = fc.reset_index().merge(th, on=["origin", "countryname"], how="inner")
    fc["event"] = fc.t2 > fc["T"]
    arms = C.ARMS
    for arm in arms:
        fc[f"alert_{arm}"] = (np.exp(fc[arm]) - C.EPS) > fc["T"]
        fc[f"score_{arm}"] = fc[arm] - np.log(fc["T"] + C.EPS)

    rng = np.random.default_rng(C.SEED + 5)
    rows = []
    for (m, h), d in fc.groupby(["model", "h"]):
        rec = {"model": m, "h": h, "n": len(d), "events": int(d.event.sum()),
               "origins": d.origin.nunique()}
        rec.update(metrics(d, arms))
        for arm in arms:
            rec[f"auroc_{arm}"] = roc_auc_score(d.event, d[f"score_{arm}"]) if d.event.nunique() == 2 else np.nan
        origins = np.array(sorted(d.origin.unique()))
        by_o = {o: g for o, g in d.groupby("origin")}
        idx = vl_evaluate._block_samples(len(origins), rng)
        boot = []
        for b in idx:
            bd = pd.concat([by_o[origins[i]] for i in b], ignore_index=True)
            boot.append(metrics(bd, arms))
        boot = pd.DataFrame(boot)
        for arm in arms:
            for k in ("sens", "far"):
                rec[f"{k}_{arm}_lo"], rec[f"{k}_{arm}_hi"] = np.nanquantile(boot[f"{k}_{arm}"], [.025, .975])
        diff = boot[f"sens_{arms[0]}"] - boot[f"sens_{arms[1]}"]
        rec["sens_A_minus_B"] = rec[f"sens_{arms[0]}"] - rec[f"sens_{arms[1]}"]
        rec["sens_A_minus_B_lo"], rec["sens_A_minus_B_hi"] = np.nanquantile(diff, [.025, .975])
        rows.append(rec)
    res = pd.DataFrame(rows)
    os.makedirs(os.path.join(out, "tables"), exist_ok=True)

    # gradient boosting one week ahead without Estonia and Austria (countries with incomplete first reports)
    d = fc[(fc.model == "gbm") & (fc.h == 1) & ~fc.countryname.isin(["Estonia", "Austria"])]
    origins = np.array(sorted(d.origin.unique()))
    by_o = {o: g for o, g in d.groupby("origin")}
    idx = vl_evaluate._block_samples(len(origins), np.random.default_rng(C.SEED + 6))
    boot = pd.DataFrame([metrics(pd.concat([by_o[origins[i]] for i in b], ignore_index=True), arms) for b in idx])
    pt = metrics(d, arms)
    drop_two = {"n": len(d), "events": int(d.event.sum())}
    for arm in arms:
        drop_two[f"sens_{arm}"] = pt[f"sens_{arm}"]
        drop_two[f"sens_{arm}_lo"], drop_two[f"sens_{arm}_hi"] = np.nanquantile(boot[f"sens_{arm}"], [.025, .975])
    dd = boot[f"sens_{arms[0]}"] - boot[f"sens_{arms[1]}"]
    drop_two["A_minus_B"] = pt[f"sens_{arms[0]}"] - pt[f"sens_{arms[1]}"]
    drop_two["A_minus_B_lo"], drop_two["A_minus_B_hi"] = np.nanquantile(dd, [.025, .975])
    pd.Series(drop_two).to_csv(os.path.join(out, "tables", "main_alerts_without_estonia_austria.csv"),
                               header=["value"])
    res.to_csv(os.path.join(out, "tables", "main_alerts.csv"), index=False)
    by_country = fc[(fc.model == "gbm") & (fc.h == 1)].groupby("countryname").agg(
        n=("event", "size"), events=("event", "sum"))
    for arm in arms:
        g = fc[(fc.model == "gbm") & (fc.h == 1) & fc.event].groupby("countryname")[f"alert_{arm}"].mean()
        by_country[f"sens_{arm[0]}"] = g
    by_country.to_csv(os.path.join(out, "tables", "main_alerts_by_country_gbm_h1.csv"))

    L = ["# Surge-alert analysis (main analysis)", "",
         f"Threshold: {C.ALERT_QUANTILE:.0%} quantile of the {C.ALERT_WINDOW} weeks ending {C.ALERT_LAG} weeks "
         "before the origin, from the snapshot of the origin; event: week-8 value above it; alert: forecast above it.", ""]
    for r in res.to_dict("records"):
        L.append(f"## {r['model']} h={r['h']}: {r['n']} forecasts, {r['events']} high-activity weeks, {r['origins']} origins")
        for arm in arms:
            L.append(f"- {arm}: sensitivity {100 * r[f'sens_{arm}']:.0f}% "
                     f"({100 * r[f'sens_{arm}_lo']:.0f} to {100 * r[f'sens_{arm}_hi']:.0f}); false-alert rate "
                     f"{100 * r[f'far_{arm}']:.0f}% ({100 * r[f'far_{arm}_lo']:.0f} to {100 * r[f'far_{arm}_hi']:.0f}); "
                     f"AUROC {r[f'auroc_{arm}']:.2f}")
        L.append(f"- sensitivity A minus B: {100 * r['sens_A_minus_B']:.0f} points "
                 f"({100 * r['sens_A_minus_B_lo']:.0f} to {100 * r['sens_A_minus_B_hi']:.0f})")
        L.append("")
    L += ["## Without Estonia and Austria (gbm, 1 week)", "",
          f"{drop_two['n']} forecasts, {drop_two['events']} high-activity weeks; " + "; ".join(
              f"{arm} sensitivity {100 * drop_two[f'sens_{arm}']:.0f}% ({100 * drop_two[f'sens_{arm}_lo']:.0f} to "
              f"{100 * drop_two[f'sens_{arm}_hi']:.0f})" for arm in arms)
          + f"; A minus B {100 * drop_two['A_minus_B']:.0f} points ({100 * drop_two['A_minus_B_lo']:.0f} to "
            f"{100 * drop_two['A_minus_B_hi']:.0f})", ""]
    L += ["## By country (gbm, 1 week)", "", by_country.round(2).to_string(), ""]
    with open(os.path.join(out, "alerts_summary.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print("\n".join(L))


if __name__ == "__main__":
    main()
