"""
Page 2 — What If? Prevention Simulator
Live counterfactual sliders: drag a feature to its healthy target and watch
the risk gauge update in real time.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import plotly.graph_objects as go
import streamlit as st
from shared import (
    MODIFIABLE_FEATURES,
    build_sidebar_inputs,
    predict_risk,
    risk_gauge,
    risk_tier,
    scan_counterfactuals,
)

st.set_page_config(
    page_title="What If? — Stroke Prevention Demo",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.sidebar.title("Health Information")
st.sidebar.caption("Your profile. Change these to update your baseline risk.")
user_inputs = build_sidebar_inputs()

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.title("💡 What If? — Prevention Simulator")
st.markdown(
    "Change one factor at a time and watch your risk update live. "
    "Your sidebar inputs set your **baseline**. "
    "The sliders below simulate clinical interventions."
)
st.divider()

if not user_inputs:
    st.stop()

baseline_risk = predict_risk(user_inputs)
b_label, b_color, b_emoji = risk_tier(baseline_risk)

# ---------------------------------------------------------------------------
# Quick summary at the top
# ---------------------------------------------------------------------------
st.markdown(
    f"#### Baseline: **{baseline_risk*100:.1f}%** — {b_emoji} {b_label}"
)

# ---------------------------------------------------------------------------
# Build intervention controls
# ---------------------------------------------------------------------------
# Separate modifiable features into categorical and numeric
CAT_FEATURES = {
    "smoke":           {"label": "Smoking", "options": {0: "Non-smoker", 1: "Smoker"}},
    "alcohol":         {"label": "Alcohol use", "options": {0: "No", 1: "Yes"}},
    "sleep disorder":  {"label": "Sleep disorder", "options": {1: "Yes", 2: "No"}},
    "hypertension":    {"label": "Hypertension", "options": {0: "No", 1: "Yes"}},
    "diabetes":        {"label": "Diabetes", "options": {0: "No", 1: "Yes"}},
    "high cholesterol":{"label": "High cholesterol", "options": {0: "No", 1: "Yes"}},
    "Body Mass Index": {"label": "BMI category", "options": {1: "Underweight (<18.5)", 2: "Normal (18.5–24.9)", 3: "Overweight (25–29.9)", 4: "Obese (≥30)"}},
}

NUM_FEATURES = {
    "Systolic blood pressure":  {"label": "Systolic BP (mmHg)",     "min": 70,  "max": 240, "step": 1,   "healthy": 120},
    "Diastolic blood pressure": {"label": "Diastolic BP (mmHg)",    "min": 30,  "max": 130, "step": 1,   "healthy": 80},
    "Fasting Glucose":          {"label": "Fasting Glucose (mmol/L)","min": 2.0, "max": 20.0,"step": 0.1, "healthy": 5.0},
    "Glycohemoglobin":          {"label": "HbA1c (%)",              "min": 3.5, "max": 15.0,"step": 0.1, "healthy": 5.7},
    "sleep time":               {"label": "Sleep (hours/night)",    "min": 1.0, "max": 14.0,"step": 0.5, "healthy": 8.0},
    "Dietary fiber":            {"label": "Dietary fiber (g/day)",  "min": 1.0, "max": 70.0,"step": 1.0, "healthy": 30.0},
    "Sodium":                   {"label": "Sodium (mg/day)",        "min": 300, "max": 6000,"step": 50,  "healthy": 2300},
}

# Keep intervention controls tied to the current sidebar profile. Without this,
# Streamlit preserves old What If values after a user changes the baseline.
profile_signature = tuple(sorted(user_inputs.items()))
if st.session_state.get("cf_profile_signature") != profile_signature:
    for feat in list(CAT_FEATURES) + list(NUM_FEATURES):
        st.session_state.pop(f"cf_{feat}", None)
    st.session_state["cf_profile_signature"] = profile_signature
    st.session_state["cf_best_case_applied"] = False


def apply_best_case() -> None:
    for feat, healthy_val, _ in MODIFIABLE_FEATURES:
        key = f"cf_{feat}"
        if feat in CAT_FEATURES:
            st.session_state[key] = CAT_FEATURES[feat]["options"][healthy_val]
        elif feat in NUM_FEATURES:
            st.session_state[key] = float(healthy_val)
    st.session_state["cf_best_case_applied"] = True


overrides: dict = dict(user_inputs)

st.subheader("Adjust Clinical & Lifestyle Factors")
st.button(
    "🎯 Show Best Case — set all to healthy targets",
    type="secondary",
    on_click=apply_best_case,
)
if st.session_state.get("cf_best_case_applied"):
    st.info("Controls below are set to healthy target values for the best-case scenario.")

cat_col, num_col = st.columns(2, gap="large")

with cat_col:
    st.markdown("**Lifestyle & Conditions**")
    for feat, cfg in CAT_FEATURES.items():
        if feat not in user_inputs:
            continue
        current = user_inputs[feat]
        opts = list(cfg["options"].keys())
        labels = [cfg["options"][o] for o in opts]
        current_idx = opts.index(current) if current in opts else 0
        chosen = st.selectbox(
            cfg["label"],
            options=labels,
            index=current_idx,
            key=f"cf_{feat}",
        )
        overrides[feat] = opts[labels.index(chosen)]

with num_col:
    st.markdown("**Measurable Values**")
    for feat, cfg in NUM_FEATURES.items():
        if feat not in user_inputs:
            continue
        current = float(user_inputs[feat])
        # Clamp current to slider range
        current_clamped = max(cfg["min"], min(cfg["max"], current))
        overrides[feat] = st.slider(
            cfg["label"],
            min_value=float(cfg["min"]),
            max_value=float(cfg["max"]),
            value=current_clamped,
            step=float(cfg["step"]),
            key=f"cf_{feat}",
            help=f"Healthy target: {cfg['healthy']}",
        )

adjusted_risk = predict_risk(overrides)
a_label, a_color, _ = risk_tier(adjusted_risk)
delta_pp = (baseline_risk - adjusted_risk) * 100

# ---------------------------------------------------------------------------
# Before / After gauges
# ---------------------------------------------------------------------------
st.divider()
st.subheader("Before vs. After")

g_left, g_right, g_delta = st.columns([2, 2, 1])

with g_left:
    st.plotly_chart(
        risk_gauge(baseline_risk, "Baseline Risk"),
        width="stretch",
        key="gauge_before",
    )

with g_right:
    st.plotly_chart(
        risk_gauge(adjusted_risk, "Adjusted Risk"),
        width="stretch",
        key="gauge_after",
    )

with g_delta:
    st.metric(
        label="Change",
        value=f"{adjusted_risk*100:.1f}%",
        delta=f"{delta_pp:+.1f}pp",
        delta_color="inverse",
    )
    if delta_pp > 0:
        st.success(f"↓ {delta_pp:.1f}pp reduction")
    elif delta_pp < 0:
        st.warning(f"↑ {abs(delta_pp):.1f}pp increase")
    else:
        st.info("No change")

# ---------------------------------------------------------------------------
# Impact ranking
# ---------------------------------------------------------------------------
st.divider()
st.subheader("Which Intervention Matters Most for You?")
st.caption(
    "Each bar shows the risk drop if ONLY that one factor changes to its healthy target, "
    "everything else held at your baseline."
)

cf_df = scan_counterfactuals(user_inputs)

if not cf_df.empty:
    positive = cf_df[cf_df["risk_drop"] > 0].copy()
    if not positive.empty:
        positive_sorted = positive.sort_values("risk_drop")
        fig = go.Figure(go.Bar(
            x=positive_sorted["risk_drop_pct"],
            y=positive_sorted["intervention"],
            orientation="h",
            marker_color=[
                "#28a745" if v > 5 else "#fd7e14" if v > 2 else "#adb5bd"
                for v in positive_sorted["risk_drop_pct"]
            ],
            text=[f"→ {r*100:.1f}%" for r in positive_sorted["counterfactual_risk"]],
            textposition="outside",
            customdata=positive_sorted[["baseline_risk", "counterfactual_risk"]].values,
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Risk drops by <b>%{x:.1f}pp</b><br>"
                "From %{customdata[0]:.1%} → %{customdata[1]:.1%}<extra></extra>"
            ),
        ))
        fig.update_layout(
            title="Single-Factor Risk Reduction (baseline profile)",
            xaxis_title="Risk reduction (percentage points)",
            height=max(300, 40 * len(positive_sorted) + 100),
            margin=dict(l=20, r=80, t=50, b=30),
            xaxis=dict(range=[0, positive_sorted["risk_drop_pct"].max() * 1.3]),
            yaxis=dict(automargin=True),
        )
        st.plotly_chart(fig, width="stretch")

        best_combo = dict(user_inputs)
        for _, row in cf_df[cf_df["risk_drop"] > 0].iterrows():
            best_combo[row["feature"]] = row["target_value"]
        best_risk = predict_risk(best_combo)
        total_drop = (baseline_risk - best_risk) * 100

        st.info(
            f"**Best case (all interventions combined):** "
            f"Risk drops from **{baseline_risk*100:.1f}%** → **{best_risk*100:.1f}%** "
            f"(↓ {total_drop:.1f} percentage points)"
        )
    else:
        st.success("All modifiable factors are already at healthy targets!")
else:
    st.info("All modifiable risk factors in your profile are already at or better than healthy targets.")

st.divider()
st.caption(
    "All estimates are model predictions — a single feature changed, everything else held constant. "
    "Not medical advice. Discuss any lifestyle or medication changes with a healthcare provider."
)
