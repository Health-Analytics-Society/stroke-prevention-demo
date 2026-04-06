# Baseline Metrics (Final Demo Baseline)

## Model
Logistic Regression with Elastic Net (penalty=elasticnet, C=1, l1_ratio=0.5, solver=saga)

## Evaluation
method: stratified_k_fold_cv
folds: 5
shuffle: yes
random_state: 42
stratify: yes
outlier_clipping: yes
clip_iqr_multiplier: 2.0

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

## Metrics from 5-fold stratified CV (out-of-fold)
Accuracy: 0.3483
Precision: 0.0993
Recall: 0.9033
ROC AUC: 0.6759

## Confusion matrix from 5-fold stratified CV (out-of-fold)
Format is [[TN FP]
           [FN TP]]

[[1276 2965]
 [  35  327]]

## Per-fold metrics
- fold=1 | n=921 | positives=72 | accuracy=0.3616 | precision=0.1067 | recall=0.9722 | auc=0.6975 | clipped_values=1872
- fold=2 | n=921 | positives=73 | accuracy=0.3626 | precision=0.1046 | recall=0.9315 | auc=0.7022 | clipped_values=1859
- fold=3 | n=921 | positives=73 | accuracy=0.3464 | precision=0.0998 | recall=0.9041 | auc=0.6442 | clipped_values=1883
- fold=4 | n=920 | positives=72 | accuracy=0.3391 | precision=0.0939 | recall=0.8611 | auc=0.6373 | clipped_values=1912
- fold=5 | n=920 | positives=72 | accuracy=0.3315 | precision=0.0917 | recall=0.8472 | auc=0.6978 | clipped_values=1895

## Score cutoffs from CV out-of-fold probabilities
- min: 0.016345
- median_p50: 0.437170
- p80: 0.625333
- p95: 0.751644
- max: 0.910096

## Threshold scan (CV out-of-fold)
- threshold=0.05 | precision=0.0792 | recall=0.9972 | cm=[[45, 4196], [1, 361]]
- threshold=0.10 | precision=0.0811 | recall=0.9945 | cm=[[161, 4080], [2, 360]]
- threshold=0.20 | precision=0.0892 | recall=0.9779 | cm=[[627, 3614], [8, 354]]
- threshold=0.30 | precision=0.0993 | recall=0.9033 | cm=[[1276, 2965], [35, 327]]
