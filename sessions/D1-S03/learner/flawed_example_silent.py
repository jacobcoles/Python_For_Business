r"""D1-S03 example 2 of 2: code that runs without an error and is still wrong.

Nothing crashes and a number is printed, which is what makes this kind of mistake risky.
Before trusting the number, decide whether it is right and show how you know.

Run from the course folder:
    .virtual-env-folder\Scripts\python.exe sessions\D1-S03\learner\flawed_example_silent.py
"""
from pathlib import Path

import pandas as pd

data_file = Path("case_pack/data/clean/tiny/transactions_2025-12_N01.csv")
transactions = pd.read_csv(data_file, dtype={"account_code": "string"})

used = transactions                      # the rows that are added up
operating_result = used["amount"].sum()

print(f"Rows used: {len(used)}")
print(f"Operating result for N01, 2025-12: EUR {operating_result:,.2f}")
