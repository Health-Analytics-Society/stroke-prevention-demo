# Risk Level Labels

This document defines simple risk level labels (Low / Medium / High) for the demo stroke risk score.

## Source of Cutoffs

Cutoffs were provided by the Data + Pipeline team based on predicted probabilities (`y_prob`) from the balanced baseline model (Logistic Regression, `class_weight="balanced"`, test_size=0.2, seed=42, stratify=yes) run on the NHANES-derived dataset (DP-3b).

| Statistic | Value |
|---|---|
| Min | 0.0127 |
| Median (50th percentile) | 0.3903 |
| 80th percentile | 0.6236 |
| 95th percentile | 0.7743 |
| Max | 0.9501 |

## Risk Level Bins

The model outputs a **predicted probability** between 0.0 and 1.0. For display purposes these are shown as percentages (e.g., 0.62 → 62%).

| Risk Level | Probability Range | Percentage Display | Description |
|---|---|---|---|
| 🟢 Low | below 0.6236 | below ~62% | Score is below the 80th percentile of the test set distribution. |
| 🟡 Medium | 0.6236 – 0.7743 | ~62% – ~77% | Score is between the 80th and 95th percentile. |
| 🔴 High | above 0.7743 | above ~77% | Score is above the 95th percentile of the test set distribution. |

## Important Note

These are demo labels, not clinical thresholds. The bins are based on the distribution of predicted probabilities in the NHANES-derived test set and are intended only to make demo outputs interpretable. They should not be used to make any medical or clinical decisions.
