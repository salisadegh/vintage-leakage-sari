"""Forecasts under four evaluation arms.

A  retrospective: the weeks in the vintage published at the origin, each value replaced by its
   value in the latest file where one exists.
B  real-time: the vintage published at the origin.
C  real-time with completeness correction learned only from vintages up to the origin.
D  vintage-trained: models trained on features as published at earlier origins, with targets
   already stable at the origin.
All arms forecast the same country-weeks with the same model classes. Arms A-C see exactly the
same weeks at each origin (those in the snapshot published at the origin); A replaces each value
by its value in the latest file where one exists, so A-C differ in values only.
Ridge and gradient boosting include one indicator per country. Training pairs whose change
exceeds MAX_TRAIN_JUMP-fold are dropped in every arm (a screen for gross data errors).
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.linear_model import Ridge

import config as C

LAGCOLS = [f"l{k}" for k in range(C.LAGS)]
BASE_FEATS = LAGCOLS + ["s1", "s2", "h"]


def add_country(df, countries):
    """One indicator column per country in the analysis (fixed order)."""
    for c in countries:
        df[f"c_{c}"] = (df.countryname == c).astype(float)
    return df


def feats_for(countries):
    return BASE_FEATS + [f"c_{c}" for c in countries]


def _season(df, col):
    woy = df[col].dt.isocalendar().week.astype(float).values
    df["s1"] = np.sin(2 * np.pi * woy / 52.18)
    df["s2"] = np.cos(2 * np.pi * woy / 52.18)
    return df


def lag_frame(hist, hmax):
    """Rows (country, week) with LAGS log-rate lags; targets dy_h = log y(week+h) - log y(week)."""
    out = []
    for c, g in hist.groupby("countryname", sort=True):
        s = g.set_index("week").value.sort_index().asfreq("7D")
        lv = np.log(s + C.EPS)
        df = pd.DataFrame({"week": lv.index})
        for k in range(C.LAGS):
            df[f"l{k}"] = lv.shift(k).values
        df = df[df[LAGCOLS].notna().all(axis=1)]
        df["countryname"] = c
        for h in range(hmax + 1):
            df[f"y{h}"] = lv.shift(-h).reindex(df.week).values
        out.append(df)
    df = pd.concat(out, ignore_index=True)
    return _season(df, "week")


def screen(tr):
    """Drop training pairs whose change exceeds MAX_TRAIN_JUMP-fold; return (kept, n_dropped)."""
    ok = tr.dy.abs() <= np.log(C.MAX_TRAIN_JUMP)
    return tr[ok], int((~ok).sum())


def training_rows(lf):
    parts = []
    for h in C.TRAIN_HORIZONS:
        t = lf[lf[f"y{h}"].notna()].copy()
        t["h"] = h
        t["dy"] = t[f"y{h}"] - t.l0
        parts.append(t)
    return screen(pd.concat(parts, ignore_index=True))


def fit_models(tr, feats):
    ridge = Ridge(alpha=1.0).fit(tr[feats], tr.dy)
    gbm = HistGradientBoostingRegressor(max_iter=200, learning_rate=0.05,
                                        random_state=C.MODEL_SEED).fit(tr[feats], tr.dy)
    return {"ridge": ridge, "gbm": gbm}


def predict(cur, models, origin, arm, feats, n_train, n_dropped=0):
    rows = []
    for h in C.HORIZONS:
        q = cur.copy()
        q["h"] = h
        preds = {"persistence": q.l0.values}
        if h >= 1 and models is not None:
            for m, mod in models.items():
                preds[m] = q.l0.values + mod.predict(q[feats])
        for m, p in preds.items():
            r = q[["countryname", "week"]].rename(columns={"week": "ow"})
            r = r.assign(target_week=r.ow + pd.to_timedelta(7 * h, unit="D"), origin=origin,
                         arm=arm, model=m, h=h, pred=p, l0=q.l0.values, n_train=n_train,
                         n_dropped=n_dropped)
            rows.append(r)
    return rows


def completeness_factors(vk_o_past, origin, kmax):
    """Median (value at report age k) / (value at origin) per country and k, using timely first
    reports aged >= kmax at the origin. No look-ahead."""
    ref = vk_o_past[vk_o_past.vintage == origin][["countryname", "week", "value", "d0", "timely"]]
    ref = ref[(((origin - ref.d0).dt.days / 7) >= kmax) & ref.timely]
    ref = ref.rename(columns={"value": "ref"})[["countryname", "week", "ref"]]
    j = vk_o_past[vk_o_past.k < kmax].merge(ref, on=["countryname", "week"])
    j = j[(j.ref > 0) & (j.value > 0)]
    j["r"] = j.value / j.ref
    c = j.groupby(["countryname", "k"]).r.agg(["median", "size"]).reset_index()
    pooled = j.groupby("k").r.median()
    c["c"] = np.where(c["size"] >= 5, c["median"], c.k.map(pooled))
    return c.set_index(["countryname", "k"]).c


def vintage_features(vin):
    """Feature row per country from one published vintage: its last LAGS weeks."""
    rows = []
    for c, s in vin.groupby("countryname"):
        s = s.set_index("week").value.sort_index().asfreq("7D")
        if len(s) < C.LAGS or s.iloc[-C.LAGS:].isna().any():
            continue
        lv = np.log(s.iloc[-C.LAGS:].values[::-1] + C.EPS)
        rows.append((c, s.index[-1], *lv))
    df = pd.DataFrame(rows, columns=["countryname", "week"] + LAGCOLS)
    return _season(df, "week")


def run_arms(vk, latest, countries, age, kmax=C.TRUTH_WEEKS):
    """vk: vintages with d0/k (from vl_data.first_reports); latest: latest file.
    Returns one long table of predictions for arms A-D."""
    vk = vk[(vk.age == age) & vk.countryname.isin(countries)].copy()
    lat = latest[(latest.age == age) & latest.countryname.isin(countries)][["countryname", "week", "value"]]
    vint = {o: g[["countryname", "week", "value", "d0", "k", "timely"]] for o, g in vk.groupby("vintage")}
    origins_all = pd.DatetimeIndex(sorted(vint))
    feats_by_vintage = {u: vintage_features(vint[u]) for u in origins_all}
    origins = origins_all[origins_all >= pd.Timestamp(C.FIRST_ORIGIN)]
    cl = sorted(countries)
    feats = feats_for(cl)
    feats_by_vintage = {u: add_country(f, cl) for u, f in feats_by_vintage.items()}
    out = []
    for o in origins:
        vin = vint[o]
        last = vin.groupby("countryname").week.max()
        hist_b = vin[["countryname", "week", "value"]]
        # arm A: the same weeks as the snapshot, each value replaced by its latest-file value if any
        hist_a = hist_b.merge(lat.rename(columns={"value": "v_latest"}), on=["countryname", "week"], how="left")
        hist_a = hist_a.assign(value=hist_a.v_latest.fillna(hist_a.value))[["countryname", "week", "value"]]
        cf = completeness_factors(vk[vk.vintage <= o], o, kmax)
        # correct only timely recent weeks; late historical uploads are already complete when first published
        fac = np.array([cf.get((c, k), 1.0) if (k < kmax and t) else 1.0
                        for c, k, t in zip(vin.countryname, vin.k, vin.timely)])
        hist_c = hist_b.assign(value=vin.value.values / np.clip(fac, 0.05, None))
        for arm, hist in (("A_retrospective", hist_a), ("B_realtime", hist_b), ("C_realtime_corrected", hist_c)):
            lf = add_country(lag_frame(hist, max(C.TRAIN_HORIZONS)), cl)
            tr, nd = training_rows(lf)
            models = fit_models(tr, feats)
            cur = lf[lf.week == lf.countryname.map(last)]
            out += predict(cur, models, o, arm, feats, len(tr), nd)
        # arm D: train on (features as published at u < o) -> (targets stable at o)
        known = vin[((o - vin.d0).dt.days / 7) >= kmax][["countryname", "week", "value"]]
        tr = []
        for u in origins_all[origins_all < o]:
            fu = feats_by_vintage[u]
            for h in C.TRAIN_HORIZONS:
                t = fu.assign(h=h, tw=fu.week + pd.Timedelta(days=7 * h))
                tr.append(t.merge(known.rename(columns={"week": "tw"}), on=["countryname", "tw"]))
        tr = pd.concat(tr, ignore_index=True)
        tr["dy"] = np.log(tr.value + C.EPS) - tr.l0
        tr, nd = screen(tr)
        if len(tr) >= 60:
            models = fit_models(tr, feats)
            cur = feats_by_vintage[o]
            out += [r for r in predict(cur, models, o, "D_vintage_trained", feats, len(tr), nd)
                    if r.model.iat[0] != "persistence"]
    return pd.concat(out, ignore_index=True)
