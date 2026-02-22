import streamlit as st

st.set_page_config(
    page_title="Stroke Prevention Demo",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Stroke Prevention Demo")
st.write("If you can see this page, your setup works ✅")

st.divider()

st.subheader("What we're building this semester")
st.markdown(
    """
    By the end of the project, this app will:
    - Predict stroke risk from clinical + demographic features
    - Explain the prediction (feature importance / key biomarkers)
    - Show dataset insights and model performance
    """
)

st.divider()

st.subheader("Week 1 checklist")
st.markdown(
    """
    **Do one thing:**
    - Run this Streamlit app locally **OR**
    - Add a small note to `/docs` **OR**
    - Make a tiny code/doc improvement and push a commit

    **Progress beats perfection.**
    """
)

with st.expander("How to run locally (macOS / Linux)"):
    st.code(
        """python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app/streamlit_app.py""",
        language="bash",
    )

with st.expander("How to run locally (Windows PowerShell)"):
    st.code(
        """py -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
streamlit run app/streamlit_app.py""",
        language="powershell",
    )

st.divider()

# Results section (APP-1)
st.header("Your Stroke Risk Score")

# APP-2: Example Mode toggle
use_example = st.checkbox("Use example output", value=True)

if use_example:
    st.metric(label="Risk score", value="12% (example)")

    st.subheader("Prevention Tips")
    # Prevention tips sourced from docs/content/recommended_next_steps.md (DC-2)
    st.markdown(
        """
        - **Reduce sodium intake** — aim for less than 2,300 mg/day to help keep blood pressure in a healthy range.
        - **Increase physical activity** — at least 150 minutes of moderate-intensity exercise per week supports heart and brain health.
        - **Quit or reduce smoking** — speak with your doctor about a cessation plan; smoking significantly raises stroke risk.
        """
    )
else:
    st.info("Model output coming soon — the live prediction pipeline is under development.")

st.subheader("Disclaimer")
# Disclaimer text from docs/disclaimer_and_limitations.md (DC-3)
st.markdown(
    """
    > **Not medical advice.** This tool is a student data science project built for educational
    > purposes only. It does not provide medical advice, diagnosis, or treatment recommendations.
    > Always consult a qualified healthcare provider for any health concerns.
    >
    > **Limitations:** Dataset bias (NHANES cross-sectional); simple baseline model (ROC AUC ~0.62);
    > not clinically validated or approved by any regulatory body.
    """
)
