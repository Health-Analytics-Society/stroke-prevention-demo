# Open GitHub Issues

---

## Issue #18 — Draft "Recommended Next Steps" mapping (DC-2)

**Lane:** Docs + Content  
**Difficulty:** 🟡 Medium  
**Dependencies:** ⛓️ Depends on: **DC-1 data dictionary exists** (so factors map to real dataset columns)

**Why this dependency exists (short)**  
We want tips tied to real inputs in our dataset, not generic health advice.

**Goal**  
Turn health inputs into clear "what to do next" tips that are easy to understand.

**Tasks**
- Create or edit: `docs/content/recommended_next_steps.md`
- Pick 10 modifiable factors that match real dataset columns (use DC-1)
- For each factor, write:
  - **Risk factor:** (must match a dataset column name)
  - **Why it matters:** (1 short sentence)
  - **Recommended next steps:** (2–3 bullets)

**Suggested column pool (choose from these)**
Use column names exactly as written:
- `smoke`
- `alcohol ` (note: trailing space in dataset column name)
- `sleep time`
- `Minutes sedentary activity`
- `Body Mass Index`
- `Waist Circumference`
- `Systolic blood pressure`
- `Diastolic blood pressure`
- `Fasting Glucose`
- `Glycohemoglobin`
- `High-density lipoprotein`
- `Low-density lipoprotein`
- `Triglyceride`
- `Sodium`
- `Potassium`
- `Total fat`
- `Dietary fiber`

**Output:** `docs/content/recommended_next_steps.md`

**Quality Rules**
- Do not claim clinical guarantees
- Keep language simple and actionable

**Done when**
- File exists with 10 mapped factors
- Issue comment pastes the final content or links the PR
- If you edited files, open a PR and link it in the issue

---

## Issue #22 — Data sanity check notebook (DP-3)

Lane: Data + Pipeline  
Difficulty: 🟢 Easy  
Dependencies: ⛓️ Depends on: **Dataset loads successfully**

Why this dependency exists (short)  
The whole point is to print real outputs. If the dataset doesn't load, you can't run the checks.

Goal  
Confirm the data looks normal before we trust any model results.

Tasks  
- Create a notebook: `notebooks/data_sanity_check.ipynb`  
- In the notebook, print:
  - Number of rows and columns
  - Stroke label counts and percent
  - Full list of column names
  - For 5 numeric columns: min and max values (pick any 5 numeric columns)

Output  
File(s): `notebooks/data_sanity_check.ipynb`

Quality Rules  
- Notebook must run top to bottom without errors  
- Paste outputs or screenshots into the issue comment

Done when  
- Notebook exists and runs  
- Issue comment includes the outputs or screenshots  
- If you edited files, open a PR and link it in the issue  

---

## Issue #23 — Disclaimer + limitations text (DC-3)

Lane: Docs + Content  
Difficulty: 🟢 Easy  
Dependencies: ✅ none

Short explanation (why no dependency)  
This text can be written immediately and reused everywhere (app, README, slides) regardless of model status.

Goal  
Have clean wording we can paste into the app, README, and final slides.

Tasks  
- Create: `docs/disclaimer_and_limitations.md`  
- Add these 3 sections:

**Not medical advice** (2–3 sentences)  
**Educational purpose** (1–2 sentences)  
**Limitations** (3 bullets)

Output  
File(s): `docs/disclaimer_and_limitations.md`

Quality Rules  
- Keep it short and clear  
- Limitations bullets should be specific (dataset bias, simple model, not clinically validated)
- If you don't know, ask a lead to debrief you on the scope of the project

Done when  
- File exists with all 3 sections  
- Issue comment: "Disclaimer ready for app/README"  
- If you edited files, open a PR and link it in the issue  

---

## Issue #24 — Risk level labels (low/medium/high) (DC-5)

**Lane:** Docs + Content  
**Difficulty:** 🟢 Easy  
**Dependencies:** ⛓️ Depends on: **DP team provides typical model score cutoffs** from the test set probabilities (min, median, 80th percentile, 95th percentile, max)

**Why this dependency exists (short)**  
Docs + Content team doesn't run code. We need the Data + Pipeline team to provide the score distribution so we can make labels.

**Goal**  
Make the risk score easier to understand by adding simple labels.

