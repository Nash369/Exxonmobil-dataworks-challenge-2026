
from pathlib import Path

import pandas as pd

INTRO_FILE = Path.home() / "Downloads" / "01 Introduction.xlsx"
PRODUCTION_FILE = Path.home() / "Downloads" / "02 Field Production(1).xlsx"

OUTPUT_DIR = Path("data")
OUTPUT_FILE = OUTPUT_DIR / "production_curves_long.csv"

PRODUCTION_SHEETS = {
    "Oil production cumulative": "oil_cumulative",
    "Gas production cumulative": "gas_cumulative",
    "Water production cumulative": "water_cumulative",
}

PARAMETERS = [
    "Fault Transmissibility",
    "Porosity Multiplier",
    "Permeability Multiplier",
    "Aquifer Pore Volume",
]


def load_uncertainty_parameters():
    df = pd.read_excel(
        INTRO_FILE,
        sheet_name="Uncertainty Values",
    )

    # Extract the case number from the Item field.
    df["Case"] = df["Item"].astype(str).str.extract(
        r"(\d+)"
    )[0]

    df = df.dropna(subset=["Case"]).copy()
    df["Case"] = "Case_" + df["Case"].astype(int).astype(str)

    return df[["Case"] + PARAMETERS]


def load_production_curve(sheet_name, target_name):
    df = pd.read_excel(
        PRODUCTION_FILE,
        sheet_name=sheet_name,
        header=1,
    )

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])

    case_columns = [
        col for col in df.columns
        if str(col).startswith("Case_")
    ]

    # Keep the original observed dates and values.
    long_df = df.melt(
        id_vars=["Date"],
        value_vars=case_columns,
        var_name="Case",
        value_name=target_name,
    )

    long_df[target_name] = pd.to_numeric(
        long_df[target_name],
        errors="coerce",
    )

    long_df = long_df.dropna(subset=[target_name])

    return long_df


def main():
    for file_path in [INTRO_FILE, PRODUCTION_FILE]:
        if not file_path.exists():
            raise FileNotFoundError(
                f"Required workbook not found: {file_path}"
            )

    print("Loading uncertainty parameters...")
    parameters = load_uncertainty_parameters()

    if parameters["Case"].nunique() != 100:
        raise ValueError(
            "Expected 100 unique cases in the uncertainty workbook."
        )

    print("Loading cumulative production curves...")
    curves = []

    for sheet_name, target_name in PRODUCTION_SHEETS.items():
        curve = load_production_curve(sheet_name, target_name)
        curves.append(curve)

        print(
            f"{target_name}: {len(curve):,} valid observations "
            f"across {curve['Case'].nunique()} cases"
        )

    # Align oil, gas and water on each case's actual observation dates.
    combined = curves[0]

    for curve in curves[1:]:
        combined = combined.merge(
            curve,
            on=["Date", "Case"],
            how="outer",
            validate="one_to_one",
        )

    combined = combined.merge(
        parameters,
        on="Case",
        how="left",
        validate="many_to_one",
    )

    combined["Case_Number"] = combined["Case"].str.extract(
        r"(\d+)"
    ).astype(int)

    combined["Split"] = combined["Case_Number"].map(
        lambda n: (
            "train" if n <= 70
            else "validation" if n <= 85
            else "test"
        )
    )

    combined = combined.sort_values(
        ["Case_Number", "Date"]
    ).reset_index(drop=True)

    OUTPUT_DIR.mkdir(exist_ok=True)
    combined.to_csv(OUTPUT_FILE, index=False)

    print("\nDataset preparation complete.")
    print("Rows:", f"{len(combined):,}")
    print("Unique cases:", combined["Case"].nunique())
    print("\nSplit counts:")
    print(
        combined.groupby("Split")["Case"]
        .nunique()
        .to_string()
    )

    print("\nMissing values by production target:")
    print(
        combined[
            [
                "oil_cumulative",
                "gas_cumulative",
                "water_cumulative",
            ]
        ].isna().sum().to_string()
    )

    print(f"\nSaved local dataset: {OUTPUT_FILE.resolve()}")
    print("Keep this generated dataset out of GitHub.")


if __name__ == "__main__":
    main()
