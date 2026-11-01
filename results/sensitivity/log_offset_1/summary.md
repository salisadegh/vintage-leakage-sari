# Results summary

Data: EU-ECDC/Respiratory_viruses_weekly_data @ cb8b117d58d1b987b3ebc9ae165daa513ef1f6d5
Timely first report: within 4 weeks; log offset 1.0; restatement threshold 0.1

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
- restatement_gt10_included: 0.011 of 448 weeks
- restatement_gt10_without_gr_lv: 0.155 of 653 weeks
- spearman_completeness_vs_B_over_A: -0.95 (7 countries)
- last_origin_scored: 2026-08-21
- origins_scored_before_2026-03-21: 51

## Leakage gap by analysis (circular block bootstrap over origins)

### main
- gbm h=1 (origins 55, forecasts 329): MAE A 0.148, B 0.407, C 0.211, D 0.274; B +174% (95% CI 125 to 227); C +43% (95% CI 17 to 72); D +85% (95% CI 45 to 133); gap closed C 76% (64 to 88), D 51% (32 to 69)
- gbm h=2 (origins 55, forecasts 324): MAE A 0.170, B 0.403, C 0.222, D 0.283; B +137% (95% CI 97 to 178); C +30% (95% CI 11 to 48); D +66% (95% CI 38 to 98); gap closed C 78% (67 to 91), D 52% (32 to 71)
- persistence h=1 (origins 55, forecasts 329): MAE A 0.145, B 0.478, C 0.249, D 0.478; B +230% (95% CI 178 to 283); C +71% (95% CI 39 to 111); D +230% (95% CI 178 to 283); gap closed C 69% (56 to 80), D 0% (0 to 0)
- persistence h=2 (origins 55, forecasts 324): MAE A 0.184, B 0.486, C 0.270, D 0.486; B +164% (95% CI 135 to 207); C +47% (95% CI 23 to 72); D +164% (95% CI 135 to 207); gap closed C 72% (57 to 85), D 0% (0 to 0)
- ridge h=1 (origins 55, forecasts 329): MAE A 0.146, B 0.414, C 0.217, D 0.303; B +184% (95% CI 127 to 248); C +48% (95% CI 19 to 87); D +107% (95% CI 56 to 170); gap closed C 74% (62 to 86), D 42% (18 to 64)
- ridge h=2 (origins 55, forecasts 324): MAE A 0.173, B 0.417, C 0.235, D 0.325; B +141% (95% CI 108 to 181); C +36% (95% CI 15 to 60); D +88% (95% CI 46 to 133); gap closed C 75% (61 to 88), D 38% (9 to 66)

## Scored against the latest file (all analyses)

- main gbm h=1: MAE A 0.148, B 0.410, C 0.213; B +177% (95% CI 131 to 227); C +44% (95% CI 18 to 73); gap closed C 75% (63 to 87)
- main gbm h=2: MAE A 0.170, B 0.407, C 0.223; B +139% (95% CI 103 to 183); C +31% (95% CI 12 to 49); gap closed C 78% (67 to 90)

## Main analysis detail

