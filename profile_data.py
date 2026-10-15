
import pandas as pd
from pathlib import Path

file_path = Path.home() / "Downloads" / "03 Train Cases 1 (5).xlsx"


def main():
    print("Opening training workbook...")

    with pd.ExcelFile(file_path, engine="openpyxl") as workbook:
        summary = []

        for sheet in workbook.sheet_names:
            print(f"\nProfiling {sheet}...")

            # Read the worksheet
            df = pd.read_excel(workbook, sheet_name=sheet)

            # Count special values
            sentinel_count = (df == -999.25).sum().sum()

            # Count missing values
            missing_count = df.isna().sum().sum()

            # Count columns containing only one value
            constant_columns = [
                col for col in df.columns
                if df[col].nunique(dropna=False) <= 1
            ]

            summary.append({
                "Case": sheet,
                "Rows": len(df),
                "Columns": len(df.columns),
                "-999.25 Values": int(sentinel_count),
                "Missing Values": int(missing_count),
                "Constant Columns": len(constant_columns),
            })

        result = pd.DataFrame(summary)

        print("\n\n========== DATA PROFILE SUMMARY ==========")
        print(result.to_string(index=False))

        print("\n========== COLUMN NAMES ==========")
        print(workbook.sheet_names[0])
        print(pd.read_excel(workbook, sheet_name=workbook.sheet_names[0], nrows=0).columns.tolist())

        result.to_csv("data_profile_summary.csv", index=False)
        print("\nSaved summary to data_profile_summary.csv")


if __name__ == "__main__":
    main()
