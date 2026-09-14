r"""D1-S03 example 1 of 2: code that stops with an error.

This is the kind of code an AI assistant can plausibly return. Read the error, find the line it
points to, inspect the data, and ask for the smallest fix.

Run from the course folder:
    .virtual-env-folder\Scripts\python.exe sessions\D1-S03\learner\flawed_example_runtime.py
"""
from pathlib import Path

import pandas as pd

data_file = Path("case_pack/data/clean/tiny/transactions_2025-12_N01.csv")
transactions = pd.read_csv(data_file, dtype={"account_code": "string"})

posted = transactions[transactions["Status"] == "posted"]
operating_result = posted["amount"].sum()

print(f"Operating result for N01, 2025-12: EUR {operating_result:,.2f}")
