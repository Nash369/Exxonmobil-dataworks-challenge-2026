
import pandas as pd
from pathlib import Path

file_path = Path(
    r"C:\Users\Nashran\Downloads\02 Field Production(1).xlsx"
)

sheets_to_check = [
    "Field Production",
    "Oil production rate",
    "Gas production rate",
    "Water production rate",
    "Oil production cumulative",
    "Gas production cumulative",
    "Water production cumulative",
]


def main():
    if not file_path.exists():
        print(f"File not found: {file_path}")
        return

    with pd.ExcelFile(file_path, engine="openpyxl") as workbook:
        for sheet in sheets_to_check:
            print(f"\n===== {sheet} =====")

            if sheet == "Field Production":
                df = pd.read_excel(
                    workbook, sheet_name=sheet
                )
                date_col = "Date"
            else:
                df = pd.read_excel(
                    workbook, sheet_name=sheet, header=1
                )

                # Convert dates and remove the units row
                df["Date"] = pd.to_datetime(
                    df["Date"], errors="coerce"
                )
                df = df.dropna(subset=["Date"])
                date_col = "Date"

            print(f"Shape: {df.shape}")
            print(f"First date: {df[date_col].min()}")
            print(f"Last date: {df[date_col].max()}")
            print(f"Missing values: {df.isna().sum().sum()}")
            print("\nFirst 3 rows:")
            print(df.head(3).iloc[:, :5].to_string(index=False))


if __name__ == "__main__":
    main()
