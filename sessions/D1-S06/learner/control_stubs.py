r"""D1-S06: two Northbridge controls for you to complete.

Complete duplicate_rows (used by check C03) and reconciliation_status (used by check C08).
The other checks come in the D1-S06 ZIP from the instructor. Tolerances are teaching examples, not policy.

Self-test, from the course folder:
    .virtual-env-folder\Scripts\python.exe sessions\D1-S06\learner\control_stubs.py
"""
from pathlib import Path
import pandas as pd

KEY = ["entity", "period", "transaction_id"]

def duplicate_rows(rows):
    """Return every row whose entity, period and transaction_id appear more than once, keeping source_file and source_row."""
    # YOUR TURN: return a DataFrame of all the duplicated rows; never delete duplicates.
    return None

def reconciliation_status(observed, expected):
    """Return "pass" if observed and expected differ by at most EUR 0.01, otherwise "fail"."""
    # YOUR TURN: both inputs are amounts with two decimals; missing values are handled elsewhere.
    return None

def self_test():
    """Quick checks for your two functions (slides 5-6). Predict each answer before running."""
    rows = pd.DataFrame({
        "entity": ["N01", "N02", "N01", "N01"],
        "period": ["2025-12"] * 4,
        "transaction_id": ["T000001", "T000001", "T000042", "T000042"],
        "amount": ["100.00", "50.00", "-660.87", "-660.87"],
        "source_file": ["transactions_2025-12_N01.csv", "transactions_2025-12_N02.csv",
                        "transactions_2025-12_N01.csv", "transactions_2025-12_N01.csv"],
        "source_row": [1, 1, 42, 89],
    })
    found = duplicate_rows(rows)
    if found is None:
        print("duplicate_rows: not implemented yet (run_controls.py will report C03 as not_run)")
    else:
        got = sorted(found["source_row"].tolist())
        flag = "ok" if got == [42, 89] else "CHECK"
        print(f"duplicate_rows returned source rows {got} expected [42, 89]: {flag}"
              "  (T000001 in N01 and N02 is NOT a duplicate)")
    expected = 14023.53
    for observed, answer in [(14023.54, "pass"), (14023.55, "fail"), (14023.52, "pass"), (14023.51, "fail")]:
        got = reconciliation_status(observed, expected)
        flag = "ok" if got == answer else "CHECK"
        print(f"reconciliation_status({observed}, {expected}) -> {got!r:8} expected {answer!r}: {flag}")


if __name__ == "__main__":
    print("Self-test of your two functions:")
    self_test()
    print(r"Then run: .virtual-env-folder\Scripts\python.exe sessions\D1-S06\learner\run_controls.py  (after extracting the D1-S06 ZIP)")
