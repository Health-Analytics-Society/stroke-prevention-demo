"""
shared.py — Central helpers for all Streamlit pages.

All pages import from here. The model is retrained once at startup
(avoids sklearn version incompatibilities with the saved .joblib).
Training takes <1 second.
"""
from collections import OrderedDict
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
APP_DIR = Path(__file__).resolve().parent
ROOT = APP_DIR.parent
DATA_PATH = ROOT / "data" / "raw" / "stroke_data.csv"
DOCS_DIR = ROOT / "docs" / "app_content"
SCHEMA_PATH = DOCS_DIR / "app_input_schema.csv"
EQUITY_DIR = ROOT / "extra_analysis" / "health_equity"

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
TARGET_COL = "stroke"
THRESHOLD = 0.30
RANDOM_STATE = 42

LEAKAGE_COLS = ["General health condition", "depression", "Minutes sedentary activity"]
EXCLUDE_COLS = [
    "Coronary Heart Disease",
    "High-density lipoprotein",
    "Triglyceride",
    "Low-density lipoprotein",
    "Total fat",
]

# Categorical features the model uses (matching app sidebar; no trailing spaces)
CATEGORICAL_COLS = [
    "gender", "age", "Race", "Marital status", "alcohol", "smoke",
    "sleep disorder", "Health Insurance", "diabetes", "hypertension",
    "high cholesterol", "Body Mass Index",
]

# Risk tier thresholds (from docs/app_content/risk_level_labels.md)
TIER_LOW_MAX = 0.39
TIER_HIGH_MIN = 0.62

RACE_MAP = {
    1: "Mexican American",
    2: "Other Hispanic",
    3: "Non-Hispanic White",
    4: "Non-Hispanic Black",
    5: "Other/Multiracial",
}
INSURANCE_MAP = {1: "Insured", 2: "Uninsured"}

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
# Data & schema loading
# ---------------------------------------------------------------------------

@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.strip()
    return df


@st.cache_data
def load_schema() -> pd.DataFrame:
    try:
        return pd.read_csv(SCHEMA_PATH)
    except FileNotFoundError:
        return pd.DataFrame()


@st.cache_data
def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


# ---------------------------------------------------------------------------
# Model — retrained at startup to avoid sklearn version mismatch
# ---------------------------------------------------------------------------

@st.cache_resource
def load_pipeline() -> Pipeline:
    df = load_data()
    drop_cols = [c for c in LEAKAGE_COLS + EXCLUDE_COLS + [TARGET_COL] if c in df.columns]
    y = df[TARGET_COL]
    X = df.drop(columns=drop_cols)

    cat_cols = [c for c in CATEGORICAL_COLS if c in X.columns]
    num_cols = [c for c in X.columns if c not in cat_cols]

    try:
        ohe = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    except TypeError:
        ohe = OneHotEncoder(handle_unknown="ignore", sparse=False)

    pipeline = Pipeline([
        ("preprocess", ColumnTransformer([
            ("cat", Pipeline([
                ("imp", SimpleImputer(strategy="most_frequent")),
                ("ohe", ohe),
            ]), cat_cols),
            ("num", Pipeline([
                ("imp", SimpleImputer(strategy="median")),
                ("sc", StandardScaler()),
            ]), num_cols),
        ])),
        ("model", LogisticRegression(
            max_iter=2000, solver="liblinear",
            class_weight="balanced", C=0.1,
            random_state=RANDOM_STATE,
        )),
    ])

    X_train, _, y_train, _ = train_test_split(
        X, y, test_size=0.20, random_state=RANDOM_STATE, stratify=y
    )
    pipeline.fit(X_train, y_train)
    return pipeline


# ---------------------------------------------------------------------------
# Prediction helpers
# ---------------------------------------------------------------------------

def predict_risk(input_dict: dict) -> float:
    pipeline = load_pipeline()
    df_row = pd.DataFrame([input_dict])
    df_row.columns = df_row.columns.str.strip()
    return float(pipeline.predict_proba(df_row)[0][1])


def risk_tier(prob: float) -> tuple:
    """Returns (label, hex_color, emoji)."""
    if prob < TIER_LOW_MAX:
        return "Low Risk", "#28a745", "✅"
    elif prob < TIER_HIGH_MIN:
        return "Moderate Risk", "#fd7e14", "⚠️"
    else:
        return "High Risk", "#dc3545", "🚨"


