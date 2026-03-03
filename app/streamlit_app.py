from pathlib import Path # part of helpers
import streamlit as st


# Helper Path Function
DOCS_DIR = Path(__file__).resolve().parents[1] / "docs" / "app_content" # moves up to the project root (because app/ is one level under the root).
DC2_PATH = DOCS_DIR / "recommended_next_steps.md" 
DC3_PATH = DOCS_DIR / "disclaimer_and_limitations.md"


@st.cache_data #prevents re-reading the file from disk every rerun (so basically faster).
def read_text(path: Path) -> str:
    """Read a UTF-8 text file safely."""
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""



#It scans the markdown file line-by-line.
# It grabs the first 3 bullet lines anywhere in the file.
import re

def extract_recommended_steps(md: str, risk_factor_key: str, n: int = 3) -> list[str]:
    #the default is 3 hence the int = 3
    """
    Extract up to n bullet steps from the section:
    ## <number>. Risk factor: `<risk_factor_key>`
    under the subheader '**Recommended next steps:**'
    """
    lines = md.splitlines() #this converts the entire markdown string into a list of lines.

    # Find the risk factor header line
    header_pattern = re.compile(rf"^##\s*\d+\.\s*Risk factor:\s*`{re.escape(risk_factor_key)}`\s*$")
    # used re.escape if the your risk factor had special characters, regex could break. But it shouldn't but chat recommended it.
    # the line must start with ## based on the md file 

    #just looping through every line
    start_idx = None
    for i, line in enumerate(lines):
        if header_pattern.match(line.strip()):
            start_idx = i
            break
    if start_idx is None:
        return []

    # this allows the section goes until next "## " header or end of the file
    end_idx = len(lines)
    for j in range(start_idx + 1, len(lines)):
        if lines[j].strip().startswith("## "):
            end_idx = j
            break

    section = lines[start_idx:end_idx]

    # this finds the "Recommended next steps" marker inside the section
    rec_idx = None
    for i, line in enumerate(section):
        if "Recommended next steps" in line:
            rec_idx = i
            break
    if rec_idx is None:
        return []

    # collects the bullet lines after that marker
    tips = []
    for line in section[rec_idx + 1:]:
        s = line.strip()
        if s.startswith(("## ", "**Why it matters:**")):
            break  # stops ti if we hit a new subsection
        if s.startswith(("-", "*", "•")):
            item = s.lstrip("-*•").strip()
            if item:
                tips.append(item)
        if len(tips) >= n:
            break

    return tips



st.set_page_config(
    page_title="Stroke Prevention Demo",
    page_icon="🧠",
    layout="wide"
)




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


# RESULTS SECTION OLD 

# st.divider()
# st.subheader("Your Stroke Risk Score")


# # Placeholder example output
# st.write("Risk score: **12% (example)**")


# st.subheader("Prevention Tips")
# st.markdown(
#     """
#     - Maintain a balanced, heart-healthy diet
#     - Stay physically active throughout the week
#     - Monitor blood pressure and cholesterol regularly
#     """
# )


# st.subheader("Disclaimer")

# # TODO (DC-3): Replace this placeholder disclaimer with approved final text
# st.info(
#     "This tool is for educational purposes only and does not provide medical advice. "
#     "Always consult a qualified healthcare professional for medical decisions."
# )




st.divider()
st.subheader("Your Stroke Risk Score")

use_example = st.toggle("Use example output", value=True)

if use_example:
    # Placeholder example output
    st.write("Risk score: **12% (example)**")

    st.subheader("Prevention Tips")

    dc2_text = read_text(DC2_PATH)
    tips = extract_recommended_steps(dc2_text, risk_factor_key="sleep time", n=3)

    if tips:
        for t in tips:
            st.markdown(f"- {t}")
    else:
        st.warning(
            "Could not load prevention tips from DC-2. "
            f"Expected file at: `{DC2_PATH}`"
        )
else:
    st.info("Model output coming soon.")

st.subheader("Disclaimer")

dc3_text = read_text(DC3_PATH)
if dc3_text.strip():
    # Showing the disclaimer text directly from DC-3
    st.markdown(dc3_text)
else:
    st.warning(
        "Could not load disclaimer text from DC-3. "
        f"Expected file at: `{DC3_PATH}`"
    )