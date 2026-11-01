# Results summary

Data: EU-ECDC/Respiratory_viruses_weekly_data @ cb8b117d58d1b987b3ebc9ae165daa513ef1f6d5
Timely first report: within 4 weeks; log offset 0.1; restatement threshold 0.1

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
- gbm h=1 (origins 55, forecasts 329): MAE A 0.186, B 0.490, C 0.258, D 0.337; B +164% (95% CI 124 to 211); C +39% (95% CI 14 to 66); D +81% (95% CI 53 to 120); gap closed C 76% (64 to 89), D 51% (33 to 65)
- gbm h=2 (origins 55, forecasts 324): MAE A 0.209, B 0.476, C 0.261, D 0.348; B +128% (95% CI 95 to 166); C +25% (95% CI 7 to 42); D +67% (95% CI 46 to 91); gap closed C 80% (69 to 94), D 48% (29 to 63)
- persistence h=1 (origins 55, forecasts 329): MAE A 0.184, B 0.588, C 0.303, D 0.588; B +219% (95% CI 170 to 277); C +64% (95% CI 35 to 101); D +219% (95% CI 170 to 277); gap closed C 71% (59 to 81), D 0% (0 to 0)
- persistence h=2 (origins 55, forecasts 324): MAE A 0.228, B 0.594, C 0.325, D 0.594; B +161% (95% CI 130 to 207); C +43% (95% CI 21 to 65); D +161% (95% CI 130 to 207); gap closed C 73% (60 to 86), D 0% (0 to 0)
- ridge h=1 (origins 55, forecasts 329): MAE A 0.178, B 0.480, C 0.255, D 0.367; B +170% (95% CI 119 to 229); C +43% (95% CI 18 to 76); D +106% (95% CI 57 to 161); gap closed C 75% (63 to 87), D 37% (13 to 61)
- ridge h=2 (origins 55, forecasts 324): MAE A 0.212, B 0.484, C 0.279, D 0.391; B +128% (95% CI 98 to 167); C +31% (95% CI 13 to 52); D +84% (95% CI 44 to 130); gap closed C 76% (62 to 89), D 34% (3 to 64)

### age_65plus
- gbm h=1 (origins 54, forecasts 275): MAE A 0.140, B 0.714, C 0.242, D 0.294; B +409% (95% CI 352 to 472); C +72% (95% CI 37 to 113); D +110% (95% CI 58 to 173); gap closed C 82% (72 to 90), D 73% (57 to 86)
- gbm h=2 (origins 54, forecasts 271): MAE A 0.157, B 0.692, C 0.244, D 0.325; B +341% (95% CI 299 to 397); C +56% (95% CI 26 to 96); D +107% (95% CI 58 to 173); gap closed C 84% (73 to 92), D 69% (51 to 83)
- persistence h=1 (origins 54, forecasts 275): MAE A 0.151, B 0.794, C 0.289, D 0.794; B +426% (95% CI 364 to 499); C +92% (95% CI 58 to 134); D +426% (95% CI 364 to 499); gap closed C 78% (69 to 86), D 0% (0 to 0)
- persistence h=2 (origins 54, forecasts 271): MAE A 0.190, B 0.789, C 0.305, D 0.789; B +316% (95% CI 262 to 379); C +61% (95% CI 36 to 94); D +316% (95% CI 262 to 379); gap closed C 81% (71 to 89), D 0% (0 to 0)
- ridge h=1 (origins 54, forecasts 275): MAE A 0.146, B 0.563, C 0.220, D 0.269; B +285% (95% CI 233 to 355); C +51% (95% CI 19 to 95); D +84% (95% CI 33 to 148); gap closed C 82% (71 to 92), D 71% (55 to 87)
- ridge h=2 (origins 54, forecasts 271): MAE A 0.168, B 0.552, C 0.230, D 0.287; B +229% (95% CI 185 to 289); C +37% (95% CI 14 to 75); D +71% (95% CI 28 to 131); gap closed C 84% (71 to 94), D 69% (49 to 87)

