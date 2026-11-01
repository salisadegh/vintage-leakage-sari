# Horizon audit (gradient boosting)

Timing of each scored target week relative to the forecast (publication) date:

timing  current  future  past
h                            
1           273       0    56
2            39     268    17

## Error gap (B vs A) by subset

- all targets, h=1 (329 forecasts): MAE A 0.186, B 0.490; B +164% (124 to 211); gap closed C 76%
- all targets, h=2 (324 forecasts): MAE A 0.209, B 0.476; B +128% (95 to 166); gap closed C 80%
- not ended at forecast date, h=1 (273 forecasts): MAE A 0.169, B 0.506; B +200% (159 to 251); gap closed C 79%
- not ended at forecast date, h=2 (307 forecasts): MAE A 0.205, B 0.480; B +134% (98 to 176); gap closed C 82%
- future only, h=2 (268 forecasts): MAE A 0.195, B 0.489; B +151% (115 to 198); gap closed C 83%

## Alerts by subset

- all targets, h=1 (320 forecasts, 63 high-activity weeks): sensitivity A 86% (72 to 90), B 35% (13 to 45), C 60%; A minus B 51 points (39 to 68); AUROC A 0.96, B 0.75; false alerts A 4%, B 2%
- all targets, h=2 (315 forecasts, 61 high-activity weeks): sensitivity A 77% (50 to 87), B 34% (11 to 46), C 56%; A minus B 43 points (28 to 57); AUROC A 0.95, B 0.75; false alerts A 5%, B 2%
- not ended at forecast date, h=1 (267 forecasts, 53 high-activity weeks): sensitivity A 83% (67 to 89), B 30% (6 to 41), C 60%; A minus B 53 points (42 to 72); AUROC A 0.95, B 0.73; false alerts A 5%, B 2%
- not ended at forecast date, h=2 (298 forecasts, 57 high-activity weeks): sensitivity A 77% (52 to 87), B 35% (14 to 46), C 58%; A minus B 42 points (30 to 56); AUROC A 0.95, B 0.75; false alerts A 5%, B 2%
- future only, h=2 (262 forecasts, 50 high-activity weeks): sensitivity A 74% (44 to 86), B 30% (5 to 43), C 56%; A minus B 44 points (32 to 61); AUROC A 0.94, B 0.73; false alerts A 6%, B 2%
