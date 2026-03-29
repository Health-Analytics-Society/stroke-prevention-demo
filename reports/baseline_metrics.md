# Baseline Metrics (Final Demo Baseline)

## Model
Logistic Regression

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
Accuracy: 0.3789
Precision: 0.0928
Recall: 0.7917
ROC AUC: 0.5911

## Confusion matrix on test set
Format is [[TN FP]
           [FN TP]]

[[292 557]
 [ 15  57]]

## Score cutoffs from test set probabilities
- min: 0.034606
- median_p50: 0.405626
- p80: 0.631902
- p95: 0.754752
- max: 0.895770
