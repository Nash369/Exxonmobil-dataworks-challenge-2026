
import pandas as pd
from pathlib import Path

# Update this path if your Excel file is stored elsewhere
file_path = Path.home() / "Downloads" / "03 Train Cases 1 (5).xlsx"


def main():
    if not file_path.exists():
        print(f"File not found: {file_path}")
        print("Check the filename and location.")
        return

    print("Opening training workbook...")

    with pd.ExcelFile(file_path, engine="openpyxl") as workbook:
        sheets = workbook.sheet_names

        print(f"\nNumber of worksheets: {len(sheets)}")
        print("Worksheet names:", sheets)

        reference_columns = None

        for sheet in sheets:
            df = pd.read_excel(
                workbook,
                sheet_name=sheet,
                nrows=5
            )

            print(f"\n--- {sheet} ---")
            print(f"Number of columns: {len(df.columns)}")
            print("Columns:", df.columns.tolist())
            print("Sample rows:")
            print(df.head(3).to_string(index=False))

            if reference_columns is None:
                reference_columns = df.columns.tolist()
            elif df.columns.tolist() != reference_columns:
                print("WARNING: Column names differ from the first sheet!")

    print("\nInspection complete.")


if __name__ == "__main__":
    main()
