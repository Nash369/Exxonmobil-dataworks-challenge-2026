
from pathlib import Path

import numpy as np
import pandas as pd

PRODUCTION_FILE = (
    Path.home() / "Downloads" / "02 Field Production(1).xlsx"
)

CURVE_SHEETS = {
    "Oil production cumulative": "oil",
    "Gas production cumulative": "gas",
    "Water production cumulative": "water",
}


def load_curve(sheet_name):
    df = pd.read_excel(
        PRODUCTION_FILE,
        sheet_name=sheet_name,
        header=1,
    )

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])
    return df


def calculate_case_error(history, simulation):
    # Keep only valid observations and sort chronologically.
    history = history.dropna().sort_index()
    simulation = simulation.dropna().sort_index()

    if len(history) < 2 or len(simulation) < 2:
        return None

    # Compare only dates covered by the simulation.
    start = max(history.index.min(), simulation.index.min())
    end = min(history.index.max(), simulation.index.max())

    target = history.loc[
        (history.index >= start) & (history.index <= end)
    ]

    if len(target) < 2:
        return None

    # Interpolate simulated cumulative production at historical dates.
    sim_x = simulation.index.astype("int64").to_numpy()
    target_x = target.index.astype("int64").to_numpy()

    # Remove duplicate simulation timestamps if any exist.
    simulation = simulation[
        ~simulation.index.duplicated(keep="last")
    ]
    sim_x = simulation.index.astype("int64").to_numpy()

    predicted = np.interp(
        target_x,
        sim_x,
        simulation.to_numpy(dtype=float),
    )

    actual = target.to_numpy(dtype=float)
    errors = predicted - actual

    rmse = float(np.sqrt(np.mean(errors**2)))
    mae = float(np.mean(np.abs(errors)))

    # Normalise RMSE by the historical range for comparison
    # between production types with different units and scales.
    history_range = float(np.max(actual) - np.min(actual))
    nrmse = rmse / history_range if history_range > 0 else np.nan

    return {
        "RMSE": rmse,
        "MAE": mae,
        "NRMSE": nrmse,
        "Points": len(target),
    }


def main():
    if not PRODUCTION_FILE.exists():
        raise FileNotFoundError(
            f"Workbook not found: {PRODUCTION_FILE}"
        )

    scores = {}

    for sheet_name, production_type in CURVE_SHEETS.items():
        print(f"\nProcessing {production_type} production...")
        df = load_curve(sheet_name)

        if "RAMP_History" not in df.columns:
            raise ValueError(
                f"RAMP_History missing from {sheet_name}"
            )

        history = df.set_index("Date")["RAMP_History"]
        history = history.dropna()

        for column in df.columns:
            if not column.startswith("Case_"):
                continue

            simulation = df.set_index("Date")[column].dropna()
            result = calculate_case_error(history, simulation)

            if result is None:
                continue

            case_name = column

            if case_name not in scores:
                scores[case_name] = {}

            scores[case_name][f"{production_type}_NRMSE"] = (
                result["NRMSE"]
            )
            scores[case_name][f"{production_type}_RMSE"] = (
                result["RMSE"]
            )
            scores[case_name][f"{production_type}_MAE"] = (
                result["MAE"]
            )

    results = pd.DataFrame.from_dict(scores, orient="index")
    results.index.name = "Case"

    error_columns = [
        "oil_NRMSE",
        "gas_NRMSE",
        "water_NRMSE",
    ]

    available_columns = [
        col for col in error_columns if col in results.columns
    ]

    results["Mean_NRMSE"] = results[available_columns].mean(axis=1)
    results = results.sort_values("Mean_NRMSE")

    print("\n" + "=" * 75)
    print("BEST HISTORY-MATCHING SIMULATION CASES")
    print("=" * 75)

    print(results.head(15).round(5).to_string())

    output_file = Path("history_match_scores.csv")
    results.to_csv(output_file)

    print(f"\nFull results saved to: {output_file.resolve()}")
    print("Lower NRMSE means a closer match to historical production.")


if __name__ == "__main__":
    main()
