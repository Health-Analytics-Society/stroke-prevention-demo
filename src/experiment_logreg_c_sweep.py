from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.base import clone
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
# Config (kept aligned to notebooks/final_demo_baseline_model.ipynb)
# ---------------------------------------------------------------------------
CV_FOLDS = 5
RANDOM_STATE = 42
CV_SHUFFLE = True
THRESHOLD = 0.30  # current project threshold (not 0.5)

C_GRID = [0.001, 0.01, 0.1, 1, 10, 100, 1000]

DATA_REL_PATH = Path("data/raw/stroke_data.csv")
OUTPUT_CSV_REL_PATH = Path("reports/logreg_c_sweep_cv_results.csv")
OUTPUT_MD_REL_PATH = Path("reports/logreg_c_sweep_cv_results.md")

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

CLASS_WEIGHT = "balanced"
MAX_ITER = 2000
SOLVER = "saga"
PENALTY = "elasticnet"
L1_RATIO = 0.5


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def find_repo_root() -> Path:
    here = Path.cwd().resolve()
    for p in [here, *here.parents]:
        if (p / DATA_REL_PATH).exists():
            return p
    return here


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
        l1_ratio=L1_RATIO,
        solver=SOLVER,
        max_iter=MAX_ITER,
        class_weight=CLASS_WEIGHT,
        random_state=RANDOM_STATE,
    )

    return Pipeline(
        steps=[
            ("preprocess", preprocess),
            ("model", model),
        ]
    )


def add_engineered_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    risk_flags = ["diabetes", "hypertension", "high cholesterol", "smoke"]
    present = [c for c in risk_flags if c in out.columns]
    out["multimorbidity"] = out[present].sum(axis=1)

    out["age_x_hypertension"] = out["age"] * out["hypertension"]
    out["age_x_smoke"] = out["age"] * out["smoke"]
    out["age_x_high_cholesterol"] = out["age"] * out["high cholesterol"]

    return out


def load_and_prepare_data(data_path: Path) -> tuple[pd.DataFrame, pd.Series, dict[str, list[str]]]:
    df = pd.read_csv(data_path)

    # Match current notebook preprocessing
    df.columns = df.columns.str.strip()
    df = df.drop_duplicates().reset_index(drop=True)

    zero_cols_present = [c for c in ZERO_AS_MISSING_COLS if c in df.columns]
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

    metadata = {
        "dropped_leakage": drop_cols,
        "dropped_excluded": exclude_cols,
        "dropped_redundant": redundant_cols,
        "ord_cols": ord_cols,
        "nom_cols": nom_cols,
        "num_cols": num_cols,
    }
    return X, y, metadata