### age_0to4
- gbm h=1 (origins 53, forecasts 251): MAE A 0.232, B 0.473, C 0.389, D 0.449; B +104% (95% CI 67 to 145); C +68% (95% CI 47 to 90); D +94% (95% CI 44 to 146); gap closed C 35% (17 to 47), D 10% (-97 to 67)
- gbm h=2 (origins 53, forecasts 249): MAE A 0.270, B 0.473, C 0.401, D 0.476; B +76% (95% CI 42 to 108); C +49% (95% CI 28 to 69); D +77% (95% CI 35 to 133); gap closed C 35% (5 to 51), D -2% (-161 to 62)
- persistence h=1 (origins 54, forecasts 256): MAE A 0.257, B 0.563, C 0.457, D 0.563; B +119% (95% CI 82 to 156); C +78% (95% CI 58 to 103); D +119% (95% CI 82 to 156); gap closed C 34% (16 to 46), D 0% (0 to 0)
- persistence h=2 (origins 54, forecasts 254): MAE A 0.313, B 0.577, C 0.483, D 0.577; B +84% (95% CI 54 to 114); C +54% (95% CI 40 to 70); D +84% (95% CI 54 to 114); gap closed C 35% (6 to 50), D 0% (0 to 0)
- ridge h=1 (origins 53, forecasts 251): MAE A 0.256, B 0.449, C 0.392, D 0.347; B +75% (95% CI 44 to 110); C +53% (95% CI 37 to 69); D +35% (95% CI 13 to 60); gap closed C 29% (2 to 44), D 53% (-13 to 85)
- ridge h=2 (origins 53, forecasts 249): MAE A 0.292, B 0.454, C 0.404, D 0.379; B +55% (95% CI 29 to 85); C +38% (95% CI 23 to 51); D +30% (95% CI 13 to 48); gap closed C 31% (-10 to 49), D 46% (-26 to 81)

### truth_12wk
- gbm h=1 (origins 45, forecasts 272): MAE A 0.192, B 0.489, C 0.261, D 0.373; B +155% (95% CI 122 to 194); C +36% (95% CI 11 to 65); D +94% (95% CI 59 to 135); gap closed C 77% (62 to 92), D 39% (16 to 59)
- gbm h=2 (origins 45, forecasts 270): MAE A 0.213, B 0.485, C 0.264, D 0.382; B +128% (95% CI 98 to 164); C +24% (95% CI 3 to 45); D +79% (95% CI 54 to 109); gap closed C 81% (64 to 98), D 38% (7 to 60)
- persistence h=1 (origins 49, forecasts 296): MAE A 0.188, B 0.579, C 0.321, D 0.579; B +208% (95% CI 167 to 269); C +71% (95% CI 32 to 122); D +208% (95% CI 167 to 269); gap closed C 66% (47 to 82), D 0% (0 to 0)
- persistence h=2 (origins 49, forecasts 294): MAE A 0.238, B 0.602, C 0.353, D 0.602; B +153% (95% CI 124 to 198); C +48% (95% CI 22 to 82); D +153% (95% CI 124 to 198); gap closed C 68% (46 to 86), D 0% (0 to 0)
- ridge h=1 (origins 45, forecasts 272): MAE A 0.188, B 0.476, C 0.256, D 0.426; B +154% (95% CI 115 to 205); C +37% (95% CI 10 to 73); D +127% (95% CI 65 to 207); gap closed C 76% (60 to 92), D 17% (-16 to 51)
- ridge h=2 (origins 45, forecasts 270): MAE A 0.223, B 0.499, C 0.280, D 0.442; B +124% (95% CI 97 to 163); C +26% (95% CI 5 to 47); D +99% (95% CI 46 to 166); gap closed C 79% (63 to 96), D 20% (-25 to 61)