Per country (gbm, 1 week; ratio to A with 95% block-bootstrap CI over that country's origins):
- Estonia (54 origins): A 0.103, B 1.068 x10.40 (8.45-12.77), C x3.36 (2.21-4.88), D x2.90 (2.18-3.77)
- Austria (54 origins): A 0.085, B 0.586 x6.88 (4.76-9.98), C x1.95 (1.20-3.23), D x2.29 (1.31-3.85)
- Germany (43 origins): A 0.093, B 0.194 x2.09 (1.55-2.68), C x0.97 (0.77-1.20), D x1.40 (1.19-1.61)
- Spain (54 origins): A 0.066, B 0.079 x1.20 (0.96-1.52), C x0.95 (0.80-1.12), D x1.61 (1.12-2.41)
- Malta (54 origins): A 0.191, B 0.218 x1.14 (0.92-1.38), C x1.16 (1.00-1.35), D x1.29 (1.09-1.55)
- Cyprus (54 origins): A 0.316, B 0.344 x1.09 (0.89-1.41), C x1.18 (0.91-1.67), D x1.83 (1.13-2.79)
- Luxembourg (16 origins): A 0.145, B 0.137 x0.95 (0.80-1.01), C x0.88 (0.60-0.97), D x3.13 (1.94-6.17)

Country-cluster bootstrap (countries resampled; gbm, 1 week): B_excess_pct 15 to 541; C_excess_pct 7 to 119; D_excess_pct 52 to 142; gap_closed_C_pct 14 to 87
Share of the pooled B-A gap (origin-averaged MAE) by country: Estonia 60.7%, Austria 31.3%, Germany 5.1%, Malta 1.7%, Spain 0.8%, Cyprus 0.6%, Luxembourg -0.1%
Without Estonia and Austria (55 origins): B +19% (1 to 40), C +10% (-6 to 34), D +67% (28 to 114); gap closed C 48%
1-week targets in the ISO week of publication: 0.830; by country: Austria 0.72, Cyprus 0.54, Estonia 0.96, Germany 0.84, Luxembourg 1.00, Malta 0.93, Spain 0.94
Training rows (gbm) at first / median / last scored origin: A 1880 / 2054 / 2581; B 1880 / 2054 / 2581; C 1880 / 2054 / 2581; D 60 / 368 / 869
Training pairs dropped by the gross-error screen (max over origins): A 0; B 0; C 0; D 2
Bias by country (gbm, 1 week; mean log error): Austria: A +0.01, B -0.59, C -0.09, D -0.07; Cyprus: A +0.06, B +0.04, C +0.11, D +0.42; Estonia: A +0.00, B -1.07, C -0.19, D +0.03; Germany: A +0.02, B -0.19, C -0.02, D +0.03; Luxembourg: A +0.02, B +0.02, C +0.01, D +0.45; Malta: A -0.04, B -0.13, C -0.02, D +0.09; Spain: A +0.03, B -0.03, C +0.01, D +0.05
- median per-country excess B 20%, C 16%, D 83%; countries with B excess >10%: 5 of 7

Leave one country out (gbm, 1 week):

  left_out  B_excess_pct  C_excess_pct  gap_closed_C_pct
   Austria         134.0          38.4              71.4
    Cyprus         282.0          60.7              78.5
   Estonia          78.5          18.1              76.9
   Germany         180.1          46.9              74.0
Luxembourg         187.1          46.4              75.2
     Malta         219.9          50.5              77.0
     Spain         188.5          47.0              75.1

Scored against the latest file instead of the week-8 value (gbm/ridge/persistence):

- gbm h=1: MAE A 0.148, B 0.410, C 0.213; B +177% (95% CI 131 to 227); C +44% (95% CI 18 to 73)
- gbm h=2: MAE A 0.170, B 0.407, C 0.223; B +139% (95% CI 103 to 183); C +31% (95% CI 12 to 49)
- persistence h=1: MAE A 0.146, B 0.483, C 0.250; B +231% (95% CI 182 to 284); C +72% (95% CI 38 to 113)
- persistence h=2: MAE A 0.186, B 0.492, C 0.273; B +165% (95% CI 136 to 205); C +47% (95% CI 25 to 74)
- ridge h=1: MAE A 0.146, B 0.417, C 0.217; B +187% (95% CI 130 to 250); C +49% (95% CI 20 to 87)
- ridge h=2: MAE A 0.173, B 0.421, C 0.237; B +144% (95% CI 111 to 183); C +37% (95% CI 16 to 60)

Bias (log) by arm:

arm            A_retrospective  B_realtime  C_realtime_corrected  D_vintage_trained
model       h                                                                      
gbm         1            0.013      -0.316                -0.033              0.111
            2            0.016      -0.309                -0.026              0.120
persistence 1            0.006      -0.394                -0.060                NaN
            2            0.006      -0.389                -0.055                NaN
ridge       1            0.019      -0.318                -0.026              0.048
            2            0.020      -0.314                -0.021              0.040

Rankings:

 h                                           arm                     order  MAE_persistence  MAE_ridge  MAE_gbm
 1                               A_retrospective persistence < ridge < gbm         0.145033   0.145861 0.148177
 1                                    B_realtime gbm < ridge < persistence         0.478081   0.414113 0.406535
 1                          C_realtime_corrected gbm < ridge < persistence         0.248508   0.216546 0.211222
 1                             D_vintage_trained gbm < ridge < persistence         0.478081   0.302628 0.273570
 1 P(leader under A differs from leader under B)                     0.695              NaN        NaN      NaN
 2                               A_retrospective gbm < ridge < persistence         0.183901   0.173084 0.170326
 2                                    B_realtime gbm < ridge < persistence         0.486254   0.417305 0.403137
 2                          C_realtime_corrected gbm < ridge < persistence         0.269879   0.235088 0.221522
 2                             D_vintage_trained gbm < ridge < persistence         0.486254   0.325255 0.283164
 2 P(leader under A differs from leader under B)                     0.344              NaN        NaN      NaN
