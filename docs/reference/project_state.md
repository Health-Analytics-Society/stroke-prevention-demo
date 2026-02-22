# Project State

Last updated: Week 04 (February 2026)

This file reflects where the project currently stands. Update it when major milestones complete.

---

## Current phase

**Active development — baseline complete, polish + app wiring next.**

We have a working end-to-end pipeline (data → model → metrics). The next phase is improving the model, wiring outputs into the app, and finishing content.

---

## What is done

| Area | Status | Notes |
|---|---|---|
| Dataset selected | ✅ Done | NHANES-derived stroke dataset |
| Data dictionary | ✅ Done | `docs/reference/data_dictionary.md` |
| Leakage candidates | ✅ Done | `docs/reference/leakage_candidates.md` |
| Baseline model | ✅ Done | Logistic regression, see `reports/baseline_metrics.md` |
| Baseline EDA notebook | ✅ Done | `notebooks/example_quick_eda.ipynb` |
| Baseline training notebook | ✅ Done | `notebooks/train_baseline.ipynb` |
| Weekly recaps (Weeks 0–4) | ✅ Done | `docs/reference/recaps/` |
| Workflow docs | ✅ Done | `docs/workflow/` |
| App scaffold | ✅ Done | `app/streamlit_app.py` (placeholder, not wired to model) |

---

## What is in progress

| Area | Status | Notes |
|---|---|---|
| Data sanity check notebook | 🔄 In progress | Started Week 04, not fully finished |
| App content (labels, tips, disclaimers) | 🔄 In progress | Stubs created in `docs/app_content/`, not finalized |

---

## What is not started yet

| Area | Notes |
|---|---|
| Model improvement | Baseline has ROC AUC ~0.60 and predicts all-negative (class imbalance not addressed yet) |
| Feature selection | Leakage candidates identified but not yet formally dropped in pipeline |
| App wiring | Model not connected to Streamlit input form yet |
| Risk score output UI | Risk level labels and next-steps copy not integrated into app |
| Presentation | Final deliverable not started |

---

## Baseline model summary

- **Model:** Logistic Regression
- **Split:** 80/20, stratified by `stroke`, random_state=42
- **Dataset size:** 4,603 rows (4,241 negative / 362 positive stroke cases)
- **Class imbalance:** ~92% negative, ~8% positive — model currently predicts all-negative
- **Test-set metrics:**
  - Accuracy: 0.92 (misleading due to imbalance)
  - Precision: 0.00
  - Recall: 0.00
  - ROC AUC: 0.60

> The baseline is intentionally minimal. The next modeling step is to address class imbalance (e.g., class weights, resampling) and drop confirmed leakage columns.

Full metrics: [`reports/baseline_metrics.md`](../../reports/baseline_metrics.md)

---

## Lane status (as of Week 04)

| Lane | Lead status | Current focus |
|---|---|---|
| Data + Pipeline | Active | Data sanity check, model improvement |
| Docs + Content | Active | App content files, refining reference docs |
| App | Paused | Lead was absent Week 04, resuming when available |

---

## Key decisions made

- **Dataset:** NHANES-derived stroke dataset (individual-level, reputable source, rich features)
- **Model framing:** Prevention-style risk scoring — inputs should not include post-stroke consequences
- **Leakage policy:** `General health condition`, `Minutes sedentary activity`, and `depression` are first-drop candidates
- **No conda:** project uses plain Python `venv`

---

## Links

- [Data dictionary](data_dictionary.md)
- [Leakage candidates](leakage_candidates.md)
- [Baseline metrics](../../reports/baseline_metrics.md)
- [Latest recap](recaps/week-04.md)
- [Workflow overview](../workflow/workflow.md)
