"""Worked example: reconciling two lists of transactions (built on D1-S04's joins).

What it does: compares N01's December transactions with a settlement extract from another system, and reports every
item as matched, missing from the settlement, extra in the settlement, or matched with an amount difference.
Adapt it: use other files, change the tolerance, or report the totals by status.
"""
# SUPPLIED: course setup. It lets this file find the course folder, so it works from the Run button or the
# terminal, including after you copy it into outputs/projects/. You do not need to change these lines.
import os, sys
from pathlib import Path
COURSE_FOLDER = next(p for p in Path(__file__).resolve().parents if (p / "case_pack").is_dir())
os.chdir(COURSE_FOLDER)
sys.path.insert(0, str(COURSE_FOLDER))

# ---- SETTINGS ----
OUR_FILE = "case_pack/data/clean/tiny/transactions_2025-12_N01.csv"
THEIR_FILE = "case_pack/starters/tracks/multi_file_reconciliation/settlement_extract_2025-12.csv"
TOLERANCE_EUR = 0.01
OUTPUT_FOLDER = (Path(__file__).resolve().parent if "projects" in Path(__file__).resolve().parts
                 else Path("outputs/projects/multi_file_reconciliation"))   # a copy writes beside itself
KEY = ["period", "entity", "transaction_id"]        # what identifies one transaction in both files

import pandas as pd

# 1. Read both files as text, keep only posted rows on our side, then convert amounts to numbers.
ours = pd.read_csv(OUR_FILE, dtype=str)
ours = ours[ours["status"] == "posted"].copy()
ours["our_amount"] = pd.to_numeric(ours["amount"])
theirs = pd.read_csv(THEIR_FILE, dtype=str)
theirs["their_amount"] = pd.to_numeric(theirs["settlement_amount"])

# 2. Stop if either side repeats a transaction: matching would then be ambiguous.
for label, table in [("our file", ours), ("their file", theirs)]:
    if table.duplicated(KEY).any():
        raise SystemExit(f"STOPPED: {label} lists a transaction twice. Resolve that before reconciling.")

# 3. Outer join keeps every item from BOTH sides; indicator says where each row was found.
both = ours[KEY + ["our_amount"]].merge(theirs[KEY + ["their_amount"]], on=KEY, how="outer", indicator=True)
both["difference"] = (both["their_amount"] - both["our_amount"]).round(2)

# 4. Give each item a plain status.
def status(row):
    if row["_merge"] == "left_only":
        return "missing from settlement"
    if row["_merge"] == "right_only":
        return "extra in settlement"
    return "matched" if abs(row["difference"]) <= TOLERANCE_EUR else "amount difference"

both["status"] = both.apply(status, axis=1)
result = both[KEY + ["status", "our_amount", "their_amount", "difference"]].sort_values(KEY)
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
print("Saving into:", OUTPUT_FOLDER.resolve())
result.to_csv(OUTPUT_FOLDER / "reconciliation.csv", index=False)
print(result.to_string(index=False))

# 5. Independent check: the totals on each side must be fully explained by the statuses.
print(f"\nOur posted total: {ours['our_amount'].sum():,.2f}   Their total: {theirs['their_amount'].sum():,.2f}")
counts = result["status"].value_counts().rename_axis("status").reset_index(name="items")
print()
print(counts.to_string(index=False))
missing = result.loc[result["status"] == "missing from settlement", "our_amount"].sum()
extra = result.loc[result["status"] == "extra in settlement", "their_amount"].sum()
differences = result.loc[result["status"].isin(["matched", "amount difference"]), "difference"].sum()
explained = ours["our_amount"].sum() - missing + extra + differences
print(f"Check: {ours['our_amount'].sum():,.2f} - {missing:,.2f} missing + {extra:,.2f} extra "
      f"+ {differences:,.2f} differences = {explained:,.2f}, their total {theirs['their_amount'].sum():,.2f}")
print(f"Saved {OUTPUT_FOLDER.as_posix()}/reconciliation.csv")
