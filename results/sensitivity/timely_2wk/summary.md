# Results summary

Data: EU-ECDC/Respiratory_viruses_weekly_data @ cb8b117d58d1b987b3ebc9ae165daa513ef1f6d5
Timely first report: within 2 weeks; log offset 0.1; restatement threshold 0.1

## RQ1 revisions (all ages, clean first reports)

- n_vintages: 86
- first_vintage: 2024-11-08
- last_vintage: 2026-10-30
- first_publications_after_first_snapshot: 1706
- late_historical_uploads: 979
- clean_first_reports_nonzero: 657
- countries: 13
- share_abs_rev_gt_10pct: 0.651
- upward_share_of_revised_gt_1pct: 0.702
- weeks_with_8wk_followup: 532
- backfill_share_gt_10pct: 0.575
- backfill_upward_share: 0.824
- backfill_median_when_revised: 0.261
- restatement_share_gt_10pct: 0.180
- reporting_lag_median_weeks: 0.714
- convergence: IQR at week 8 = [0.992, 1.017]

## Inclusion rule

- Included (7): Austria, Cyprus, Estonia, Germany, Luxembourg, Malta, Spain
- Sensitivity set (11): Austria, Belgium, Cyprus, Estonia, Germany, Ireland, Luxembourg, Malta, Romania, Slovakia, Spain
- Non-stale incl. scale breaks (13): Austria, Belgium, Cyprus, Estonia, Germany, Greece, Ireland, Latvia, Luxembourg, Malta, Romania, Slovakia, Spain

- Austria: included
- Belgium: excluded (restatement)
- Croatia: excluded (stale)
- Cyprus: included
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
- restatement_gt10_included: 0.012 of 338 weeks
- restatement_gt10_without_gr_lv: 0.122 of 451 weeks
- spearman_completeness_vs_B_over_A: -0.95 (7 countries)
- last_origin_scored: 2026-08-21
- origins_scored_before_2026-03-21: 51

## Leakage gap by analysis (circular block bootstrap over origins)

### main
- gbm h=1 (origins 55, forecasts 329): MAE A 0.186, B 0.490, C 0.275, D 0.337; B +164% (95% CI 124 to 211); C +48% (95% CI 21 to 79); D +81% (95% CI 53 to 120); gap closed C 71% (56 to 85), D 51% (33 to 65)
- gbm h=2 (origins 55, forecasts 324): MAE A 0.209, B 0.476, C 0.276, D 0.348; B +128% (95% CI 95 to 166); C +32% (95% CI 10 to 54); D +67% (95% CI 46 to 91); gap closed C 75% (58 to 91), D 48% (29 to 63)
- persistence h=1 (origins 55, forecasts 329): MAE A 0.184, B 0.588, C 0.320, D 0.588; B +219% (95% CI 170 to 277); C +74% (95% CI 38 to 119); D +219% (95% CI 170 to 277); gap closed C 66% (51 to 80), D 0% (0 to 0)
- persistence h=2 (origins 55, forecasts 324): MAE A 0.228, B 0.594, C 0.341, D 0.594; B +161% (95% CI 130 to 207); C +50% (95% CI 23 to 78); D +161% (95% CI 130 to 207); gap closed C 69% (51 to 85), D 0% (0 to 0)
- ridge h=1 (origins 55, forecasts 329): MAE A 0.178, B 0.480, C 0.270, D 0.367; B +170% (95% CI 119 to 229); C +52% (95% CI 21 to 92); D +106% (95% CI 57 to 161); gap closed C 70% (54 to 85), D 37% (13 to 61)
- ridge h=2 (origins 55, forecasts 324): MAE A 0.212, B 0.484, C 0.289, D 0.391; B +128% (95% CI 98 to 167); C +36% (95% CI 14 to 62); D +84% (95% CI 44 to 130); gap closed C 72% (54 to 88), D 34% (3 to 64)

## Scored against the latest file (all analyses)

- main gbm h=1: MAE A 0.186, B 0.494, C 0.276; B +166% (95% CI 128 to 210); C +48% (95% CI 21 to 81); gap closed C 71% (55 to 85)
- main gbm h=2: MAE A 0.208, B 0.480, C 0.277; B +131% (95% CI 100 to 169); C +33% (95% CI 13 to 53); gap closed C 75% (57 to 90)

## Main analysis detail

