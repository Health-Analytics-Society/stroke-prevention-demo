"""
Page 5 — About This Project
FAQ, model card, data source, and full disclaimer.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
from shared import DOCS_DIR, build_sidebar_inputs, read_text

st.set_page_config(
    page_title="About — Stroke Prevention Demo",
    page_icon="ℹ️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.sidebar.title("Health Information")
build_sidebar_inputs()

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.title("ℹ️ About This Project")
st.markdown(
    "A Health Analytics Society initiative exploring stroke risk prediction, "
    "health equity, and the limits of machine learning in clinical contexts."
)
st.divider()

# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------
tab_faq, tab_model, tab_data, tab_team, tab_disc = st.tabs([
    "FAQ", "Model Card", "Data Source", "Team", "Disclaimer",
])

# ---------------------------------------------------------------------------
# FAQ
# ---------------------------------------------------------------------------
with tab_faq:
    faq_text = read_text(DOCS_DIR / "faq.md")
    if faq_text.strip():
        st.markdown(faq_text)
    else:
        st.subheader("Frequently Asked Questions")
        faqs = [
            ("What does this tool do?",
             "It predicts stroke risk from clinical and lifestyle data using a logistic regression model "
             "trained on NHANES survey data. It's designed for educational exploration, not diagnosis."),
            ("What is a stroke?",
             "A stroke occurs when blood flow to part of the brain is blocked (ischemic) or a blood "
             "vessel ruptures (hemorrhagic), causing brain cells to die. It's a leading cause of "
             "disability and death in the US."),
            ("What does my risk score mean?",
             "The score is the model's estimated probability that a patient with your profile had a "
             "stroke event in this dataset. Low: <39%, Moderate: 39–62%, High: >62%. "
             "It is NOT a clinical prognosis."),
            ("How accurate is the model?",
             "ROC AUC ≈ 0.67 overall. Accuracy varies significantly by subgroup — "
             "see the 'Is This Tool Fair?' page for stratified performance."),
            ("Should I use this to make health decisions?",
             "No. This is an educational tool. For medical advice, consult a licensed healthcare provider."),
        ]
        for q, a in faqs:
            with st.expander(q):
                st.write(a)

# ---------------------------------------------------------------------------
# Model Card
# ---------------------------------------------------------------------------
with tab_model:
    st.subheader("Model Card")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
**Algorithm:** Logistic Regression (L2 penalty)
- Solver: `liblinear`
- Regularization: C = 0.1
- Class weighting: `balanced` (to handle 12:1 class imbalance)
- Decision threshold: **0.30** (tuned for recall over precision)
- Max iterations: 2,000

**Training setup:**
- 80/20 stratified train-test split (seed=42)
- 5-fold stratified cross-validation for hyperparameter selection
- Features: 27 (12 categorical + 15 numeric)
- No SHAP or deep learning
        """)

    with c2:
        st.markdown("""
**Overall Performance (test set, n=921):**
| Metric | Value |
|--------|-------|
| ROC AUC | 0.600 |
| Recall (sensitivity) | 0.889 |
| Precision | 0.099 |
| False Negative Rate | 11.1% |
| Operating threshold | 0.30 |

**Intended use:** Education, demonstration, health data literacy.
**Not intended for:** Clinical diagnosis, screening, or any medical decision.
        """)

    st.markdown("---")
    st.markdown("**Features used by the model:**")

    col_cat, col_num = st.columns(2)
    with col_cat:
        st.markdown("""
*Categorical (12):*
- Gender
- Age group (20–39 / 40–59 / 60+)
- Race/Ethnicity
- Marital status
- Alcohol use
- Smoking
- Sleep disorder
- Health Insurance
- Diabetes
- Hypertension
- High cholesterol
- BMI category
        """)

    with col_num:
        st.markdown("""
*Numeric (15):*
- Sleep time (hrs/night)
- Waist circumference (cm)
- Systolic & diastolic BP (mmHg)
- Fasting glucose (mmol/L)
- HbA1c (%)
- Energy, protein, carbohydrate, fiber (g/day)
- Saturated, monounsaturated, polyunsaturated fat (g/day)
- Potassium, sodium (mg/day)
        """)

    st.markdown("---")
    st.markdown("""
**Preprocessing:**
- Categorical columns: most-frequent imputation then one-hot encoding
- Numeric columns: median imputation then standard scaling
- Leakage columns removed from training: *General health condition*, *Depression*, *Minutes sedentary activity*
- Columns not collected in app removed: *Coronary Heart Disease*, *HDL*, *LDL*, *Triglycerides*, *Total fat*

**Fairness note:**
Performance varies significantly across racial/ethnic groups and insurance status.
See the "Is This Tool Fair?" page for full stratified evaluation.
Overall AUC hides a 0.310–0.839 range across subgroups.
The model should not be considered equally reliable for all populations.
    """)

# ---------------------------------------------------------------------------
# Data Source
# ---------------------------------------------------------------------------
with tab_data:
    st.subheader("Data Source")
    st.markdown("""
**National Health and Nutrition Examination Survey (NHANES)**

NHANES is a program of studies conducted by the CDC's National Center for Health Statistics (NCHS)
designed to assess the health and nutritional status of adults and children in the United States.
It combines interviews and physical examinations and is a primary source for national health statistics.

**This dataset:**
- Derived from NHANES cycles with stroke outcome data
- **4,603 participants**, no missing values
- **Stroke prevalence: 7.9%** (362 cases)
- Features include self-reported health, measured vitals, lab values (SI units), and 24-hour dietary recalls

**Race/Ethnicity distribution:**

| Group | n | % |
|-------|---|---|
| Non-Hispanic White | 2,192 | 47.6% |
| Non-Hispanic Black | 1,101 | 23.9% |
| Mexican American | 518 | 11.3% |
| Other Hispanic | 447 | 9.7% |
| Other/Multiracial | 345 | 7.5% |

**Important limitations:**
- NHANES is a cross-sectional survey — it captures a snapshot in time, not causality
- Self-reported variables (smoking, alcohol) are subject to recall and social desirability bias
- Stroke outcome is self-reported ("Has a doctor ever told you that you had a stroke?")
- Dietary recall data (24-hr) is inherently noisy and single-day estimates have high variability
- Social determinants of health (neighborhood, food access, income) are not included

**Units:** Lab values use SI units (glucose in mmol/L, lipids in mmol/L, HbA1c in %).
    """)

# ---------------------------------------------------------------------------
# Team
# ---------------------------------------------------------------------------
with tab_team:
    st.subheader("Health Analytics Society")
    st.markdown("""
This project is built by the **Health Analytics Society** — an interdisciplinary student RSO
exploring the intersection of data science, machine learning, and public health.

**Project goal:** Build a polished, end-to-end demonstration of stroke risk prediction
that showcases health equity analysis, explainability, and the limitations of algorithmic tools in healthcare.

**Stack:**
- Python 3.10+ · pandas · numpy · scikit-learn
- Streamlit (web app)
- Plotly (interactive charts)
- Jupyter (analysis notebooks)

**Source code:** Available in this repository.
    """)

# ---------------------------------------------------------------------------
# Disclaimer
# ---------------------------------------------------------------------------
with tab_disc:
    disc_text = read_text(DOCS_DIR / "disclaimer_and_limitations.md")
    if disc_text.strip():
        st.markdown(disc_text)
    else:
        st.warning(
            "This tool is for educational purposes only. It is not a medical device, "
            "diagnostic tool, or substitute for professional medical advice. "
            "The model was trained on survey data and has not been clinically validated. "
            "Do not make health decisions based on these outputs."
        )
