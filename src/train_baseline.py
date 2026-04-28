from pathlib import Path
import joblib
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


# =========================================================
# 1. CONFIG
# This is the main section most people should touch
# =========================================================

# Column we are trying to predict
TARGET_COL = "stroke"

# Keep split settings fixed unless a ticket says otherwise
TEST_SIZE = 0.20
RANDOM_STATE = 42
TRY_STRATIFY = True

# Demo threshold for turning probabilities into 0 or 1
# Lower threshold usually increases recall and decreases precision
THRESHOLD = 0.30

# Thresholds to quickly compare precision and recall tradeoffs
THRESHOLD_SCAN = [0.05, 0.10, 0.20, 0.30]

# Relative paths from repo root
DATA_REL_PATH = Path("data/raw/stroke_data.csv")
REPORT_REL_PATH = Path("reports/baseline_metrics.md")
MODEL_REL_PATH = Path("models/baseline_pipeline.joblib")

# Columns to drop because they may leak post-stroke information
LEAKAGE_COLS = [
    "General health condition",
    "depression",
    "Minutes sedentary activity",
]

# These are not collected by the Streamlit app, so the app-facing baseline
# excludes them during training.
EXCLUDE_COLS = [
    "Coronary Heart Disease",
    "High-density lipoprotein",
    "Triglyceride",
    "Low-density lipoprotein",
    "Total fat",
]

# These columns look numeric in the CSV but are actually categories
# Keep the exact spellings from the dataset
CODED_CATEGORICAL_COLS = [
    "gender",
    "age",
    "Race",
    "Marital status",
    "alcohol",
    "smoke",
    "sleep disorder",
    "Health Insurance",
    "diabetes",
    "hypertension",
    "high cholesterol",
    "Coronary Heart Disease",
    "Body Mass Index",
]

# Logistic regression settings
CLASS_WEIGHT = "balanced"
C_VALUE = 0.1
MAX_ITER = 2000
SOLVER = "liblinear"


# =========================================================
# 2. HELPER FUNCTIONS
# =========================================================

def find_repo_root() -> Path:
    """
    Find the repo root by searching upward for the data file.
    This makes the script easier to run from different locations.
    """
    here = Path(__file__).resolve().parent
    for p in [here, *here.parents]:
        if (p / DATA_REL_PATH).exists():
            return p
    return Path.cwd().resolve()


def build_onehot_encoder():
    """
    Make OneHotEncoder work on both newer and older sklearn versions.
    Newer versions use sparse_output=False
    Older versions use sparse=False
    """
    try:
        return OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    except TypeError:
        return OneHotEncoder(handle_unknown="ignore", sparse=False)


# =========================================================
# 3. FIND PATHS
# =========================================================

ROOT = find_repo_root()
DATA_PATH = ROOT / DATA_REL_PATH
REPORT_PATH = ROOT / REPORT_REL_PATH
MODEL_PATH = ROOT / MODEL_REL_PATH


# =========================================================
# 4. LOAD DATA
# =========================================================

if not DATA_PATH.exists():
    raise FileNotFoundError(f"Could not find dataset at: {DATA_PATH}")

df = pd.read_csv(DATA_PATH)
df.columns = df.columns.str.strip()

if TARGET_COL not in df.columns:
    raise ValueError(f"Dataset must contain a '{TARGET_COL}' column.")


# =========================================================
# 5. DEFINE LABEL AND FEATURES
# Drop leakage columns before splitting
# =========================================================

drop_cols = [c for c in LEAKAGE_COLS + EXCLUDE_COLS if c in df.columns]
df_clean = df.drop(columns=drop_cols)

y = df_clean[TARGET_COL]
X = df_clean.drop(columns=[TARGET_COL])

print("Dropped leakage columns:", drop_cols)
print()
print("Label counts")
print(y.value_counts(dropna=False))
print()
print("Label proportions")
print(y.value_counts(normalize=True, dropna=False))


# =========================================================
# 6. TRAIN TEST SPLIT
# Keep this fixed for reproducibility
# =========================================================

try:
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y if TRY_STRATIFY else None,
    )
    stratify_used = "yes" if TRY_STRATIFY else "no"
    stratify_note = ""
except ValueError as e:
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=None,
    )
    stratify_used = "no"
    stratify_note = str(e)

print()
print(f"Split standardized: test_size={TEST_SIZE}, seed={RANDOM_STATE}, stratify={stratify_used}")
if stratify_note:
    print("Stratify note")
    print(stratify_note)


# =========================================================
# 7. PREPROCESSING
# Coded categorical columns get imputed + one hot encoded
# Numeric columns get imputed + scaled
# =========================================================

cat_cols = [c for c in CODED_CATEGORICAL_COLS if c in X.columns]
num_cols = [c for c in X.columns if c not in cat_cols]

print()
print("Categorical columns (coded):", cat_cols)
print("Number of categorical columns:", len(cat_cols))
print("Number of numeric columns:", len(num_cols))

cat_pipe = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", build_onehot_encoder()),
    ]
)

num_pipe = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ]
)

preprocess = ColumnTransformer(
    transformers=[
        ("cat", cat_pipe, cat_cols),
        ("num", num_pipe, num_cols),
    ]
)


# =========================================================
# 8. MODEL
# Logistic regression baseline with class imbalance handling
# =========================================================

model = LogisticRegression(
    C=C_VALUE,
    max_iter=MAX_ITER,
    solver=SOLVER,
    class_weight=CLASS_WEIGHT,
    random_state=RANDOM_STATE,
)

pipeline = Pipeline(
    steps=[
        ("preprocess", preprocess),
        ("model", model),
    ]
)


