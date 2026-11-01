# Surge-alert analysis (main analysis)

Threshold: 50% quantile of the 52 weeks ending 8 weeks before the origin, from the snapshot of the origin; event: week-8 value above it; alert: forecast above it.

## gbm h=1: 320 forecasts, 118 high-activity weeks, 55 origins
- A_retrospective: sensitivity 85% (68 to 94); false-alert rate 8% (3 to 17); AUROC 0.95
- B_realtime: sensitivity 40% (23 to 50); false-alert rate 3% (1 to 8); AUROC 0.79
- C_realtime_corrected: sensitivity 72% (57 to 81); false-alert rate 9% (6 to 14); AUROC 0.89
- D_vintage_trained: sensitivity 82% (66 to 90); false-alert rate 17% (10 to 28); AUROC 0.89
- sensitivity A minus B: 45 points (39 to 50)

## gbm h=2: 315 forecasts, 115 high-activity weeks, 55 origins
- A_retrospective: sensitivity 81% (56 to 93); false-alert rate 10% (4 to 19); AUROC 0.95
- B_realtime: sensitivity 38% (11 to 54); false-alert rate 2% (1 to 5); AUROC 0.80
- C_realtime_corrected: sensitivity 70% (47 to 81); false-alert rate 9% (6 to 14); AUROC 0.89
- D_vintage_trained: sensitivity 80% (61 to 89); false-alert rate 20% (11 to 35); AUROC 0.90
- sensitivity A minus B: 43 points (36 to 48)

## persistence h=1: 320 forecasts, 118 high-activity weeks, 55 origins
- A_retrospective: sensitivity 91% (78 to 98); false-alert rate 6% (3 to 12); AUROC 0.97
- B_realtime: sensitivity 43% (30 to 51); false-alert rate 3% (1 to 7); AUROC 0.77
- C_realtime_corrected: sensitivity 75% (62 to 83); false-alert rate 9% (6 to 14); AUROC 0.87
- D_vintage_trained: sensitivity 43% (30 to 51); false-alert rate 3% (1 to 7); AUROC 0.77
- sensitivity A minus B: 47 points (39 to 59)

## persistence h=2: 315 forecasts, 115 high-activity weeks, 55 origins
- A_retrospective: sensitivity 85% (65 to 96); false-alert rate 8% (3 to 16); AUROC 0.96
- B_realtime: sensitivity 42% (27 to 51); false-alert rate 4% (2 to 8); AUROC 0.78
- C_realtime_corrected: sensitivity 74% (54 to 86); false-alert rate 10% (7 to 15); AUROC 0.88
- D_vintage_trained: sensitivity 42% (27 to 51); false-alert rate 4% (2 to 8); AUROC 0.78
- sensitivity A minus B: 43 points (32 to 57)

## ridge h=1: 320 forecasts, 118 high-activity weeks, 55 origins
- A_retrospective: sensitivity 86% (73 to 94); false-alert rate 8% (3 to 17); AUROC 0.97
- B_realtime: sensitivity 42% (20 to 55); false-alert rate 3% (1 to 7); AUROC 0.80
- C_realtime_corrected: sensitivity 76% (62 to 85); false-alert rate 10% (6 to 16); AUROC 0.89
- D_vintage_trained: sensitivity 92% (76 to 98); false-alert rate 22% (7 to 45); AUROC 0.94
- sensitivity A minus B: 44 points (33 to 58)

## ridge h=2: 315 forecasts, 115 high-activity weeks, 55 origins
- A_retrospective: sensitivity 83% (69 to 93); false-alert rate 8% (3 to 17); AUROC 0.96
- B_realtime: sensitivity 43% (21 to 57); false-alert rate 2% (1 to 5); AUROC 0.81
- C_realtime_corrected: sensitivity 76% (61 to 86); false-alert rate 10% (6 to 16); AUROC 0.90
- D_vintage_trained: sensitivity 93% (75 to 99); false-alert rate 20% (6 to 40); AUROC 0.94
- sensitivity A minus B: 41 points (30 to 57)

## Without Estonia and Austria (gbm, 1 week)

212 forecasts, 73 high-activity weeks; A_retrospective sensitivity 77% (48 to 91); B_realtime sensitivity 64% (38 to 81); C_realtime_corrected sensitivity 79% (59 to 90); D_vintage_trained sensitivity 92% (75 to 98); A minus B 12 points (2 to 21)

## By country (gbm, 1 week)

              n  events  sens_A  sens_B  sens_C  sens_D
countryname                                            
Austria      54      20    1.00    0.00    0.75    0.70
Cyprus       45      10    1.00    1.00    1.00    1.00
Estonia      54      25    0.96    0.00    0.48    0.64
Germany      43       9    0.78    0.56    0.78    1.00
Luxembourg   16      12    0.83    0.83    0.83    1.00
Malta        54      20    0.35    0.25    0.55    0.70
Spain        54      22    1.00    0.77    0.91    1.00
