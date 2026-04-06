from __future__ import annotations

import numpy as np
import pandas as pd

from logreg_experiment_utils import (
    CLIP_IQR_MULTIPLIER,
    CLIP_OUTLIERS,
    DATA_REL_PATH,
    RANDOM_STATE,
    CV_FOLDS,
    CV_SHUFFLE,
    apply_iqr_clipping,
    balanced_score,
    build_pipeline,
    class_weight_label,
    cv_splits,
    find_repo_root,
    fold_metrics_from_predictions,
    load_and_prepare_data,
    write_table_txt,
)


# Keep current model hyperparameters fixed; vary only threshold.
FIXED_C = 0.1
FIXED_L1_RATIO = 0.5
FIXED_CLASS_WEIGHT = "balanced"

THRESHOLD_GRID = [round(float(t), 2) for t in np.arange(0.05, 1.00, 0.05)]

OUTPUT_SUMMARY_CSV = "reports/threshold_sweep_cv_results.csv"
OUTPUT_FOLDS_CSV = "reports/threshold_sweep_cv_fold_results.csv"
OUTPUT_TXT = "reports/threshold_sweep_cv_results.txt"


def main() -> None:
    root = find_repo_root()
    prepared = load_and_prepare_data(root / DATA_REL_PATH)

    splits = cv_splits(prepared.X, prepared.y)

    # Fit once per fold, then evaluate all thresholds from the same probabilities.
    fold_cache = []
    for fold_idx, (train_idx, valid_idx) in enumerate(splits, start=1):
        X_train = prepared.X.iloc[train_idx].copy()
        X_valid = prepared.X.iloc[valid_idx].copy()
        y_train = prepared.y.iloc[train_idx]
        y_valid = prepared.y.iloc[valid_idx]

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
            c_value=FIXED_C,
            l1_ratio=FIXED_L1_RATIO,
            class_weight=FIXED_CLASS_WEIGHT,
        )
        pipeline.fit(X_train, y_train)

        y_prob = pipeline.predict_proba(X_valid)[:, 1]

        fold_cache.append(
            {
                "fold": fold_idx,
                "y_valid": y_valid,
                "y_prob": y_prob,
                "clipped_values": clipped,
            }
        )

    per_fold_rows = []
    summary_rows = []

    for threshold in THRESHOLD_GRID:
        fold_metrics_rows = []
        for fold_item in fold_cache:
            metrics = fold_metrics_from_predictions(
                y_true=fold_item["y_valid"],
                y_prob=fold_item["y_prob"],
                threshold=threshold,
            )
            row = {
                "threshold": threshold,
                "fold": fold_item["fold"],
                "C": FIXED_C,
                "l1_ratio": FIXED_L1_RATIO,
                "class_weight": class_weight_label(FIXED_CLASS_WEIGHT),
                "clipped_values": fold_item["clipped_values"],
            }
            row.update(metrics)
            fold_metrics_rows.append(row)
            per_fold_rows.append(row)

        fold_df = pd.DataFrame(fold_metrics_rows)

        summary = {
            "threshold": threshold,
            "C": FIXED_C,
            "l1_ratio": FIXED_L1_RATIO,
            "class_weight": class_weight_label(FIXED_CLASS_WEIGHT),
            "mean_recall": float(fold_df["recall"].mean()),
            "std_recall": float(fold_df["recall"].std(ddof=1)),
            "mean_precision": float(fold_df["precision"].mean()),
            "std_precision": float(fold_df["precision"].std(ddof=1)),
            "mean_f1": float(fold_df["f1"].mean()),
            "std_f1": float(fold_df["f1"].std(ddof=1)),
            "mean_roc_auc": float(fold_df["roc_auc"].mean()),
            "std_roc_auc": float(fold_df["roc_auc"].std(ddof=1)),
            "mean_accuracy": float(fold_df["accuracy"].mean()),
            "std_accuracy": float(fold_df["accuracy"].std(ddof=1)),
        }
        summary["balanced_score"] = balanced_score(
            summary["mean_recall"],
            summary["mean_precision"],
            summary["mean_f1"],
            summary["mean_roc_auc"],
        )
        summary_rows.append(summary)

    summary_df = pd.DataFrame(summary_rows).sort_values(
        by=["balanced_score", "mean_f1", "mean_precision", "mean_recall", "mean_roc_auc"],
        ascending=False,
    ).reset_index(drop=True)

    best_threshold = float(summary_df.loc[0, "threshold"])
    summary_df["is_best"] = summary_df["threshold"].eq(best_threshold)

    fold_results_df = pd.DataFrame(per_fold_rows)

    summary_path = root / OUTPUT_SUMMARY_CSV
    folds_path = root / OUTPUT_FOLDS_CSV
    txt_path = root / OUTPUT_TXT

    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_df.to_csv(summary_path, index=False)
    fold_results_df.to_csv(folds_path, index=False)

    view_cols = [
        "threshold",
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
        "balanced_score",
        "is_best",
    ]
    write_table_txt(
        summary_df[view_cols],
        txt_path,
        title="Threshold Sweep (Current Logistic Setup, 5-fold Stratified CV)",
    )

    print("Threshold-only experiment complete")
    print(f"Fixed model: C={FIXED_C}, l1_ratio={FIXED_L1_RATIO}, class_weight={FIXED_CLASS_WEIGHT}")
    print(f"CV: n_splits={CV_FOLDS}, shuffle={CV_SHUFFLE}, random_state={RANDOM_STATE}")
    print()
    print(summary_df[["threshold", "mean_recall", "mean_precision", "mean_f1", "mean_roc_auc", "balanced_score", "is_best"]].to_string(index=False))
    print()
    print(f"BEST_THRESHOLD={best_threshold}")
    print(f"Saved summary: {summary_path}")
    print(f"Saved per-fold: {folds_path}")
    print(f"Saved text table: {txt_path}")


if __name__ == "__main__":
    main()