# =========================================================
# 9. TRAIN
# Fit on training data only
# =========================================================

print()
print("Training baseline model...")
pipeline.fit(X_train, y_train)


# =========================================================
# 10. EVALUATE ON TEST SET
# y_prob is the risk score
# =========================================================

y_prob = pipeline.predict_proba(X_test)[:, 1]
y_pred = (y_prob >= THRESHOLD).astype(int)

accuracy = float(accuracy_score(y_test, y_pred))
precision = float(precision_score(y_test, y_pred, zero_division=0))
recall = float(recall_score(y_test, y_pred, zero_division=0))
auc = float(roc_auc_score(y_test, y_prob))
fnr = 1.0 - recall
cm = confusion_matrix(y_test, y_pred)

print()
print("Threshold", THRESHOLD)
print("Accuracy", accuracy)
print("Precision", precision)
print("Recall", recall)
print("False Negative Rate", fnr)
print("ROC AUC", auc)
print("Confusion matrix")
print(cm)


# =========================================================
# 11. SCORE DISTRIBUTION CUTOFFS
# These are for demo labels only, not clinical thresholds
# =========================================================

cutoffs = {
    "min": float(np.min(y_prob)),
    "median_p50": float(np.percentile(y_prob, 50)),
    "p80": float(np.percentile(y_prob, 80)),
    "p95": float(np.percentile(y_prob, 95)),
    "max": float(np.max(y_prob)),
}

print()
print("Score cutoffs")
for k, v in cutoffs.items():
    print(f"{k}: {v:.6f}")


# =========================================================
# 12. QUICK THRESHOLD SCAN
# Helps compare precision and recall tradeoffs
# =========================================================

threshold_scan_results = []

print()
print("Threshold scan")
for t in THRESHOLD_SCAN:
    yp = (y_prob >= t).astype(int)
    p = float(precision_score(y_test, yp, zero_division=0))
    r = float(recall_score(y_test, yp, zero_division=0))
    c = confusion_matrix(y_test, yp)

    threshold_scan_results.append(
        {
            "threshold": float(t),
            "precision": p,
            "recall": r,
            "confusion_matrix": c.tolist(),
        }
    )

    print(f"threshold={t:.2f} | precision={p:.4f} | recall={r:.4f} | cm={c.tolist()}")


# =========================================================
# 13. SAVE METRICS REPORT
# =========================================================

REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

with open(REPORT_PATH, "w", encoding="utf-8") as f:
    f.write("# Baseline Metrics\n\n")
    f.write("This report matches the model configuration used by the Streamlit app.\n\n")

    f.write("## Model\n")
    f.write("Logistic Regression with L2 penalty\n\n")
    f.write(f"- `solver`: `{SOLVER}`\n")
    f.write(f"- `C`: `{C_VALUE}`\n")
    f.write(f"- `class_weight`: `{CLASS_WEIGHT}`\n")
    f.write(f"- `max_iter`: `{MAX_ITER}`\n\n")

    f.write("## Split\n")
    f.write(f"test_size: {TEST_SIZE}\n")
    f.write(f"random_state: {RANDOM_STATE}\n")
    f.write(f"stratify: {stratify_used}\n")
    if stratify_note:
        f.write("stratify_note:\n")
        f.write(f"{stratify_note}\n")
    f.write("\n")

    f.write("## Leakage handling\n")
    f.write("Dropped columns\n")
    if drop_cols:
        for c in drop_cols:
            f.write(f"- {c}\n")
    else:
        f.write("- None\n")
    f.write("\n")

    f.write("## Feature columns used by the pipeline\n")
    for c in X.columns:
        f.write(f"- {c}\n")
    f.write("\n")

    f.write("## Threshold\n")
    f.write(f"threshold: {THRESHOLD}\n\n")

    f.write("## Label balance\n")
    f.write("Counts\n")
    f.write(y.value_counts(dropna=False).to_string())
    f.write("\n\n")

    f.write("Proportions\n")
    f.write(y.value_counts(normalize=True, dropna=False).to_string())
    f.write("\n\n")

    f.write("## Metrics on test set\n")
    f.write(f"Accuracy: {accuracy:.4f}\n")
    f.write(f"Precision: {precision:.4f}\n")
    f.write(f"Recall: {recall:.4f}\n")
    f.write(f"False Negative Rate: {fnr:.4f}\n")
    f.write(f"ROC AUC: {auc:.4f}\n\n")

    f.write("## Confusion matrix on test set\n")
    f.write("Format is [[TN, FP], [FN, TP]]\n\n")
    f.write(str(cm.tolist()))
    f.write("\n\n")

    f.write("## Score cutoffs from test set probabilities\n")
    for k, v in cutoffs.items():
        f.write(f"- {k}: {v:.6f}\n")
    f.write("\n")

    f.write("## Threshold scan\n")
    for row in threshold_scan_results:
        f.write(
            f"- threshold={row['threshold']:.2f} | "
            f"precision={row['precision']:.4f} | "
            f"recall={row['recall']:.4f} | "
            f"cm={row['confusion_matrix']}\n"
        )
    f.write("\n")
    f.write("## Interpretation\n\n")
    f.write(
        "This is a recall-oriented educational baseline, not a clinical model. "
        "At the 0.30 operating threshold it catches most held-out stroke cases, "
        "but it also creates many false positives and has weak discrimination overall.\n"
    )

print()
print(f"Saved report to {REPORT_PATH}")


# =========================================================
# 14. EXPORT TRAINED PIPELINE FOR STREAMLIT
# This is the main artifact the integration team will load
# =========================================================

MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
joblib.dump(pipeline, MODEL_PATH)

print(f"Saved pipeline to {MODEL_PATH}")
