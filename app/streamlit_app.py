from pathlib import Path
import re

import joblib
import pandas as pd
import streamlit as st


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
DOCS_DIR = Path(__file__).resolve().parents[1] / "docs" / "app_content"
DC2_PATH = DOCS_DIR / "recommended_next_steps.md"
DC3_PATH = DOCS_DIR / "disclaimer_and_limitations.md"
SCHEMA_PATH = DOCS_DIR / "app_input_schema.csv"
MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "baseline_pipeline.joblib"

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Columns the pipeline was trained without (post-stroke proxies)
LEAKAGE_COLS = [
    "General health condition",
    "depression",
    "Minutes sedentary activity",
]

# Threshold for converting probability to High/Low risk label
THRESHOLD = 0.30


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

@st.cache_data
def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


@st.cache_data
def load_schema(path: Path) -> pd.DataFrame:
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
    lines = md.splitlines()

    header_pattern = re.compile(
        rf"^##\s*\d+\.\s*Risk factor:\s*`{re.escape(risk_factor_key)}`(?:\s+.*)?$"
    )

    start_idx = None
    for i, line in enumerate(lines):
        if header_pattern.match(line.strip()):
            start_idx = i
            break

    if start_idx is None:
        return None, []

    end_idx = len(lines)
    for j in range(start_idx + 1, len(lines)):
        if lines[j].strip().startswith("## "):
            end_idx = j
            break

    section = lines[start_idx:end_idx]

    why_text = None
    rec_idx = None
    for i, line in enumerate(section):
        if line.strip().startswith("**Why it matters:**"):
            why_text = line.replace("**Why it matters:**", "").strip()
        if "Recommended next steps" in line:
            rec_idx = i
            break

    tips = []
    if rec_idx is not None:
        for line in section[rec_idx + 1:]:
            s = line.strip()
            if s.startswith(("## ", "**Why it matters:**")):
                break
            if s.startswith(("-", "*", "•")):
                item = s.lstrip("-*•").strip()
                if item:
                    tips.append(item)
            if len(tips) >= n:
                break

    return why_text, tips


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


# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Stroke Prevention Demo",
    page_icon="🧠",
    layout="wide",
)

st.title("🧠 Stroke Prevention Demo")

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

# ---------------------------------------------------------------------------
# Build sidebar inputs from schema
# ---------------------------------------------------------------------------

schema_df = load_schema(SCHEMA_PATH)

if schema_df.empty:
    st.error("Input schema file is missing. Cannot build the input form.")
    st.stop()

user_inputs = build_inputs_from_schema(schema_df)
input_df = pd.DataFrame([user_inputs])

# ---------------------------------------------------------------------------
# Results section
# ---------------------------------------------------------------------------

st.divider()
st.subheader("Your Stroke Risk Score")

use_example = st.toggle("Use example output", value=False)

if use_example:
    st.write("Risk score: **12% (example)**")

    dc2_text = read_text(DC2_PATH)
    risk_factor_key = st.selectbox(
        "Select a risk factor to explore",
        [
            "smoke",
            "alcohol",
            "sleep time",
            "Body Mass Index",
            "Systolic blood pressure",
            "Fasting Glucose",
            "Glycohemoglobin",
            "High-density lipoprotein",
            "Dietary fiber",
        ],
    )
    why_text, tips = extract_recommended_steps(dc2_text, risk_factor_key=risk_factor_key, n=3)

    st.subheader("Why This Matters")
    if why_text:
        st.write(why_text)
    else:
        st.warning("Could not load 'Why this matters' text.")

    st.subheader("Prevention Tips")
    if tips:
        for t in tips:
            st.markdown(f"- {t}")
    else:
        st.warning("Could not load prevention tips.")

else:
    model = load_model(MODEL_PATH)

    if model is None:
        st.warning(
            "Model file not found at `models/baseline_pipeline.joblib`. "
            "Run the notebook top-to-bottom to train and export the pipeline, then restart the app."
        )
    else:
        try:
            # Strip column names and drop leakage cols to match what the pipeline was trained on
            model_input = input_df.copy()
            model_input.columns = model_input.columns.str.strip()
            model_input = model_input.drop(
                columns=[c for c in LEAKAGE_COLS if c in model_input.columns]
            )

            probability = model.predict_proba(model_input)[0][1]
            risk_label = "High Risk" if probability >= THRESHOLD else "Low Risk"

            st.success("✅ Model Output")
            st.metric(label="Stroke Risk Score", value=f"{probability * 100:.1f}%")
            st.write(f"Risk classification: **{risk_label}**")
            st.caption(f"Threshold used: {THRESHOLD}")

        except Exception as e:
            st.error(f"Could not generate model output: {e}")

# ---------------------------------------------------------------------------
# Disclaimer
# ---------------------------------------------------------------------------

st.subheader("Disclaimer")

dc3_text = read_text(DC3_PATH)
if dc3_text.strip():
    st.markdown(dc3_text)
else:
    st.warning("Could not load disclaimer text.")
