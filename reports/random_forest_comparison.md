# Random Forest vs Baseline Comparison
## Split settings (identical for both models)
- test_size: 0.2
- random_state: 42
- stratify: yes
- threshold: 0.3
## Metrics at threshold 0.30

| Metric    | Baseline (LR) | Random Forest |  Delta  |
|-----------|:-------------:|:-------------:|:-------:|
| Accuracy  | 0.3550        | 0.7872        | +0.4322 |
| Precision | 0.0960        | 0.0921        | -0.0039 |
| Recall    | 0.8611        | 0.1944        | -0.6667 |
| ROC AUC   | 0.5830        | 0.5692        | -0.0138 |

## Random Forest confusion matrixFormat:
 [[TN FP] / [FN TP]][[711, 138], [58, 14]]
 
 
 ## Random Forest setting
 - n_estimators: 100
 - class_weight: balanced
 - max_depth: None
 - min_samples_leaf: 5
 
 ## Top 10 features by importance
 - num__Dietary fiber: 0.0569
 - num__Total polyunsaturated fatty acids: 0.0560
 - num__Total saturated fatty acids: 0.0550
 - num__Total monounsaturated fatty acids: 0.0518
 - num__protein: 0.0512- num__Carbohydrate: 0.0510
 - num__Systolic blood pressure: 0.0498
 - num__Waist Circumference: 0.0488
 - num__Sodium: 0.0485
 - num__Fasting Glucose: 0.0484
 
 ## SummaryRandom Forest (100 trees, balanced weights, min_samples_leaf=5)
  - scored ROC AUC 0.5692 vs the logistic regression baseline of 0.5830 (delta -0.0138). 
  - Recall changed from 0.8611 to 0.1944 and precision from 0.0960 to 0.0921. 
  - Logistic Regression outperforms Random Forest on ROC AUC; the baseline remains stronger. 
  - Logistic Regression catches more true stroke cases (higher recall). 
  - Logistic Regression remains the stronger demo model.