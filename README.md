# Vintage leakage in SARI forecasting: a vintage-pinned evaluation on ECDC ERVISS data

This repository reproduces every number in the paper from public ECDC data pinned to one commit.
Version: **v1.0.0** (the release cited in the paper). `results/paper_numbers.md` lists each number reported in
the paper next to the output file it comes from.
It compares four ways of evaluating forecasts of the same country-weeks of weekly SARI rates:

| Arm | History the model sees at each forecast origin |
| --- | --- |
| A Retrospective | the weeks in the snapshot published at the origin, each value replaced by its value in the latest ERVISS file |
| B Real-time | the snapshot ECDC published on that date |
| C Real-time + correction | B, with timely weeks under 8 weeks old divided by completeness factors (median ratio of as-published to stable value by country and report age) learned only from snapshots available at the origin; a multiplicative, chain-ladder-type nowcast |
| D Vintage-trained | models trained on features as published in earlier snapshots, with targets already stable at the origin |

All arms forecast the same country-weeks with the same models (persistence, ridge, gradient boosting;
ridge and gradient boosting include one indicator per country) and are scored against the same truth:
the value reported 8 weeks after first publication (robustness: 12 weeks, and the latest file).
Arms A-C see exactly the same weeks at every origin, so they differ only in the values they see.
In every arm, training pairs whose change exceeds 50-fold are dropped (a screen for gross data errors;
it removes two arm-D pairs built on one erroneous German first report in the 10 January 2025 snapshot).
Confidence intervals use a circular block bootstrap over forecast origins (blocks of 6, 2,000 resamples).
The paper calls the arms "evaluation settings".

## Data

- Source: [EU-ECDC/Respiratory_viruses_weekly_data](https://github.com/EU-ECDC/Respiratory_viruses_weekly_data),
  commit `cb8b117d58d1b987b3ebc9ae165daa513ef1f6d5` (30 Oct 2026), licence EUPL v1.2.
- Files: `data/SARIRates.csv` and the 86 weekly snapshots `data/snapshots/*_SARIRates.csv` (8 Nov 2024 to 30 Oct 2026).
- `manifest_SARIRates.csv` records the SHA-256 of each file. `run_all.py` refuses to run if any file differs.
- Aggregate open surveillance data; no individual-level data, so no ethics approval is required.

## Quick start: reproduce everything

```powershell
py -m pip install -r requirements.txt
py reproduce.py --data-dir data
```

`reproduce.py` downloads and verifies the pinned data, then runs every step below in order and ends with
`results/paper_numbers.md`.

## Where each result in the paper is computed

| Result in the paper | Script | Output |
| --- | --- | --- |
| Revisions, first-report completeness (Results, Figure 1a) | `run_all.py` (`vl_revisions.py`) | `results/tables/rq1_*.csv` |
| Forecast errors A-D, excess, gap closed, bias, CIs (Table 1, Figure 1b) | `run_all.py` (`vl_forecast.py`, `vl_evaluate.py`) | `results/tables/gap_by_arm_*.csv`, `per_country_*.csv`, `main_*.csv` |
| Countries resampled; without Estonia and Austria; share of the gap by country | `run_all.py` (`vl_evaluate.py`) | `main_country_cluster_bootstrap.csv`, `main_without_estonia_austria.csv`, `main_gap_share_by_country.csv` |
| Robustness (ages, 12-week truth, latest-file truth, 11 and 13 series, leave one out) | `run_all.py` | `gap_by_arm_*.csv`, `main_leave_one_country_out.csv` |
| Sensitivity runs (timeliness, log offset, restatement threshold) | `run_all.py` with options | `results/sensitivity/*/` |
| Surge alerts: sensitivity, false-alert rate, AUROC, CIs, by country, without Estonia and Austria | `alerts.py` | `results/alerts_summary.md`, `results/tables/main_alerts*.csv` |
| Alert thresholds at the 50th and 90th percentiles | `alerts.py --quantile` | `results/sensitivity/alerts_q50/`, `alerts_q90/` |
| Forecast horizon audit (targets already ended, current or future at the forecast date) | `horizon_audit.py` | `results/horizon_audit.md`, `results/tables/horizon_audit_*.csv` |
| Every number in the paper with its source file | `reproduce.py` | runs every step in order |
| `paper_numbers.py` | `results/paper_numbers.md` |

## Run step by step (Windows PowerShell)

```powershell
py -m pip install -r requirements.txt
py fetch_data.py --data-dir data
py run_all.py --data-dir data --out results --jobs 2
py make_paper_figure.py --data-dir data --results results
py alerts.py --data-dir data --results results
py alerts.py --data-dir data --results results --quantile 0.5
py alerts.py --data-dir data --results results --quantile 0.9
py horizon_audit.py --data-dir data --results results
py paper_numbers.py --results results
```

On macOS or Linux use `python3` in place of `py`. A full run takes several minutes on a laptop.
The committed `results/` folder was produced this way on Linux (Python 3.13; exact package versions in
`requirements-lock.txt`). A Windows run of the first public version reproduced that version's numbers exactly.

Sensitivity runs reported in the paper (each writes its own folder):

```powershell
py run_all.py --data-dir data --out results/sensitivity/timely_2wk --only main --first-delay 2
py run_all.py --data-dir data --out results/sensitivity/timely_6wk --only main --first-delay 6
py run_all.py --data-dir data --out results/sensitivity/log_offset_1 --only main --eps 1.0
py run_all.py --data-dir data --out results/sensitivity/restatement_5pct --only main --max-restatement 0.05
```

## Outputs

- `results/summary.md`: full results of the run.
- `results/paper_numbers.md`: each number in the paper, with its source file.
- `results/tables/`: revision statistics (RQ1), inclusion rule, leakage gap by arm with
  circular block bootstrap intervals (week-8 truth and latest-file truth, every analysis), per-country
  ratios with bootstrap intervals, country-cluster bootstrap, results without Estonia and Austria,
  bias, model rankings, leave-one-country-out, training rows per origin.
- `results/figures/`: `fig1_paper` (Figure 1 of the paper, drawn by `make_paper_figure.py`),
  `fig_gap_by_country` and `fig_backfill_shape`, as PNG and PDF.
- `results/sensitivity/`: timely-report thresholds of 2 and 6 weeks, log offset 1, restatement threshold 5%,
  and alert thresholds at the 50th and 90th percentiles (`alerts_q50`, `alerts_q90`).
- `results/alerts_summary.md` and `results/tables/main_alerts*.csv`: surge alerts (see below).
- `results/horizon_audit.md` and `results/tables/horizon_audit_*.csv`: forecast-horizon audit (see below).
- `results/predictions_*.csv.gz`: every forecast, for independent re-scoring.

## Analyses

| Name | Countries | Age group | Truth window |
| --- | --- | --- | --- |
| main | inclusion rule | all ages | 8 weeks |
| age_65plus | inclusion rule | 65+ | 8 weeks |
| age_0to4 | inclusion rule | 0-4 | 8 weeks |
| truth_12wk | inclusion rule | all ages | 12 weeks |
| all_series | all non-stale series without a scale break | all ages | 8 weeks |
| with_scale_breaks | all non-stale series, scale breaks kept | all ages | 8 weeks |

A first report counts as timely if the week was first published after the first snapshot and within
4 weeks of the week's start. Weeks first published later are historical uploads (671 of 1,706 first
publications, e.g. 233 in Estonia and 160 in Luxembourg); they are excluded from revision statistics
and from the completeness factors of arm C, because they are not real-time reports.

