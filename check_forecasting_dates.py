
from pathlib import Path

import pandas as pd

DATA_FILE = Path("data") / "production_curves_long.csv"

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

    df = pd.read_csv(DATA_FILE, parse_dates=["Date"])

    print("=" * 70)
    print("FORECASTING DATE CHECK")
    print("=" * 70)

    print("\nRows by split:")
    print(df.groupby("Split")["Case"].nunique().to_string())

    print("\nDate coverage by split:")
    for split in ["train", "validation", "test"]:
        subset = df[df["Split"] == split]

        print(f"\n{split.upper()}")
        print("Cases:", subset["Case"].nunique())
        print("Earliest date:", subset["Date"].min())
        print("Latest date:", subset["Date"].max())

    print("\nObservation counts by target:")
    for target in TARGETS:
        print(f"\n{target}")
        print(
            df.groupby("Split")[target]
            .count()
            .to_string()
        )

    print("\nChecking whether target dates align within each case...")

    for target in TARGETS:
        valid = df.dropna(subset=[target])
        counts = valid.groupby("Case_Number")["Date"].nunique()

        print(
            f"{target}: minimum dates per case = {counts.min()}, "
            f"maximum = {counts.max()}"
        )

    print("\nFirst and last dates for selected cases:")
    for case_number in [1, 70, 71, 85, 86, 100]:
        subset = df[df["Case_Number"] == case_number]

        if subset.empty:
            print(f"Case {case_number}: not found")
            continue

        print(
            f"Case {case_number}: "
            f"{subset['Date'].min()} to {subset['Date'].max()}, "
            f"{len(subset)} rows"
        )

    print("\nDate check complete. No files were modified.")


if __name__ == "__main__":
    main()
