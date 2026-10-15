
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.ensemble import ExtraTreesRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

DATA_FILE = Path("data") / "production_curves_long.csv"
MODEL_DIR = Path("models")
OUTPUT_DIR = Path("outputs")

FEATURES = [
    "Fault Transmissibility",
    "Porosity Multiplier",
    "Permeability Multiplier",
    "Aquifer Pore Volume",
    "Elapsed_Days",
]

TARGETS = [
    "oil_cumulative",
    "gas_cumulative",
    "water_cumulative",
]


def rmse(actual, predicted):
    return float(np.sqrt(mean_squared_error(actual, predicted)))


def main():
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_FILE}. "
            "Run prepare_forecasting_data.py first."
        )

    df = pd.read_csv(DATA_FILE, parse_dates=["Date"])

    required = FEATURES[:-1] + TARGETS + [
        "Date",
        "Case_Number",
        "Split",
    ]

    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # Use each case's first available date as its time origin.
    first_dates = df.groupby("Case_Number")["Date"].min()
    df["First_Date"] = df["Case_Number"].map(first_dates)

    df["Elapsed_Days"] = (
        df["Date"] - df["First_Date"]
    ).dt.total_seconds() / 86400.0

    # Keep each split separate by case, not by individual observation.
    train = df[df["Split"] == "train"].copy()
    validation = df[df["Split"] == "validation"].copy()

    if train.empty or validation.empty:
        raise ValueError("Training or validation data is empty.")

    MODEL_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)

    all_metrics = []
    all_predictions = []

    for target in TARGETS:
        print(f"\nTraining model for {target}...")

        model = make_pipeline(
            SimpleImputer(strategy="median"),
            ExtraTreesRegressor(
                n_estimators=200,
                min_samples_leaf=2,
                max_features=1.0,
                random_state=42,
                n_jobs=-1,
            ),
        )

        model.fit(train[FEATURES], train[target])

        predicted = model.predict(validation[FEATURES])
        actual = validation[target].to_numpy()

        model_rmse = rmse(actual, predicted)
        model_mae = float(mean_absolute_error(actual, predicted))

        # Simple baseline: use the training-set mean for every row.
        baseline_predicted = np.full(
            len(validation),
            train[target].mean(),
        )

        baseline_rmse = rmse(actual, baseline_predicted)
        baseline_mae = float(
            mean_absolute_error(actual, baseline_predicted)
        )

        improvement = (
            100 * (baseline_rmse - model_rmse) / baseline_rmse
            if baseline_rmse > 0 else np.nan
        )

        all_metrics.append({
            "Target": target,
            "Model_RMSE": model_rmse,
            "Baseline_RMSE": baseline_rmse,
            "Model_MAE": model_mae,
            "Baseline_MAE": baseline_mae,
            "RMSE_Improvement_Percent": improvement,
        })

        prediction_frame = validation[
            ["Case", "Case_Number", "Date", "Elapsed_Days", target]
        ].copy()

        prediction_frame = prediction_frame.rename(
            columns={target: "Actual"}
        )
        prediction_frame["Predicted"] = predicted
        prediction_frame["Target"] = target

        all_predictions.append(prediction_frame)

        joblib.dump(
            model,
            MODEL_DIR / f"{target}_extra_trees.joblib",
        )

        print(f"Validation RMSE: {model_rmse:,.3f}")
        print(f"Baseline RMSE:   {baseline_rmse:,.3f}")
        print(f"Validation MAE:  {model_mae:,.3f}")
        print(f"Baseline MAE:    {baseline_mae:,.3f}")
        print(f"RMSE improvement: {improvement:.2f}%")

    metrics_df = pd.DataFrame(all_metrics)
    predictions_df = pd.concat(
        all_predictions,
        ignore_index=True,
    )

    metrics_file = OUTPUT_DIR / "validation_metrics.csv"
    predictions_file = OUTPUT_DIR / "validation_predictions.csv"

    metrics_df.to_csv(metrics_file, index=False)
    predictions_df.to_csv(predictions_file, index=False)

    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    print(metrics_df.round(3).to_string(index=False))

    print(f"\nMetrics saved to: {metrics_file.resolve()}")
    print(f"Predictions saved to: {predictions_file.resolve()}")
    print(f"Models saved in: {MODEL_DIR.resolve()}")
    print("\nKeep generated data, models and outputs out of GitHub.")


if __name__ == "__main__":
    main()
