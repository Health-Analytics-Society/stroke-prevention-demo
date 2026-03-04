import streamlit as st

st.title("🧠 Stroke Prevention Demo")
st.write("If you can see this page, your setup works ✅")

st.divider()

st.subheader("What we’re building this semester")
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
