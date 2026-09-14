r"""D1-S07: fill the Northbridge management template.

The checked December figures are supplied. Complete populate_and_save below.
The master template is only read; every run saves a new workbook under outputs/D1-S07.
The Summary sheet shows costs as positive numbers; the ByLine sheet keeps the stored signs.
A blocked run writes the control results and exceptions, but no figures.

Run from the course folder (after extracting the D1-S07 ZIP):
    .virtual-env-folder\Scripts\python.exe sessions\D1-S07\learner\writer_scaffold.py
"""
from pathlib import Path
import sys
import pandas as pd

# ---- Settings for this run: change these three lines, not the code below ----
CONTROL_RUN = "clean_2025-12"          # "clean_2025-12" (all pass) or "F03_duplicate_mapping" (a failed control)
RELEASE = "ready"                      # "ready" for clean_2025-12, "blocked" for F03_duplicate_mapping
OUTPUT_FOLDER = Path("outputs/D1-S07/run-01")   # use run-02 for the blocked pack

HANDOUT = Path("outputs/handoffs/D1-S07")
if not (HANDOUT / "report_components.py").exists():
    raise SystemExit("SETUP: cannot find outputs/handoffs/D1-S07/report_components.py. Check that you are running from the course folder and that the D1-S07 ZIP from the instructor was extracted into it.")
sys.path.insert(0, str(HANDOUT.resolve()))
import report_components as report  # supplied, already-tested functions

PERIOD = "2025-12"
TEMPLATE = Path("case_pack/templates/northbridge_reporting_template.xlsx")
INPUT_FOLDERS = {"clean_2025-12": "case_pack/data/clean",
                 "F03_duplicate_mapping": "case_pack/data/faulty/F03_duplicate_mapping"}

# Supplied preparation (not the exercise): the validated December figures.
actuals = pd.read_csv("case_pack/data/clean/checkpoints/actuals_by_line_2025-12.csv", dtype={"period": str})
clean_inputs = report.load_inputs("case_pack/data/clean", PERIOD)
summary = report.build_summary(actuals, clean_inputs["budget"], clean_inputs["entities"], PERIOD)


def read_control_run(name):
    """Return (inputs, controls, exceptions) for 'clean_2025-12' or 'F03_duplicate_mapping'."""
    inputs = report.load_inputs(INPUT_FOLDERS[name], PERIOD)
    folder = HANDOUT / name
    controls = pd.read_csv(folder / "control_summary.csv", keep_default_na=False)
    exceptions = pd.read_csv(folder / "exceptions.csv", keep_default_na=False)
    return inputs, controls, exceptions


def populate_and_save(inputs, controls, exceptions, release, output_folder):
    """Write a NEW dated workbook from the master template and return its path.

    YOUR TURN: call report.write_workbook(...) with the output folder, inputs, release status,
    control summary, exceptions and summary. Read its docstring first (help(report.write_workbook)).
    Never pass the template path as the output. Do not decide 'ready' yourself: use `release`.
    """
    return None


if __name__ == "__main__":
    inputs, controls, exceptions = read_control_run(CONTROL_RUN)
    failed = controls.loc[controls["status"] != "pass", "check_id"].tolist()
    print(f"Control run {CONTROL_RUN}: checks not passing = {failed or 'none'}; release setting = {RELEASE}")
    print("Result:", populate_and_save(inputs, controls, exceptions, RELEASE, OUTPUT_FOLDER))
