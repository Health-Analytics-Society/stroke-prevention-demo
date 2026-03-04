from pathlib import Path # part of helpers
import streamlit as st



# Helper Path Function
DOCS_DIR = Path(__file__).resolve().parents[1] / "docs" / "app_content" # moves up to the project root (because app/ is one level under the root).
DC2_PATH = DOCS_DIR / "recommended_next_steps.md" 
DC3_PATH = DOCS_DIR / "disclaimer_and_limitations.md"


@st.cache_data #prevents re-reading the file from disk every rerun (so basically faster).
def read_text(path: Path) -> str: # reading the text file safely
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""




import re # for regex

def extract_recommended_steps(md: str, risk_factor_key: str, n: int = 3):
    #the default is 3 hence the int = 3
    # extracting up to n bullet steps from the section:

    lines = md.splitlines() #this converts the entire markdown string into a list of lines.

    # Find the risk factor header line
    header_pattern = re.compile(rf"^##\s*\d+\.\s*Risk factor:\s*`{re.escape(risk_factor_key)}`\s*$")
    # used re.escape if the your risk factor had special characters, regex could break. But it shouldn't but chat recommended it.
    # the line must start with ## based on the md file 

    #just looping through every line until finding the matching header
    start_idx = None
    for i, line in enumerate(lines):
        if header_pattern.match(line.strip()):
            start_idx = i
            break

    if start_idx is None:
        return [], None

    # this allows the section goes until next "## " header or end of the file
    end_idx = len(lines)
    for j in range(start_idx + 1, len(lines)):
        if lines[j].strip().startswith("## "):
            end_idx = j
            break

    # making sure it only extarcts the lines belonging to this risk factor section
    section = lines[start_idx:end_idx]

    # this finds the "Recommended next steps" & "why it matters" marker inside the section
    why_text = None
    rec_idx = None
    for i, line in enumerate(section):

        if line.strip().startswith("**Why it matters:**"):
            why_text = line.replace("**Why it matters:**", "").strip()

        if "Recommended next steps" in line:
            rec_idx = i
            break
    # storage of recommendation bullets
    tips = []

    if rec_idx is not None:

    # scans the lines after the "Recommended next steps" marker
        for line in section[rec_idx + 1:]:
            s = line.strip()

            if s.startswith(("## ", "**Why it matters:**")):
                break  # stops it if we hit a new subsection
            #makes sures we only accept the bullet lines
            if s.startswith(("-", "*", "•")):
                item = s.lstrip("-*•").strip()
                if item:
                    tips.append(item)

            # not to exceed the number of tips requested
            if len(tips) >= n:
                break

        return why_text,tips



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



st.divider()
st.subheader("Your Stroke Risk Score")

use_example = st.toggle("Use example output", value=True)

if use_example:
    # Placeholder example output
    st.write("Risk score: **12% (example)**")

    st.subheader("Prevention Tips")

    dc2_text = read_text(DC2_PATH)
    why_text, tips = extract_recommended_steps(dc2_text, risk_factor_key="sleep time", n=3)

    st.subheader("Why This Matters")
    
    if why_text:
        st.write(why_text)
    else:
        st.warning("Could not load 'Why this matters' text.")

    st.subheader('Prevention Tips')

    if tips:
        for t in tips:
            st.markdown(f"- {t}")
    else:
        st.warning(
            "Could not load prevention tips."
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
        "Could not load disclaimer text."
    )