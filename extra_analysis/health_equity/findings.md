# Health Equity & Algorithmic Fairness — Findings

**Health Analytics Society | Stroke Prevention Demo**
**Analysis type:** Stratified model evaluation across race/ethnicity and insurance status
**Dataset:** NHANES-derived, n=4,603 | Model: Logistic Regression (C=0.1, balanced class weight)
**Test set:** n=921 (80/20 stratified split, seed=42) | Threshold: 0.30

---

## Overview

A model with good *overall* performance can still cause harm if it performs systematically worse for specific populations. This analysis evaluates whether our baseline stroke risk model is **equally reliable across racial/ethnic groups and insurance status** — with special attention to **false negative rates (FNR)**, which measure how often the model misses real stroke cases.

In clinical terms: a high FNR for a subgroup means patients in that group are more likely to receive a falsely reassuring "low risk" score.

---

## Key Metrics Explained

| Metric | Definition | Why it matters |
|--------|-----------|----------------|
| **AUC** | Area under the ROC curve — overall discrimination ability | Lower AUC = model is worse at separating stroke vs. no-stroke for that group |
| **Recall (Sensitivity)** | Proportion of actual stroke cases correctly flagged | Lower recall = more missed strokes |
| **FNR** | `1 - Recall` — proportion of stroke cases the model *misses* | The most clinically dangerous disparity |
| **FPR** | Rate of false alarms (no stroke, flagged as high risk) | Affects over-treatment burden |

---

## Findings: Stratified by Race/Ethnicity

| Subgroup | n | Stroke cases | AUC | Recall | FNR | FPR |
|----------|---|-------------|-----|--------|-----|-----|
| Mexican American | 105 | 9 | 0.544 | 0.667 | 0.333 | 0.521 |
| Other Hispanic | 101 | 3 | 0.381 | 0.333 | **0.667** | 0.551 |
| Non-Hispanic White | 467 | 44 | 0.611 | 0.932 | **0.068** | 0.702 |
| Non-Hispanic Black | 199 | 12 | 0.585 | 0.833 | 0.167 | 0.679 |
| Other/Multiracial | 49 | 4 | 0.856 | 1.000 | **0.000** | 0.556 |
| **Overall** | **921** | **72** | **0.611** | **0.861** | **0.139** | **0.651** |

### Interpretation

**AUC disparity:**
AUC ranges from 0.381 (Other Hispanic) to 0.856 (Other/Multiracial) — a spread of 0.475 points. The model discriminates best for Non-Hispanic White patients (0.611, matching overall) and Other/Multiracial (0.856), and worst for Other Hispanic (0.381), which is barely better than random guessing (0.5). This likely reflects severe underrepresentation: Other Hispanic has only 447 training examples vs. 2,192 for Non-Hispanic White — the model has simply learned less about this group's risk patterns.

**False Negative Rate disparity — the headline finding:**
The FNR gap between the best and worst-performing racial groups is **59.9 percentage points**:

- Non-Hispanic White: FNR = **6.8%** — 1 in 15 stroke cases missed
- Other Hispanic: FNR = **66.7%** — 2 in 3 stroke cases missed
- Mexican American: FNR = **33.3%** — 1 in 3 stroke cases missed
- Non-Hispanic Black: FNR = **16.7%** — 1 in 6 stroke cases missed

Put plainly: **if this model were deployed in a clinic, a Hispanic patient with a stroke would be more than 9× as likely to be told "low risk" as a Non-Hispanic White patient.**

**AUC note for Other/Multiracial:**
The very high AUC (0.856) with a small n=49 and only 4 stroke cases should be treated with caution — this is likely a statistical artifact of the small sample, not a genuine signal that the model works better for this group.

---

## Findings: Stratified by Insurance Status

| Subgroup | n | Stroke cases | AUC | Recall | FNR | FPR |
|----------|---|-------------|-----|--------|-----|-----|
| Insured | 801 | 65 | 0.610 | 0.908 | 0.092 | 0.683 |
| Uninsured | 120 | 7 | 0.507 | 0.429 | **0.571** | 0.442 |
| **Overall** | **921** | **72** | **0.611** | **0.861** | **0.139** | **0.651** |

### Interpretation

**FNR gap (Uninsured − Insured): +0.479 (+47.9 percentage points)**

The model misses **57.1% of strokes in uninsured patients** vs. **9.2% in insured patients**. This is a nearly 5× difference in missed stroke rate.

The AUC for uninsured patients is 0.507 — statistically indistinguishable from a coin flip. For uninsured individuals, the model provides essentially **no predictive value** for stroke detection.

This compounds an existing structural disparity: uninsured patients already face barriers to preventive care, have fewer follow-up touchpoints, and are less likely to catch a missed risk early. A tool that performs worst for the population least able to absorb the consequences of a missed diagnosis is actively misaligned with health equity goals.

---

## Intersectional Findings (Race × Insurance)

