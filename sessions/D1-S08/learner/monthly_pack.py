r"""D1-S08: the January pack.

January's exports have arrived. Complete run_month, run it, and decide whether management can use the figures.
Do not edit the exports. If finance sends a corrected mapping, set MAPPING_FILE and mention it in your handover note.

Run from the course folder (after extracting the D1-S08 ZIP):
    .virtual-env-folder\Scripts\python.exe sessions\D1-S08\learner\monthly_pack.py
"""
from pathlib import Path
import sys

# ---- Settings for this run: change these lines, not the code below ----
ATTEMPT = "attempt-01"      # attempt-02 for the corrected run; a new name for every run
MAPPING_FILE = None         # after diagnosis: Path("case_pack/data/faulty/F10_january_unmapped_account/late_delivery/account_mapping_updated.csv")

HANDOUT = Path("outputs/handoffs/D1-S08")
if not (HANDOUT / "report_components.py").exists():
    raise SystemExit("SETUP: cannot find outputs/handoffs/D1-S08/report_components.py. Check that you are running from the course folder and that the D1-S08 ZIP from the instructor was extracted into it.")
sys.path.insert(0, str(HANDOUT.resolve()))
import report_components as components  # load_inputs, run_controls, expected_exports, build_actuals, build_summary, write_workbook

input_folder = Path("case_pack/data/faulty/F10_january_unmapped_account")
period = "2026-01"
output_folder = Path("outputs/D1-S08")


def run_month(input_folder, period, output_folder, mapping_file=None):
    """Run the whole month in order: load, check, report.

    1. inputs = load_inputs(input_folder, period, mapping_file=mapping_file)
    2. controls, exceptions, release = run_controls(inputs)
    3. always write control_summary.csv and exceptions.csv into output_folder
    4. only if release is not 'blocked': build actuals and summary, and write actuals_by_line.csv
    5. write_workbook(output_folder, inputs, release, controls, exceptions, summary)  (summary=None when blocked)
    6. return (release_status, workbook_path)
    """
    # YOUR TURN: call the steps in order, and only build figures if the release is not blocked.
    # Do not hard-code a release decision.
    return None


if __name__ == "__main__":
    if not (input_folder / f"input_manifest_{period}.json").exists():
        raise SystemExit("Cannot find the January input folder. Run this from the course folder.")
    target = output_folder / ATTEMPT
    if target.exists():
        raise SystemExit(f"{target} already exists: keep it as evidence and set ATTEMPT to a new name.")
    print(f"Inputs ready. Running {ATTEMPT} with mapping_file={MAPPING_FILE}")
    print("Result:", run_month(input_folder, period, target, MAPPING_FILE))
