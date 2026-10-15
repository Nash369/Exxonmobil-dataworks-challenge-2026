

import pandas as pd
from pathlib import Path

file_path = Path.home() / "Downloads" / "02 Field Production(1).xlsx"
output_path = Path(__file__).parent / "production_summary.txt"


def main():
    lines = []

    with pd.ExcelFile(file_path, engine="openpyxl") as workbook:
        lines.append(f"Worksheets: {workbook.sheet_names}\n")

        for sheet in workbook.sheet_names:
            lines.append(f"\n========== {sheet} ==========\n")

            df = pd.read_excel(workbook, sheet_name=sheet, nrows=5)

            lines.append(f"Columns: {df.columns.tolist()}\n")
            lines.append("\nFirst 5 rows:\n")
            lines.append(df.to_string(index=False))
            lines.append("\n")

    output_path.write_text("\n".join(lines), encoding="utf-8")

    print("Inspection complete!")
    print(f"Summary saved to: {output_path}")


if __name__ == "__main__":
    main()