@st.cache_data
def _all_dataset_scores() -> np.ndarray:
    """Precompute risk scores for all 4,603 patients (for percentile lookup)."""
    pipeline = load_pipeline()
    df = load_data()
    drop_cols = [c for c in LEAKAGE_COLS + EXCLUDE_COLS + [TARGET_COL] if c in df.columns]
    X_all = df.drop(columns=drop_cols)
    return pipeline.predict_proba(X_all)[:, 1]


def get_risk_percentile(prob: float) -> int:
    """Return percentile rank (0–100) of this score in the full dataset."""
    scores = _all_dataset_scores()
    return int(np.searchsorted(np.sort(scores), prob) / len(scores) * 100)


# ---------------------------------------------------------------------------
# Feature contributions
# ---------------------------------------------------------------------------

def get_feature_contributions(input_dict: dict) -> list[tuple]:
    """
    Returns [(original_feature_name, log_odds_contribution)] sorted by abs value.
    Computed as coef_i * x_i for each transformed feature, grouped back to
    original feature names.
    """
    pipeline = load_pipeline()
    preproc = pipeline.named_steps["preprocess"]
    model = pipeline.named_steps["model"]

    df_row = pd.DataFrame([input_dict])
    df_row.columns = df_row.columns.str.strip()

    X_transformed = preproc.transform(df_row)
    coefs = model.coef_[0]
    raw_contributions = coefs * X_transformed[0]

    try:
        feature_names = preproc.get_feature_names_out()
    except Exception:
        return []

    grouped: dict[str, float] = {}
    for fname, contrib in zip(feature_names, raw_contributions):
        if fname.startswith("cat__"):
            # e.g. "cat__Race_3.0" -> original = "Race"
            stripped = fname[len("cat__"):]
            parts = stripped.rsplit("_", 1)
            original = parts[0] if len(parts) == 2 else stripped
        elif fname.startswith("num__"):
            original = fname[len("num__"):]
        else:
            original = fname
        grouped[original] = grouped.get(original, 0.0) + float(contrib)

    return sorted(grouped.items(), key=lambda x: abs(x[1]), reverse=True)


# ---------------------------------------------------------------------------
# Counterfactual scanner
# ---------------------------------------------------------------------------

# (feature_col, healthy_target, human_readable_label)
MODIFIABLE_FEATURES: list[tuple] = [
    ("smoke",                    0,      "Quit smoking"),
    ("alcohol",                  0,      "Reduce alcohol use"),
    ("sleep disorder",           2,      "Treat sleep disorder"),
    ("hypertension",             0,      "Control blood pressure"),
    ("diabetes",                 0,      "Manage diabetes"),
    ("high cholesterol",         0,      "Control cholesterol"),
    ("Body Mass Index",          2,      "Reach healthy BMI (18.5–24.9)"),
    ("Systolic blood pressure",  120,    "Lower systolic BP to 120 mmHg"),
    ("Diastolic blood pressure", 80,     "Lower diastolic BP to 80 mmHg"),
    ("Fasting Glucose",          5.0,    "Normalize fasting glucose"),
    ("Glycohemoglobin",          5.7,    "Reduce HbA1c to normal range"),
    ("sleep time",               8.0,    "Get 8 hours of sleep"),
    ("Dietary fiber",            30.0,   "Increase dietary fiber to 30g/day"),
    ("Sodium",                   2300.0, "Reduce sodium to 2300mg/day"),
]

_LOWER_IS_BETTER = {
    "Systolic blood pressure", "Diastolic blood pressure",
    "Fasting Glucose", "Glycohemoglobin", "Sodium",
}
_HIGHER_IS_BETTER = {"sleep time", "Dietary fiber"}


def scan_counterfactuals(input_dict: dict) -> pd.DataFrame:
    """
    For each modifiable feature, compute the risk if ONLY that feature changes
    to its healthy target. Returns a DataFrame sorted by risk_drop descending.
    """
    baseline_risk = predict_risk(input_dict)
    rows = []

    for feat, healthy_val, description in MODIFIABLE_FEATURES:
        if feat not in input_dict:
            continue
        current_val = input_dict[feat]

        # Skip if already at or better than target
        if feat in _LOWER_IS_BETTER and float(current_val) <= float(healthy_val):
            continue
        if feat in _HIGHER_IS_BETTER and float(current_val) >= float(healthy_val):
            continue
        if feat not in _LOWER_IS_BETTER and feat not in _HIGHER_IS_BETTER:
            if current_val == healthy_val:
                continue

        cf = dict(input_dict)
        cf[feat] = healthy_val
        cf_risk = predict_risk(cf)
        drop = baseline_risk - cf_risk

        rows.append({
            "intervention": description,
            "feature": feat,
            "current_value": current_val,
            "target_value": healthy_val,
            "baseline_risk": baseline_risk,
            "counterfactual_risk": cf_risk,
            "risk_drop": drop,
            "risk_drop_pct": drop * 100,
        })

    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(rows).sort_values("risk_drop", ascending=False)


