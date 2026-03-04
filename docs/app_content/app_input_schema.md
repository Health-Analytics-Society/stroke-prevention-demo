<!-- leakage columns are already removed -->
Column_name, Type, Allowed_values/Range, Example;
'stroke', category, 0 = No stroke; 1 = Stroke, "0";
'gender', category, 1 = Male; 2 = Female, "2";
'age', category, 1 = 20–39 years; 2 = 40–59 years; 3 = 60+ years, "2";
'Race', category,  1 = Mexican American; 2 = Other Hispanic; 3 = Non-Hispanic White; 4 = Non-Hispanic Black; 5 = Other race(incl. multiracial), "5";
'Marital status', category, 1 = Married; 2 = Widowed; 3 = Divorced; 4 = Separated; 5 = Never married; 6 = Living with partner
'alcohol ', category,  0 = No; 1 = Yes, "1";
'smoke', category,  0 = No; 1 = Yes, "0";
'sleep disorder', category, 1 = Yes; 2 = No, "0";
'Health Insurance', category, 1 = Yes; 2 = No, "1";
'General health condition', category, 1 = Excellent; 2 = Very good; 3 = Good; 4 = Fair; 5 = Poor, "4";
'depression', category, 1 = Several days; 2 = More than half the days; 3 = Nearly every day, "3";
'sleep time', number, numeric (hours); observed range in this file: 1–14, "7";
'diabetes', category, 0 = No; 1 = Yes, "1";
'hypertension', category, 0 = No; 1 = Yes, "0";
'high cholesterol', category, 0 = No; 1 = Yes, "0";
'Minutes sedentary activity', number, numeric (minutes/day); observed range in this file: 0–1200, "1000";
'Coronary Heart Disease', category, 0 = No; 1 = Yes, "1"
'Body Mass Index', category, 1 = Underweight (<18.5); 2 = Normal (18.5–24.9); 3 = Overweight (25–29.9); 4 = Obese (≥30), "3";
'Waist Circumference', number, numeric (cm); observed range in this file: 63.5–176, "70.0";
'Systolic blood pressure', number, numeric (mm Hg); observed range in this file: 66–238, "80";
'Diastolic blood pressure', number, numeric (mm Hg); observed range in this file: 32–124, ”50“;
'High-density lipoprotein', number, numeric (mmol/L (SI)); observed range in this file: 0.28–5.84, "3.00";
'Triglyceride', number, numeric (mmol/L (SI)); observed range in this file: 0.203–28.778, "1.457";
'Low-density lipoprotein', number, numeric (mmol/L (SI)); observed range in this file: 0.388–9.232, "7.44";
'Fasting Glucose', number, numeric (mmol/L (SI)); observed range in this file: 1.998–26.09, "20.00";
'Glycohemoglobin', number, numeric (%); observed range in this file: 2–16.4, "14.0";
'energy', number, numeric (kcal/day); observed range in this file: 0–13687, "5000";
'protein', number, numeric (g/day); observed range in this file: 0–387.37, "300";
'Carbohydrate', number, numeric (g/day); observed range in this file: 0–1815.02, "1000.00";
'Dietary fiber', number, numeric (g/day); observed range in this file: 0–107, "100";
'Total fat', number, numeric (g/day); observed range in this file: 0–553.79, "450";
'Total saturated fatty acids', number, numeric (g/day); observed range in this file: 0–205.673, "200.00";
'Total monounsaturated fatty acids', number, numeric (g/day); observed range in this file: 0–221.673, "220.00";
'Total polyunsaturated fatty acids', number, numeric (g/day); observed range in this file: 0–147.082, "140";
'Potassium', number, numeric (mg/day); observed range in this file: 0–14812, "14120";
'Sodium', number, numeric (mg/day); observed range in this file: 7–20183, "20183";