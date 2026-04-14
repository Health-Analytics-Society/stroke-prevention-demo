from pathlib import Path
import re
from collections import OrderedDict

import joblib
import pandas as pd
import streamlit as st

from typing import Optional

# ---------------------------------------------------------------------------
# Paths & constants
# ---------------------------------------------------------------------------
DOCS_DIR  = Path(__file__).resolve().parents[1] / "docs" / "app_content"
DC2_PATH  = DOCS_DIR / "recommended_next_steps.md"
DC3_PATH  = DOCS_DIR / "disclaimer_and_limitations.md"
SCHEMA_PATH = DOCS_DIR / "app_input_schema.csv"
MODEL_PATH  = Path(__file__).resolve().parents[1] / "models" / "baseline_pipeline.joblib"

LEAKAGE_COLS = [
    "General health condition",
    "depression",
    "Minutes sedentary activity",
    "Coronary Heart Disease",
]

EXCLUDE_COLS = [
    "High-density lipoprotein",
    "Triglyceride",
    "Low-density lipoprotein",
    "Total fat",
]

THRESHOLD = 0.30

# Sidebar input groups — order controls display order
SIDEBAR_GROUPS = OrderedDict([
    ("👤 Demographics", ["gender", "age", "Race", "Marital status"]),
    ("🏃 Lifestyle", ["alcohol", "smoke", "sleep disorder", "sleep time", "Health Insurance"]),
    ("🩺 Clinical", [
        "diabetes", "hypertension", "high cholesterol", "Body Mass Index",
        "Waist Circumference", "Systolic blood pressure", "Diastolic blood pressure",
        "Fasting Glucose", "Glycohemoglobin",
    ]),
    ("🥗 Diet (24-hr recall)", [
        "energy", "protein", "Carbohydrate", "Dietary fiber",
        "Total saturated fatty acids", "Total monounsaturated fatty acids",
        "Total polyunsaturated fatty acids", "Potassium", "Sodium",
    ]),
])


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


def label_map_from_description(description: str, int_options: list) -> dict:
    """Parse '1 = Male; 2 = Female' into {1: 'Male', 2: 'Female'}."""
    mapping = {}
    for part in str(description).split(";"):
        part = part.strip()
        if "=" in part:
            code_str, label = part.split("=", 1)
            try:
                mapping[int(code_str.strip())] = label.strip()
            except ValueError:
                pass
    for o in int_options:
        if o not in mapping:
            mapping[o] = str(o)
    return mapping


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
    why_text, rec_idx = None, None
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

def validate_numeric_input(column_name: str, value: float) -> Optional[str]:
    """Return a short validation message if the value is invalid."""
    if column_name == "sleep time" and not (0 <= value <= 24):
        return "Sleep hours must be between 0 and 24."
    if column_name in ["Systolic blood pressure", "Diastolic blood pressure"] and value <= 0:
        return "Blood pressure must be positive."
    if column_name == "Waist Circumference" and value <= 0:
        return "Waist circumference must be positive."
    return None

def build_inputs_from_schema(schema_df: pd.DataFrame) -> tuple[dict, dict]:
    """Render grouped sidebar inputs with human-readable category labels."""
    user_inputs = {}
    validation_errors = {}
    schema_idx = schema_df.set_index("column_name").to_dict("index")
    placed = set()

    for group_label, cols in SIDEBAR_GROUPS.items():
        group_cols = [c for c in cols if c in schema_idx]
        if not group_cols:
            continue

        st.sidebar.markdown(f"### {group_label}")

        for col in group_cols:
            placed.add(col)
            row = schema_idx[col]
            input_type = row["type"]
            description = str(row.get("description", col))

            if input_type == "category":
                raw_options = str(row["options"]).split("|")
                int_options = [int(o) for o in raw_options if o.strip()]
                lmap = label_map_from_description(description, int_options)
                display_options = [lmap[o] for o in int_options]

                default_val = int(row["default"]) if pd.notna(row.get("default")) else int_options[0]
                default_idx = int_options.index(default_val) if default_val in int_options else 0

                selected = st.sidebar.selectbox(
                    label=col,
                    options=display_options,
                    index=default_idx,
                )
                user_inputs[col] = int_options[display_options.index(selected)]

            elif input_type == "number":
                min_val = float(row["min"]) if pd.notna(row.get("min")) else None
                max_val = float(row["max"]) if pd.notna(row.get("max")) else None
                default_val = float(row["default"]) if pd.notna(row.get("default")) else 0.0

                value = st.sidebar.number_input(
                    label=col,
                    min_value=min_val,
                    max_value=max_val,
                    value=default_val,
                    help=description,
                )
                user_inputs[col] = value

                error_msg = validate_numeric_input(col, value)
                if error_msg:
                    validation_errors[col] = error_msg
                    st.sidebar.warning(error_msg)

        st.sidebar.markdown("---")

    remaining = [c for c in schema_df["column_name"] if c not in placed and c in schema_idx]
    if remaining:
        st.sidebar.markdown("### Other")
        for col in remaining:
            row = schema_idx[col]
            input_type = row["type"]
            description = str(row.get("description", col))

            if input_type == "category":
                raw_options = str(row["options"]).split("|")
                int_options = [int(o) for o in raw_options if o.strip()]
                lmap = label_map_from_description(description, int_options)
                display_options = [lmap[o] for o in int_options]
                default_val = int(row["default"]) if pd.notna(row.get("default")) else int_options[0]
                default_idx = int_options.index(default_val) if default_val in int_options else 0
                selected = st.sidebar.selectbox(label=col, options=display_options, index=default_idx)
                user_inputs[col] = int_options[display_options.index(selected)]

            elif input_type == "number":
                min_val = float(row["min"]) if pd.notna(row.get("min")) else None
                max_val = float(row["max"]) if pd.notna(row.get("max")) else None
                default_val = float(row["default"]) if pd.notna(row.get("default")) else 0.0

                value = st.sidebar.number_input(
                    label=col,
                    min_value=min_val,
                    max_value=max_val,
                    value=default_val,
                    help=description,
                )
                user_inputs[col] = value

                error_msg = validate_numeric_input(col, value)
                if error_msg:
                    validation_errors[col] = error_msg
                    st.sidebar.warning(error_msg)

    return user_inputs, validation_errors


