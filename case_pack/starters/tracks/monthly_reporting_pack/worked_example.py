"""Worked example: a monthly reporting pack from recurring exports (built on D1-S06 to D1-S08).

What it does: reads one month's exports, runs the nine checks, saves the check results, and only if the month may
be released calculates the figures, compares them with the checkpoint, and fills the management template.
Adapt it: change PERIOD or INPUT_FOLDER, add a check, or change what goes into the template.
"""
# SUPPLIED: course setup. It lets this file find the course folder, so it works from the Run button or the
# terminal, including after you copy it into outputs/projects/. You do not need to change these lines.
import os, sys
from pathlib import Path
COURSE_FOLDER = next(p for p in Path(__file__).resolve().parents if (p / "case_pack").is_dir())
os.chdir(COURSE_FOLDER)
sys.path.insert(0, str(COURSE_FOLDER))

# ---- SETTINGS: change these to adapt the example ----
INPUT_FOLDER = "case_pack/data/clean"      # a folder with an input_manifest_<period>.json
PERIOD = "2026-01"                         # the month to report, as "YYYY-MM"
OUTPUT_FOLDER = (Path(__file__).resolve().parent if "projects" in Path(__file__).resolve().parts
                 else Path("outputs/projects/monthly_reporting_pack"))   # a copy writes beside itself / PERIOD

import pandas as pd
from case_pack.course_tools.reporting import (load_month, run_checks, save_check_results, build_figures,
                                              save_figures, write_pack, fresh_output_folder)

print("Saving into:", OUTPUT_FOLDER.resolve())

# 1. Start with an empty output folder, so no earlier figures sit beside this run.
fresh_output_folder(OUTPUT_FOLDER)

# 2. Read the month and run the checks. The checks decide whether figures may be released.
inputs = load_month(INPUT_FOLDER, PERIOD, None)
controls, exceptions, release = run_checks(inputs)
save_check_results(controls, exceptions, OUTPUT_FOLDER)

# 3. Figures only when the checks allow it; otherwise the pack shows the checks and no figures.
summary = None
if release != "blocked":
    summary = build_figures(inputs)
    save_figures(summary, OUTPUT_FOLDER)
write_pack(inputs, controls, exceptions, release, summary, OUTPUT_FOLDER)

# 4. Independent check: compare the nine figures with the checkpoint prepared separately for this month.
checkpoint_file = Path(f"case_pack/data/clean/checkpoints/actuals_by_line_{PERIOD}.csv")
if summary is not None and checkpoint_file.exists():
    mine = pd.read_csv(OUTPUT_FOLDER / "actuals_by_line.csv", dtype={"period": str})
    checkpoint = pd.read_csv(checkpoint_file, dtype={"period": str})
    both = checkpoint.merge(mine, on=["period", "entity", "report_line"], suffixes=("_checkpoint", "_mine"))
    matches = (both["actual_amount_mine"] - both["actual_amount_checkpoint"]).abs().le(0.01).sum()
    print(f"Check against the checkpoint: {matches} of {len(checkpoint)} figures match within EUR 0.01")
elif summary is None:
    print("Released figures: none, because the checks blocked this month. See exceptions.csv.")
else:
    print("No checkpoint exists for this month: check at least one unit by hand.")
