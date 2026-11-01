"""Fixed settings for the vintage-leakage analysis. Change nothing here after results are frozen."""

# Source: EU-ECDC Respiratory_viruses_weekly_data, pinned commit (published 30 Oct 2026)
REPO = "EU-ECDC/Respiratory_viruses_weekly_data"
COMMIT = "cb8b117d58d1b987b3ebc9ae165daa513ef1f6d5"
RAW_BASE = f"https://raw.githubusercontent.com/{REPO}/{COMMIT}/data"
MANIFEST = "manifest_SARIRates.csv"

# Forecasting
EPS = 0.1              # offset before taking logs of rates (handles zero weeks)
LAGS = 4               # lagged log rates used as features
HORIZONS = (0, 1, 2)   # weeks after the last reported week; 0 = nowcast of that week
TRAIN_HORIZONS = (1, 2)
MAX_TRAIN_JUMP = 50.0  # drop training pairs whose target/last-value ratio exceeds 50-fold (gross data errors)
FIRST_ORIGIN = "2025-03-07"  # 17 weeks after the first snapshot, so arm D has stable training targets

# Truth: value k weeks after first report (k in [TRUTH_WEEKS, TRUTH_WEEKS + 1])
TRUTH_WEEKS = 8

# A first report counts as timely if published within this many weeks of the week's start.
# Weeks first published later are historical uploads, not real-time reports.
MAX_FIRST_DELAY = 4

# Inclusion rule (data quality only; computed on all-age series)
MAX_LEVEL_SHIFT = 10.0      # exclude if the series level changes 10-fold or more across vintages
MAX_RESTATEMENT = 0.10      # exclude if >= 10% of weeks change by >10% after week 8
MAX_ZERO_FIRST = 0.50       # exclude if >= 50% of first reports are zero
MAX_STALE_WEEKS = 8         # exclude if the latest reported week is older than this at the final snapshot

# Inference
BLOCK = 6                   # circular block bootstrap block length, in consecutive origins
MIN_ORIGINS_CI = 20         # per-country intervals are flagged below this number of scored origins
N_BOOT = 2000
SEED = 1
MODEL_SEED = 0

ARMS = ["A_retrospective", "B_realtime", "C_realtime_corrected", "D_vintage_trained"]
MODELS = ["persistence", "ridge", "gbm"]

# Surge-alert analysis (alerts.py), fixed before results were seen:
# a "high-activity week" is one whose week-8 value exceeds the ALERT_QUANTILE of the country's values in the
# ALERT_WINDOW weeks starting at least ALERT_LAG weeks before the origin, taken from the snapshot published at the origin.
# An alert is a forecast above the same threshold.
ALERT_QUANTILE = 0.75
ALERT_WINDOW = 52
ALERT_LAG = 8
ALERT_MIN_WEEKS = 26

