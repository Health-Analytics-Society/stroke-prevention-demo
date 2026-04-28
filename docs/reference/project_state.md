# Project State

Last updated: April 28, 2026

## Current Phase

**Demo-ready for educational use.**

The Streamlit app is wired end-to-end: sidebar inputs feed the baseline model,
the main page explains the score, the What If page runs counterfactual scenarios,
the Equity page shows subgroup performance, and the About page includes the
model card, data source notes, FAQ, and disclaimer.

This project is not production-ready for clinical or regulated healthcare use.
It is ready to present as an educational dashboard and public health analytics
demo.

## Completed Scope

| Area | Status | Notes |
|---|---|---|
| Dataset | Done | NHANES-derived stroke dataset in `data/raw/stroke_data.csv` |
| App | Done | Multi-page Streamlit app in `app/` |
| Baseline model | Done | Logistic regression trained at app startup from source data |
| Metrics | Done | App-facing baseline metrics in `reports/baseline_metrics.md` |
| App content | Done | FAQ, risk labels, disclaimer, and next steps in `docs/app_content/` |
| Equity analysis | Done | Subgroup charts and findings in `extra_analysis/health_equity/` |
| Workflow docs | Done | Contributor setup and workflow docs retained in `docs/workflow/` |

## Current App Model

- **Model:** Logistic Regression, L2 penalty
- **Regularization:** `C=0.1`
- **Class weighting:** `balanced`
- **Split for reported metrics:** 80/20 stratified split, `random_state=42`
- **Operating threshold:** `0.30`
- **Held-out ROC AUC:** `0.600`
- **Held-out recall:** `0.889`
- **Held-out precision:** `0.099`

The model is intentionally recall-oriented for demonstration purposes. It should
not be interpreted as clinically reliable.

## Known Limitations

- The dataset is cross-sectional and includes self-reported stroke history.
- The baseline model has weak discrimination and many false positives.
- Subgroup performance varies materially by race/ethnicity and insurance status.
- The app excludes features that are not collected in the sidebar form.
- The app is not externally validated and must not be used for medical decisions.

## Useful Links

- [App input schema](../app_content/app_input_schema.md)
- [Risk labels](../app_content/risk_level_labels.md)
- [Disclaimer](../app_content/disclaimer_and_limitations.md)
- [Baseline metrics](../../reports/baseline_metrics.md)
- [Data dictionary](data_dictionary.md)
- [Leakage candidates](leakage_candidates.md)
