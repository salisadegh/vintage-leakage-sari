# Surge-alert analysis (main analysis)

Threshold: 90% quantile of the 52 weeks ending 8 weeks before the origin, from the snapshot of the origin; event: week-8 value above it; alert: forecast above it.

## gbm h=1: 320 forecasts, 28 high-activity weeks, 55 origins
- A_retrospective: sensitivity 68% (48 to 100); false-alert rate 2% (0 to 5); AUROC 0.97
- B_realtime: sensitivity 25% (0 to 36); false-alert rate 1% (0 to 2); AUROC 0.67
- C_realtime_corrected: sensitivity 39% (27 to 56); false-alert rate 3% (1 to 7); AUROC 0.79
- D_vintage_trained: sensitivity 61% (31 to 80); false-alert rate 8% (2 to 15); AUROC 0.87
- sensitivity A minus B: 43 points (18 to 79)

## gbm h=2: 315 forecasts, 30 high-activity weeks, 55 origins
- A_retrospective: sensitivity 60% (31 to 100); false-alert rate 1% (0 to 3); AUROC 0.97
- B_realtime: sensitivity 13% (0 to 22); false-alert rate 1% (0 to 2); AUROC 0.66
- C_realtime_corrected: sensitivity 33% (17 to 61); false-alert rate 3% (0 to 6); AUROC 0.79
- D_vintage_trained: sensitivity 53% (32 to 76); false-alert rate 9% (2 to 19); AUROC 0.84
- sensitivity A minus B: 47 points (15 to 100)

## persistence h=1: 320 forecasts, 28 high-activity weeks, 55 origins
- A_retrospective: sensitivity 75% (54 to 100); false-alert rate 3% (1 to 6); AUROC 0.96
- B_realtime: sensitivity 25% (0 to 35); false-alert rate 1% (0 to 2); AUROC 0.62
- C_realtime_corrected: sensitivity 46% (33 to 61); false-alert rate 6% (1 to 13); AUROC 0.75
- D_vintage_trained: sensitivity 25% (0 to 35); false-alert rate 1% (0 to 2); AUROC 0.62
- sensitivity A minus B: 50 points (23 to 91)

## persistence h=2: 315 forecasts, 30 high-activity weeks, 55 origins
- A_retrospective: sensitivity 57% (29 to 100); false-alert rate 4% (1 to 10); AUROC 0.91
- B_realtime: sensitivity 17% (0 to 29); false-alert rate 1% (0 to 4); AUROC 0.59
- C_realtime_corrected: sensitivity 37% (21 to 62); false-alert rate 7% (1 to 14); AUROC 0.71
- D_vintage_trained: sensitivity 17% (0 to 29); false-alert rate 1% (0 to 4); AUROC 0.59
- sensitivity A minus B: 40 points (12 to 88)

## ridge h=1: 320 forecasts, 28 high-activity weeks, 55 origins
- A_retrospective: sensitivity 64% (42 to 100); false-alert rate 1% (0 to 4); AUROC 0.97
- B_realtime: sensitivity 25% (0 to 36); false-alert rate 0% (0 to 1); AUROC 0.66
- C_realtime_corrected: sensitivity 46% (31 to 61); false-alert rate 3% (0 to 7); AUROC 0.78
- D_vintage_trained: sensitivity 68% (42 to 79); false-alert rate 12% (3 to 24); AUROC 0.91
- sensitivity A minus B: 39 points (11 to 80)

## ridge h=2: 315 forecasts, 30 high-activity weeks, 55 origins
- A_retrospective: sensitivity 50% (23 to 100); false-alert rate 2% (0 to 8); AUROC 0.94
- B_realtime: sensitivity 17% (0 to 29); false-alert rate 1% (0 to 5); AUROC 0.64
- C_realtime_corrected: sensitivity 37% (21 to 63); false-alert rate 4% (1 to 10); AUROC 0.76
- D_vintage_trained: sensitivity 60% (38 to 82); false-alert rate 13% (3 to 26); AUROC 0.88
- sensitivity A minus B: 33 points (6 to 89)

## Without Estonia and Austria (gbm, 1 week)

212 forecasts, 12 high-activity weeks; A_retrospective sensitivity 67% (33 to 100); B_realtime sensitivity 58% (25 to 100); C_realtime_corrected sensitivity 50% (25 to 100); D_vintage_trained sensitivity 83% (67 to 100); A minus B 8 points (0 to 14)

## By country (gbm, 1 week)

              n  events  sens_A  sens_B  sens_C  sens_D
countryname                                            
Austria      54       1    1.00    0.00    0.00     1.0
Cyprus       45       0     NaN     NaN     NaN     NaN
Estonia      54      15    0.67    0.00    0.33     0.4
Germany      43       2    1.00    1.00    1.00     1.0
Luxembourg   16       3    0.33    0.33    0.00     1.0
Malta        54       2    0.50    0.00    0.00     0.5
Spain        54       5    0.80    0.80    0.80     0.8
