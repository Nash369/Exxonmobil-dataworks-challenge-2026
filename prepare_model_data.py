
import pandas as pd
from pathlib import Path

DATA_DIR = Path(r"C:\Users\Nashran\Downloads")

UNCERTAINTY_FILE = DATA_DIR / "01 Introduction.xlsx"
PRODUCTION_FILE = DATA_DIR / "02 Field Production(1).xlsx"

PRODUCTION_SHEETS = [
    "Oil production cumulative",
    "Gas production cumulative",
    "Water production cumulative",
]


def load_uncertainty_values():
    """Load and inspect the uncertainty-value table."""
    df = pd.read_excel(
        UNCERTAINTY_FILE,
        sheet_name="Uncertainty Values",
        engine="openpyxl",
    )

    print("\n===== UNCERTAINTY VALUES =====")
    print("Columns:", df.columns.tolist())
    print("Shape:", df.shape)
    print(df.head(5).to_string(index=False))

    return df


def load_production_curve(sheet_name):
    """Load a cumulative production curve sheet."""
    df = pd.read_excel(
        PRODUCTION_FILE,
        sheet_name=sheet_name,
        header=1,
        engine="openpyxl",
    )

    df["Date"] = pd.to_datetime(
        df["Date"], errors="coerce"
    )
    df = df.dropna(subset=["Date"]).copy()

    case_columns = [
        col for col in df.columns
        if str(col).startswith("Case_")
    ]

    print(f"\n===== {sheet_name} =====")
    print("Shape:", df.shape)
    print("Case columns:", len(case_columns))
    print("First date:", df["Date"].min())
    print("Last date:", df["Date"].max())

    if case_columns:
        print("Example cases:", case_columns[:5])
        print(
            "Valid values in Case_1:",
            int(df["Case_1"].notna().sum()),
        )

    return df


def main():
    if not UNCERTAINTY_FILE.exists():
        print("Uncertainty file not found:", UNCERTAINTY_FILE)
        return

    if not PRODUCTION_FILE.exists():
        print("Production file not found:", PRODUCTION_FILE)
        return

    uncertainty = load_uncertainty_values()

    curves = {}
    for sheet in PRODUCTION_SHEETS:
        curves[sheet] = load_production_curve(sheet)

    print("\n===== ALIGNMENT CHECK =====")
    print("Uncertainty rows:", len(uncertainty))

    for sheet, df in curves.items():
        cases = [
            col for col in df.columns
            if str(col).startswith("Case_")
        ]
        print(f"{sheet}: {len(cases)} case columns")

    print("\nInspection complete. No files were modified.")


if __name__ == "__main__":
    main()
