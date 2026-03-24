from pathlib import Path # part of helpers
import streamlit as st
import re # for regex
import pandas as pd
import joblib # for the baseline pipeline



# Helper Path Function
DOCS_DIR = Path(__file__).resolve().parents[1] / "docs" / "app_content"
DC2_PATH = DOCS_DIR / "recommended_next_steps.md"
DC3_PATH = DOCS_DIR / "disclaimer_and_limitations.md"


SCHEMA_PATH = DOCS_DIR / "app_input_schema.csv"
MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "baseline_pipeline.joblib"
# MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "fake_model.joblib"

@st.cache_data # prevents re-reading the file from disk every rerun (so basically faster).
def read_text(path: Path) -> str: # reading the text file safely
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""
    
@st.cache_data 
def load_schema(path: Path) -> pd.DataFrame:  # reading the csv file safely
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        return pd.DataFrame()


@st.cache_resource
def load_model(path: Path):
    try:
        return joblib.load(path)
    except FileNotFoundError:
        return None


def extract_recommended_steps(md: str, risk_factor_key: str, n: int = 3):
    #the default is 3 hence the int = 3
    # extracting up to n bullet steps from the section:

    lines = md.splitlines() #this converts the entire markdown string into a list of lines.

    # Find the risk factor header line
    # header_pattern = re.compile(rf"^##\s*\d+\.\s*Risk factor:\s*`{re.escape(risk_factor_key)}`\s*$")
    header_pattern = re.compile(
    rf"^##\s*\d+\.\s*Risk factor:\s*`{re.escape(risk_factor_key)}`(?:\s+.*)?$"
)
    # used re.escape if the your risk factor had special characters, regex could break. But it shouldn't but chat recommended it.
    # the line must start with ## based on the md file 

    #just looping through every line until finding the matching header
    start_idx = None
    for i, line in enumerate(lines):
        if header_pattern.match(line.strip()):
            start_idx = i
            break

    if start_idx is None:
        return None, []

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


#helper funciton to build the user input form from the schema
def build_inputs_from_schema(schema_df: pd.DataFrame) -> dict:
    user_inputs = {}

    st.sidebar.header("Enter Health Information")

    for _, row in schema_df.iterrows():
        column_name = row["column_name"]
        input_type = row["type"]
        description = row["description"]

        if input_type == "number":
            min_val = float(row["min"]) if pd.notna(row["min"]) else None
            max_val = float(row["max"]) if pd.notna(row["max"]) else None
            default_val = float(row["default"]) if pd.notna(row["default"]) else 0.0

            user_inputs[column_name] = st.sidebar.number_input(
                label=column_name,
                min_value=min_val,
                max_value=max_val,
                value=default_val,
                help=description,
            )

        elif input_type == "category":
            raw_options = str(row["options"]).split("|")
            options = [int(opt) for opt in raw_options if opt != ""]
            default_val = int(row["default"]) if pd.notna(row["default"]) else options[0]
            default_index = options.index(default_val) if default_val in options else 0

            user_inputs[column_name] = st.sidebar.selectbox(
                label=column_name,
                options=options,
                index=default_index,
                help=description,
            )

    return user_inputs



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



schema_df = load_schema(SCHEMA_PATH)

if schema_df.empty:
    st.error("Input schema file is missing. Cannot build the app form.")
    st.stop()

user_inputs = build_inputs_from_schema(schema_df)
input_df = pd.DataFrame([user_inputs])




st.divider()
st.subheader("Your Stroke Risk Score")

use_example = st.toggle("Use example output", value=True)

if use_example:
    # Placeholder example output
    st.write("Risk score: **12% (example)**")

    dc2_text = read_text(DC2_PATH)
    risk_factor_key = st.selectbox(
    "Select a risk factor to explore",
    [
        "smoke",
        "alcohol ",
        "sleep time",
        "Minutes sedentary activity",
        "Body Mass Index",
        "Systolic blood pressure",
        "Fasting Glucose",
        "Glycohemoglobin",
        "High-density lipoprotein",
        "Dietary fiber"
    ]
    )
    why_text, tips = extract_recommended_steps(dc2_text, risk_factor_key=risk_factor_key, n=3)

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
    model = load_model(MODEL_PATH)

    if model is None:
        st.warning("Model file is missing. Real model output is not available right now.")
    else:
        try:
            probability = model.predict_proba(input_df)[0][1]

            threshold = 0.30
            risk_label = "High Risk" if probability >= threshold else "Low Risk"

            st.success("Model Output")
            # st.markdown("`Model output`")

            st.write(f"Risk score: **{probability * 100:.1f}%**")
            st.write(f"Risk classification: **{risk_label}**")

            st.caption(f"Threshold: {threshold}")

        except Exception as e:
            st.error(f"Could not generate model output: {e}")

st.subheader("Disclaimer")

dc3_text = read_text(DC3_PATH)
if dc3_text.strip():
    # Showing the disclaimer text directly from DC-3
    st.markdown(dc3_text)
else:
    st.warning(
        "Could not load disclaimer text."
    )