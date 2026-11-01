# Results summary

Data: EU-ECDC/Respiratory_viruses_weekly_data @ cb8b117d58d1b987b3ebc9ae165daa513ef1f6d5
Timely first report: within 4 weeks; log offset 0.1; restatement threshold 0.05

## RQ1 revisions (all ages, clean first reports)

- n_vintages: 86
- first_vintage: 2024-11-08
- last_vintage: 2026-10-30
- first_publications_after_first_snapshot: 1706
- late_historical_uploads: 671
- clean_first_reports_nonzero: 951
- countries: 13
- share_abs_rev_gt_10pct: 0.588
- upward_share_of_revised_gt_1pct: 0.703
- weeks_with_8wk_followup: 767
- backfill_share_gt_10pct: 0.497
- backfill_upward_share: 0.793
- backfill_median_when_revised: 0.211
- restatement_share_gt_10pct: 0.203
- reporting_lag_median_weeks: 0.714
- convergence: IQR at week 8 = [0.990, 1.006]

## Inclusion rule

- Included (6): Austria, Estonia, Germany, Luxembourg, Malta, Spain
- Sensitivity set (11): Austria, Belgium, Cyprus, Estonia, Germany, Ireland, Luxembourg, Malta, Romania, Slovakia, Spain
- Non-stale incl. scale breaks (13): Austria, Belgium, Cyprus, Estonia, Germany, Greece, Ireland, Latvia, Luxembourg, Malta, Romania, Slovakia, Spain

- Austria: included
- Belgium: excluded (restatement)
- Croatia: excluded (stale)
- Cyprus: excluded (restatement)
- Estonia: included
- Germany: included
- Greece: excluded (level shift, restatement)
- Iceland: excluded (stale)
- Ireland: excluded (restatement)
- Latvia: excluded (level shift, restatement)
- Lithuania: excluded (stale)
- Luxembourg: included
- Malta: included
- Romania: excluded (restatement)
- Slovakia: excluded (zero first reports)
- Spain: included

## Context

- snapshot_spacing_days: 7 d x77, 14 d x6, 21 d x1, 77 d x1
- restatement_gt10_included: 0.003 of 385 weeks
- restatement_gt10_without_gr_lv: 0.155 of 653 weeks
- spearman_completeness_vs_B_over_A: -1.00 (6 countries)
- last_origin_scored: 2026-08-21
- origins_scored_before_2026-03-21: 50

## Leakage gap by analysis (circular block bootstrap over origins)

### main
- gbm h=1 (origins 54, forecasts 275): MAE A 0.123, B 0.514, C 0.201, D 0.275; B +317% (95% CI 255 to 383); C +63% (95% CI 31 to 102); D +123% (95% CI 68 to 185); gap closed C 80% (71 to 89), D 61% (47 to 75)
- gbm h=2 (origins 54, forecasts 271): MAE A 0.152, B 0.501, C 0.212, D 0.302; B +229% (95% CI 175 to 291); C +39% (95% CI 12 to 70); D +98% (95% CI 53 to 153); gap closed C 83% (73 to 94), D 57% (41 to 73)
- persistence h=1 (origins 54, forecasts 275): MAE A 0.122, B 0.599, C 0.245, D 0.599; B +390% (95% CI 322 to 468); C +100% (95% CI 59 to 148); D +390% (95% CI 322 to 468); gap closed C 74% (65 to 83), D 0% (0 to 0)
- persistence h=2 (origins 54, forecasts 271): MAE A 0.161, B 0.598, C 0.262, D 0.598; B +271% (95% CI 222 to 339); C +63% (95% CI 34 to 100); D +271% (95% CI 222 to 339); gap closed C 77% (65 to 87), D 0% (0 to 0)
- ridge h=1 (origins 54, forecasts 275): MAE A 0.122, B 0.477, C 0.196, D 0.245; B +293% (95% CI 228 to 372); C +61% (95% CI 27 to 107); D +102% (95% CI 46 to 174); gap closed C 79% (69 to 89), D 65% (46 to 82)
- ridge h=2 (origins 54, forecasts 271): MAE A 0.151, B 0.471, C 0.212, D 0.258; B +212% (95% CI 172 to 262); C +40% (95% CI 15 to 74); D +71% (95% CI 24 to 134); gap closed C 81% (68 to 92), D 66% (40 to 88)

## Scored against the latest file (all analyses)

- main gbm h=1: MAE A 0.124, B 0.519, C 0.203; B +319% (95% CI 261 to 386); C +64% (95% CI 30 to 102); gap closed C 80% (71 to 89)
- main gbm h=2: MAE A 0.151, B 0.506, C 0.214; B +234% (95% CI 183 to 299); C +41% (95% CI 16 to 72); gap closed C 82% (73 to 92)

## Main analysis detail

