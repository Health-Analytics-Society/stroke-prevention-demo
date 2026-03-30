# Baseline Metrics (Final Demo Baseline)

## Model
Logistic Regression with Elastic Net (penalty=elasticnet, C=0.1, l1_ratio=0.5, solver=saga)

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
Accuracy: 0.3550
Precision: 0.0960
Recall: 0.8611
ROC AUC: 0.5830

## Confusion matrix on test set
Format is [[TN FP]
           [FN TP]]

[[265 584]
 [ 10  62]]

## Score cutoffs from test set probabilities
- min: 0.029966
- median_p50: 0.413971
- p80: 0.622575
- p95: 0.744849
- max: 0.888002
