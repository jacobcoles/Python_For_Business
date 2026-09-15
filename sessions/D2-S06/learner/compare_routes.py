"""D2-S06: write one Python step and use it in VS Code, Power BI and KNIME. Instructions: sessions/D2-S06/D2-S06_instructions.md
"""
# SUPPLIED: course setup. It lets this file find the course folder, so it works from the Run button or the
# terminal. You do not need to read or change these lines.
import os, sys
from pathlib import Path
COURSE_FOLDER = next(p for p in Path(__file__).resolve().parents if (p / "case_pack").is_dir())
os.chdir(COURSE_FOLDER)
sys.path.insert(0, str(COURSE_FOLDER))

from case_pack.course_tools import integration

# SUPPLIED: in VS Code we read the file ourselves. In Power BI and KNIME, the application gives Python this same
# table, already named `dataset`, so these two lines are NOT copied there.
dataset = integration.load_dataset()
integration.check_complete(dataset)

# ---- COPY FROM HERE into Power BI and KNIME ----------------------------------------------------
# YOUR TURN: paste Copilot's lines below. They must create a table called `result` from `dataset`:
# one row per period and entity, with the sum of actual_amount in a column called operating_result.
# Use only `dataset` and pandas (`pd`), so that the same lines work inside the other two tools.
import pandas as pd

result = None
# ---- COPY TO HERE ------------------------------------------------------------------------------

# SUPPLIED: check your result and save it as the clean handover file.
integration.check_and_save(result)
