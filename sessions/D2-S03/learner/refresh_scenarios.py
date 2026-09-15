"""D2-S03: run four controlled refresh scenarios using your rule. Instructions: sessions/D2-S03/D2-S03_instructions.md

Change MAX_AGE_DAYS to test a different policy. Nothing here contacts the internet unless you choose the live option.
"""
# SUPPLIED: course setup. It lets this file find the course folder, so it works from the Run button or the
# terminal. You do not need to read or change these lines.
import os, sys
from pathlib import Path
COURSE_FOLDER = next(p for p in Path(__file__).resolve().parents if (p / "case_pack").is_dir())
os.chdir(COURSE_FOLDER)
sys.path.insert(0, str(COURSE_FOLDER))
sys.path.insert(0, str(Path(__file__).resolve().parent))

# ---- YOUR SETTINGS ----
MAX_AGE_DAYS = 35           # the course policy is 35; try 20 in Step 4, then set it back
RUN_LIVE_REFRESH = False    # optional extension only: True makes one real request to the OECD

# SUPPLIED: run the scenarios with your rule from freshness_rule.py and print the results.
from freshness_rule import data_status_for_saved_data
from case_pack.course_tools import refresh_scenarios
from case_pack.course_tools.settings import require_number, require_true_or_false

require_number("MAX_AGE_DAYS", MAX_AGE_DAYS, 1, 90)
require_true_or_false("RUN_LIVE_REFRESH", RUN_LIVE_REFRESH)

rows = refresh_scenarios.run(data_status_for_saved_data, MAX_AGE_DAYS, keep_example_in="outputs/D2-S03/example_cache")
refresh_scenarios.print_table(rows, MAX_AGE_DAYS)
print("\nA saved copy from case B is in outputs/D2-S03/example_cache/. Open its .meta.json file:")
print("retrieved_at_utc is when the data was downloaded; last_attempt_utc is when we last tried.")

if RUN_LIVE_REFRESH:
    import datetime as dt
    from case_pack.course_tools import refresh
    print("\nLIVE REFRESH: one real request to the OECD (saved copy in outputs/D2-S03/live_cache/)")
    result = refresh.refresh(Path("outputs/D2-S03/live_cache"), dt.datetime.now(dt.timezone.utc),
                             max_age_days=MAX_AGE_DAYS, status_rule=data_status_for_saved_data)
    print(f"refresh_outcome={result.refresh_outcome}  data_status={result.data_status}  "
          f"retrieved_at_utc={result.retrieved_at_utc}  rows={result.rows}")
    print(f"detail: {result.detail}")
