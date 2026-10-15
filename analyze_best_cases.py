
from pathlib import Path

import pandas as pd

INTRO_FILE = Path.home() / "Downloads" / "01 Introduction.xlsx"

SCORES_FILE = Path("history_match_scores.csv")

PARAMETERS = [
    "Fault Transmissibility",
    "Porosity Multiplier",
    "Permeability Multiplier",
    "Aquifer Pore Volume",
]


def main():
    if not INTRO_FILE.exists():
        raise FileNotFoundError(
            f"Introduction workbook not found: {INTRO_FILE}"
        )

    if not SCORES_FILE.exists():
        raise FileNotFoundError(
            "history_match_scores.csv not found. "
            "Run compare_history_match.py first."
        )

    uncertainty = pd.read_excel(
        INTRO_FILE,
        sheet_name="Uncertainty Values",
    )

    scores = pd.read_csv(SCORES_FILE)

    # Match Case_6 to the corresponding Case 6 uncertainty row.
    uncertainty["Case"] = uncertainty["Item"].astype(str).str.extract(
        r"(\d+)"
    )[0]
    uncertainty["Case"] = "Case_" + uncertainty["Case"]

    merged = scores.merge(
        uncertainty[["Case"] + PARAMETERS],
        on="Case",
        how="left",
    )

    merged = merged.sort_values("Mean_NRMSE")

    print("=" * 75)
    print("TOP 15 HISTORY-MATCHING CASES AND UNCERTAINTY PARAMETERS")
    print("=" * 75)

    columns = ["Case", "Mean_NRMSE"] + PARAMETERS
    print(merged[columns].head(15).round(6).to_string(index=False))

    print("\n" + "=" * 75)
    print("CASE_6 PARAMETER RANKS")
    print("=" * 75)

    case6 = merged.loc[merged["Case"] == "Case_6"]

    if case6.empty:
        print("Case_6 was not found in the merged results.")
    else:
        for parameter in PARAMETERS:
            value = case6.iloc[0][parameter]
            ascending_rank = uncertainty[parameter].rank(
                ascending=True,
                method="min",
            )
            case_rank = uncertainty.loc[
                uncertainty["Case"] == "Case_6"
            ].index

            if len(case_rank):
                original_index = case_rank[0]
                rank = int(ascending_rank.loc[original_index])
                print(
                    f"{parameter}: {value:.6f} "
                    f"(rank {rank} of {len(uncertainty)}, "
                    "lowest to highest)"
                )

    output = Path("best_case_parameters.csv")
    merged[columns].to_csv(output, index=False)
    print(f"\nSaved analysis to: {output.resolve()}")


if __name__ == "__main__":
    main()