# ---------------------------------------------------------------------------
# Plotly charts
# ---------------------------------------------------------------------------

def risk_gauge(prob: float, title: str = "Stroke Risk Score") -> go.Figure:
    label, color, _ = risk_tier(prob)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=round(prob * 100, 1),
        number={"suffix": "%", "font": {"size": 44, "color": color}},
        title={"text": f"{title}<br><span style='font-size:13px;color:{color}'>{label}</span>",
               "font": {"size": 15}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#888"},
            "bar": {"color": color, "thickness": 0.55},
            "bgcolor": "white",
            "borderwidth": 1,
            "bordercolor": "#ddd",
            "steps": [
                {"range": [0, TIER_LOW_MAX * 100],  "color": "#d4edda"},
                {"range": [TIER_LOW_MAX * 100, TIER_HIGH_MIN * 100], "color": "#fff3cd"},
                {"range": [TIER_HIGH_MIN * 100, 100], "color": "#f8d7da"},
            ],
            "threshold": {
                "line": {"color": "#333", "width": 3},
                "thickness": 0.8,
                "value": THRESHOLD * 100,
            },
        },
    ))
    fig.update_layout(height=270, margin=dict(l=20, r=20, t=60, b=10))
    return fig


def contribution_chart(contributions: list[tuple], top_n: int = 8) -> go.Figure:
    top = [c for c in contributions[:top_n] if abs(c[1]) > 0.001]
    if not top:
        return go.Figure()
    top_sorted = sorted(top, key=lambda x: x[1])
    features = [c[0] for c in top_sorted]
    values = [c[1] for c in top_sorted]
    colors = ["#dc3545" if v > 0 else "#28a745" for v in values]

    fig = go.Figure(go.Bar(
        x=values, y=features, orientation="h",
        marker_color=colors,
        text=[f"{v:+.2f}" for v in values],
        textposition="outside",
    ))
    fig.update_layout(
        title={"text": "What's Driving Your Score", "font": {"size": 15}},
        xaxis_title="Log-odds contribution  (red = raises risk · green = protective)",
        height=min(50 * len(top) + 120, 420),
        margin=dict(l=20, r=60, t=50, b=30),
        xaxis=dict(zeroline=True, zerolinecolor="#999", zerolinewidth=1.5),
        yaxis=dict(automargin=True),
    )
    return fig


# ---------------------------------------------------------------------------
# Sidebar builder (called by every page so inputs persist across navigation)
# ---------------------------------------------------------------------------

def _label_map(description: str, int_options: list) -> dict:
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


def build_sidebar_inputs() -> dict:
    """Render grouped sidebar and return user_inputs dict."""
    schema_df = load_schema()
    if schema_df.empty:
        st.sidebar.error("Schema not found — cannot build input form.")
        return {}

    schema_idx = schema_df.set_index("column_name").to_dict("index")
    user_inputs: dict = {}
    placed: set = set()

    for group_label, cols in SIDEBAR_GROUPS.items():
        group_cols = [c for c in cols if c in schema_idx]
        if not group_cols:
            continue
        st.sidebar.markdown(f"### {group_label}")
        for col in group_cols:
            placed.add(col)
            row = schema_idx[col]
            description = str(row.get("description", col))

            if row["type"] == "category":
                raw_options = str(row["options"]).split("|")
                int_options = [int(o) for o in raw_options if o.strip()]
                lmap = _label_map(description, int_options)
                display_options = [lmap[o] for o in int_options]
                default_val = int(row["default"]) if pd.notna(row.get("default")) else int_options[0]
                default_idx = int_options.index(default_val) if default_val in int_options else 0
                selected = st.sidebar.selectbox(label=col, options=display_options, index=default_idx, key=f"sb_{col}")
                user_inputs[col] = int_options[display_options.index(selected)]

            elif row["type"] == "number":
                min_val = float(row["min"]) if pd.notna(row.get("min")) else None
                max_val = float(row["max"]) if pd.notna(row.get("max")) else None
                default_val = float(row["default"]) if pd.notna(row.get("default")) else 0.0
                user_inputs[col] = st.sidebar.number_input(
                    label=col, min_value=min_val, max_value=max_val,
                    value=default_val, help=description, key=f"sb_{col}"
                )
        st.sidebar.markdown("---")

    return user_inputs
