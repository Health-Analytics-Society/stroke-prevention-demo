from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler


# ---------------------------------------------------------------------------
# Current project setup (aligned to notebooks/final_demo_baseline_model.ipynb)
# ---------------------------------------------------------------------------
CV_FOLDS = 5
RANDOM_STATE = 42
CV_SHUFFLE = True

DATA_REL_PATH = Path("data/raw/stroke_data.csv")

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
]

REDUNDANT_COLS = [
    "Total fat",
]

NOMINAL_CATEGORICAL_COLS = [
    "gender",
    "Race",
    "Marital status",
    "sleep disorder",
    "Health Insurance",
    "Body Mass Index",
]

ORDINAL_COLS = ["age"]
ORDINAL_CATEGORIES = [[1, 2, 3]]

ZERO_AS_MISSING_COLS = [
    "energy",
    "protein",
    "Carbohydrate",
    "Dietary fiber",
    "Total saturated fatty acids",
    "Total monounsaturated fatty acids",
    "Total polyunsaturated fatty acids",
    "Potassium",
    "Sodium",
]

PHYSIOLOGICAL_CAPS = {
    "energy": (400, 6000),
    "protein": (5, 280),
    "Carbohydrate": (5, 700),
    "Dietary fiber": (1, 70),
    "Total saturated fatty acids": (0.5, 100),
    "Total monounsaturated fatty acids": (0.5, 100),
    "Total polyunsaturated fatty acids": (0.5, 75),
    "Potassium": (200, 8000),
    "Sodium": (300, 12000),
    "Glycohemoglobin": (3.5, 18.0),
}

CLIP_OUTLIERS = True
CLIP_IQR_MULTIPLIER = 2.0

MAX_ITER = 2000
SOLVER = "saga"
PENALTY = "elasticnet"


@dataclass
class PreparedData:
    X: pd.DataFrame
    y: pd.Series
    ord_cols: list[str]
    nom_cols: list[str]
    num_cols: list[str]
    dropped_leakage: list[str]
    dropped_excluded: list[str]
    dropped_redundant: list[str]


# ---------------------------------------------------------------------------
# Core helpers
# ---------------------------------------------------------------------------
def find_repo_root() -> Path:
    here = Path.cwd().resolve()
    for p in [here, *here.parents]:
        if (p / DATA_REL_PATH).exists():
            return p
    return here


def class_weight_label(class_weight: Any) -> str:
    if class_weight is None:
        return "none"
    if isinstance(class_weight, str):
        return class_weight
    if isinstance(class_weight, dict):
        items = sorted(class_weight.items(), key=lambda x: x[0])
        return ",".join([f"{k}:{v}" for k, v in items])
    return str(class_weight)


def add_engineered_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    risk_flags = ["diabetes", "hypertension", "high cholesterol", "smoke"]
    present = [c for c in risk_flags if c in out.columns]
    out["multimorbidity"] = out[present].sum(axis=1)

    out["age_x_hypertension"] = out["age"] * out["hypertension"]
    out["age_x_smoke"] = out["age"] * out["smoke"]
    out["age_x_high_cholesterol"] = out["age"] * out["high cholesterol"]

    return out


def load_and_prepare_data(data_path: Path) -> PreparedData:
    df = pd.read_csv(data_path)

    df.columns = df.columns.str.strip()
    df = df.drop_duplicates().reset_index(drop=True)

    zero_cols_present = [c for c in ZERO_AS_MISSING_COLS if c in df.columns]
    if zero_cols_present:
        df[zero_cols_present] = df[zero_cols_present].replace(0, np.nan)

    for col, (lo, hi) in PHYSIOLOGICAL_CAPS.items():
        if col in df.columns:
            df[col] = df[col].clip(lower=lo, upper=hi)

    df = add_engineered_features(df)

    if "stroke" not in df.columns:
        raise ValueError("Dataset must contain a 'stroke' column.")

    drop_cols = [c for c in LEAKAGE_COLS if c in df.columns]
    exclude_cols = [c for c in EXCLUDE_COLS if c in df.columns]
    redundant_cols = [c for c in REDUNDANT_COLS if c in df.columns]

    df_clean = df.drop(columns=drop_cols + exclude_cols + redundant_cols)

    y = df_clean["stroke"].copy()
    X = df_clean.drop(columns=["stroke"]).copy()

    ord_cols = [c for c in ORDINAL_COLS if c in X.columns]
    nom_cols = [c for c in NOMINAL_CATEGORICAL_COLS if c in X.columns]
    num_cols = [c for c in X.columns if c not in ord_cols + nom_cols]

    return PreparedData(
        X=X,
        y=y,
        ord_cols=ord_cols,
        nom_cols=nom_cols,
        num_cols=num_cols,
        dropped_leakage=drop_cols,
        dropped_excluded=exclude_cols,
        dropped_redundant=redundant_cols,
    )