def evaluate_c_grid(
    X: pd.DataFrame,
    y: pd.Series,
    ord_cols: list[str],
    nom_cols: list[str],
    num_cols: list[str],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    cv = StratifiedKFold(
        n_splits=CV_FOLDS,
        shuffle=CV_SHUFFLE,
        random_state=RANDOM_STATE,
    )

    per_fold_rows: list[dict[str, float]] = []
    summary_rows: list[dict[str, float]] = []

    for c_value in C_GRID:
        fold_metrics = {
            "recall": [],
            "precision": [],
            "f1": [],
            "roc_auc": [],
            "accuracy": [],
        }

        base_pipeline = build_pipeline(ord_cols, nom_cols, num_cols, c_value)

        for fold_idx, (train_idx, valid_idx) in enumerate(cv.split(X, y), start=1):
            X_train = X.iloc[train_idx].copy()
            X_valid = X.iloc[valid_idx].copy()
            y_train = y.iloc[train_idx]
            y_valid = y.iloc[valid_idx]

            if CLIP_OUTLIERS:
                X_train, X_valid, clipped = apply_iqr_clipping(
                    X_train,
                    X_valid,
                    num_cols,
                    CLIP_IQR_MULTIPLIER,
                )
            else:
                clipped = 0

            fold_pipeline = clone(base_pipeline)
            fold_pipeline.fit(X_train, y_train)

            valid_prob = fold_pipeline.predict_proba(X_valid)[:, 1]
            valid_pred = (valid_prob >= THRESHOLD).astype(int)

            recall = float(recall_score(y_valid, valid_pred, zero_division=0))
            precision = float(precision_score(y_valid, valid_pred, zero_division=0))
            f1 = float(f1_score(y_valid, valid_pred, zero_division=0))
            roc_auc = float(roc_auc_score(y_valid, valid_prob))
            accuracy = float(accuracy_score(y_valid, valid_pred))

            fold_metrics["recall"].append(recall)
            fold_metrics["precision"].append(precision)
            fold_metrics["f1"].append(f1)
            fold_metrics["roc_auc"].append(roc_auc)
            fold_metrics["accuracy"].append(accuracy)

            per_fold_rows.append(
                {
                    "C": float(c_value),
                    "fold": int(fold_idx),
                    "recall": recall,
                    "precision": precision,
                    "f1": f1,
                    "roc_auc": roc_auc,
                    "accuracy": accuracy,
                    "clipped_values": int(clipped),
                }
            )

        row: dict[str, float] = {"C": float(c_value)}
        for metric_name, values in fold_metrics.items():
            row[f"mean_{metric_name}"] = float(np.mean(values))
            row[f"std_{metric_name}"] = float(np.std(values, ddof=1))
        summary_rows.append(row)

    summary_df = pd.DataFrame(summary_rows)

    # Useful sort: prioritize F1 and precision/recall balance, then AUC
    summary_df = summary_df.sort_values(
        by=["mean_f1", "mean_precision", "mean_recall", "mean_roc_auc"],
        ascending=False,
    ).reset_index(drop=True)

    best_c = float(summary_df.loc[0, "C"])
    summary_df["is_best"] = summary_df["C"].eq(best_c)

    per_fold_df = pd.DataFrame(per_fold_rows)
    return summary_df, per_fold_df


def main() -> None:
    root = find_repo_root()
    data_path = root / DATA_REL_PATH
    output_csv = root / OUTPUT_CSV_REL_PATH
    output_md = root / OUTPUT_MD_REL_PATH

    if not data_path.exists():
        raise FileNotFoundError(f"Could not find dataset at: {data_path}")

    X, y, metadata = load_and_prepare_data(data_path)

    summary_df, per_fold_df = evaluate_c_grid(
        X=X,
        y=y,
        ord_cols=metadata["ord_cols"],
        nom_cols=metadata["nom_cols"],
        num_cols=metadata["num_cols"],
    )

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    summary_df.to_csv(output_csv, index=False)

    # Save a markdown table for quick inspection
    table_cols = [
        "C",
        "mean_recall",
        "std_recall",
        "mean_precision",
        "std_precision",
        "mean_f1",
        "std_f1",
        "mean_roc_auc",
        "std_roc_auc",
        "mean_accuracy",
        "std_accuracy",
        "is_best",
    ]
    with open(output_md, "w", encoding="utf-8") as f:
        f.write("# Logistic Regression C Sweep (5-fold Stratified CV)\n\n")
        f.write(f"Threshold used for class predictions: {THRESHOLD}\n\n")
        f.write("## Summary metrics (sorted)\n\n")
        f.write("```text\n")
        f.write(
            summary_df[table_cols].to_string(
                index=False,
                float_format=lambda x: f"{x:.4f}",
            )
        )
        f.write("\n```\n\n")
        f.write("## Per-fold metrics\n\n")
        f.write("```text\n")
        f.write(
            per_fold_df.to_string(
                index=False,
                float_format=lambda x: f"{x:.4f}",
            )
        )
        f.write("\n```\n")

    best_row = summary_df.iloc[0]
    best_c = float(best_row["C"])

    print("Current setup preserved:")
    print("- Model type: LogisticRegression")
    print(f"- penalty={PENALTY}, solver={SOLVER}, l1_ratio={L1_RATIO}, class_weight={CLASS_WEIGHT}")
    print(f"- CV: StratifiedKFold(n_splits={CV_FOLDS}, shuffle={CV_SHUFFLE}, random_state={RANDOM_STATE})")
    print(f"- Threshold for class metrics: {THRESHOLD}")
    print()

    print("Dropped columns:")
    print(f"- leakage: {metadata['dropped_leakage']}")
    print(f"- excluded: {metadata['dropped_excluded']}")
    print(f"- redundant: {metadata['dropped_redundant']}")
    print()

    print("C sweep summary (sorted):")
    print(
        summary_df[
            [
                "C",
                "mean_recall",
                "mean_precision",
                "mean_f1",
                "mean_roc_auc",
                "mean_accuracy",
                "is_best",
            ]
        ].to_string(index=False)
    )
    print()
    print(f"BEST_C={best_c}")
    print(f"Saved CSV: {output_csv}")
    print(f"Saved Markdown: {output_md}")


if __name__ == "__main__":
    main()
