"""Supplied helpers for D2-S06 (the same Python step in VS Code, Power BI and KNIME).

Learners call these from compare_routes.py. They do not need to read this file.
"""
from pathlib import Path

import pandas as pd

INPUT = Path("case_pack/data/clean/checkpoints/actuals_by_line_2025-12.csv")
EXPECTED = {"N01": 29862.50, "N02": 23444.83, "N03": 14023.53}


def load_dataset():
    """Read the nine checked reporting lines. Power BI and KNIME hand the same table to Python as `dataset`."""
    dataset = pd.read_csv(INPUT, dtype={"period": str, "entity": str, "report_line": str})
    print(f"dataset: {len(dataset)} rows, columns {list(dataset.columns)}")
    return dataset


def check_complete(dataset):
    """Stop if a reporting line is missing or repeated: a missing line must never be treated as zero."""
    keys = ["period", "entity", "report_line"]
    if dataset[keys + ["actual_amount"]].isna().any().any() or dataset.duplicated(keys).any():
        raise SystemExit("STOPPED: missing values or a repeated reporting line in the input.")
    if not dataset.groupby(["period", "entity"]).size().eq(3).all():
        raise SystemExit("STOPPED: a unit is missing one of revenue, direct_cost or overhead.")
    print("OK: every unit has exactly three reporting lines.")


def check_and_save(result, path="outputs/D2-S06/unit_results.csv"):
    """Check the YOUR TURN table against the expected operating results, then save it as the handover file."""
    if result is None:
        print("NOT DONE YET: `result` is still empty. Paste Copilot's lines under YOUR TURN and run again.")
        return
    if not isinstance(result, pd.DataFrame) or not {"period", "entity", "operating_result"}.issubset(result.columns):
        print("PROBLEM: `result` must be a table with the columns period, entity and operating_result.")
        return
    ok_rows = len(result) == 3
    print("OK: three rows, one per unit." if ok_rows else f"PROBLEM: {len(result)} rows; expected one per unit (3).")
    mine = result.set_index("entity")["operating_result"].round(2)
    matches = all(abs(mine.get(unit, float("nan")) - value) <= 0.01 for unit, value in EXPECTED.items())
    print("OK: operating results N01 29,862.50, N02 23,444.83, N03 14,023.53." if matches else
          "PROBLEM: an operating result differs. It should be the sum of each unit's three signed lines.")
    if ok_rows and matches:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        result[["period", "entity", "operating_result"]].to_csv(path, index=False, float_format="%.2f")
        print(f"Saved {path.as_posix()} (the clean file you could hand to a colleague)")
