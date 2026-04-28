"""
Page 1 — Your Risk
Entry point for the Stroke Prevention Demo Streamlit app.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import streamlit as st
from shared import (
    DOCS_DIR,
    THRESHOLD,
    build_sidebar_inputs,
    contribution_chart,
    get_feature_contributions,
    get_risk_percentile,
    predict_risk,
    read_text,
    risk_gauge,
    risk_tier,
    scan_counterfactuals,
    load_pipeline,
)

st.set_page_config(
    page_title="Stroke Prevention Demo",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
st.sidebar.title("Health Information")
st.sidebar.caption("Fill in your details, then explore results across all pages.")

user_inputs = build_sidebar_inputs()

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.title("🧠 Stroke Prevention Demo")
st.caption("Educational tool — not a clinical diagnostic. See the About page for full disclaimer.")
st.divider()

if not user_inputs:
    st.error("Could not load input schema. Check that `docs/app_content/app_input_schema.csv` exists.")
    st.stop()

# Warm up model quietly so all pages feel fast
with st.spinner("Loading model..."):
    load_pipeline()

# ---------------------------------------------------------------------------
# Compute risk
# ---------------------------------------------------------------------------
try:
    prob = predict_risk(user_inputs)
except Exception as e:
    st.error(f"Model error: {e}")
    st.stop()

label, color, emoji = risk_tier(prob)
percentile = get_risk_percentile(prob)

# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------
col_gauge, col_detail = st.columns([1, 1], gap="large")

with col_gauge:
    st.subheader("Your Stroke Risk Score")
    st.plotly_chart(risk_gauge(prob), width="stretch")

    pct_text = (
        f"You're in the **{percentile}th percentile** of stroke risk scores across "
        f"the 4,603-patient dataset used to train this model."
    )
    st.caption(pct_text)
    st.caption(
        f"Operating threshold: {THRESHOLD*100:.0f}% · "
        f"Low <42% · Moderate 42–62% · High >62%"
    )

with col_detail:
    # --- Feature contributions ---
    st.subheader("What's Driving Your Score")
    contributions = get_feature_contributions(user_inputs)
    if contributions:
        fig = contribution_chart(contributions, top_n=8)
        st.plotly_chart(fig, width="stretch")
        st.caption(
            "Red bars raise your risk · green bars lower it. "
            "Heights reflect each feature's contribution to the model's log-odds output."
        )
    else:
        st.info("Feature contributions not available.")

st.divider()

# ---------------------------------------------------------------------------
# Personalized top tip
# ---------------------------------------------------------------------------
st.subheader("Your Top Prevention Opportunity")

cf_df = scan_counterfactuals(user_inputs)
positive_cf = cf_df[cf_df["risk_drop"] > 0] if not cf_df.empty else cf_df
if not positive_cf.empty:
    best = positive_cf.iloc[0]
    new_risk = best["counterfactual_risk"]
    new_label, new_color, new_emoji = risk_tier(new_risk)
    drop_pp = best["risk_drop_pct"]

    tip_col, arrow_col = st.columns([3, 1])
    with tip_col:
        st.markdown(
            f"**{best['intervention']}**  \n"
            f"Your risk could drop from **{prob*100:.1f}%** → **{new_risk*100:.1f}%** "
            f"(↓ {drop_pp:.1f} percentage points).  \n"
            f"That would move you from **{label}** to **{new_label}**."
        )
    with arrow_col:
        st.metric(
            label="Risk after intervention",
            value=f"{new_risk*100:.1f}%",
            delta=f"−{drop_pp:.1f}pp",
            delta_color="inverse",
        )

    st.caption(
        "This is a model estimate — a single feature changed, everything else held constant. "
        "Explore all interventions on the **What If?** page."
    )
else:
    st.success(
        "The single-factor scenarios did not identify a risk-lowering change from the "
        "modifiable targets in this profile."
    )

st.divider()

# ---------------------------------------------------------------------------
# Prevention tips (existing content)
# ---------------------------------------------------------------------------
st.subheader("Explore a Risk Factor")

dc2_text = read_text(DOCS_DIR / "recommended_next_steps.md")
if dc2_text:
    import re

    def extract_tips(md: str, key: str, n: int = 3):
        lines = md.splitlines()
        pat = re.compile(rf"^##\s*\d+\.\s*Risk factor:\s*`{re.escape(key)}`")
        start = next((i for i, l in enumerate(lines) if pat.match(l.strip())), None)
        if start is None:
            return None, []
        end = next((j for j in range(start + 1, len(lines)) if lines[j].strip().startswith("## ")), len(lines))
        section = lines[start:end]
        why = next((l.replace("**Why it matters:**", "").strip() for l in section if "**Why it matters:**" in l), None)
        rec_i = next((i for i, l in enumerate(section) if "Recommended next steps" in l), None)
        tips = []
        if rec_i:
            for l in section[rec_i + 1:]:
                s = l.strip()
                if s.startswith(("## ", "**Why")):
                    break
                if s.startswith(("-", "*", "•")):
                    item = s.lstrip("-*•").strip()
                    if item:
                        tips.append(item)
                if len(tips) >= n:
                    break
        return why, tips

    risk_factor_key = st.selectbox(
        "Select a risk factor to explore",
        ["smoke", "alcohol", "sleep time", "Body Mass Index",
         "Systolic blood pressure", "Fasting Glucose", "Glycohemoglobin", "Dietary fiber"],
    )
    why_text, tips = extract_tips(dc2_text, risk_factor_key)
    if why_text:
        st.markdown(f"**Why it matters:** {why_text}")
    if tips:
        st.markdown("**Prevention tips:**")
        for t in tips:
            st.markdown(f"- {t}")
    elif not why_text:
        st.warning("Could not load tips for this risk factor.")

st.divider()

# ---------------------------------------------------------------------------
# Footer disclaimer (short)
# ---------------------------------------------------------------------------
with st.expander("Disclaimer & Limitations"):
    disc = read_text(DOCS_DIR / "disclaimer_and_limitations.md")
    if disc.strip():
        st.markdown(disc)
    else:
        st.warning("Could not load disclaimer.")
