
from pathlib import Path

import joblib
import pandas as pd

DATA_FILE = Path("data") / "production_curves_long.csv"
MODEL_DIR = Path("models")
OUTPUT_DIR = Path("outputs")

TARGETS = [
    "oil_cumulative",
    "gas_cumulative",
    "water_cumulative",
]

PARAMETERS = [
    "Fault Transmissibility",
    "Porosity Multiplier",
    "Permeability Multiplier",
    "Aquifer Pore Volume",
]

FEATURES = PARAMETERS + ["Elapsed_Days"]


def main():
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_FILE}. "
            "Run prepare_forecasting_data.py first."
        )

    missing_models = [
        target for target in TARGETS
        if not (MODEL_DIR / f"{target}_extra_trees.joblib").exists()
    ]

    if missing_models:
        raise FileNotFoundError(
            "Missing trained models for: "
            + ", ".join(missing_models)
            + ". Run train_baseline_model.py first."
        )

    df = pd.read_csv(DATA_FILE, parse_dates=["Date"])

    required = {
        "Case",
        "Case_Number",
        "Date",
        "Split",
        *FEATURES[:-1],
    }

    missing_columns = required - set(df.columns)
    if missing_columns:
        raise ValueError(
            f"Dataset missing columns: {sorted(missing_columns)}"
        )

    # Keep only the held-out test cases: Cases 86–100.
    test = df[df["Split"] == "test"].copy()

    if test.empty:
        raise ValueError("No test cases found.")

    found_cases = sorted(test["Case_Number"].unique().tolist())
    expected_cases = list(range(86, 101))

    if found_cases != expected_cases:
        raise ValueError(
            f"Expected test cases 86–100, but found: {found_cases}"
        )

    # Use the same elapsed-time definition as the training script.
    first_dates = df.groupby("Case_Number")["Date"].min()
    test["First_Date"] = test["Case_Number"].map(first_dates)
    test["Elapsed_Days"] = (
        test["Date"] - test["First_Date"]
    ).dt.total_seconds() / 86400.0

    OUTPUT_DIR.mkdir(exist_ok=True)

    all_predictions = []

    for target in TARGETS:
        model_path = MODEL_DIR / f"{target}_extra_trees.joblib"
        model = joblib.load(model_path)

        predicted = model.predict(test[FEATURES])

        result = test[
            ["Case", "Case_Number", "Date", "Elapsed_Days"]
            + PARAMETERS
        ].copy()

        result["Target"] = target
        result["Predicted"] = predicted

        all_predictions.append(result)

        print(
            f"{target}: generated {len(result):,} predictions "
            f"for {result['Case'].nunique()} test cases"
        )

    predictions = pd.concat(all_predictions, ignore_index=True)

    output_file = OUTPUT_DIR / "test_predictions.csv"
    predictions.to_csv(output_file, index=False)

    print("\n" + "=" * 70)
    print("TEST PREDICTIONS GENERATED")
    print("=" * 70)
    print("Cases:", len(found_cases))
    print("Case range:", f"{found_cases[0]}–{found_cases[-1]}")
    print("Prediction rows:", f"{len(predictions):,}")
    print("Missing predictions:", int(predictions["Predicted"].isna().sum()))
    print("Non-finite predictions:", int((~predictions["Predicted"].map(
        lambda value: pd.notna(value) and abs(value) != float("inf")
    )).sum()))
    print(f"Saved to: {output_file.resolve()}")

    print("\nThis file contains model predictions, not measured test outcomes.")
    print("Do not commit the predictions or challenge datasets to GitHub.")


if __name__ == "__main__":
    main()
