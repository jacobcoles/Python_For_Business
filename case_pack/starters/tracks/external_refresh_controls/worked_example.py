"""Worked example: an external data refresh with honest status (built on D2-S02 and D2-S03).

What it does: requests the OECD consumer-price series (or uses the saved response), checks and saves it with a
source record, and reports how fresh the data is under the course's 35-day policy.
Adapt it: change the months, the age limit, or document a different approved source with the same checks.
"""
# SUPPLIED: course setup. It lets this file find the course folder, so it works from the Run button or the
# terminal, including after you copy it into outputs/projects/. You do not need to change these lines.
import os, sys
from pathlib import Path
COURSE_FOLDER = next(p for p in Path(__file__).resolve().parents if (p / "case_pack").is_dir())
os.chdir(COURSE_FOLDER)
sys.path.insert(0, str(COURSE_FOLDER))

# ---- SETTINGS ----
MODE = "offline"               # "offline" uses the saved response; "live" sends a real request
AREAS = ["SWE", "EA"]
START, END = "2025-01", "2026-01"
MAX_AGE_DAYS = 35
OUTPUT_FOLDER = (Path(__file__).resolve().parent if "projects" in Path(__file__).resolve().parts
                 else Path("outputs/projects/external_refresh_controls"))   # a copy writes beside itself

import datetime as dt
from case_pack.course_tools import oecd, refresh

print("Saving into:", OUTPUT_FOLDER.resolve())

# 1. Request (or reuse), look, tabulate and check, exactly as in D2-S02.
request = oecd.build_request(AREAS, START, END)
response = oecd.get_response(request, MODE)
table = oecd.to_table(response, request)

# 2. Save the table with its source record. Nothing is saved if a check failed.
oecd.save_extract(table, response, OUTPUT_FOLDER)

# 3. How fresh is what we would hand over today? Age is measured from the original download, never from today's run.
if response is not None:
    downloaded = refresh.parse_utc(response["retrieved_at_utc"])
    age_days = (dt.datetime.now(dt.timezone.utc) - downloaded).total_seconds() / 86400
    status = "live" if MODE == "live" else refresh.policy_rule(age_days, MAX_AGE_DAYS)
    print(f"\ndata_status: {status} (downloaded {response['retrieved_at_utc']}, {age_days:.1f} days ago, limit {MAX_AGE_DAYS})")
    print("The age is measured against today's date, so this saved copy becomes stale once it is more than "
          f"{MAX_AGE_DAYS} days old. Refresh it live, or say plainly that it is out of date.")
else:
    print("\ndata_status: unavailable (no usable response). Record the failure; do not relabel old data as new.")