def apply_iqr_clipping(
    train_df: pd.DataFrame,
    valid_df: pd.DataFrame,
    numeric_cols: list[str],
    k: float,
) -> tuple[pd.DataFrame, pd.DataFrame, int]:
    if not numeric_cols:
        return train_df.copy(), valid_df.copy(), 0

    q1 = train_df[numeric_cols].quantile(0.25)
    q3 = train_df[numeric_cols].quantile(0.75)
    iqr = q3 - q1
    lower_bounds = q1 - k * iqr
    upper_bounds = q3 + k * iqr

    train_out = train_df.copy()
    valid_out = valid_df.copy()

    train_out[numeric_cols] = train_out[numeric_cols].clip(
        lower=lower_bounds,
        upper=upper_bounds,
        axis=1,
    )
    valid_out[numeric_cols] = valid_out[numeric_cols].clip(
        lower=lower_bounds,
        upper=upper_bounds,
        axis=1,
    )

    clipped_low = (train_df[numeric_cols] < lower_bounds).sum()
    clipped_high = (train_df[numeric_cols] > upper_bounds).sum()
    total_clipped = int((clipped_low + clipped_high).sum())

    return train_out, valid_out, total_clipped


def build_pipeline(
    ord_cols: list[str],
    nom_cols: list[str],
    num_cols: list[str],
    c_value: float,
    l1_ratio: float,
    class_weight: Any,
) -> Pipeline:
    ord_pipe = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("ordinal", OrdinalEncoder(categories=ORDINAL_CATEGORIES)),
        ]
    )

    nom_pipe = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
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
            ("ord", ord_pipe, ord_cols),
            ("nom", nom_pipe, nom_cols),
            ("num", num_pipe, num_cols),
        ]
    )

    model = LogisticRegression(
        penalty=PENALTY,
        C=c_value,
        l1_ratio=l1_ratio,
        solver=SOLVER,
        max_iter=MAX_ITER,
        class_weight=class_weight,
        random_state=RANDOM_STATE,
    )

    return Pipeline(
        steps=[
            ("preprocess", preprocess),
            ("model", model),
        ]
    )


def cv_splits(X: pd.DataFrame, y: pd.Series):
    cv = StratifiedKFold(
        n_splits=CV_FOLDS,
        shuffle=CV_SHUFFLE,
        random_state=RANDOM_STATE,
    )
    return list(cv.split(X, y))


def fold_metrics_from_predictions(
    y_true: pd.Series,
    y_prob: np.ndarray,
    threshold: float,
) -> dict[str, float]:
    y_pred = (y_prob >= threshold).astype(int)
    return {
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_true, y_prob)),
        "accuracy": float(accuracy_score(y_true, y_pred)),
    }


def evaluate_setting(
    prepared: PreparedData,
    c_value: float,
    l1_ratio: float,
    class_weight: Any,
    threshold: float,
) -> tuple[dict[str, float], pd.DataFrame]:
    X = prepared.X
    y = prepared.y

    splits = cv_splits(X, y)

    fold_rows: list[dict[str, float]] = []

    for fold_idx, (train_idx, valid_idx) in enumerate(splits, start=1):
        X_train = X.iloc[train_idx].copy()
        X_valid = X.iloc[valid_idx].copy()
        y_train = y.iloc[train_idx]
        y_valid = y.iloc[valid_idx]

        if CLIP_OUTLIERS:
            X_train, X_valid, clipped = apply_iqr_clipping(
                X_train,
                X_valid,
                prepared.num_cols,
                CLIP_IQR_MULTIPLIER,
            )
        else:
            clipped = 0

        pipeline = build_pipeline(
            ord_cols=prepared.ord_cols,
            nom_cols=prepared.nom_cols,
            num_cols=prepared.num_cols,
            c_value=c_value,
            l1_ratio=l1_ratio,
            class_weight=class_weight,
        )
        pipeline.fit(X_train, y_train)

        y_prob = pipeline.predict_proba(X_valid)[:, 1]
        metrics = fold_metrics_from_predictions(y_valid, y_prob, threshold)

        row = {
            "fold": int(fold_idx),
            "threshold": float(threshold),
            "C": float(c_value),
            "l1_ratio": float(l1_ratio),
            "class_weight": class_weight_label(class_weight),
            "clipped_values": int(clipped),
        }
        row.update(metrics)
        fold_rows.append(row)

    fold_df = pd.DataFrame(fold_rows)

    summary: dict[str, float] = {
        "threshold": float(threshold),
        "C": float(c_value),
        "l1_ratio": float(l1_ratio),
        "class_weight": class_weight_label(class_weight),
    }
    for metric in ["recall", "precision", "f1", "roc_auc", "accuracy"]:
        summary[f"mean_{metric}"] = float(fold_df[metric].mean())
        summary[f"std_{metric}"] = float(fold_df[metric].std(ddof=1))

    return summary, fold_df


def balanced_score(
    mean_recall: float,
    mean_precision: float,
    mean_f1: float,
    mean_roc_auc: float,
) -> float:
    # Weighted composite to avoid over-optimizing a single metric.
    return (
        0.30 * mean_recall
        + 0.25 * mean_precision
        + 0.25 * mean_f1
        + 0.20 * mean_roc_auc
    )


def write_table_txt(df: pd.DataFrame, path: Path, title: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write("```text\n")
        f.write(df.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
        f.write("\n```\n")