**Tasks**
- Create: `docs/content/risk_level_labels.md`
- Use the cutoffs provided by the DP team to define bins such as:
  - Low: min to 80th percentile
  - Medium: 80th percentile to 95th percentile
  - High: above 95th percentile
- Keep labels simple and readable as percentages
- Add this sentence: "These are demo labels, not clinical thresholds."

**Output:** `docs/content/risk_level_labels.md`

**Quality Rules**
- Do NOT guess bins
- Use the cutoffs provided by DP in the issue comment or report

**Done when**
- File exists with bins + disclaimer
- Issue comment states what bins you used and references the DP-provided cutoffs
- If you edited files, open a PR and link it in the issue

---

## Issue #25 — Results section layout (placeholders only) (APP-1)

**Lane:** App  
**Difficulty:** 🟢 Easy  
**Dependencies:** ✅ none

**Goal**  
Make the Streamlit app look real even before model wiring is finished.

**Tasks**
- In Streamlit, add a Results section/page that shows:
  - Header: "Your Stroke Risk Score"
  - Placeholder: "Risk score: 12% (example)"
  - Header: "Prevention Tips"
  - Placeholder list of 3 bullets (these can be generic placeholders for now)
  - Header: "Disclaimer"
  - Placeholder disclaimer text for now
- Add a short note in the code indicating DC-3 will replace the placeholder disclaimer text when ready

**Output:** Streamlit app file(s)

**Quality Rules**
- Keep layout clean and simple
- Placeholders are allowed in this ticket

**Done when**
- Results section exists and displays all placeholders
- Issue comment includes a screenshot of the Results section
- If you edited files, open a PR and link it in the issue

---

## Issue #26 — "Example Mode" toggle (APP-2)

**Lane:** App  
**Difficulty:** 🟡 Medium  
**Dependencies:** ⛓️ Depends on: **APP-1 exists** and **DC-2 + DC-3 exist** (so example tips and disclaimer text are consistent across app and docs)

**Why this dependency exists (short)**  
Example Mode needs real placeholder content (tips + disclaimer) that comes from Docs + Content.

**Goal**  
Let users switch between "example output" and "real model output coming soon."

**Tasks**
- Add a checkbox/toggle: "Use example output"
- If checked, show:
  - Example risk score
  - Example prevention tips (3 bullets) pulled from DC-2
- If unchecked, show:
  - "Model output coming soon" message
- Always show disclaimer text from DC-3 in the Results section

**Output:** Streamlit app file(s)

**Quality Rules**
- Keep the UI simple and obvious
- Do not write new prevention tips in the app; reuse DC-2
- Do not write a new disclaimer in the app; reuse DC-3

**Done when**
- Toggle works and switches output states correctly
- Example Mode displays 3 prevention tips sourced from DC-2
- Disclaimer section displays text sourced from DC-3
- Issue comment includes a screenshot or short screen recording
- If you edited files, open a PR and link it in the issue

---

## Issue #32 — Baseline Fix: class imbalance (DP-4)

Lane: Data + Pipeline  
Difficulty: 🟢 Easy  
Dependencies: ⛓️ Depends on: Baseline training notebook runs end to end and writes reports/baseline_metrics.md

Why this dependency exists (short)  
We need a working baseline first so we can measure whether class imbalance fixes actually help.

Goal  
Get the baseline to predict at least some positives so recall is not stuck at 0.

Tasks  
- In the baseline notebook, change LogisticRegression to use `class_weight="balanced"`  
- Rerun baseline with the same split settings (test_size 0.2, seed 42, stratify yes)  
- Update `reports/baseline_metrics.md` with the new metrics and confusion matrix

Output  
File(s): `reports/baseline_metrics.md` updated

Quality Rules  
- Do not change the split settings  
- Evaluate on test set only  
- Notebook runs top to bottom without errors

Done when  
- New report is saved and includes updated metrics  
- Issue comment includes the new metrics and confusion matrix  
- PR opened and linked

---

## Issue #33 — Baseline Fix: class imbalance (DP-4)

Lane: Data + Pipeline  
Difficulty: 🟢 Easy  
Dependencies: ⛓️ Depends on: Baseline training notebook runs end to end and writes reports/baseline_metrics.md

