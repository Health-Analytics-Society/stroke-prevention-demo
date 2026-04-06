from __future__ import annotations

from itertools import product

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


# Joint sweep across C, l1_ratio, and class_weight.
# Threshold is held fixed to isolate training-time settings.
C_GRID = [0.01, 0.1, 1.0, 10.0]
L1_RATIO_GRID = [0.2, 0.5, 0.8]
CLASS_WEIGHT_GRID = [
    None,
    "balanced",
    {0: 1.0, 1: 2.0},
    {0: 1.0, 1: 4.0},
    {0: 1.0, 1: 6.0},
]
FIXED_THRESHOLD = 0.30

OUTPUT_SUMMARY_CSV = "reports/joint_c_l1_classweight_cv_results.csv"
OUTPUT_FOLDS_CSV = "reports/joint_c_l1_classweight_cv_fold_results.csv"
OUTPUT_TXT = "reports/joint_c_l1_classweight_cv_results.txt"


def main() -> None:
    root = find_repo_root()
    prepared = load_and_prepare_data(root / DATA_REL_PATH)

    summary_rows = []
    fold_tables = []

    grid = list(product(C_GRID, L1_RATIO_GRID, CLASS_WEIGHT_GRID))
    total = len(grid)

    for idx, (c_value, l1_ratio, class_weight) in enumerate(grid, start=1):
        summary, fold_df = evaluate_setting(
            prepared=prepared,
            c_value=float(c_value),
            l1_ratio=float(l1_ratio),
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

        print(
            f"[{idx:>2}/{total}] C={summary['C']}, l1_ratio={summary['l1_ratio']}, "
            f"class_weight={summary['class_weight']} | "
            f"rec={summary['mean_recall']:.4f} prec={summary['mean_precision']:.4f} "
            f"f1={summary['mean_f1']:.4f} auc={summary['mean_roc_auc']:.4f} "
            f"score={summary['balanced_score']:.4f}"
        )

    summary_df = pd.DataFrame(summary_rows).sort_values(
        by=["balanced_score", "mean_f1", "mean_precision", "mean_recall", "mean_roc_auc"],
        ascending=False,
    ).reset_index(drop=True)

    top_key = (
        summary_df.loc[0, "C"],
        summary_df.loc[0, "l1_ratio"],
        summary_df.loc[0, "class_weight"],
    )

    summary_df["is_best"] = summary_df.apply(
        lambda r: (r["C"], r["l1_ratio"], r["class_weight"]) == top_key,
        axis=1,
    )

    fold_results_df = pd.concat(fold_tables, axis=0, ignore_index=True)

    summary_path = root / OUTPUT_SUMMARY_CSV
    folds_path = root / OUTPUT_FOLDS_CSV
    txt_path = root / OUTPUT_TXT

    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_df.to_csv(summary_path, index=False)
    fold_results_df.to_csv(folds_path, index=False)

    view_cols = [
        "C",
        "l1_ratio",
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
        title="Joint Sweep: C x l1_ratio x class_weight (5-fold Stratified CV)",
    )

    best = summary_df.iloc[0]

    print("Joint experiment complete")
    print(f"Threshold fixed at: {FIXED_THRESHOLD}")
    print(f"CV: n_splits={CV_FOLDS}, shuffle={CV_SHUFFLE}, random_state={RANDOM_STATE}")
    print()
    print(summary_df[["C", "l1_ratio", "class_weight", "mean_recall", "mean_precision", "mean_f1", "mean_roc_auc", "balanced_score", "is_best"]].head(20).to_string(index=False))
    print()
    print(
        "BEST_COMBINATION="
        f"C:{best['C']},l1_ratio:{best['l1_ratio']},class_weight:{best['class_weight']}"
    )
    print(f"Saved summary: {summary_path}")
    print(f"Saved per-fold: {folds_path}")
    print(f"Saved text table: {txt_path}")


if __name__ == "__main__":
    main()
