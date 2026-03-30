# Baseline Metrics (Final Demo Baseline)

## Model
Logistic Regression with Elastic Net (penalty=elasticnet, C=1.0, l1_ratio=0.5, solver=saga)

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

## Threshold
threshold: 0.3

## Label balance
Counts
stroke
0    4241
1     362

## Metrics on test set
Accuracy: 0.3768
Precision: 0.0952
Recall: 0.8194
ROC AUC: 0.5868

## Confusion matrix on test set
Format is [[TN FP]
           [FN TP]]

[[288 561]
 [ 13  59]]

## Score cutoffs from test set probabilities
- min: 0.015510
- median_p50: 0.416681
- p80: 0.632803
- p95: 0.760670
- max: 0.896320