Why this dependency exists (short)  
We need a working baseline first so we can measure whether class imbalance fixes actually help.

Goal  
Get the baseline to predict at least some positives so recall is not stuck at 0.

Tasks  
- In the baseline notebook, change LogisticRegression to use `class_weight="balanced"`  
- Rerun baseline with the same split settings (test_size 0.2, seed 42, stratify yes)  
- Update `reports/baseline_metrics.md` with the new metrics and confusion matrix

Output  
File(s): `reports/baseline_metrics.md` updated

Quality Rules  
- Do not change the split settings  
- Evaluate on test set only  
- Notebook runs top to bottom without errors

Done when  
- New report is saved and includes updated metrics  
- Issue comment includes the new metrics and confusion matrix  
- PR opened and linked

---

## Issue #34 — Quick Threshold Scan: choose a demo threshold (DP-5)

Lane: Data + Pipeline  
Difficulty: 🟢 Easy  
Dependencies: ⛓️ Depends on: DP-4 complete

Why this dependency exists (short)  
Risk labels and the app need a default threshold that produces nonzero positives.

Goal  
Pick a simple default probability threshold for demo classification.

Tasks  
- Using `y_prob` on the test set, evaluate thresholds: 0.05, 0.10, 0.20, 0.30  
- For each threshold, print precision, recall, and confusion matrix  
- Pick one threshold and write one short sentence why (example: prioritize recall)

Output  
File(s): Add a short section to `reports/baseline_metrics.md` called "Threshold Scan"

Quality Rules  
- Same split settings as baseline  
- Keep it simple, no hyperparameter tuning  
- Do not claim clinical thresholds

Done when  
- Threshold scan results are added to the report  
- A default threshold is chosen and documented  
- PR opened and linked

---

## Issue #35 — Drop Confirmed Leakage Columns: rerun baseline (DP-6)

Lane: Data + Pipeline  
Difficulty: 🟢 Easy  
Dependencies: ⛓️ Depends on: `docs/content/leakage_candidates.md` exists AND **DP-4 is complete** (baseline predicts some positives so comparisons are meaningful)

Why this dependency exists (short)  
We want to avoid fake improvements caused by post-stroke proxy variables, and we want the before/after comparison to be interpretable (not stuck at all-zero predictions).

Goal  
Remove columns marked "yes leakage" and compare metrics.

Tasks  
- Use `docs/leakage_candidates.md`
- In the baseline notebook, drop columns marked "yes leakage" before the split  
- Rerun baseline with the same split settings  
- Update `reports/baseline_metrics.md` with the new metrics  
- Add 2 bullet comparison: old vs new ROC AUC and recall

Output  
File(s): `reports/baseline_metrics.md` updated

Quality Rules  
- Do not change split settings  
- Only drop "yes leakage" columns, not "maybe"  
- If a column name mismatch happens, note it and skip it

Done when  
- Report updated and comparison included  
- Issue comment summarizes differences  
- PR opened and linked

---

## Issue #36 — Export Baseline Pipeline for App Use (DP-7)

Lane: Data + Pipeline  
Difficulty: 🟢 Easy  
Dependencies: ⛓️ Depends on: **DP-6 complete** (leakage columns dropped) and baseline notebook runs end to end

Why this dependency exists (short)  
We want the app to load the clean baseline model (class imbalance handled and leakage removed) without retraining every time.

Goal  
Save the trained preprocessing + model pipeline so the app can load it for real outputs.

Tasks  
- In the baseline notebook after training, save the full pipeline (preprocessing + model) to:  
  - `models/baseline_pipeline.joblib`
- Create the `models/` folder if it does not exist
- Add a short markdown note in the notebook showing how to load it back, example:  
  - `pipeline = joblib.load("models/baseline_pipeline.joblib")`

Output  
File(s): `models/baseline_pipeline.joblib`  
File(s) optional: short note in notebook or `docs/model_loading.md`

Quality Rules  
- Use the same standardized split settings (test_size 0.2, seed 42, stratify yes)
- Do not change model settings in this ticket
- If the file is too large to commit, document an alternative storage plan in the issue comment

Done when  
- Pipeline save runs without errors and the file exists locally  
- Issue comment includes the save path and the load snippet  
- If you edited files, open a PR and link it in the issue
