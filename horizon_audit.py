"""Horizon audit: where do forecast targets fall relative to the forecast (publication) date?

Usage:  python horizon_audit.py --data-dir data --results results
Targets are defined relative to the last reported week (h = 1, 2 weeks after it). Because reporting lags,
a target can be a week that has already ended at the forecast date ("past"), the week containing the forecast
date ("current"), or a later week ("future"). This script counts each case and repeats the main error
comparison and the alert analysis on (i) targets that had not ended at the forecast date and (ii) future
targets only. Writes results/tables/horizon_audit_*.csv and results/horizon_audit.md.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from sklearn.metrics import roc_auc_score  # noqa: E402

import alerts  # noqa: E402
import config as C  # noqa: E402
import vl_data  # noqa: E402
import vl_evaluate  # noqa: E402


def timing(target_week, origin):
    week_end = target_week + pd.Timedelta(days=6)
    return np.where(week_end < origin, "past", np.where(target_week <= origin, "current", "future"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data")
    ap.add_argument("--results", default="results")
    a = ap.parse_args()
    T = os.path.join(a.results, "tables")
    v, latest = vl_data.load(a.data_dir)
    vk, _ = vl_data.first_reports(v)
    truth = vl_data.truth_table(vk, latest, C.TRUTH_WEEKS)
    pred = pd.read_csv(os.path.join(a.results, "predictions_main.csv.gz"), parse_dates=["origin", "target_week", "ow"])
    p = vl_evaluate.attach_truth(pred, truth, "total")
    p["timing"] = timing(p.target_week, p.origin)
    key = ["model", "h", "origin", "countryname"]
    tm = p.drop_duplicates(key).set_index(key).timing

    # 1. counts
    counts = vl_evaluate.scored_panel(p).join(tm).reset_index()
    counts = counts[counts.model == "gbm"].groupby(["h", "timing"]).size().unstack(fill_value=0)
    counts.to_csv(os.path.join(T, "horizon_audit_counts.csv"))

    # 2. error gap on subsets
    subsets = {"all targets": ["past", "current", "future"], "not ended at forecast date": ["current", "future"],
               "future only": ["future"]}
    gaps = []
    for name, keep in subsets.items():
        panel = vl_evaluate.scored_panel(p[p.timing.isin(keep)])
        panel = panel[panel.index.get_level_values("h").isin(
            [h for h in C.TRAIN_HORIZONS if (panel.index.get_level_values("h") == h).sum() > 0])]
        gt = vl_evaluate.gap_table(panel, np.random.default_rng(C.SEED))
        gaps.append(gt[gt.model == "gbm"].assign(subset=name))
    gaps = pd.concat(gaps, ignore_index=True)
    gaps.to_csv(os.path.join(T, "horizon_audit_gap.csv"), index=False)

    # 3. alerts on subsets (same definitions as alerts.py)
    fc = vl_evaluate.scored_panel(p, "pred")
    fc = fc.join(p.drop_duplicates(key).set_index(key)[["t2", "timing"]], how="left")
    th = alerts.thresholds(vk, fc.index.get_level_values("origin").unique(),
                           fc.index.get_level_values("countryname").unique())
    fc = fc.reset_index().merge(th, on=["origin", "countryname"], how="inner")
    fc["event"] = fc.t2 > fc["T"]
    for arm in C.ARMS:
        fc[f"alert_{arm}"] = (np.exp(fc[arm]) - C.EPS) > fc["T"]
        fc[f"score_{arm}"] = fc[arm] - np.log(fc["T"] + C.EPS)
    rows = []
    rng = np.random.default_rng(C.SEED + 7)
    for name, keep in subsets.items():
        for h in C.TRAIN_HORIZONS:
            d = fc[(fc.model == "gbm") & (fc.h == h) & fc.timing.isin(keep)]
            if d.empty:
                continue
            rec = {"subset": name, "h": h, "n": len(d), "events": int(d.event.sum())}
            rec.update(alerts.metrics(d, C.ARMS))
            for arm in C.ARMS:
                rec[f"auroc_{arm}"] = roc_auc_score(d.event, d[f"score_{arm}"]) if d.event.nunique() == 2 else np.nan
            origins = np.array(sorted(d.origin.unique()))
            by_o = {o: g for o, g in d.groupby("origin")}
            idx = vl_evaluate._block_samples(len(origins), rng)
            boot = pd.DataFrame([alerts.metrics(pd.concat([by_o[origins[i]] for i in b], ignore_index=True), C.ARMS)
                                 for b in idx])
            diff = boot[f"sens_{C.ARMS[0]}"] - boot[f"sens_{C.ARMS[1]}"]
            rec["A_minus_B"] = rec[f"sens_{C.ARMS[0]}"] - rec[f"sens_{C.ARMS[1]}"]
            rec["A_minus_B_lo"], rec["A_minus_B_hi"] = np.nanquantile(diff, [.025, .975])
            for arm in C.ARMS[:3]:
                rec[f"sens_{arm}_lo"], rec[f"sens_{arm}_hi"] = np.nanquantile(boot[f"sens_{arm}"], [.025, .975])
            rows.append(rec)
    al = pd.DataFrame(rows)
    al.to_csv(os.path.join(T, "horizon_audit_alerts.csv"), index=False)

    L = ["# Horizon audit (gradient boosting)", "",
         "Timing of each scored target week relative to the forecast (publication) date:", "",
         counts.to_string(), "", "## Error gap (B vs A) by subset", ""]
    for r in gaps.to_dict("records"):
        L.append(f"- {r['subset']}, h={r['h']} ({r['n_forecasts']} forecasts): MAE A {r['MAE_A']:.3f}, "
                 f"B {r['MAE_B']:.3f}; B {r['B_excess_pct']:+.0f}% ({r['B_lo']:.0f} to {r['B_hi']:.0f}); "
                 f"gap closed C {r['gap_closed_C_pct']:.0f}%")
    L += ["", "## Alerts by subset", ""]
    for r in al.to_dict("records"):
        L.append(f"- {r['subset']}, h={r['h']} ({r['n']} forecasts, {r['events']} high-activity weeks): sensitivity "
                 f"A {100 * r['sens_A_retrospective']:.0f}% ({100 * r['sens_A_retrospective_lo']:.0f} to "
                 f"{100 * r['sens_A_retrospective_hi']:.0f}), B {100 * r['sens_B_realtime']:.0f}% "
                 f"({100 * r['sens_B_realtime_lo']:.0f} to {100 * r['sens_B_realtime_hi']:.0f}), "
                 f"C {100 * r['sens_C_realtime_corrected']:.0f}%; A minus B {100 * r['A_minus_B']:.0f} points "
                 f"({100 * r['A_minus_B_lo']:.0f} to {100 * r['A_minus_B_hi']:.0f}); AUROC A "
                 f"{r['auroc_A_retrospective']:.2f}, B {r['auroc_B_realtime']:.2f}; false alerts A "
                 f"{100 * r['far_A_retrospective']:.0f}%, B {100 * r['far_B_realtime']:.0f}%")
    with open(os.path.join(a.results, "horizon_audit.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
