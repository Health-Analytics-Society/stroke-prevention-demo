"""
Page 4 — Explore the Data
Self-guided population explorer. Visitors discover patterns in the NHANES-derived
dataset — stroke rates by demographic group, clinical feature distributions, etc.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import plotly.graph_objects as go
import streamlit as st
from shared import (
    build_sidebar_inputs,
    load_data,
)

st.set_page_config(
    page_title="Explore the Data — Stroke Prevention Demo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.sidebar.title("Health Information")
st.sidebar.caption("Your inputs are used on other pages. Feel free to explore here.")
build_sidebar_inputs()

df = load_data()

# Readable labels
RACE_LABELS = {1: "Mex. Am.", 2: "Oth. Hisp.", 3: "NH White", 4: "NH Black", 5: "Other"}
INS_LABELS  = {1: "Insured", 2: "Uninsured"}
SMOKE_LABELS  = {0: "Non-smoker", 1: "Smoker"}
ALCOHOL_LABELS = {0: "No alcohol", 1: "Drinks alcohol"}
HTN_LABELS = {0: "No hypertension", 1: "Has hypertension"}
DIAB_LABELS = {0: "No diabetes", 1: "Has diabetes"}
CHOL_LABELS = {0: "Normal cholesterol", 1: "High cholesterol"}
BMI_LABELS  = {1: "Underweight", 2: "Normal", 3: "Overweight", 4: "Obese"}
AGE_LABELS  = {1: "20–39 yrs", 2: "40–59 yrs", 3: "60+ yrs"}
GENDER_LABELS = {1: "Male", 2: "Female"}

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.title("📊 Explore the Data")
st.markdown(
    "Discover patterns in the **4,603-patient NHANES-derived dataset** behind this model. "
    "Use the controls below to explore stroke rates by group and clinical distributions. "
    "Everything is interactive — hover, zoom, and click."
)
st.divider()

# ---------------------------------------------------------------------------
# Did You Know? — stat cards
# ---------------------------------------------------------------------------
st.subheader("Did You Know?")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Overall stroke prevalence", "7.9%", help="362 stroke cases in 4,603 patients")
    st.caption("~1 in 13 patients in this dataset had a stroke event.")

with c2:
    smoker_rate = df.groupby("smoke")["stroke"].mean()
    ratio = smoker_rate.get(1, 0) / smoker_rate.get(0, 1)
    st.metric("Smoker stroke rate vs. non-smoker", f"{ratio:.1f}×",
              help="9.5% (smokers) vs. 6.1% (non-smokers)")
    st.caption("Smokers have 1.6× the stroke rate of non-smokers in this dataset.")

with c3:
    age_rate = df.groupby("age")["stroke"].mean()
    ratio_age = age_rate.get(3, 0) / max(age_rate.get(1, 0.001), 0.001)
    st.metric("Stroke rate: 60+ vs. 20–39", f"{ratio_age:.0f}×",
              help="12.3% (60+) vs. 1.9% (20–39)")
    st.caption("Patients 60+ have a stroke rate 6.5× higher than those in their 20s–30s.")

with c4:
    htn_rate = df.groupby("hypertension")["stroke"].mean()
    st.metric("Have hypertension", f"{df['hypertension'].mean():.0%}",
              help="83% of this dataset has hypertension — an unusually high rate.")
    st.caption("An unusually high baseline comorbidity rate in this NHANES sample.")

st.divider()

# ---------------------------------------------------------------------------
# Stroke Rate by Categorical Feature
# ---------------------------------------------------------------------------
st.subheader("Stroke Rate by Group")
st.markdown("Select a variable to see the stroke rate for each category.")

CAT_OPTIONS = {
    "Race/Ethnicity":    ("Race",             RACE_LABELS),
    "Insurance Status":  ("Health Insurance", INS_LABELS),
    "Age Group":         ("age",              AGE_LABELS),
    "Smoking":           ("smoke",            SMOKE_LABELS),
    "Alcohol Use":       ("alcohol",          ALCOHOL_LABELS),
    "Hypertension":      ("hypertension",     HTN_LABELS),
    "Diabetes":          ("diabetes",         DIAB_LABELS),
    "High Cholesterol":  ("high cholesterol", CHOL_LABELS),
    "BMI Category":      ("Body Mass Index",  BMI_LABELS),
    "Gender":            ("gender",           GENDER_LABELS),
}

chosen_cat = st.selectbox("Group by:", list(CAT_OPTIONS.keys()))
col_name, label_map = CAT_OPTIONS[chosen_cat]

if col_name in df.columns:
    grp = (
        df.groupby(col_name)
          .agg(stroke_rate=("stroke", "mean"), n=("stroke", "count"), stroke_n=("stroke", "sum"))
          .reset_index()
    )
    grp["label"] = grp[col_name].map(label_map).fillna(grp[col_name].astype(str))
    grp["stroke_pct"] = grp["stroke_rate"] * 100

    overall_rate = df["stroke"].mean() * 100

    fig_cat = go.Figure(go.Bar(
        x=grp["label"],
        y=grp["stroke_pct"],
        marker_color=[
            "#dc3545" if v > overall_rate * 1.2 else
            "#fd7e14" if v > overall_rate else
            "#28a745"
            for v in grp["stroke_pct"]
        ],
        text=[f"{v:.1f}%" for v in grp["stroke_pct"]],
        textposition="outside",
        customdata=grp[["n", "stroke_n"]].values,
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Stroke rate: %{y:.1f}%<br>"
            "n=%{customdata[0]} · %{customdata[1]} strokes<extra></extra>"
        ),
    ))
    fig_cat.add_hline(
        y=overall_rate, line_dash="dash", line_color="#555",
        annotation_text=f"Overall: {overall_rate:.1f}%",
        annotation_position="top right",
    )
    fig_cat.update_layout(
        yaxis_title="Stroke Rate (%)",
        yaxis_range=[0, grp["stroke_pct"].max() * 1.35],
        height=400,
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis_tickangle=-20,
    )
    st.plotly_chart(fig_cat, width="stretch")

    st.caption(
        f"Red = above 120% of overall rate ({overall_rate:.1f}%) · "
        f"Orange = above overall · Green = below overall"
    )

st.divider()

# ---------------------------------------------------------------------------
# Score Distribution: Stroke vs. Non-Stroke
# ---------------------------------------------------------------------------
st.subheader("Clinical Feature Distribution")
st.markdown(
    "Select a numeric feature to compare its distribution for stroke vs. non-stroke patients. "
    "Features with separated distributions are more predictive."
)

NUM_OPTIONS = {
    "Systolic Blood Pressure (mmHg)":       "Systolic blood pressure",
    "Diastolic Blood Pressure (mmHg)":      "Diastolic blood pressure",
    "Waist Circumference (cm)":             "Waist Circumference",
    "Fasting Glucose (mmol/L)":             "Fasting Glucose",
    "HbA1c / Glycohemoglobin (%)":          "Glycohemoglobin",
    "Sleep Time (hours/night)":             "sleep time",
    "Dietary Fiber (g/day)":               "Dietary fiber",
    "Sodium Intake (mg/day)":              "Sodium",
    "Total Energy Intake (kcal/day)":       "energy",
    "Protein Intake (g/day)":              "protein",
}

chosen_num = st.selectbox("Feature:", list(NUM_OPTIONS.keys()))
feat_col = NUM_OPTIONS[chosen_num]

if feat_col in df.columns:
    stroke_yes = df[df["stroke"] == 1][feat_col].dropna()
    stroke_no  = df[df["stroke"] == 0][feat_col].dropna()

    # Clip extreme outliers for display
    p1, p99 = df[feat_col].quantile([0.01, 0.99])
    stroke_yes_clipped = stroke_yes.clip(p1, p99)
    stroke_no_clipped  = stroke_no.clip(p1, p99)

    fig_dist = go.Figure()
    fig_dist.add_trace(go.Histogram(
        x=stroke_no_clipped, name="No stroke",
        marker_color="steelblue", opacity=0.65,
        nbinsx=40, histnorm="percent",
    ))
    fig_dist.add_trace(go.Histogram(
        x=stroke_yes_clipped, name="Stroke",
        marker_color="crimson", opacity=0.8,
        nbinsx=40, histnorm="percent",
    ))
    fig_dist.update_layout(
        barmode="overlay",
        xaxis_title=chosen_num,
        yaxis_title="% of group",
        height=380,
        legend=dict(x=0.75, y=0.95),
        margin=dict(l=20, r=20, t=30, b=30),
    )

    mean_yes = stroke_yes.mean()
    mean_no  = stroke_no.mean()
    fig_dist.add_vline(x=mean_yes, line_dash="dash", line_color="crimson",
                       annotation_text=f"Stroke mean: {mean_yes:.1f}", annotation_position="top right")
    fig_dist.add_vline(x=mean_no, line_dash="dash", line_color="steelblue",
                       annotation_text=f"No stroke mean: {mean_no:.1f}", annotation_position="top left")

    st.plotly_chart(fig_dist, width="stretch")
    st.caption(
        f"Mean {chosen_num}: **stroke cases = {mean_yes:.1f}**, **non-stroke = {mean_no:.1f}**. "
        f"Wider separation = stronger signal for the model. "
        f"(Values clipped to 1st–99th percentile for display.)"
    )

st.divider()

# ---------------------------------------------------------------------------
# Comorbidity combinations
# ---------------------------------------------------------------------------
st.subheader("Comorbidity Combinations & Stroke Risk")
st.markdown(
    "How does having multiple risk conditions simultaneously affect stroke rate? "
    "Select two conditions to see a 2×2 heatmap."
)

COMORBID_OPTIONS = {
    "Hypertension":      "hypertension",
    "Diabetes":          "diabetes",
    "High Cholesterol":  "high cholesterol",
    "Smoking":           "smoke",
    "Alcohol Use":       "alcohol",
}
COMORBID_LABEL_MAPS = {
    "hypertension":     {0: "No HTN", 1: "HTN"},
    "diabetes":         {0: "No DM", 1: "Diabetes"},
    "high cholesterol": {0: "Normal Chol.", 1: "High Chol."},
    "smoke":            {0: "Non-smoker", 1: "Smoker"},
    "alcohol":          {0: "No alcohol", 1: "Alcohol"},
}

c_left, c_right = st.columns(2)
with c_left:
    cond_a_label = st.selectbox("Condition A", list(COMORBID_OPTIONS.keys()), index=0)
with c_right:
    remaining = [k for k in COMORBID_OPTIONS if k != cond_a_label]
    cond_b_label = st.selectbox("Condition B", remaining, index=0)

cond_a = COMORBID_OPTIONS[cond_a_label]
cond_b = COMORBID_OPTIONS[cond_b_label]

if cond_a in df.columns and cond_b in df.columns:
    pivot = df.groupby([cond_a, cond_b])["stroke"].mean().unstack(fill_value=0)
    lmap_a = COMORBID_LABEL_MAPS[cond_a]
    lmap_b = COMORBID_LABEL_MAPS[cond_b]

    z = pivot.values * 100
    x_labels = [lmap_b.get(c, str(c)) for c in pivot.columns]
    y_labels = [lmap_a.get(r, str(r)) for r in pivot.index]

    fig_heat = go.Figure(go.Heatmap(
        z=z, x=x_labels, y=y_labels,
        colorscale="RdYlGn_r",
        text=[[f"{v:.1f}%" for v in row] for row in z],
        texttemplate="%{text}",
        textfont={"size": 16},
        showscale=True,
        colorbar=dict(title="Stroke Rate (%)"),
    ))
    fig_heat.update_layout(
        title=f"Stroke Rate: {cond_a_label} × {cond_b_label}",
        height=280,
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis_title=cond_b_label,
        yaxis_title=cond_a_label,
    )
    st.plotly_chart(fig_heat, width="stretch")

    max_risk = z.max()
    min_risk = z.min()
    st.caption(
        f"Highest-risk combination: **{max_risk:.1f}%**. "
        f"Lowest-risk combination: **{min_risk:.1f}%**. "
        f"Darker red = higher stroke rate in that combination."
    )

st.divider()

# ---------------------------------------------------------------------------
# Dataset overview
# ---------------------------------------------------------------------------
with st.expander("Dataset Summary"):
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"""
**Dataset:** NHANES-derived stroke dataset
- **Total patients:** {len(df):,}
- **Stroke cases:** {int(df['stroke'].sum())} ({df['stroke'].mean():.1%} prevalence)
- **Features:** {df.shape[1] - 1} (demographics, lifestyle, clinical, dietary)
- **Missing values:** None

**Demographics:**
- Female: {(df['gender'] == 2).mean():.1%}
- Age 60+: {(df['age'] == 3).mean():.1%}
- Non-Hispanic White: {(df['Race'] == 3).mean():.1%}
- Uninsured: {(df['Health Insurance'] == 2).mean():.1%}
        """)
    with col_b:
        st.markdown(f"""
**Clinical profile:**
- Have hypertension: {df['hypertension'].mean():.1%}
- Smoke: {df['smoke'].mean():.1%}
- Have diabetes: {df['diabetes'].mean():.1%}
- High cholesterol: {df['high cholesterol'].mean():.1%}
- Obese (BMI cat. 4): {(df['Body Mass Index'] == 4).mean():.1%}

**Lab means (all patients):**
- Systolic BP: {df['Systolic blood pressure'].mean():.1f} mmHg
- Fasting glucose: {df['Fasting Glucose'].mean():.2f} mmol/L
- HbA1c: {df['Glycohemoglobin'].mean():.2f}%
        """)
