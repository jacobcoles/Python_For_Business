"""Worked example: audit exception testing across several deliveries (built on D1-S06).

What it does: runs the nine checks on the clean delivery and on each faulty delivery, then saves one summary row per
delivery and one combined list of every exception, labelled with the delivery it came from.
Adapt it: choose other deliveries, add a check of your own, or summarise the exceptions differently.
"""
# SUPPLIED: course setup. It lets this file find the course folder, so it works from the Run button or the
# terminal, including after you copy it into outputs/projects/. You do not need to change these lines.
import os, sys
from pathlib import Path
COURSE_FOLDER = next(p for p in Path(__file__).resolve().parents if (p / "case_pack").is_dir())
os.chdir(COURSE_FOLDER)
sys.path.insert(0, str(COURSE_FOLDER))

# ---- SETTINGS: the deliveries to test (folder name -> reporting period) ----
DELIVERIES = {
    "case_pack/data/clean": "2025-12",
    "case_pack/data/faulty/F01_missing_source": "2025-12",
    "case_pack/data/faulty/F02_duplicate_record": "2025-12",
    "case_pack/data/faulty/F04_unmapped_account": "2025-12",
    "case_pack/data/faulty/F07_large_genuine_movement": "2025-12",
    "case_pack/data/faulty/F08_wrong_currency": "2025-12",
}
OUTPUT_FOLDER = (Path(__file__).resolve().parent if "projects" in Path(__file__).resolve().parts
                 else Path("outputs/projects/audit_exceptions"))   # a copy writes beside itself

import pandas as pd
from case_pack.course_tools import northbridge

summary_rows, all_exceptions = [], []
for folder, period in DELIVERIES.items():
    name = Path(folder).name
    inputs = northbridge.load_inputs(folder, period)                 # read the delivery
    controls, exceptions, release = northbridge.run_controls(inputs) # run the nine checks
    not_passing = controls.loc[controls["status"] != "pass", ["check_id", "status"]]
    summary_rows.append({
        "delivery": name, "period": period, "release": release,
        "checks_not_passing": ", ".join(f"{c} {s}" for c, s in not_passing.itertuples(index=False)) or "none",
        "exception_rows": len(exceptions),
    })
    all_exceptions.append(exceptions.assign(delivery=name))           # keep where each exception came from

summary = pd.DataFrame(summary_rows)
exceptions = pd.concat(all_exceptions, ignore_index=True)
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
print("Saving into:", OUTPUT_FOLDER.resolve())
summary.to_csv(OUTPUT_FOLDER / "delivery_summary.csv", index=False)
exceptions.to_csv(OUTPUT_FOLDER / "all_exceptions.csv", index=False)
print(summary.to_string(index=False))
print(f"\nSaved delivery_summary.csv and all_exceptions.csv ({len(exceptions)} exception rows) in {OUTPUT_FOLDER.as_posix()}")

# Independent check: the clean delivery must pass everything; every faulty one must not be released as "ready".
clean_ok = summary.loc[summary["delivery"] == "clean", "release"].eq("ready").all()
print("Check: clean delivery released as ready:", "yes" if clean_ok else "NO")
print("Check: release decision for each faulty delivery (only a warning may still be released):",
      ", ".join(f"{r.delivery} {r.release}" for r in summary[summary["delivery"] != "clean"].itertuples()))
