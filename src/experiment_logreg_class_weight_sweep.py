from __future__ import annotations

import pandas as pd

from logreg_experiment_utils import (
    CV_FOLDS,
    CV_SHUFFLE,
    DATA_REL_PATH,
    RANDOM_STATE,
    balanced_score,
    evaluate_setting,
    find_repo_root,
    load_and_prepare_data,
    write_table_txt,
)


# Keep current baseline settings fixed, vary only class_weight.
FIXED_C = 0.1
FIXED_L1_RATIO = 0.5
FIXED_THRESHOLD = 0.30

CLASS_WEIGHT_GRID = [
    None,
    "balanced",
    {0: 1.0, 1: 0.50},
    {0: 1.0, 1: 0.75},
    {0: 1.0, 1: 1.50},
    {0: 1.0, 1: 2.00},
    {0: 1.0, 1: 3.00},
    {0: 1.0, 1: 4.00},
    {0: 1.0, 1: 6.00},
    {0: 1.0, 1: 8.00},
]

OUTPUT_SUMMARY_CSV = "reports/class_weight_sweep_cv_results.csv"
OUTPUT_FOLDS_CSV = "reports/class_weight_sweep_cv_fold_results.csv"
OUTPUT_TXT = "reports/class_weight_sweep_cv_results.txt"


def main() -> None:
    root = find_repo_root()
    prepared = load_and_prepare_data(root / DATA_REL_PATH)

    summary_rows = []
    fold_tables = []

    for class_weight in CLASS_WEIGHT_GRID:
        summary, fold_df = evaluate_setting(
            prepared=prepared,
            c_value=FIXED_C,
            l1_ratio=FIXED_L1_RATIO,
            class_weight=class_weight,
            threshold=FIXED_THRESHOLD,
        )
        summary["balanced_score"] = balanced_score(
            summary["mean_recall"],
            summary["mean_precision"],
            summary["mean_f1"],
            summary["mean_roc_auc"],
        )
        summary_rows.append(summary)
        fold_tables.append(fold_df)

    summary_df = pd.DataFrame(summary_rows).sort_values(
        by=["balanced_score", "mean_f1", "mean_precision", "mean_recall", "mean_roc_auc"],
        ascending=False,
    ).reset_index(drop=True)

    best_class_weight = summary_df.loc[0, "class_weight"]
    summary_df["is_best"] = summary_df["class_weight"].eq(best_class_weight)

    fold_results_df = pd.concat(fold_tables, axis=0, ignore_index=True)

    summary_path = root / OUTPUT_SUMMARY_CSV
    folds_path = root / OUTPUT_FOLDS_CSV
    txt_path = root / OUTPUT_TXT

    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_df.to_csv(summary_path, index=False)
    fold_results_df.to_csv(folds_path, index=False)

    view_cols = [
        "class_weight",
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
        title="Class-Weight Sweep (Current Logistic Setup, 5-fold Stratified CV)",
    )

    print("Class-weight-only experiment complete")
    print(f"Fixed model: C={FIXED_C}, l1_ratio={FIXED_L1_RATIO}, threshold={FIXED_THRESHOLD}")
    print(f"CV: n_splits={CV_FOLDS}, shuffle={CV_SHUFFLE}, random_state={RANDOM_STATE}")
    print()
    print(summary_df[["class_weight", "mean_recall", "mean_precision", "mean_f1", "mean_roc_auc", "balanced_score", "is_best"]].to_string(index=False))
    print()
    print(f"BEST_CLASS_WEIGHT={best_class_weight}")
    print(f"Saved summary: {summary_path}")
    print(f"Saved per-fold: {folds_path}")
    print(f"Saved text table: {txt_path}")


if __name__ == "__main__":
    main()