Per country (gbm, 1 week; ratio to A with 95% block-bootstrap CI over that country's origins):
- Estonia (54 origins): A 0.109, B 1.275 x11.66 (9.24-14.87), C x4.13 (2.47-6.25), D x3.16 (2.31-4.19)
- Austria (54 origins): A 0.088, B 0.641 x7.25 (4.99-10.79), C x2.32 (1.36-4.08), D x2.54 (1.40-4.46)
- Germany (43 origins): A 0.101, B 0.220 x2.17 (1.62-2.80), C x1.01 (0.85-1.20), D x1.55 (1.28-1.83)
- Spain (54 origins): A 0.074, B 0.087 x1.18 (0.95-1.51), C x1.01 (0.85-1.23), D x1.53 (1.06-2.26)
- Malta (54 origins): A 0.217, B 0.252 x1.16 (0.93-1.42), C x1.20 (1.00-1.43), D x1.29 (1.10-1.53)
- Cyprus (54 origins): A 0.490, B 0.519 x1.06 (0.86-1.31), C x1.11 (0.93-1.35), D x1.61 (1.12-2.34)
- Luxembourg (16 origins): A 0.229, B 0.222 x0.97 (0.87-1.03), C x0.97 (0.92-1.02), D x2.22 (1.59-3.56)

Country-cluster bootstrap (countries resampled; gbm, 1 week): B_excess_pct 13 to 580; C_excess_pct 8 to 153; D_excess_pct 52 to 149; gap_closed_C_pct 15 to 81
Share of the pooled B-A gap (origin-averaged MAE) by country: Estonia 62.2%, Austria 29.4%, Germany 5.0%, Malta 1.9%, Cyprus 0.8%, Spain 0.8%, Luxembourg -0.1%
Without Estonia and Austria (55 origins): B +18% (3 to 34), C +10% (-3 to 24), D +59% (31 to 96); gap closed C 43%
1-week targets in the ISO week of publication: 0.830; by country: Austria 0.72, Cyprus 0.54, Estonia 0.96, Germany 0.84, Luxembourg 1.00, Malta 0.93, Spain 0.94
Training rows (gbm) at first / median / last scored origin: A 1880 / 2054 / 2581; B 1880 / 2054 / 2581; C 1880 / 2054 / 2581; D 60 / 368 / 869
Training pairs dropped by the gross-error screen (max over origins): A 0; B 0; C 0; D 2
Bias by country (gbm, 1 week; mean log error): Austria: A +0.01, B -0.64, C -0.12, D -0.10; Cyprus: A +0.11, B +0.09, C +0.20, D +0.47; Estonia: A +0.01, B -1.27, C -0.27, D -0.04; Germany: A +0.02, B -0.21, C -0.01, D +0.03; Luxembourg: A +0.02, B +0.01, C +0.02, D +0.50; Malta: A -0.04, B -0.16, C +0.01, D +0.10; Spain: A +0.03, B -0.04, C +0.01, D +0.04
- median per-country excess B 18%, C 11%, D 61%; countries with B excess >10%: 5 of 7

Leave one country out (gbm, 1 week):

  left_out  B_excess_pct  C_excess_pct  gap_closed_C_pct
   Austria         126.5          41.6              67.1
    Cyprus         292.4          78.9              73.0
   Estonia          69.1          19.6              71.6
   Germany         165.6          51.3              69.0
Luxembourg         177.7          51.5              71.0
     Malta         200.0          54.8              72.6
     Spain         175.0          51.4              70.6

Scored against the latest file instead of the week-8 value (gbm/ridge/persistence):

- gbm h=1: MAE A 0.186, B 0.494, C 0.276; B +166% (95% CI 128 to 210); C +48% (95% CI 21 to 81)
- gbm h=2: MAE A 0.208, B 0.480, C 0.277; B +131% (95% CI 100 to 169); C +33% (95% CI 13 to 53)
- persistence h=1: MAE A 0.185, B 0.594, C 0.323; B +221% (95% CI 172 to 276); C +74% (95% CI 37 to 121)
- persistence h=2: MAE A 0.230, B 0.601, C 0.345; B +161% (95% CI 132 to 206); C +50% (95% CI 24 to 82)
- ridge h=1: MAE A 0.178, B 0.483, C 0.271; B +172% (95% CI 122 to 228); C +52% (95% CI 20 to 94)
- ridge h=2: MAE A 0.212, B 0.489, C 0.292; B +131% (95% CI 100 to 170); C +38% (95% CI 15 to 63)

Bias (log) by arm:

arm            A_retrospective  B_realtime  C_realtime_corrected  D_vintage_trained
model       h                                                                      
gbm         1            0.023      -0.359                -0.029              0.106
            2            0.023      -0.351                -0.021              0.109
persistence 1            0.005      -0.471                -0.077                NaN
            2            0.004      -0.465                -0.073                NaN
ridge       1            0.019      -0.354                -0.048              0.049
            2            0.020      -0.350                -0.044              0.039

Rankings:

 h                                           arm                     order  MAE_persistence  MAE_ridge  MAE_gbm
 1                               A_retrospective ridge < persistence < gbm         0.184189   0.178011 0.186037
 1                                    B_realtime ridge < gbm < persistence         0.588156   0.479863 0.490258
 1                          C_realtime_corrected ridge < gbm < persistence         0.320236   0.269801 0.274552
 1                             D_vintage_trained gbm < ridge < persistence         0.588156   0.366795 0.336540
 1 P(leader under A differs from leader under B)                     0.264              NaN        NaN      NaN
 2                               A_retrospective gbm < ridge < persistence         0.227821   0.212110 0.208570
 2                                    B_realtime gbm < ridge < persistence         0.594370   0.484356 0.476032
 2                          C_realtime_corrected gbm < ridge < persistence         0.340994   0.289355 0.275641
 2                             D_vintage_trained gbm < ridge < persistence         0.594370   0.391148 0.347652
 2 P(leader under A differs from leader under B)                     0.232              NaN        NaN      NaN
