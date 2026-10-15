
from pathlib import Path

import numpy as np
import pandas as pd

PREDICTIONS_FILE = Path("outputs") / "validation_predictions.csv"
OUTPUT_FILE = Path("outputs") / "validation_case_metrics.csv"


def calculate_metrics(group):
    actual = group["Actual"].to_numpy(dtype=float)
    predicted = group["Predicted"].to_numpy(dtype=float)

    errors = predicted - actual

    rmse = float(np.sqrt(np.mean(errors**2)))
    mae = float(np.mean(np.abs(errors)))

    actual_range = float(actual.max() - actual.min())
    nrmse = rmse / actual_range if actual_range > 0 else np.nan

    final_actual = float(actual[-1])
    final_predicted = float(predicted[-1])

    final_error_pct = (
        100 * (final_predicted - final_actual) / abs(final_actual)
        if final_actual != 0 else np.nan
    )

    return pd.Series({
        "Observations": len(group),
        "RMSE": rmse,
        "MAE": mae,
        "NRMSE": nrmse,
        "Final_Actual": final_actual,
        "Final_Predicted": final_predicted,
        "Final_Error_Percent": final_error_pct,
    })


def main():
    if not PREDICTIONS_FILE.exists():
        raise FileNotFoundError(
            f"Predictions file not found: {PREDICTIONS_FILE}. "
            "Run train_baseline_model.py first."
        )

    predictions = pd.read_csv(
        PREDICTIONS_FILE,
        parse_dates=["Date"],
    )

    required = {
        "Case",
        "Date",
        "Actual",
        "Predicted",
        "Target",
    }

    missing = required - set(predictions.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    predictions = predictions.sort_values(["Target", "Case", "Date"])

    metrics = (
        predictions.groupby(["Target", "Case"], sort=False)
        .apply(calculate_metrics, include_groups=False)
        .reset_index()
    )

    print("=" * 75)
    print("VALIDATION PERFORMANCE BY CASE")
    print("=" * 75)

    for target in metrics["Target"].unique():
        subset = metrics[metrics["Target"] == target].copy()
        subset = subset.sort_values("NRMSE")

        print(f"\n{target}")
        print(
            subset[
                [
                    "Case",
                    "Observations",
                    "NRMSE",
                    "Final_Actual",
                    "Final_Predicted",
                    "Final_Error_Percent",
                ]
            ].round(4).to_string(index=False)
        )

        print("\nAverage case-level NRMSE:", round(subset["NRMSE"].mean(), 5))
        print("Median case-level NRMSE:", round(subset["NRMSE"].median(), 5))

    metrics.to_csv(OUTPUT_FILE, index=False)
    print(f"\nSaved case-level metrics to: {OUTPUT_FILE.resolve()}")


if __name__ == "__main__":
    main()