The inclusion rule uses data quality only and is computed in code (`vl_revisions.inclusion_rule`):
a series is excluded if its level shifts 10-fold or more across snapshots, if 10% or more of weeks
change by more than 10% after week 8, if half or more of first reports are zero, or if its latest
reported week is more than 8 weeks old at the final snapshot.

## Surge alerts (`alerts.py`)

Defined in `config.py` before the alert results were seen. A high-activity week is one whose week-8 value
exceeds the 75th percentile of the country's values in the 52 weeks starting at least 8 weeks before the forecast origin,
as published in the snapshot of the origin (no look-ahead). An alert is a forecast above that threshold.
The script reports sensitivity, false-alert rate and AUROC for each setting, with circular block bootstrap
intervals, overall, without Estonia and Austria, and by country. `--quantile` reruns it with another threshold
percentile (sensitivity analysis reported in the paper: 0.5 and 0.9).

## Files

| File | Purpose |
| --- | --- |
| `config.py` | all fixed settings (commit, thresholds, seeds) |
| `fetch_data.py` | downloads the pinned files and checks hashes |
| `vl_data.py` | loading, first-report and truth tables |
| `vl_revisions.py` | revision statistics and the inclusion rule |
| `vl_forecast.py` | the four evaluation arms |
| `vl_evaluate.py` | scoring, bootstrap, rankings, robustness checks |
| `vl_figures.py` | figures |
| `run_all.py` | runs everything and writes `results/` |
| `make_paper_figure.py` | draws Figure 1 of the paper from the data and `results/` |
| `alerts.py` | surge-alert analysis from the saved forecasts |
| `horizon_audit.py` | timing of targets relative to the forecast date; results on future targets only |
| `paper_numbers.py` | collects every number in the paper from `results/` into `results/paper_numbers.md` |

## Version notes

v1.0.0 is the version used in the paper. Surge alerts are computed by `alerts.py`, whose thresholds use only the
snapshot published at each forecast origin.

## Forecast horizons (`horizon_audit.py`)

Targets are the first and second weeks after the last reported week ("one and two weeks ahead"). Because
reporting lags, a target can be a week that had already ended at the forecast date. `horizon_audit.py` counts
past, current and future targets and repeats the main error comparison and the alert analysis on targets that
had not ended at the forecast date and on future targets only (`results/horizon_audit.md`,
`results/tables/horizon_audit_*.csv`).

## Licence and citation

Code: MIT (see `LICENSE`). ECDC data: EUPL v1.2, not redistributed here; `fetch_data.py` downloads it.
Files in `results/` that contain values derived from ECDC data (for example the predictions) remain subject
to the ECDC licence terms. Citation details are in `CITATION.cff`.

## Reporting checklist proposed in the paper

1. Name the data vintage (snapshot) used at every forecast origin.
2. Report real-time and retrospective scores side by side, per country, not only pooled.
3. Report first-report completeness for each series.
4. State the truth window, and check results against the latest file.
5. Publish snapshot hashes and the code release.