### all_series
- gbm h=1 (origins 55, forecasts 507): MAE A 0.233, B 0.392, C 0.287, D 0.306; B +68% (95% CI 41 to 104); C +23% (95% CI -1 to 58); D +31% (95% CI 6 to 61); gap closed C 66% (40 to 103), D 54% (32 to 87)
- gbm h=2 (origins 56, forecasts 498): MAE A 0.247, B 0.386, C 0.277, D 0.311; B +56% (95% CI 35 to 84); C +12% (95% CI -8 to 37); D +26% (95% CI 8 to 48); gap closed C 78% (51 to 121), D 54% (27 to 80)
- persistence h=1 (origins 55, forecasts 507): MAE A 0.248, B 0.486, C 0.324, D 0.486; B +96% (95% CI 67 to 141); C +31% (95% CI 10 to 60); D +96% (95% CI 67 to 141); gap closed C 68% (55 to 86), D 0% (0 to 0)
- persistence h=2 (origins 56, forecasts 498): MAE A 0.267, B 0.469, C 0.319, D 0.469; B +76% (95% CI 50 to 112); C +19% (95% CI 2 to 41); D +76% (95% CI 50 to 112); gap closed C 74% (59 to 96), D 0% (0 to 0)
- ridge h=1 (origins 55, forecasts 507): MAE A 0.234, B 0.375, C 0.277, D 0.341; B +61% (95% CI 40 to 87); C +18% (95% CI -1 to 42); D +46% (95% CI 19 to 75); gap closed C 70% (48 to 102), D 24% (-25 to 64)
- ridge h=2 (origins 56, forecasts 498): MAE A 0.248, B 0.363, C 0.276, D 0.335; B +46% (95% CI 28 to 71); C +11% (95% CI -6 to 31); D +35% (95% CI 16 to 55); gap closed C 75% (52 to 118), D 24% (-31 to 63)

### with_scale_breaks
- gbm h=1 (origins 55, forecasts 591): MAE A 0.589, B 0.476, C 0.588, D 0.417; B -19% (95% CI -57 to 78); C -0% (95% CI -55 to 134); D -29% (95% CI -63 to 56); gap closed C 99% (-1120 to 1152), D -52% (-467 to 467)
- gbm h=2 (origins 56, forecasts 581): MAE A 0.594, B 0.476, C 0.580, D 0.425; B -20% (95% CI -55 to 64); C -2% (95% CI -54 to 121); D -28% (95% CI -59 to 44); gap closed C 88% (-676 to 788), D -44% (-346 to 345)
- persistence h=1 (origins 55, forecasts 591): MAE A 0.596, B 0.553, C 0.623, D 0.553; B -7% (95% CI -49 to 89); C +5% (95% CI -51 to 133); D -7% (95% CI -49 to 89); gap closed C 164% (-729 to 867), D -0% (0 to 0)
- persistence h=2 (origins 56, forecasts 581): MAE A 0.607, B 0.548, C 0.622, D 0.548; B -10% (95% CI -49 to 89); C +2% (95% CI -49 to 127); D -10% (95% CI -49 to 89); gap closed C 126% (-901 to 1042), D -0% (0 to 0)
- ridge h=1 (origins 55, forecasts 591): MAE A 0.586, B 0.458, C 0.561, D 0.461; B -22% (95% CI -59 to 65); C -4% (95% CI -57 to 118); D -21% (95% CI -53 to 57); gap closed C 80% (-850 to 757), D 2% (-176 to 178)
- ridge h=2 (origins 56, forecasts 581): MAE A 0.589, B 0.453, C 0.562, D 0.445; B -23% (95% CI -58 to 61); C -5% (95% CI -53 to 109); D -24% (95% CI -54 to 48); gap closed C 80% (-794 to 1130), D -6% (-222 to 177)

## Scored against the latest file (all analyses)

