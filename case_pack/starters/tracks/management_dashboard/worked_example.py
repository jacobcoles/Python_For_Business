"""Worked example: preparing clean data for an Excel or Power BI dashboard (built on D2-S04 and D2-S06).

What it does: builds one tidy table per unit (actual, budget and variance for December 2025) from the checked files,
checks it against the nine source lines, saves it as a CSV for Excel or Power BI, and saves a preview chart.
Adapt it: add a month, a unit filter, or another measure; then build the report in Excel or Power BI from the CSV.
"""
# SUPPLIED: course setup. It lets this file find the course folder, so it works from the Run button or the
# terminal, including after you copy it into outputs/projects/. You do not need to change these lines.
import os, sys
from pathlib import Path
COURSE_FOLDER = next(p for p in Path(__file__).resolve().parents if (p / "case_pack").is_dir())
os.chdir(COURSE_FOLDER)
sys.path.insert(0, str(COURSE_FOLDER))

# ---- SETTINGS ----
PERIOD = "2025-12"
OUTPUT_FOLDER = (Path(__file__).resolve().parent if "projects" in Path(__file__).resolve().parts
                 else Path("outputs/projects/management_dashboard"))   # a copy writes beside itself

import pandas as pd
import matplotlib
matplotlib.use("Agg")                     # save the chart to a file instead of opening a window
import matplotlib.pyplot as plt

# 1. Read the checked unit comparison and the nine checked reporting lines it must agree with.
units = pd.read_csv(f"case_pack/data/clean/analysis/unit_comparison_{PERIOD}.csv", dtype={"period": str})
lines = pd.read_csv(f"case_pack/data/clean/checkpoints/actuals_by_line_{PERIOD}.csv", dtype={"period": str})

# 2. Independent check: each unit's operating result must equal the sum of its three signed lines.
from_lines = lines.groupby("entity")["actual_amount"].sum().round(2)
agree = (units.set_index("entity")["operating_result"].round(2) - from_lines).abs().le(0.01).all()
print("Check: unit results equal the sum of their reporting lines:", "yes" if agree else "NO")
if not agree:
    raise SystemExit("STOPPED: the two checked files disagree. Do not publish a dashboard from them.")

# 3. The dashboard table: one row per unit, with plain column names a report user understands.
dashboard = units[["period", "entity", "entity_name", "operating_result", "budget_operating_result",
                   "favourable_variance"]].rename(columns={
    "entity": "unit", "entity_name": "unit_name", "operating_result": "actual_eur",
    "budget_operating_result": "budget_eur", "favourable_variance": "variance_eur"})
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
print("Saving into:", OUTPUT_FOLDER.resolve())
dashboard.to_csv(OUTPUT_FOLDER / "dashboard_units.csv", index=False, float_format="%.2f")
print(dashboard.to_string(index=False))

# 4. A preview chart, so you can check the figures before building the report.
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.bar(dashboard["unit"], dashboard["variance_eur"], color=["#2874a6" if v >= 0 else "#b14b39" for v in dashboard["variance_eur"]])
for x, value in zip(dashboard["unit"], dashboard["variance_eur"]):
    ax.annotate(f"{value:+,.2f}", (x, value), ha="center", va="bottom" if value >= 0 else "top")
ax.axhline(0, color="#555555", linewidth=1)
ax.set_title(f"Operating result against budget by unit, {PERIOD} (EUR, positive = favourable)")
fig.tight_layout()
fig.savefig(OUTPUT_FOLDER / "preview_variance_by_unit.png", dpi=150)
print(f"\nSaved dashboard_units.csv and preview_variance_by_unit.png in {OUTPUT_FOLDER.as_posix()}")
print("Next: in Excel (Data > From Text/CSV) or Power BI (Get data > Text/CSV), load dashboard_units.csv.")
