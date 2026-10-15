
import pandas as pd
from pathlib import Path

file_path = Path.home() / "Downloads" / "03 Train Cases 1 (5).xlsx"
sentinel = -999.25


def main():
    with pd.ExcelFile(file_path, engine="openpyxl") as workbook:
        df = pd.read_excel(workbook, sheet_name="Case 1")

    print("Sentinel count by column:")
    counts = (df == sentinel).sum()
    print(counts[counts > 0].to_string())

    print("\nPercentage of sentinel values by column:")
    percentages = (df == sentinel).mean() * 100
    print(percentages[percentages > 0].round(2).to_string())

    print("\nRows with sentinel in Pore Volume:")
    pore_col = "Pore Volume (PORV)"
    print(df.loc[df[pore_col] == sentinel].head(5).to_string(index=False))

    print("\nRows with zero Pore Volume:")
    print(df.loc[df[pore_col] == 0].head(5).to_string(index=False))

    print("\nRows with positive Pore Volume:")
    print(df.loc[df[pore_col] > 0].head(5).to_string(index=False))


if __name__ == "__main__":
    main()
