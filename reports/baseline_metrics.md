# Baseline Metrics

This report matches the model configuration used by the Streamlit app.

## Model
Logistic Regression with L2 penalty

- `solver`: `liblinear`
- `C`: `0.1`
- `class_weight`: `balanced`
- `max_iter`: `2000`

## Split
test_size: 0.2
random_state: 42
stratify: yes

## Leakage handling
Dropped columns
- General health condition
- depression
- Minutes sedentary activity
- Coronary Heart Disease
- High-density lipoprotein
- Triglyceride
- Low-density lipoprotein
- Total fat

## Feature columns used by the pipeline
- gender
- age
- Race
- Marital status
- alcohol
- smoke
- sleep disorder
- Health Insurance
- sleep time
- diabetes
- hypertension
- high cholesterol
- Body Mass Index
- Waist Circumference
- Systolic blood pressure
- Diastolic blood pressure
- Fasting Glucose
- Glycohemoglobin
- energy
- protein
- Carbohydrate
- Dietary fiber
- Total saturated fatty acids
- Total monounsaturated fatty acids
- Total polyunsaturated fatty acids
- Potassium
- Sodium

## Threshold
threshold: 0.3

## Label balance
Counts
stroke
0    4241
1     362

Proportions
stroke
0    0.921356
1    0.078644

## Metrics on test set
Accuracy: 0.3561
Precision: 0.0986
Recall: 0.8889
False Negative Rate: 0.1111
ROC AUC: 0.5995

## Confusion matrix on test set
Format is [[TN, FP], [FN, TP]]

[[264, 585], [8, 64]]

## Score cutoffs from test set probabilities
- min: 0.014779
- median_p50: 0.419332
- p80: 0.622469
- p95: 0.743040
- max: 0.904589

## Threshold scan
- threshold=0.05 | precision=0.0786 | recall=1.0000 | cm=[[5, 844], [0, 72]]
- threshold=0.10 | precision=0.0795 | recall=0.9722 | cm=[[38, 811], [2, 70]]
- threshold=0.20 | precision=0.0883 | recall=0.9444 | cm=[[147, 702], [4, 68]]
- threshold=0.30 | precision=0.0986 | recall=0.8889 | cm=[[264, 585], [8, 64]]

## Interpretation

This is a recall-oriented educational baseline, not a clinical model. At the 0.30 operating threshold it catches most held-out stroke cases, but it also creates many false positives and has weak discrimination overall.
