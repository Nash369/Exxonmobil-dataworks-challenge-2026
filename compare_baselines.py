
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error

DATA_FILE = Path("data") / "production_curves_long.csv"
PREDICTIONS_FILE = Path("outputs") / "validation_predictions.csv"

TARGETS = [
    "oil_cumulative",
    "gas_cumulative",
    "water_cumulative",
]


def calculate_metrics(actual, predicted):
    rmse = float(np.sqrt(mean_squared_error(actual, predicted)))
    mae = float(mean_absolute_error(actual, predicted))
    return rmse, mae


def main():
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_FILE}. "
            "Run prepare_forecasting_data.py first."
        )

    if not PREDICTIONS_FILE.exists():
        raise FileNotFoundError(
            f"Predictions not found: {PREDICTIONS_FILE}. "
            "Run train_baseline_model.py first."
        )

    df = pd.read_csv(DATA_FILE, parse_dates=["Date"])
    predictions = pd.read_csv(
        PREDICTIONS_FILE,
        parse_dates=["Date"],
    )

    required = {
        "Case",
        "Case_Number",
        "Date",
        "Split",
        "oil_cumulative",
        "gas_cumulative",
        "water_cumulative",
    }

    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Dataset missing columns: {sorted(missing)}")

    prediction_required = {
        "Case_Number",
        "Date",
        "Actual",
        "Predicted",
        "Target",
    }

    missing = prediction_required - set(predictions.columns)
    if missing:
        raise ValueError(
            f"Predictions missing columns: {sorted(missing)}"
        )

    # Calculate elapsed time relative to each case's first date.
    first_dates = df.groupby("Case_Number")["Date"].min()
    df["First_Date"] = df["Case_Number"].map(first_dates)
    df["Elapsed_Days"] = (
        df["Date"] - df["First_Date"]
    ).dt.total_seconds() / 86400.0

    train = df[df["Split"] == "train"].copy()
    validation = df[df["Split"] == "validation"].copy()

    if train.empty or validation.empty:
        raise ValueError("Training or validation data is empty.")

    print("=" * 75)
    print("EXTRA TREES VS TIME-BASED BASELINE")
    print("=" * 75)

    for target in TARGETS:
        print(f"\nTarget: {target}")

        # Average the training cases at each elapsed time.
        baseline_curve = (
            train.groupby("Elapsed_Days")[target]
            .mean()
            .sort_index()
        )

        if baseline_curve.empty:
            print("No training values available for this target.")
            continue

        # Build the time-based baseline for validation observations.
        baseline = validation[
            ["Case", "Case_Number", "Date", "Elapsed_Days", target]
        ].copy()

        baseline["Baseline_Predicted"] = np.interp(
            baseline["Elapsed_Days"].to_numpy(dtype=float),
            baseline_curve.index.to_numpy(dtype=float),
            baseline_curve.to_numpy(dtype=float),
        )

        # Match predictions by case and date.
        model_rows = predictions[
            predictions["Target"] == target
        ][
            ["Case_Number", "Date", "Actual", "Predicted"]
        ].copy()

        baseline["Date"] = pd.to_datetime(baseline["Date"])
        model_rows["Date"] = pd.to_datetime(model_rows["Date"])

        comparison = baseline.merge(
            model_rows,
            on=["Case_Number", "Date"],
            how="inner",
            validate="one_to_one",
        )

        if comparison.empty:
            print("No matching validation predictions found.")
            continue

        model_rmse, model_mae = calculate_metrics(
            comparison["Actual"],
            comparison["Predicted"],
        )

        baseline_rmse, baseline_mae = calculate_metrics(
            comparison[target],
            comparison["Baseline_Predicted"],
        )

        improvement = (
            100.0 * (baseline_rmse - model_rmse) / baseline_rmse
            if baseline_rmse > 0
            else np.nan
        )

        print(f"Matched observations: {len(comparison):,}")
        print(f"Extra Trees RMSE:     {model_rmse:,.3f}")
        print(f"Time baseline RMSE:   {baseline_rmse:,.3f}")
        print(f"Extra Trees MAE:      {model_mae:,.3f}")
        print(f"Time baseline MAE:    {baseline_mae:,.3f}")
        print(f"RMSE improvement:     {improvement:.2f}%")

        if model_rmse < baseline_rmse:
            print("Result: Extra Trees has lower RMSE.")
        elif model_rmse > baseline_rmse:
            print("Result: Time baseline has lower RMSE.")
        else:
            print("Result: Both models have equal RMSE.")

    print("\nComparison complete. Existing models and predictions were not changed.")


if __name__ == "__main__":
    main()

