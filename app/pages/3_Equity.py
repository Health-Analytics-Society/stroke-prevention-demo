"""
Page 3 — Is This Tool Fair?
Health equity and algorithmic fairness dashboard.
Shows real stratified model performance and gives users a personalized callout
based on their demographic profile.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import plotly.graph_objects as go
import streamlit as st
from shared import (
    EQUITY_DIR,
    INSURANCE_MAP,
    RACE_MAP,
    build_sidebar_inputs,
)

st.set_page_config(
    page_title="Is This Tool Fair? — Stroke Prevention Demo",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.sidebar.title("Health Information")
st.sidebar.caption("Your Race and Insurance inputs are used for the personalized callout.")
user_inputs = build_sidebar_inputs()

# ---------------------------------------------------------------------------
# Pre-computed metrics for the app's baseline model.
# Test set n=921, seed=42, threshold=0.30, C=0.1 logistic regression.
# ---------------------------------------------------------------------------

# False Negative Rate: probability a REAL stroke case is missed by the model
RACE_FNR = {
    1: 0.333,  # Mexican American
    2: 0.333,  # Other Hispanic
    3: 0.045,  # Non-Hispanic White
    4: 0.167,  # Non-Hispanic Black
    5: 0.000,  # Other/Multiracial (n=49, interpret carefully)
}

RACE_AUC = {
    1: 0.537,
    2: 0.310,
    3: 0.604,
    4: 0.559,
    5: 0.839,
}

RACE_N = {1: 105, 2: 101, 3: 467, 4: 199, 5: 49}
RACE_STROKE_CASES = {1: 9, 2: 3, 3: 44, 4: 12, 5: 4}

INS_FNR  = {1: 0.062, 2: 0.571}
INS_AUC  = {1: 0.596, 2: 0.502}
INS_N    = {1: 801, 2: 120}

OVERALL_FNR = 0.111
OVERALL_AUC = 0.600

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.title("⚖️ Is This Tool Fair?")
st.markdown(
    "A model that performs well **on average** can still systematically fail specific populations. "
    "This page shows how our baseline model performs across racial/ethnic groups and insurance status — "
    "and what that means for the people it's supposed to help."
)
st.divider()

# ---------------------------------------------------------------------------
# Personalized callout
# ---------------------------------------------------------------------------
st.subheader("Your Profile")

if user_inputs:
    race_code = int(user_inputs.get("Race", 3))
    ins_code  = int(user_inputs.get("Health Insurance", 1))
    race_label = RACE_MAP.get(race_code, "Unknown")
    ins_label  = INSURANCE_MAP.get(ins_code, "Unknown")
    race_fnr   = RACE_FNR.get(race_code)
    ins_fnr    = INS_FNR.get(ins_code)

    c1, c2 = st.columns(2)
    with c1:
        pct = int((race_fnr or 0) * 100)
        if race_code == 3:
            color, icon = "green", "✅"
        elif (race_fnr or 0) >= 0.3:
            color, icon = "red", "🚨"
        elif (race_fnr or 0) >= 0.15:
            color, icon = "orange", "⚠️"
        else:
            color, icon = "green", "✅"

        st.markdown(f"**Race/Ethnicity: {race_label}**")
        if race_fnr is not None:
            st.markdown(
                f"{icon} For **{race_label}** patients, this model misses "
                f"**{pct}%** of real stroke cases (False Negative Rate = {race_fnr:.1%})."
            )
            if race_code == 5:
                st.caption("Note: n=49 for this group — interpret with caution due to small sample size.")
        st.caption(f"Overall model FNR: {OVERALL_FNR:.1%}")

    with c2:
        ins_pct = int((ins_fnr or 0) * 100)
        if ins_code == 1:
            ins_icon = "✅"
        else:
            ins_icon = "🚨"
        st.markdown(f"**Insurance Status: {ins_label}**")
        if ins_fnr is not None:
            st.markdown(
                f"{ins_icon} For **{ins_label}** patients, this model misses "
                f"**{ins_pct}%** of real stroke cases (FNR = {ins_fnr:.1%})."
            )
        if ins_code == 2:
            st.warning(
                "Uninsured patients already face barriers to follow-up care. "
                "A model with FNR = 57.1% for this group would provide essentially no reliable warning."
            )

st.divider()

# ---------------------------------------------------------------------------
# FNR comparison — race
# ---------------------------------------------------------------------------
st.subheader("False Negative Rate by Race/Ethnicity")
st.markdown(
    "**FNR = the rate at which real stroke cases are *missed* and labelled 'low risk'.** "
    "A higher FNR means patients in that group are more likely to receive a falsely reassuring score."
)

races = [RACE_MAP[k] for k in sorted(RACE_MAP)]
fnr_vals = [RACE_FNR[k] for k in sorted(RACE_MAP)]
n_vals   = [RACE_N[k]   for k in sorted(RACE_MAP)]

bar_colors = [
    "#28a745" if v < 0.15 else
    "#fd7e14" if v < 0.30 else
    "#dc3545"
    for v in fnr_vals
]

fig_fnr = go.Figure(go.Bar(
    x=races,
    y=[v * 100 for v in fnr_vals],
    marker_color=bar_colors,
    text=[f"{v:.1%}" for v in fnr_vals],
    textposition="outside",
    customdata=n_vals,
    hovertemplate="<b>%{x}</b><br>FNR: %{y:.1f}%<br>n=%{customdata}<extra></extra>",
))
fig_fnr.add_hline(
    y=OVERALL_FNR * 100,
    line_dash="dash",
    line_color="#333",
    annotation_text=f"Overall FNR ({OVERALL_FNR:.1%})",
    annotation_position="top right",
)
fig_fnr.update_layout(
    yaxis_title="False Negative Rate (%)",
    yaxis_range=[0, 80],
    height=380,
    margin=dict(l=20, r=20, t=30, b=20),
    xaxis_tickangle=-20,
)
st.plotly_chart(fig_fnr, width="stretch")

st.caption(
    "The largest observed race/ethnicity FNR gap is **33.3 percentage points**. "
    "The Hispanic subgroup estimates are based on small stroke-case counts, so the exact "
    "percentage is unstable, but the reliability concern is material."
)

# ---------------------------------------------------------------------------
# AUC comparison — race
# ---------------------------------------------------------------------------
st.subheader("Model Discrimination (AUC) by Race/Ethnicity")
st.markdown(
    "AUC measures how well the model separates stroke from non-stroke cases. "
    "0.5 = coin flip. The model performs very differently across groups."
)

auc_vals = [RACE_AUC[k] for k in sorted(RACE_MAP)]
auc_colors = [
    "#28a745" if v >= 0.65 else
    "#fd7e14" if v >= 0.55 else
    "#dc3545"
    for v in auc_vals
]

fig_auc = go.Figure(go.Bar(
    x=races,
    y=auc_vals,
    marker_color=auc_colors,
    text=[f"{v:.3f}" for v in auc_vals],
    textposition="outside",
    customdata=n_vals,
    hovertemplate="<b>%{x}</b><br>AUC: %{y:.3f}<br>n=%{customdata}<extra></extra>",
))
fig_auc.add_hline(y=0.5, line_dash="dot", line_color="#999",
                  annotation_text="Random (0.500)", annotation_position="top left")
fig_auc.add_hline(y=OVERALL_AUC, line_dash="dash", line_color="#333",
                  annotation_text=f"Overall ({OVERALL_AUC:.3f})", annotation_position="top right")
fig_auc.update_layout(
    yaxis_title="ROC AUC",
    yaxis_range=[0.2, 1.0],
    height=380,
    margin=dict(l=20, r=20, t=30, b=20),
    xaxis_tickangle=-20,
)
st.plotly_chart(fig_auc, width="stretch")
st.caption(
    "Other Hispanic AUC = 0.310 — below random chance on this split. "
    "This is a small subgroup with only three stroke cases in the test set, so the "
    "number should be interpreted as a warning flag rather than a precise estimate."
)

st.divider()

# ---------------------------------------------------------------------------
# Insurance
# ---------------------------------------------------------------------------
st.subheader("Performance by Insurance Status")

ins_labels = [INSURANCE_MAP[k] for k in sorted(INSURANCE_MAP)]
ins_fnr_vals = [INS_FNR[k] * 100 for k in sorted(INSURANCE_MAP)]
ins_auc_vals = [INS_AUC[k] for k in sorted(INSURANCE_MAP)]
ins_n_vals   = [INS_N[k] for k in sorted(INSURANCE_MAP)]

col_ifnr, col_iauc = st.columns(2)

with col_ifnr:
    fig_i = go.Figure(go.Bar(
        x=ins_labels,
        y=ins_fnr_vals,
        marker_color=["#28a745", "#dc3545"],
        text=[f"{v:.1f}%" for v in ins_fnr_vals],
        textposition="outside",
    ))
    fig_i.add_hline(y=OVERALL_FNR * 100, line_dash="dash", line_color="#333",
                    annotation_text=f"Overall ({OVERALL_FNR:.1%})")
    fig_i.update_layout(
        title="False Negative Rate",
        yaxis_title="FNR (%)",
        yaxis_range=[0, 75],
        height=320,
        margin=dict(l=10, r=10, t=40, b=20),
    )
    st.plotly_chart(fig_i, width="stretch")

with col_iauc:
    fig_ia = go.Figure(go.Bar(
        x=ins_labels,
        y=ins_auc_vals,
        marker_color=["#28a745", "#dc3545"],
        text=[f"{v:.3f}" for v in ins_auc_vals],
        textposition="outside",
    ))
    fig_ia.add_hline(y=0.5, line_dash="dot", line_color="#999",
                     annotation_text="Random (0.500)", annotation_position="top left")
    fig_ia.add_hline(y=OVERALL_AUC, line_dash="dash", line_color="#333",
                     annotation_text=f"Overall ({OVERALL_AUC:.3f})")
    fig_ia.update_layout(
        title="ROC AUC",
        yaxis_title="AUC",
        yaxis_range=[0.3, 0.8],
        height=320,
        margin=dict(l=10, r=10, t=40, b=20),
    )
    st.plotly_chart(fig_ia, width="stretch")

st.error(
    "**The uninsured FNR gap is 50.9 percentage points** (6.2% insured vs 57.1% uninsured). "
    "For uninsured patients, the model's AUC is 0.502 — essentially random. "
    "These are the patients who can least afford a missed diagnosis, and the model is least reliable for them."
)

# ---------------------------------------------------------------------------
# Charts from notebook (if available)
# ---------------------------------------------------------------------------
st.divider()
st.subheader("Score Distributions by Race")
st.markdown(
    "These histograms show how predicted risk scores are distributed for stroke vs. non-stroke cases "
    "within each racial group. When stroke cases (red) cluster *below* the 0.30 threshold, they get missed."
)

score_dist_path = EQUITY_DIR / "score_distribution_by_race.png"
race_chart_path = EQUITY_DIR / "race_stratified_metrics.png"

if score_dist_path.exists():
    st.image(str(score_dist_path), width="stretch")
    st.caption(
        "For Non-Hispanic White patients, stroke cases (red) spread broadly above 0.30 — easy to flag. "
        "For Hispanic groups, stroke cases cluster near or below the threshold — systematically missed."
    )
else:
    st.info("Run `extra_analysis/health_equity/health_equity_analysis.ipynb` to generate charts.")

if race_chart_path.exists():
    st.image(str(race_chart_path), width="stretch")

# ---------------------------------------------------------------------------
# Why does this happen?
# ---------------------------------------------------------------------------
st.divider()
with st.expander("Why does this happen? — Understanding the root causes"):
    st.markdown("""
