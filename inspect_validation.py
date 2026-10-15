
import pandas as pd
from pathlib import Path

file_path = Path(r"C:\Users\Nashran\Downloads\07  Validation Cases.xlsx")


def main():
    if not file_path.exists():
        print(f"File not found: {file_path}")
        return

    with pd.ExcelFile(file_path, engine="openpyxl") as workbook:
        print(f"Worksheets: {workbook.sheet_names}")

        for sheet in workbook.sheet_names:
            print(f"\n===== {sheet} =====")

            df = pd.read_excel(
                workbook,
                sheet_name=sheet,
                nrows=5
            )

            print(f"Shape (first 5 rows): {df.shape}")
            print(f"Columns: {df.columns.tolist()}")
            print(df.to_string(index=False, max_cols=8))


if __name__ == "__main__":
    main()
