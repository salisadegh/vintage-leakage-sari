# Surge-alert analysis (main analysis)

Threshold: 75% quantile of the 52 weeks ending 8 weeks before the origin, from the snapshot of the origin; event: week-8 value above it; alert: forecast above it.

## gbm h=1: 320 forecasts, 63 high-activity weeks, 55 origins
- A_retrospective: sensitivity 86% (73 to 90); false-alert rate 4% (1 to 11); AUROC 0.96
- B_realtime: sensitivity 35% (14 to 45); false-alert rate 2% (0 to 5); AUROC 0.75
- C_realtime_corrected: sensitivity 60% (40 to 74); false-alert rate 5% (2 to 12); AUROC 0.85
- D_vintage_trained: sensitivity 70% (46 to 82); false-alert rate 14% (8 to 23); AUROC 0.87
- sensitivity A minus B: 51 points (40 to 68)

## gbm h=2: 315 forecasts, 61 high-activity weeks, 55 origins
- A_retrospective: sensitivity 77% (50 to 87); false-alert rate 5% (1 to 12); AUROC 0.95
- B_realtime: sensitivity 34% (11 to 46); false-alert rate 2% (0 to 5); AUROC 0.75
- C_realtime_corrected: sensitivity 56% (37 to 69); false-alert rate 6% (2 to 14); AUROC 0.84
- D_vintage_trained: sensitivity 75% (56 to 88); false-alert rate 12% (6 to 21); AUROC 0.89
- sensitivity A minus B: 43 points (28 to 57)

## persistence h=1: 320 forecasts, 63 high-activity weeks, 55 origins
- A_retrospective: sensitivity 78% (63 to 85); false-alert rate 6% (2 to 13); AUROC 0.96
- B_realtime: sensitivity 37% (18 to 45); false-alert rate 2% (0 to 5); AUROC 0.72
- C_realtime_corrected: sensitivity 63% (45 to 75); false-alert rate 9% (4 to 16); AUROC 0.82
- D_vintage_trained: sensitivity 37% (18 to 45); false-alert rate 2% (0 to 5); AUROC 0.72
- sensitivity A minus B: 41 points (30 to 60)

## persistence h=2: 315 forecasts, 61 high-activity weeks, 55 origins
- A_retrospective: sensitivity 72% (49 to 86); false-alert rate 8% (2 to 17); AUROC 0.94
- B_realtime: sensitivity 34% (22 to 42); false-alert rate 3% (0 to 8); AUROC 0.72
- C_realtime_corrected: sensitivity 59% (35 to 76); false-alert rate 10% (4 to 18); AUROC 0.81
- D_vintage_trained: sensitivity 34% (22 to 42); false-alert rate 3% (0 to 8); AUROC 0.72
- sensitivity A minus B: 38 points (22 to 52)

## ridge h=1: 320 forecasts, 63 high-activity weeks, 55 origins
- A_retrospective: sensitivity 79% (67 to 86); false-alert rate 4% (1 to 10); AUROC 0.96
- B_realtime: sensitivity 37% (17 to 45); false-alert rate 2% (0 to 6); AUROC 0.76
- C_realtime_corrected: sensitivity 65% (50 to 76); false-alert rate 7% (2 to 15); AUROC 0.85
- D_vintage_trained: sensitivity 84% (64 to 91); false-alert rate 19% (8 to 35); AUROC 0.92
- sensitivity A minus B: 43 points (34 to 63)

## ridge h=2: 315 forecasts, 61 high-activity weeks, 55 origins
- A_retrospective: sensitivity 74% (53 to 86); false-alert rate 6% (1 to 14); AUROC 0.94
- B_realtime: sensitivity 34% (18 to 44); false-alert rate 3% (0 to 9); AUROC 0.76
- C_realtime_corrected: sensitivity 61% (38 to 77); false-alert rate 8% (2 to 17); AUROC 0.84
- D_vintage_trained: sensitivity 85% (71 to 92); false-alert rate 18% (6 to 36); AUROC 0.91
- sensitivity A minus B: 39 points (31 to 50)

## Without Estonia and Austria (gbm, 1 week)

212 forecasts, 38 high-activity weeks; A_retrospective sensitivity 76% (50 to 84); B_realtime sensitivity 58% (27 to 69); C_realtime_corrected sensitivity 71% (50 to 88); D_vintage_trained sensitivity 87% (69 to 95); A minus B 18 points (7 to 36)

## By country (gbm, 1 week)

              n  events  sens_A  sens_B  sens_C  sens_D
countryname                                            
Austria      54       7    1.00    0.00    0.43    0.43
Cyprus       45       9    0.89    0.89    0.89    0.89
Estonia      54      18    1.00    0.00    0.44    0.44
Germany      43       5    0.80    0.40    0.80    0.80
Luxembourg   16       6    0.67    0.67    0.67    1.00
Malta        54       9    0.44    0.11    0.33    0.78
Spain        54       9    1.00    0.78    0.89    0.89
