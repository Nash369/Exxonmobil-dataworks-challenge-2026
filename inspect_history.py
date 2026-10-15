
from pathlib import Path

import pandas as pd

# Update this path only if your workbook is stored elsewhere.
PRODUCTION_FILE = (
    Path.home() / "Downloads" / "02 Field Production(1).xlsx"
)

CURVE_SHEETS = {
    "Oil production cumulative": "oil cumulative",
    "Gas production cumulative": "gas cumulative",
    "Water production cumulative": "water cumulative",
}


def load_curve(sheet_name):
    df = pd.read_excel(
        PRODUCTION_FILE,
        sheet_name=sheet_name,
        header=1,
    )

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])

    return df


def main():
    if not PRODUCTION_FILE.exists():
        raise FileNotFoundError(
            f"Workbook not found: {PRODUCTION_FILE}\n"
            "Check that the file is in your Downloads folder."
        )

    print("=" * 70)
    print("HISTORY DATA INSPECTION")
    print("=" * 70)

    # Inspect the separate field-production history sheet.
    field = pd.read_excel(
        PRODUCTION_FILE,
        sheet_name="Field Production",
    )

    print("\nFIELD PRODUCTION SHEET")
    print("Shape:", field.shape)
    print("Columns:", field.columns.tolist())
    print(field.head(5).to_string(index=False))

    # Inspect cumulative production curves.
    for sheet_name, label in CURVE_SHEETS.items():
        print(f"\n{'=' * 70}")
        print(f"{label.upper()}")

        df = load_curve(sheet_name)

        print("Shape:", df.shape)
        print("Date range:", df["Date"].min(), "to", df["Date"].max())

        if "RAMP_History" not in df.columns:
            print("RAMP_History column not found.")
            continue

        history = df[["Date", "RAMP_History"]].dropna(
            subset=["RAMP_History"]
        )

        print("Historical observations:", len(history))

        if history.empty:
            print("No historical observations found.")
            continue

        print("\nFirst 10 historical observations:")
        print(history.head(10).to_string(index=False))

        print("\nLast 10 historical observations:")
        print(history.tail(10).to_string(index=False))

        print("\nHistorical value range:")
        print("Minimum:", history["RAMP_History"].min())
        print("Maximum:", history["RAMP_History"].max())

        print("\nSimulation case example:")
        if "Case_1" in df.columns:
            example = df[["Date", "Case_1"]].dropna(
                subset=["Case_1"]
            )
            print("Case_1 valid observations:", len(example))
            print(example.head(5).to_string(index=False))
            print(example.tail(5).to_string(index=False))


if __name__ == "__main__":
    main()