Per country (gbm, 1 week; ratio to A with 95% block-bootstrap CI over that country's origins):
- Estonia (54 origins): A 0.113, B 1.382 x12.20 (9.71-15.42), C x3.44 (2.19-5.27), D x3.13 (2.17-4.30)
- Austria (54 origins): A 0.091, B 0.652 x7.17 (4.73-11.56), C x1.90 (1.11-3.64), D x1.72 (0.88-3.23)
- Germany (43 origins): A 0.088, B 0.214 x2.42 (1.93-3.06), C x1.15 (1.00-1.33), D x2.32 (1.42-3.33)
- Malta (54 origins): A 0.211, B 0.255 x1.21 (1.01-1.45), C x1.17 (0.96-1.40), D x1.21 (0.97-1.52)
- Spain (54 origins): A 0.073, B 0.088 x1.21 (0.98-1.47), C x0.93 (0.75-1.08), D x1.70 (1.17-2.38)
- Luxembourg (16 origins): A 0.237, B 0.243 x1.02 (0.86-1.11), C x0.98 (0.84-1.05), D x4.88 (2.74-10.13)

Country-cluster bootstrap (countries resampled; gbm, 1 week): B_excess_pct 31 to 721; C_excess_pct 7 to 153; D_excess_pct 46 to 226; gap_closed_C_pct 71 to 89
Share of the pooled B-A gap (origin-averaged MAE) by country: Estonia 63.8%, Austria 28.2%, Germany 5.1%, Malta 2.1%, Spain 0.8%, Luxembourg 0.1%
Without Estonia and Austria (54 origins): B +38% (21 to 55), C +9% (-4 to 22), D +111% (55 to 176); gap closed C 76%
1-week targets in the ISO week of publication: 0.887; by country: Austria 0.72, Estonia 0.96, Germany 0.84, Luxembourg 1.00, Malta 0.93, Spain 0.94
Training rows (gbm) at first / median / last scored origin: A 1843 / 1973 / 2400; B 1843 / 1973 / 2400; C 1843 / 1973 / 2400; D 60 / 317 / 743
Training pairs dropped by the gross-error screen (max over origins): A 0; B 0; C 0; D 2
Bias by country (gbm, 1 week; mean log error): Austria: A +0.00, B -0.65, C -0.09, D +0.04; Estonia: A -0.00, B -1.38, C -0.24, D -0.02; Germany: A +0.01, B -0.21, C -0.03, D +0.16; Luxembourg: A +0.04, B +0.05, C +0.04, D +1.15; Malta: A -0.04, B -0.15, C -0.02, D +0.16; Spain: A +0.03, B -0.03, C +0.00, D +0.08
- median per-country excess B 81%, C 16%, D 102%; countries with B excess >10%: 5 of 6

Leave one country out (gbm, 1 week):

  left_out  B_excess_pct  C_excess_pct  gap_closed_C_pct
   Austria         266.7          59.2              77.8
   Estonia         140.1          22.8              83.7
   Germany         338.1          68.5              79.7
Luxembourg         363.0          73.6              79.7
     Malta         468.1          86.8              81.4
     Spain         355.9          72.4              79.7

Scored against the latest file instead of the week-8 value (gbm/ridge/persistence):

- gbm h=1: MAE A 0.124, B 0.519, C 0.203; B +319% (95% CI 261 to 386); C +64% (95% CI 30 to 102)
- gbm h=2: MAE A 0.151, B 0.506, C 0.214; B +234% (95% CI 183 to 299); C +41% (95% CI 16 to 72)
- persistence h=1: MAE A 0.123, B 0.606, C 0.247; B +391% (95% CI 323 to 474); C +101% (95% CI 58 to 151)
- persistence h=2: MAE A 0.164, B 0.605, C 0.267; B +270% (95% CI 220 to 334); C +63% (95% CI 34 to 101)
- ridge h=1: MAE A 0.121, B 0.481, C 0.197; B +298% (95% CI 237 to 375); C +63% (95% CI 30 to 108)
- ridge h=2: MAE A 0.150, B 0.477, C 0.214; B +217% (95% CI 176 to 267); C +42% (95% CI 17 to 74)

Bias (log) by arm:

arm            A_retrospective  B_realtime  C_realtime_corrected  D_vintage_trained
model       h                                                                      
gbm         1            0.002      -0.466                -0.070              0.142
            2            0.015      -0.445                -0.054              0.161
persistence 1            0.008      -0.562                -0.096                NaN
            2            0.017      -0.545                -0.080                NaN
ridge       1            0.011      -0.436                -0.056              0.113
            2            0.022      -0.421                -0.040              0.128

Rankings:

 h                                           arm                     order  MAE_persistence  MAE_ridge  MAE_gbm
 1                               A_retrospective ridge < persistence < gbm         0.122410   0.121540 0.123349
 1                                    B_realtime ridge < gbm < persistence         0.599303   0.477414 0.514175
 1                          C_realtime_corrected ridge < gbm < persistence         0.245114   0.195749 0.201216
 1                             D_vintage_trained ridge < gbm < persistence         0.599303   0.245392 0.274864
 1 P(leader under A differs from leader under B)                     0.593              NaN        NaN      NaN
 2                               A_retrospective ridge < gbm < persistence         0.161222   0.150928 0.152380
 2                                    B_realtime ridge < gbm < persistence         0.597733   0.471256 0.500821
 2                          C_realtime_corrected ridge < gbm < persistence         0.262325   0.211722 0.211830
 2                             D_vintage_trained ridge < gbm < persistence         0.597733   0.258400 0.301723
 2 P(leader under A differs from leader under B)                     0.429              NaN        NaN      NaN
