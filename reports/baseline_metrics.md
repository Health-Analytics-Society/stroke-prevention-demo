# Baseline Metrics

## Model
Logistic Regression (class_weight=balanced, DP-4)

## Split
test_size: 0.2
random_state: 42
stratify: yes

## Label balance
Counts
stroke
0    4241
1     362

## Leakage columns dropped (DP-6)
Dropped: ['General health condition', 'Minutes sedentary activity', 'depression']

## Metrics on test set

### Before DP-4 (original baseline, no class weight fix)
- ROC AUC: 0.6045
- Recall: 0.0000

### After DP-4 + DP-6 (class_weight=balanced, leakage dropped)
Accuracy: 0.6547
Precision: 0.1108
Recall: 0.4861
ROC AUC: 0.6103

## Confusion matrix on test set
Format is [[TN FP]
           [FN TP]]

[[568 281]
 [ 37  35]]

## Threshold Scan (DP-5)
Evaluating thresholds on y_prob from test set.

| Threshold | Precision | Recall | Confusion Matrix |
|---|---|---|---|
| 0.05 | 0.0797 | 1.0000 | [[18, 831], [0, 72]] |
| 0.10 | 0.0831 | 0.9861 | [[66, 783], [1, 71]] |
| 0.20 | 0.0893 | 0.9028 | [[186, 663], [7, 65]] |
| 0.30 | 0.1009 | 0.7917 | [[341, 508], [15, 57]] |

**Default threshold chosen: 0.10** — prioritizes recall (catches most positive cases) while being slightly more selective than 0.05.

## Score Cutoffs (DP-3b)
Predicted probability distribution from test set:

- Min: 0.0127
- Median (50th percentile): 0.3903
- 80th percentile: 0.6236
- 95th percentile: 0.7743
- Max: 0.9501
