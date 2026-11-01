"""Loading ERVISS SARI rate snapshots and building first-report and truth tables."""
import glob
import hashlib
import os

import pandas as pd

import config as C


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify(data_dir, manifest_path):
    """Check every file in the manifest exists with the recorded SHA-256."""
    man = pd.read_csv(manifest_path)
    bad = []
    for r in man.itertuples():
        p = os.path.join(data_dir, r.path)
        if not os.path.exists(p) or sha256(p) != r.sha256:
            bad.append(r.path)
    if bad:
        raise SystemExit(f"{len(bad)} file(s) missing or changed, e.g. {bad[:3]}. Run fetch_data.py again.")
    return len(man)


def _iso_monday(yw):
    y, w = yw.split("-W")
    return pd.Timestamp.fromisocalendar(int(y), int(w), 1)


def _add_week(d):
    m = {yw: _iso_monday(yw) for yw in d["yearweek"].unique()}
    d["week"] = d["yearweek"].map(m)
    return d


def load(data_dir):
    """Return (vintages, latest): long tables of SARI rates by country, age group and ISO week."""
    files = sorted(glob.glob(os.path.join(data_dir, "snapshots", "*_SARIRates.csv")))
    parts = []
    for f in files:
        d = pd.read_csv(f)
        d["vintage"] = pd.Timestamp(os.path.basename(f)[:10])
        parts.append(d)
    v = _add_week(pd.concat(parts, ignore_index=True))
    latest = _add_week(pd.read_csv(os.path.join(data_dir, "SARIRates.csv")))
    cols = ["countryname", "week", "age", "value"]
    return v[["vintage"] + cols], latest[cols]


def first_reports(v):
    """First vintage in which each country-age-week appears, and report age k of every row."""
    key = ["countryname", "age", "week"]
    first = v.groupby(key, as_index=False).vintage.min().rename(columns={"vintage": "d0"})
    first["delay"] = (first.d0 - first.week).dt.days / 7   # weeks from week start to first publication
    first["timely"] = (first.d0 > v.vintage.min()) & (first.delay <= C.MAX_FIRST_DELAY)
    out = v.merge(first, on=key)
    out["k"] = ((out.vintage - out.d0).dt.days / 7).round().astype(int)
    return out, first


def truth_table(vk, latest, truth_weeks=C.TRUTH_WEEKS):
    """t2 = value reported truth_weeks (or +1) weeks after first report; t1 = latest file."""
    key = ["countryname", "age", "week"]
    t2 = (vk[vk.k.between(truth_weeks, truth_weeks + 1)].sort_values("k")
          .groupby(key, as_index=False).value.first().rename(columns={"value": "t2"}))
    return latest.rename(columns={"value": "t1"}).merge(t2, on=key, how="left")