- main gbm h=1: MAE A 0.186, B 0.494, C 0.259; B +166% (95% CI 128 to 210); C +40% (95% CI 16 to 66); gap closed C 76% (63 to 89)
- main gbm h=2: MAE A 0.208, B 0.480, C 0.263; B +131% (95% CI 100 to 169); C +26% (95% CI 9 to 42); gap closed C 80% (68 to 93)
- age_65plus gbm h=1: MAE A 0.137, B 0.717, C 0.241; B +422% (95% CI 364 to 485); C +75% (95% CI 38 to 116); gap closed C 82% (72 to 91)
- age_65plus gbm h=2: MAE A 0.156, B 0.697, C 0.246; B +346% (95% CI 302 to 403); C +57% (95% CI 27 to 94); gap closed C 83% (73 to 92)
- age_0to4 gbm h=1: MAE A 0.232, B 0.479, C 0.393; B +107% (95% CI 67 to 149); C +70% (95% CI 49 to 94); gap closed C 35% (17 to 46)
- age_0to4 gbm h=2: MAE A 0.271, B 0.479, C 0.407; B +77% (95% CI 43 to 112); C +50% (95% CI 29 to 70); gap closed C 35% (5 to 50)
- truth_12wk gbm h=1: MAE A 0.191, B 0.491, C 0.261; B +156% (95% CI 123 to 193); C +37% (95% CI 11 to 67); gap closed C 77% (61 to 92)
- truth_12wk gbm h=2: MAE A 0.212, B 0.486, C 0.264; B +130% (95% CI 100 to 168); C +25% (95% CI 4 to 45); gap closed C 81% (64 to 97)
- all_series gbm h=1: MAE A 0.182, B 0.452, C 0.347; B +149% (95% CI 117 to 186); C +91% (95% CI 70 to 111); gap closed C 39% (29 to 48)
- all_series gbm h=2: MAE A 0.207, B 0.446, C 0.341; B +115% (95% CI 96 to 140); C +65% (95% CI 51 to 79); gap closed C 44% (34 to 55)
- with_scale_breaks gbm h=1: MAE A 0.185, B 0.888, C 1.002; B +379% (95% CI 216 to 593); C +441% (95% CI 339 to 577); gap closed C -16% (-63 to 5)
- with_scale_breaks gbm h=2: MAE A 0.215, B 0.869, C 0.976; B +305% (95% CI 169 to 459); C +354% (95% CI 265 to 456); gap closed C -16% (-68 to 5)

## Main analysis detail

