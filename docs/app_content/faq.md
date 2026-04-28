# Frequently Asked Questions (FAQ)

This FAQ answers the most common questions about the Stroke Prevention Demo app.

---

## About the tool

### What is this tool?

The Stroke Prevention Demo is an educational app that takes basic health and demographic inputs, runs a statistical risk model, and returns a stroke risk score along with plain-language prevention tips. It was built as a student learning project to explore how public health data can illustrate stroke risk factors.

### Who built this?

This demo was built by students at the Health Analytics Society (HAS). It is a learning project, not a commercial or clinical product.

### Is this free to use?

Yes. The demo is freely available as an educational resource. No account or payment is required.

---

## About stroke

### What is a stroke?

A stroke occurs when blood flow to part of the brain is cut off — either by a blocked artery (ischemic stroke, the most common type) or a burst blood vessel (hemorrhagic stroke). Brain cells begin to die within minutes, so stroke is a medical emergency.

Common warning signs (FAST):
- **F**ace drooping
- **A**rm weakness
- **S**peech difficulty
- **T**ime to call emergency services

### What are the main risk factors for stroke?

Major modifiable risk factors include high blood pressure, smoking, diabetes, high cholesterol, physical inactivity, heavy alcohol use, obesity, and poor diet. Non-modifiable factors include age, sex, race/ethnicity, and family history.

---

## About the risk score

### What does the risk score number mean?

The score is the model's estimated probability (0 to 1, or 0% to 100%) that your input profile resembles the profiles of people in the training data who reported having had a stroke. A higher score means more co-occurring risk factors are present in your profile compared to the dataset average.

**The score is not a clinical probability.** It does not mean you have a 1-in-X chance of having a stroke. It is a relative ranking for educational purposes only.

### What do "Low," "Moderate," and "High" mean?

These labels group your score into three bands based on where it falls compared to the test-set score distribution from the baseline model:

| Label | Score range | Meaning |
|---|---|---|
| Low | Below ~0.42 (below median) | Fewer co-occurring risk factors relative to the dataset |
| Moderate | ~0.42 – ~0.62 (median to 80th percentile) | Several risk factors present |
| High | Above ~0.62 (top 20%) | Multiple high-weight risk factors active in your profile |

See `docs/app_content/risk_level_labels.md` for full details and display copy.

### Why might my score seem high even though I feel healthy?

The model was trained on self-reported and measured NHANES survey data and balances for class imbalance (stroke cases are rare, about 8% of the dataset). This means it is deliberately calibrated to be sensitive to stroke-related patterns, which can raise scores for people with even a few co-occurring risk factors. The score reflects patterns across a large population, not a precise individual prediction.

### Why might my score seem low even though I know I have risk factors?

The model only uses the inputs you provide through the app form. If a risk factor is not one of the included inputs — or if you left a field at its default — it will not influence the score.

---

## About the model

### How was the model built?

The model is a logistic regression trained on an NHANES-derived dataset:

- **Dataset:** 4,603 participants, ~8% with a reported stroke history
- **Split:** 80% training / 20% test, stratified by stroke status, random seed 42
- **Class imbalance handling:** `class_weight="balanced"` (the model is penalized more for missing stroke cases)
- **Threshold:** 0.30 (scores at or above 0.30 are flagged as high risk for yes/no output; the continuous score is always shown)
- **Leakage columns excluded:** `General health condition`, `depression`, `Minutes sedentary activity` (these can reflect post-stroke consequences rather than pre-stroke risk)
- **App-only exclusions:** `Coronary Heart Disease`, lipid panel columns, and `Total fat` are excluded because the app does not collect them

Full details: `reports/baseline_metrics.md` and `src/train_baseline.py`.

### How accurate is the model?

On the held-out test set (at the 0.30 threshold):

| Metric | Value |
|---|---|
| ROC AUC | 0.60 |
| Recall (sensitivity) | 0.89 |
| Precision | 0.10 |
| Accuracy | 0.36 |

ROC AUC of 0.60 means the model ranks a randomly chosen stroke case above a randomly chosen non-stroke case about 60% of the time — slightly better than random (0.50) but far below clinical-grade tools. This is a baseline model and has not been optimized or externally validated.

Recall (0.89) is high because the model was tuned to catch stroke cases even at the cost of more false alarms. This is intentional for a prevention demo — missing a true case is treated as worse than a false alarm.

### Why were "General health condition," "depression," and "Minutes sedentary activity" left out?

These three columns carry leakage risk. Because the dataset is cross-sectional (all data collected at the same moment), these values can reflect **consequences** of a prior stroke rather than pre-stroke risk factors:

- **General health condition:** Self-rated health often declines after a stroke.
- **Depression:** Depression rates are elevated after stroke.
- **Minutes sedentary activity:** Reduced mobility after stroke inflates sedentary time.

Including them would make the model appear more accurate than it really is for actual prevention use. See `docs/reference/leakage_candidates.md` for the full analysis.

### What data was used to train the model?

The model was trained on an NHANES-derived dataset (National Health and Nutrition Examination Survey, administered by the CDC). NHANES combines interviews, physical exams, and lab work from a nationally representative U.S. sample. The version in this project has been pre-cleaned and includes 4,603 adult participants.

See `docs/reference/data_dictionary.md` for a full column-by-column breakdown.

---

## Using the app

### Which inputs does the app ask for?

The app collects the inputs listed in `docs/app_content/app_input_schema.md`. These include demographic information (age group, sex, race/ethnicity, marital status), lifestyle factors (smoking, alcohol use, sleep), and clinical indicators (blood pressure, cholesterol, BMI, diabetes, hypertension, etc.).

### Do I need lab results to use the app?

Some fields — like blood pressure readings, fasting glucose, and cholesterol values — come from lab or clinical measurements. If you do not know those values, you can use approximate or default values and take the result as a rough illustration rather than a precise score. The app is designed for education, not clinical intake.

### What should I do if I get a high risk score?

Review the recommended next steps shown in the app. These are plain-language actions tied to the specific risk factors in your profile. Then:

1. Share this result with your primary care doctor at your next visit.
2. Do not make sudden changes to any medications based on this score.
3. Focus on one or two modifiable factors (smoking, blood pressure, activity level) rather than trying to change everything at once.

See `docs/app_content/recommended_next_steps.md` for the full list of next steps.

### Is this medical advice?

No. This tool is not a substitute for professional medical care. See `docs/app_content/disclaimer_and_limitations.md` for the full disclaimer.

---

## Technical questions

### Where can I find the source code?

The source code lives in the GitHub repository associated with this project. The main app file is `app/streamlit_app.py` and the training notebook is `notebooks/final_demo_baseline_model.ipynb`.

### How do I run the app locally?

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

**Windows PowerShell:**
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

### How do I contribute or report an issue?

Open a GitHub issue in the repository. If you are an active contributor, see `docs/workflow/workflow.md` for the branching and PR process.
