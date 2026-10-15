
import pandas as pd
from pathlib import Path

file_path = Path(
    r"C:\Users\Nashran\Downloads\02 Field Production(1).xlsx"
)

sheets = [
    "Oil production rate",
    "Gas production rate",
    "Water production rate",
    "Oil production cumulative",
    "Gas production cumulative",
    "Water production cumulative",
]


def main():
    with pd.ExcelFile(file_path, engine="openpyxl") as workbook:
        for sheet in sheets:
            df = pd.read_excel(
                workbook, sheet_name=sheet, header=1
            )

            df["Date"] = pd.to_datetime(
                df["Date"], errors="coerce"
            )
            df = df.dropna(subset=["Date"])

            case_columns = [
                col for col in df.columns
                if str(col).startswith("Case_")
            ]

            print(f"\n===== {sheet} =====")
            print("Total rows:", len(df))
            print("Case columns:", len(case_columns))
            print(
                "Missing values in case columns:",
                int(df[case_columns].isna().sum().sum())
            )
            print(
                "Cases with the most missing values:"
            )
            print(
                df[case_columns]
                .isna()
                .sum()
                .sort_values(ascending=False)
                .head(10)
                .to_string()
            )


if __name__ == "__main__":
    main()