Per country (gbm, 1 week; ratio to A with 95% block-bootstrap CI over that country's origins):
- Estonia (54 origins): A 0.109, B 1.275 x11.66 (9.24-14.87), C x3.47 (2.19-5.18), D x3.16 (2.31-4.19)
- Austria (54 origins): A 0.088, B 0.641 x7.25 (4.99-10.79), C x1.98 (1.22-3.37), D x2.54 (1.40-4.46)
- Germany (43 origins): A 0.101, B 0.220 x2.17 (1.62-2.80), C x1.02 (0.79-1.26), D x1.55 (1.28-1.83)
- Spain (54 origins): A 0.074, B 0.087 x1.18 (0.95-1.51), C x0.89 (0.74-1.05), D x1.53 (1.06-2.26)
- Malta (54 origins): A 0.217, B 0.252 x1.16 (0.93-1.42), C x1.14 (0.97-1.33), D x1.29 (1.10-1.53)
- Cyprus (54 origins): A 0.490, B 0.519 x1.06 (0.86-1.31), C x1.16 (0.91-1.53), D x1.61 (1.12-2.34)
- Luxembourg (16 origins): A 0.229, B 0.222 x0.97 (0.87-1.03), C x0.98 (0.81-1.07), D x2.22 (1.59-3.56)

Country-cluster bootstrap (countries resampled; gbm, 1 week): B_excess_pct 13 to 580; C_excess_pct 7 to 119; D_excess_pct 52 to 149; gap_closed_C_pct 13 to 87
Share of the pooled B-A gap (origin-averaged MAE) by country: Estonia 62.2%, Austria 29.4%, Germany 5.0%, Malta 1.9%, Cyprus 0.8%, Spain 0.8%, Luxembourg -0.1%
Without Estonia and Austria (55 origins): B +18% (3 to 34), C +10% (-7 to 31), D +59% (31 to 96); gap closed C 44%
1-week targets in the ISO week of publication: 0.830; by country: Austria 0.72, Cyprus 0.54, Estonia 0.96, Germany 0.84, Luxembourg 1.00, Malta 0.93, Spain 0.94
Training rows (gbm) at first / median / last scored origin: A 1880 / 2054 / 2581; B 1880 / 2054 / 2581; C 1880 / 2054 / 2581; D 60 / 368 / 869
Training pairs dropped by the gross-error screen (max over origins): A 0; B 0; C 0; D 2
Bias by country (gbm, 1 week; mean log error): Austria: A +0.01, B -0.64, C -0.09, D -0.10; Cyprus: A +0.11, B +0.09, C +0.18, D +0.47; Estonia: A +0.01, B -1.27, C -0.22, D -0.04; Germany: A +0.02, B -0.21, C -0.03, D +0.03; Luxembourg: A +0.02, B +0.01, C +0.01, D +0.50; Malta: A -0.04, B -0.16, C -0.03, D +0.10; Spain: A +0.03, B -0.04, C +0.00, D +0.04
- median per-country excess B 18%, C 14%, D 61%; countries with B excess >10%: 5 of 7

Leave one country out (gbm, 1 week):

  left_out  B_excess_pct  C_excess_pct  gap_closed_C_pct
   Austria         126.5          34.5              72.7
    Cyprus         292.4          59.4              79.7
   Estonia          69.1          16.6              75.9
   Germany         165.6          41.2              75.1
Luxembourg         177.7          42.2              76.3
     Malta         200.0          45.0              77.5
     Spain         175.0          42.5              75.7

Scored against the latest file instead of the week-8 value (gbm/ridge/persistence):

- gbm h=1: MAE A 0.186, B 0.494, C 0.259; B +166% (95% CI 128 to 210); C +40% (95% CI 16 to 66)
- gbm h=2: MAE A 0.208, B 0.480, C 0.263; B +131% (95% CI 100 to 169); C +26% (95% CI 9 to 42)
- persistence h=1: MAE A 0.185, B 0.594, C 0.305; B +221% (95% CI 172 to 276); C +65% (95% CI 34 to 101)
- persistence h=2: MAE A 0.230, B 0.601, C 0.329; B +161% (95% CI 132 to 206); C +43% (95% CI 23 to 67)
- ridge h=1: MAE A 0.178, B 0.483, C 0.256; B +172% (95% CI 122 to 228); C +44% (95% CI 18 to 76)
- ridge h=2: MAE A 0.212, B 0.489, C 0.281; B +131% (95% CI 100 to 170); C +32% (95% CI 13 to 53)

Bias (log) by arm:

arm            A_retrospective  B_realtime  C_realtime_corrected  D_vintage_trained
model       h                                                                      
gbm         1            0.023      -0.359                -0.030              0.106
            2            0.023      -0.351                -0.024              0.109
persistence 1            0.005      -0.471                -0.070                NaN
            2            0.004      -0.465                -0.065                NaN
ridge       1            0.019      -0.354                -0.023              0.049
            2            0.020      -0.350                -0.019              0.039

Rankings:

 h                                           arm                     order  MAE_persistence  MAE_ridge  MAE_gbm
 1                               A_retrospective ridge < persistence < gbm         0.184189   0.178011 0.186037
 1                                    B_realtime ridge < gbm < persistence         0.588156   0.479863 0.490258
 1                          C_realtime_corrected ridge < gbm < persistence         0.302806   0.254855 0.257689
 1                             D_vintage_trained gbm < ridge < persistence         0.588156   0.366795 0.336540
 1 P(leader under A differs from leader under B)                     0.264              NaN        NaN      NaN
 2                               A_retrospective gbm < ridge < persistence         0.227821   0.212110 0.208570
 2                                    B_realtime gbm < ridge < persistence         0.594370   0.484356 0.476032
 2                          C_realtime_corrected gbm < ridge < persistence         0.325141   0.278744 0.261339
 2                             D_vintage_trained gbm < ridge < persistence         0.594370   0.391148 0.347652
 2 P(leader under A differs from leader under B)                     0.232              NaN        NaN      NaN
