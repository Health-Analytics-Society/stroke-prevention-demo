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

## Threshold
threshold: 0.3

## Label balance
Counts
stroke
0    4241
1     362

## Metrics on test set
Accuracy: 0.4072
Precision: 0.1037
Recall: 0.8611
ROC AUC: 0.6145

## Confusion matrix on test set
Format is [[TN FP]
           [FN TP]]

[[313 536]
 [ 10  62]]

## Score cutoffs from test set probabilities
- min: 0.007715
- median_p50: 0.388876
- p80: 0.618423
- p95: 0.772234
- max: 0.925453
