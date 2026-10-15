
import pandas as pd
from pathlib import Path

file_path = Path(
    r"C:\Users\Nashran\Downloads\02 Field Production(1).xlsx"
)

cases = ["Case_1", "Case_12", "Case_100"]

sheets = [
    "Oil production rate",
    "Oil production cumulative",
]


def main():
    if not file_path.exists():
        print(f"File not found: {file_path}")
        return

    with pd.ExcelFile(file_path, engine="openpyxl") as workbook:
        for sheet in sheets:
            df = pd.read_excel(
                workbook,
                sheet_name=sheet,
                header=1,
            )

            # Convert dates and remove the units row
            df["Date"] = pd.to_datetime(
                df["Date"],
                errors="coerce",
            )
            df = df.dropna(subset=["Date"])

            print(f"\n===== {sheet} =====")

            for case in cases:
                values = pd.to_numeric(
                    df[case],
                    errors="coerce",
                )

                valid = values.notna()

                print(f"\n--- {case} ---")
                print("Valid values:", int(valid.sum()))
                print("Missing values:", int(values.isna().sum()))

                if not valid.any():
                    print("No valid observations found.")
                    continue

                valid_data = df.loc[valid, ["Date"]].copy()
                valid_data[case] = values[valid]

                print(
                    "First valid date:",
                    valid_data["Date"].min(),
                )
                print(
                    "Last valid date:",
                    valid_data["Date"].max(),
                )

                print("\nFirst 15 valid observations:")
                print(
                    valid_data.head(15).to_string(index=False)
                )

                print("\nLast 10 valid observations:")
                print(
                    valid_data.tail(10).to_string(index=False)
                )


if __name__ == "__main__":
    main()

