
from pathlib import Path

import joblib
import pandas as pd

DATA_FILE = Path("data") / "production_curves_long.csv"
MODEL_FILE = Path("models") / "production_multioutput_model.joblib"
OUTPUT_DIR = Path("outputs")
OUTPUT_FILE = OUTPUT_DIR / "test_predictions.csv"

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


def main():
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_FILE}. "
            "Run prepare_forecasting_data.py first."
        )

    if not MODEL_FILE.exists():
        raise FileNotFoundError(
            f"Combined model not found: {MODEL_FILE}. "
            "Run train_baseline_model.py first."
        )

    df = pd.read_csv(DATA_FILE, parse_dates=["Date"])

    required = FEATURES[:-1] + [
        "Date",
        "Case",
        "Case_Number",
        "Split",
    ]

    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # Calculate elapsed days from the first observation of each case.
    first_dates = df.groupby("Case_Number")["Date"].min()
    df["First_Date"] = df["Case_Number"].map(first_dates)

    df["Elapsed_Days"] = (
        df["Date"] - df["First_Date"]
    ).dt.total_seconds() / 86400.0

    test = df[df["Split"] == "test"].copy()

    if test.empty:
        raise ValueError("No test cases were found.")

    model = joblib.load(MODEL_FILE)

    predicted = model.predict(test[FEATURES])

    if predicted.shape != (len(test), len(TARGETS)):
        raise ValueError(
            f"Unexpected prediction shape: {predicted.shape}"
        )

    # Keep the same long-format CSV structure expected downstream.
    all_predictions = []

    for i, target in enumerate(TARGETS):
        prediction_frame = test[
            [
                "Case",
                "Case_Number",
                "Date",
                "Elapsed_Days",
                *FEATURES[:-1],
            ]
        ].copy()

        prediction_frame["Target"] = target
        prediction_frame["Predicted"] = predicted[:, i]

        all_predictions.append(prediction_frame)

    predictions_df = pd.concat(
        all_predictions,
        ignore_index=True,
    )

    OUTPUT_DIR.mkdir(exist_ok=True)
    predictions_df.to_csv(OUTPUT_FILE, index=False)

    print("=" * 60)
    print("TEST PREDICTIONS GENERATED")
    print("=" * 60)
    print(f"Test cases: {test['Case_Number'].nunique()}")
    print(f"Rows per target: {len(test):,}")
    print(f"Total prediction rows: {len(predictions_df):,}")
    print(f"Targets: {', '.join(TARGETS)}")
    print(f"Saved to: {OUTPUT_FILE.resolve()}")


if __name__ == "__main__":
    main()