**1. Training data imbalance — the primary driver**

Non-Hispanic White patients make up 47.6% of the dataset (2,192 of 4,603).
Other Hispanic: 9.7% (447). Mexican American: 11.2% (518).
The model has learned far more about what stroke risk looks like for the majority group.
Its decision boundary reflects patterns that work for that group — not for everyone.

**2. Threshold effects**

We apply a single global threshold (0.30) to all patients equally.
But if Hispanic patients' stroke cases produce lower predicted scores on average,
those cases will fall below the threshold even when real risk exists.
A group-specific threshold would improve equity — at the cost of added complexity.

**3. Proxy features**

Features like BMI, blood pressure, and dietary sodium correlate with race
due to social determinants of health (food access, housing stress, healthcare access).
The model may have learned associations for these proxies from the majority group
that don't generalize to others.

**4. Missing social determinants**

Structural factors — neighborhood quality, healthcare utilization history, chronic stress,
language barriers — aren't in this dataset. These factors predict stroke disparities
in Hispanic populations but are invisible to the model.

**What would help:**
- Stratified thresholds per group to equalize FNR
- Upweighting underrepresented groups during training
- Collecting and including social determinants of health variables
- Using fairness-constrained algorithms (e.g., `fairlearn`)
    """)

# ---------------------------------------------------------------------------
# Data table
# ---------------------------------------------------------------------------
st.divider()
with st.expander("Full stratified metrics table"):
    import pandas as pd
    rows = []
    for k in sorted(RACE_MAP):
        rows.append({
            "Group": RACE_MAP[k],
            "n (test set)": RACE_N[k],
            "Stroke cases": RACE_STROKE_CASES[k],
            "AUC": f"{RACE_AUC[k]:.3f}",
            "FNR": f"{RACE_FNR[k]:.1%}",
            "FNR vs. overall": f"{(RACE_FNR[k] - OVERALL_FNR)*100:+.1f}pp",
        })
    rows.append({
        "Group": "Overall",
        "n (test set)": 921,
        "Stroke cases": 72,
        "AUC": f"{OVERALL_AUC:.3f}",
        "FNR": f"{OVERALL_FNR:.1%}",
        "FNR vs. overall": "—",
    })
    st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")
    st.caption(
        "Source: `extra_analysis/health_equity/health_equity_analysis.ipynb`. "
        "Test set n=921, stratified split (seed=42), threshold=0.30, C=0.1 logistic regression."
    )
