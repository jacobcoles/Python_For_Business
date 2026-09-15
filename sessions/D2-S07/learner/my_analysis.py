"""D2-S07 transfer task: a new February sample. Instructions: sessions/D2-S07/D2-S07_instructions.md

This is your working file. Edit it, run it, and keep it: it is one of the two things you hand in.

The manager asks: for N01 in February 2026, what are revenue, direct cost and overhead, and the operating result?
The reading is supplied. The analysis under YOUR TURN is yours, with Copilot's help.
"""
# SUPPLIED: course setup. It lets this file find the course folder, so it works from the Run button or the
# terminal, wherever you saved your copy. You do not need to read or change these lines.
import os, sys
from pathlib import Path
COURSE_FOLDER = next(p for p in Path(__file__).resolve().parents if (p / "case_pack").is_dir())
os.chdir(COURSE_FOLDER)
sys.path.insert(0, str(COURSE_FOLDER))

import pandas as pd

# SUPPLIED: read both February files into one table, and the account mapping.
# Every column is read as TEXT, including amount: convert amount to a number before adding.
FOLDER = Path("case_pack/starters/transfer_fixture")
inventory = pd.read_csv(FOLDER / "expected_files.csv", dtype=str)
parts = []
for filename in inventory["filename"]:
    part = pd.read_csv(FOLDER / filename, dtype=str, keep_default_na=False)
    part["source_file"] = filename
    part["source_row"] = range(1, len(part) + 1)
    parts.append(part)
transactions = pd.concat(parts, ignore_index=True)
mapping = pd.read_csv("case_pack/data/clean/account_mapping.csv", dtype=str)
print(transactions.to_string(index=False))
print(f"\n{len(transactions)} transactions read. Columns: {list(transactions.columns)}")

notes = Path("outputs/D2-S07"); notes.mkdir(parents=True, exist_ok=True)
print(f"Write your answer in {notes.as_posix()}/my_answer.md (right-click the folder in the Explorer, New File).")

# YOUR TURN: paste Copilot's analysis below this line.