def add_engineered_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Strip column names for consistency
    df.columns = df.columns.str.strip()

    # Multimorbidity: count of selected chronic conditions
    chronic_cols = ["diabetes", "hypertension", "high cholesterol"]
    for col in chronic_cols:
        if col not in df.columns:
            df[col] = 0

    df["multimorbidity"] = (
        df["diabetes"].astype(int)
        + df["hypertension"].astype(int)
        + df["high cholesterol"].astype(int)
    )

    # Interaction terms
    if "age" not in df.columns:
        df["age"] = 0
    if "smoke" not in df.columns:
        df["smoke"] = 0
    if "hypertension" not in df.columns:
        df["hypertension"] = 0
    if "high cholesterol" not in df.columns:
        df["high cholesterol"] = 0

    df["age_x_hypertension"] = df["age"].astype(int) * df["hypertension"].astype(int)
    df["age_x_smoke"] = df["age"].astype(int) * df["smoke"].astype(int)
    df["age_x_high_cholesterol"] = df["age"].astype(int) * df["high cholesterol"].astype(int)

    return df


# ---------------------------------------------------------------------------
# Page config & layout
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Stroke Prevention Demo",
    page_icon="🧠",
    layout="wide",
)

st.title("🧠 Stroke Prevention Demo")
st.caption("Educational tool — not a clinical diagnostic. See disclaimer below.")

st.divider()

# ---------------------------------------------------------------------------
# Sidebar inputs
# ---------------------------------------------------------------------------
schema_df = load_schema(SCHEMA_PATH)

if schema_df.empty:
    st.error("Input schema file is missing. Cannot build the input form.")
    st.stop()

st.sidebar.title("Health Information")
st.sidebar.caption("Fill in the fields below, then view your risk score on the right.")

user_inputs, validation_errors = build_inputs_from_schema(schema_df)
input_df = pd.DataFrame([user_inputs])

# ---------------------------------------------------------------------------
# Results section
# ---------------------------------------------------------------------------
st.subheader("Your Stroke Risk Score")

use_example = st.toggle("Use example output (model not required)", value=False)

if use_example:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric(label="Stroke Risk Score", value="12.0%")
        st.info("Example output")

    with col2:
        dc2_text = read_text(DC2_PATH)
        risk_factor_key = st.selectbox(
            "Select a risk factor to explore",
            ["smoke", "alcohol", "sleep time", "Body Mass Index",
             "Systolic blood pressure", "Fasting Glucose",
             "Glycohemoglobin", "Dietary fiber"],
        )
        why_text, tips = extract_recommended_steps(dc2_text, risk_factor_key=risk_factor_key, n=3)

        if why_text:
            st.markdown(f"**Why it matters:** {why_text}")
        if tips:
            st.markdown("**Prevention tips:**")
            for t in tips:
                st.markdown(f"- {t}")
        elif not why_text:
            st.warning("Could not load prevention tips for this risk factor.")

else:
    model = load_model(MODEL_PATH)

    if model is None:
        st.warning(
            "Model file not found at `models/baseline_pipeline.joblib`. "
            "Run the notebook top-to-bottom to train and export the pipeline, then restart the app."
        )
    else:
        try:
            model_input = input_df.copy()
            model_input.columns = model_input.columns.str.strip()
            drop = [c for c in LEAKAGE_COLS + EXCLUDE_COLS if c in model_input.columns]
            model_input = model_input.drop(columns=drop)

            model_input = add_engineered_features(model_input)

            if validation_errors:
                st.warning("Please fix the invalid input values before running the model.")
            else:
                probability = model.predict_proba(model_input)[0][1]
                risk_label = "High Risk" if probability >= THRESHOLD else "Low Risk"

                col1, col2 = st.columns([1, 2])
                with col1:
                    st.metric(label="Stroke Risk Score", value=f"{probability * 100:.1f}%")
                    if risk_label == "High Risk":
                        st.error(f"⚠️ {risk_label}")
                    else:
                        st.success(f"✅ {risk_label}")
                    st.caption(f"Threshold: {THRESHOLD} · Model output")

                with col2:
                    dc2_text = read_text(DC2_PATH)
                    risk_factor_key = st.selectbox(
                        "Explore a risk factor",
                        ["smoke", "alcohol", "sleep time", "Body Mass Index",
                        "Systolic blood pressure", "Fasting Glucose",
                        "Glycohemoglobin", "Dietary fiber"],
                    )
                    why_text, tips = extract_recommended_steps(dc2_text, risk_factor_key=risk_factor_key, n=3)
                    if why_text:
                        st.markdown(f"**Why it matters:** {why_text}")
                    if tips:
                        st.markdown("**Prevention tips:**")
                        for t in tips:
                            st.markdown(f"- {t}")
        except Exception as e:
            st.error(f"Could not generate model output: {e}")

# ---------------------------------------------------------------------------
# Disclaimer
# ---------------------------------------------------------------------------
st.divider()
st.subheader("Disclaimer")
dc3_text = read_text(DC3_PATH)
if dc3_text.strip():
    st.markdown(dc3_text)
else:
    st.warning("Could not load disclaimer text.")