Groups below met the minimum threshold (n ≥ 8, stroke cases ≥ 3) for reporting:

| Subgroup | n | Stroke cases | AUC | Recall | FNR |
|----------|---|-------------|-----|--------|-----|
| Mexican American / Insured | 77 | 4 | 0.729 | 1.000 | **0.000** |
| Mexican American / Uninsured | 28 | 5 | 0.522 | 0.400 | **0.600** |
| Other Hispanic / Insured | 89 | 3 | 0.341 | 0.333 | **0.667** |
| Non-Hispanic White / Insured | 423 | 43 | 0.595 | 0.953 | **0.047** |
| Non-Hispanic Black / Insured | 168 | 11 | 0.533 | 0.818 | **0.182** |
| Other/Multiracial / Insured | 44 | 4 | 0.856 | 1.000 | **0.000** |

**Highest FNR group:** Other Hispanic / Insured — FNR = 66.7% (n=89, only 3 stroke cases met the filter threshold; interpret with caution on sample size)

**Worst practically-sized group:** Mexican American / Uninsured — FNR = 60.0% (n=28, 5 strokes). Despite being a larger subgroup with more stroke cases, the model misses 3 of 5 strokes.

**Best-performing group:** Non-Hispanic White / Insured — FNR = 4.7%. This is the reference group that effectively dominates the training distribution (largest n, most stroke cases).

**Widest gap:** Non-Hispanic White / Insured (FNR 4.7%) vs. Other Hispanic / Insured (FNR 66.7%) — **a 62pp intersectional gap** even when both groups are insured, meaning insurance status alone does not explain the disparity.

---

## Score Distribution Analysis

*(Refer to `score_distribution_by_race.png` generated by Section 6 of the notebook)*

The score histograms reveal the mechanism behind the FNR gaps:

- **Non-Hispanic White stroke cases** spread broadly above the 0.30 threshold — many score 0.4–0.9, making them easy to flag correctly.
- **Other Hispanic and Mexican American stroke cases** cluster more heavily in the 0.05–0.30 range — many fall just below the threshold, causing them to be missed.
- The threshold of 0.30 is implicitly calibrated to the dominant (Non-Hispanic White) distribution. A group-specific threshold would produce more equitable recall across groups.

---

## Why Does This Happen?

Several mechanisms explain this pattern:

1. **Training data imbalance — the primary driver.** Non-Hispanic White patients represent 2,192 of 4,603 observations (47.6%); Other Hispanic only 447 (9.7%) and Mexican American 518 (11.2%). The model has far less signal to learn Hispanic stroke risk patterns, and its decision boundary reflects what works for the majority group.

2. **Threshold effects.** A single global threshold (0.30) applied uniformly penalizes groups whose score distributions shift lower. Even if risk is real, if it doesn't surface above 0.30 in the model's output space, the patient is classified as low risk.

3. **Proxy features.** Features like BMI, diet variables, and blood pressure correlate with race due to social determinants of health. The model may have learned associations for these proxies primarily from the Non-Hispanic White majority, and those patterns don't generalize equally across groups.

4. **Missing variables.** Structural factors — neighborhood food access, healthcare utilization history, chronic stress, language barriers — that predict stroke disparities in Hispanic populations are not captured in this dataset. The model cannot account for what it cannot see.

---

## Potential Mitigations

| Approach | Description | Complexity |
|----------|-------------|------------|
| **Stratified thresholds** | Tune threshold per group to equalize FNR (e.g., lower threshold for Other Hispanic) | Low — requires calibration holdout |
| **Reweighting by subgroup** | Upweight Hispanic and uninsured patients during training | Medium |
| **Fairness-aware learning** | Use `fairlearn` with equalized odds or FNR constraints | Medium–High |
| **Oversample underrepresented groups** | SMOTE or similar within-group oversampling | Medium |
| **Better data** | Include SDoH variables (zip code, income, food access, language) | High — dataset limitation |
| **Disaggregated reporting standard** | Always publish stratified metrics alongside aggregate metrics — costs nothing | None |

---

## Takeaway for the Demo

The model achieves an overall AUC of 0.611 and overall FNR of 13.9% — numbers that look acceptable in isolation. But stratified evaluation reveals that this aggregate performance is carried almost entirely by Non-Hispanic White patients (n=467, 50.7% of the test set). For Other Hispanic patients, the model is effectively no better than random.

This is the core health equity problem with algorithmic tools in healthcare: **optimizing overall metrics does not prevent the creation of a two-tiered system** where well-represented populations benefit and underrepresented populations are left worse off.

The Health Analytics Society's demo is well-positioned to make this concrete: showing stratified FNR alongside aggregate AUC is exactly the analytical move that separates a thoughtful health data science project from a generic classification exercise.

---

*Generated from: `health_equity_analysis.ipynb` | Test set: n=921, seed=42, threshold=0.30*
*Model: Logistic Regression, C=0.1, class_weight=balanced, solver=liblinear*
