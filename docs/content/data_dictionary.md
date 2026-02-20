# Stroke Prevention Demo Dataset Data Dictionary (NHANES-derived)

This dataset is derived from the CDC **NHANES** (National Health and Nutrition Examination Survey) and includes demographic, questionnaire, exam, laboratory, and dietary-recall variables.

## Notes on NHANES conventions (important)
- NHANES commonly uses **special missing codes** like **7-fill** for *Refused* (7, 77, 777, …) and **9-fill** for *Don't know* (9, 99, 999, …), plus blanks for not asked/not eligible. This file was pre-cleaned, so those values appear to have been removed or recoded, so there are mostly “real” answer codes.
- Several lab measures in this file appear to be in **SI units (mmol/L)** (based on the observed ranges). NHANES often provides both **mg/dL** variables and derived **mmol/L** variables; so we should be careful in preprocessing if we merge with other NHANES extracts.
- “Safe input?” is for the demo UI:
  - **yes**: most people can answer without lab tests (self-report or simple measurement)
  - **maybe**: user might know from labs or a tracker, but not guaranteed
  - **no**: outcome label or not appropriate for user entry

## Column dictionary
| Column name | Meaning | Type | Allowed values/codes | Safe input? |
|---|---|---|---|---|
| stroke | Stroke outcome (whether the participant reports having had a stroke). NHANES: MCQ160f (ever told had a stroke), typically recoded. | category | 0 = No stroke; 1 = Stroke | no |
| gender | Sex of participant (NHANES-style coding). NHANES: RIAGENDR. | category | 1 = Male; 2 = Female | yes |
| age | Age group category (derived from age in years; adults only). | category | 1 = 20–39 years; 2 = 40–59 years; 3 = 60+ years | yes |
| Race | Race/ethnicity category (NHANES-style RIDRETH1 recode). NHANES: RIDRETH1. | category | 1 = Mexican American; 2 = Other Hispanic; 3 = Non-Hispanic White; 4 = Non-Hispanic Black; 5 = Other race (incl. multiracial) | yes |
| Marital status | Marital status category (NHANES-style DMDMARTL). NHANES: DMDMARTL. | category | 1 = Married; 2 = Widowed; 3 = Divorced; 4 = Separated; 5 = Never married; 6 = Living with partner | yes |
| alcohol  | Whether participant drinks alcohol (derived from NHANES alcohol questions). | category | 0 = No; 1 = Yes | yes |
| smoke | Whether participant smokes (derived from NHANES smoking questions). | category | 0 = No; 1 = Yes | yes |
| sleep disorder | Ever told by a doctor they have a sleep disorder (yes/no). NHANES: SLQ060 (or similar sleep disorder item). | category | 1 = Yes; 2 = No | yes |
| Health Insurance | Covered by health insurance (yes/no). NHANES: HIQ011. | category | 1 = Yes; 2 = No | yes |
| General health condition | Self-rated general health. NHANES: HSD010. | category | 1 = Excellent; 2 = Very good; 3 = Good; 4 = Fair; 5 = Poor | yes |
| depression | How often participant feels depressed/down/hopeless (PHQ-style frequency; recoded). NHANES: DPQ030 style frequency (0–3 in NHANES; this file uses 1–3). | category | 1 = Several days; 2 = More than half the days; 3 = Nearly every day | yes |
| sleep time | Average hours of sleep per night. | number | numeric (hours); observed range in this file: 1–14 | yes |
| diabetes | Whether participant has diabetes (self-report). NHANES: DIQ010 (doctor told diabetes), typically recoded. | category | 0 = No; 1 = Yes | yes |
| hypertension | Whether participant has hypertension (high blood pressure) (self-report). NHANES: BPQ020 (ever told had high blood pressure), typically recoded. | category | 0 = No; 1 = Yes | yes |
| high cholesterol | Whether participant has high cholesterol (self-report). NHANES: BPQ080 (doctor told high cholesterol), typically recoded. | category | 0 = No; 1 = Yes | maybe |
| Minutes sedentary activity | Typical daily sedentary time (minutes). NHANES: PAD680. | number | numeric (minutes/day); observed range in this file: 0–1200 | yes |
| Coronary Heart Disease | Whether participant has coronary heart disease (self-report). NHANES: MCQ160c (coronary heart disease), typically recoded. | category | 0 = No; 1 = Yes | maybe |
| Body Mass Index | BMI category (derived from BMI). | category | 1 = Underweight (<18.5); 2 = Normal (18.5–24.9); 3 = Overweight (25–29.9); 4 = Obese (≥30) | maybe |
| Waist Circumference | Waist circumference measurement. NHANES: BMXWAIST. | number | numeric (cm); observed range in this file: 63.5–176 | yes |
| Systolic blood pressure | Systolic blood pressure. NHANES: BPXSY (mm Hg) averaged/selected reading. | number | numeric (mm Hg); observed range in this file: 66–238 | maybe |
| Diastolic blood pressure | Diastolic blood pressure. NHANES: BPXDI (mm Hg) averaged/selected reading. | number | numeric (mm Hg); observed range in this file: 32–124 | maybe |
| High-density lipoprotein | HDL cholesterol. NHANES: HDL cholesterol SI (LBDHDDSI) or converted from LBXHDD. | number | numeric (mmol/L (SI)); observed range in this file: 0.28–5.84 | maybe |
| Triglyceride | Triglycerides. NHANES: triglycerides SI (LBDTRSI) or converted from LBXTR. | number | numeric (mmol/L (SI)); observed range in this file: 0.203–28.778 | maybe |
| Low-density lipoprotein | LDL cholesterol. NHANES: LDL-C SI (LBDLDLSI) or derived LDL. | number | numeric (mmol/L (SI)); observed range in this file: 0.388–9.232 | maybe |
| Fasting Glucose | Fasting plasma glucose. NHANES: fasting glucose SI (LBDGLUSI) or converted from LBXGLU. | number | numeric (mmol/L (SI)); observed range in this file: 1.998–26.09 | maybe |
| Glycohemoglobin | Glycohemoglobin (HbA1c). NHANES: LBXGH (HbA1c %). | number | numeric (%); observed range in this file: 2–16.4 | maybe |
| energy | Total energy intake from 24-hour dietary recall (day 1). NHANES dietary day 1 total nutrients: DR1TKCAL. | number | numeric (kcal/day); observed range in this file: 0–13687 | maybe |
| protein | Protein intake from 24-hour dietary recall (day 1). NHANES dietary day 1 total nutrients: DR1TPROT. | number | numeric (g/day); observed range in this file: 0–387.37 | maybe |
| Carbohydrate | Total carbohydrate intake from 24-hour dietary recall (day 1). NHANES dietary day 1 total nutrients: DR1TCARB. | number | numeric (g/day); observed range in this file: 0–1815.02 | maybe |
| Dietary fiber | Dietary fiber intake from 24-hour dietary recall (day 1). NHANES dietary day 1 total nutrients: DR1TFIBE. | number | numeric (g/day); observed range in this file: 0–107 | maybe |
| Total fat | Total fat intake from 24-hour dietary recall (day 1). NHANES dietary day 1 total nutrients: DR1TTFAT. | number | numeric (g/day); observed range in this file: 0–553.79 | maybe |
| Total saturated fatty acids | Total saturated fatty acids from 24-hour dietary recall (day 1). NHANES dietary day 1 total nutrients: DR1TSFAT. | number | numeric (g/day); observed range in this file: 0–205.673 | maybe |
| Total monounsaturated fatty acids | Total monounsaturated fatty acids from 24-hour dietary recall (day 1). NHANES dietary day 1 total nutrients: DR1TMFAT. | number | numeric (g/day); observed range in this file: 0–221.673 | maybe |
| Total polyunsaturated fatty acids | Total polyunsaturated fatty acids from 24-hour dietary recall (day 1). NHANES dietary day 1 total nutrients: DR1TPFAT. | number | numeric (g/day); observed range in this file: 0–147.082 | maybe |
| Potassium | Potassium intake from 24-hour dietary recall (day 1). NHANES dietary day 1 total nutrients: DR1TPOTA. | number | numeric (mg/day); observed range in this file: 0–14812 | maybe |
| Sodium | Sodium intake from 24-hour dietary recall (day 1). NHANES dietary day 1 total nutrients: DR1TSODI. | number | numeric (mg/day); observed range in this file: 7–20183 | maybe |


## Suggested NHANES source components (typical)
- Demographics: RIAGENDR, RIDAGEYR (derived age group), RIDRETH1, DMDMARTL
- Health insurance: HIQ011
- Health status: HSD010
- Depression screener: DPQ (PHQ-style frequency items)
- Sleep: SLQ / SLD variables
- Physical activity: PAD680 (minutes sedentary)
- Exam: BMXWAIST, BPX systolic/diastolic
- Labs: HDL, triglycerides, LDL, fasting glucose, HbA1c
- Dietary recall: DR1TOT (day 1 total nutrient intakes)

## References (for conventions and units)
- NHANES missing value coding guidance: https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/faq.aspx
- General health condition codes (HSD010): https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2013/DataFiles/HSQ_H.htm
- Blood pressure units (mm Hg): https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2013/DataFiles/BPX_H.htm
- HDL and triglyceride SI unit conversions: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/HDL_J.htm and https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/TRIGLY_J.htm
- Fasting glucose SI unit conversion: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/P_GLU.htm
- Dietary nutrient units (energy kcal, macros g, sodium/potassium mg): https://www.ars.usda.gov/ARSUserFiles/80400530/pdf/1112/var_tot_g.pdf
