"""Worked example: a budget scenario comparison (built on D2-S05).

What it does: checks the seasonal-naive baseline, applies the original scenarios and two chosen cases, shows N02's
February figures for a hand check, and saves the assumptions and a chart.
Adapt it: change the two cases, look at another unit or month, or add a scenario of your own with a business reason.
"""
# SUPPLIED: course setup. It lets this file find the course folder, so it works from the Run button or the
# terminal, including after you copy it into outputs/projects/. You do not need to change these lines.
import os, sys
from pathlib import Path
COURSE_FOLDER = next(p for p in Path(__file__).resolve().parents if (p / "case_pack").is_dir())
os.chdir(COURSE_FOLDER)
sys.path.insert(0, str(COURSE_FOLDER))

# ---- SETTINGS: two cases to compare with the original growth plan (multipliers; overhead stays 1.00) ----
FINANCE_REVENUE, FINANCE_DIRECT_COST = 1.05, 1.12
MY_REVENUE, MY_DIRECT_COST = 1.07, 1.10
OUTPUT_FOLDER = (Path(__file__).resolve().parent if "projects" in Path(__file__).resolve().parts
                 else Path("outputs/projects/budget_forecast_scenario"))   # a copy writes beside itself

from case_pack.course_tools import planning

history, baseline, assumptions = planning.load_inputs()
planning.check_baseline(history, baseline)
print(planning.holdout_errors(history).to_string(index=False))
original = planning.original_scenarios(baseline, assumptions)
chosen = planning.chosen_scenarios(baseline, FINANCE_REVENUE, FINANCE_DIRECT_COST, MY_REVENUE, MY_DIRECT_COST, OUTPUT_FOLDER)
planning.compare_n02_february(baseline, original, chosen)
planning.scenario_chart(history, original, chosen, OUTPUT_FOLDER)
print("\nIndependent check: multiply one baseline line by its multiplier on a calculator and compare with the table.")
