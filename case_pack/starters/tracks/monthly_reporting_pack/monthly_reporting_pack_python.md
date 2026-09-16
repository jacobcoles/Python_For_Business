# Monthly reporting pack in Python

The job is in `README.md`. This is how to build it.

**Tool:** a Python script in VS Code, then Excel to inspect the workbook.
**You will produce:** `control_summary.csv`, `exceptions.csv`, `actuals_by_line.csv` when released, the management
workbook, and `pack_note.md`.

## Start here

1. Right-click `outputs` > **New Folder**, name it `projects` if it is not there. Right-click `outputs/projects` >
   **New Folder**, name it after your project, for example `january_pack`.
2. Right-click `worked_example.py` > **Copy**, then right-click your folder > **Paste**.
3. Open your copy and click **Run Python File**.

**You should see** the nine checks, then:

```text
Release decision: ready (0 exception rows)
Saved control_summary.csv and exceptions.csv in ...
Calculated 9 report lines for 2026-01
Saved actuals_by_line.csv in ...
Saved workbook ...Northbridge_Management_Pack_2026-01_r01.xlsx
Check against the checkpoint: 9 of 9 figures match within EUR 0.01
```

If a workbook from a previous run is open in Excel, close it first: Windows will not let the script replace an
open file.

## Step 1: start from an empty folder

`fresh_output_folder(OUTPUT_FOLDER)` clears the folder before the run.

**Why this is not housekeeping:** if a run is blocked, no figures file is written. If last month's figures were
still sitting in the folder, a reader would find a figures file beside a blocked control summary and reasonably
assume the figures were this month's. Clearing first makes "no figures" visible as an absence.

## Step 2: read the month the manifest lists

```python
inputs = load_month(INPUT_FOLDER, PERIOD, None)
```

It reads exactly the files named in `input_manifest_<period>.json`, not everything in the folder. A file that was
promised and did not arrive is then a detectable fact rather than a silent gap, which is what check C01 reports.

The two settings at the top choose the month and the delivery:

```python
INPUT_FOLDER = "case_pack/data/clean"
PERIOD = "2026-01"
```

## Step 3: run the checks, and save the results whatever they say

```python
controls, exceptions, release = run_checks(inputs)
save_check_results(controls, exceptions, OUTPUT_FOLDER)
```

**Save before deciding.** The control results are the evidence that the month was checked, and they are needed
most when the answer is bad. A process that only writes evidence for successful months has no evidence at all.

`release` is one of three values: `ready`, `ready_with_warnings` or `blocked`.

## Step 4: figures only if the month is not blocked

```python
summary = None
if release != "blocked":
    summary = build_figures(inputs)
    save_figures(summary, OUTPUT_FOLDER)
```

**Read the condition.** It tests `!= "blocked"`, not `== "ready"`. There are three decisions, and a month with a
warning may still be released. Code that only accepts `"ready"` would withhold figures from a month that is
perfectly releasable, and the unit would be told to fix something that is not broken.

**Ask Copilot** if you want to write this yourself:

> I have a variable `release` that is one of the strings "ready", "ready_with_warnings" or "blocked", and two
> functions `build_figures(inputs)` and `save_figures(summary, folder)`. Write the few lines that build and save
> the figures only when the month may be released, and otherwise leave `summary` as None. A month with warnings
> may be released.

## Step 5: produce the pack

```python
write_pack(inputs, controls, exceptions, release, summary, OUTPUT_FOLDER)
```

With `summary=None` it writes a workbook that shows the checks, the exceptions and the release status, and **no
figures**. The filename is marked so nobody mistakes it for a released pack.

Open the workbook in Excel afterwards. A blocked pack should say the figures are withheld, and the cross-check cell
should say the same rather than showing 0.00, because there is nothing to cross-check.

## Step 6: compare with the checkpoint

**Why:** "ready" means the checks passed. It does not mean the figures are right. The checkpoint is the correct
result for that month, prepared separately by the course team, and comparing against it is a different question
from checking the inputs.

```text
Check against the checkpoint: 9 of 9 figures match within EUR 0.01
```

Then check one unit by hand: revenue plus the two costs, with the costs negative, equals the operating result.

## Run the blocked case too

**Change both settings, not just one.** The faulty deliveries are December 2025, while the clean default is
January 2026, so changing only the folder gives a confusing error about missing files:

```python
INPUT_FOLDER = "case_pack/data/faulty/F04_unmapped_account"
PERIOD = "2025-12"
```

**You should see** C05 fail, C09 `not_run`, and:

```text
Release decision: blocked (1 exception rows)
Saved control_summary.csv and exceptions.csv in ...
Saved workbook ...Northbridge_Management_Pack_2025-12_r01_BLOCKED.xlsx
Released figures: none, because the checks blocked this month. See exceptions.csv.
```

Look in the folder afterwards. There is **no** `actuals_by_line.csv`, and the workbook's name ends `_BLOCKED`.
Both absences are the point: a reader can tell at a glance that no figures were released.

## Check your result

| Run | What you should see |
|---|---|
| `case_pack/data/clean`, `2026-01` | Nine checks pass, `ready`, figures saved, 9 of 9 match the checkpoint |
| `case_pack/data/faulty/F04_unmapped_account`, `2025-12` | C05 fails, `blocked`, control summary and exceptions saved, **no** `actuals_by_line.csv`, workbook marked `_BLOCKED` |

If a blocked run produces a figures file, the order in step 4 is wrong. That is the one failure that matters here.

## Write the note

Right-click your project folder > **New File**, name it `pack_note.md`:

```text
The release decision and the reason, in one sentence:
What was saved, and what deliberately was not:
The figure I checked by hand, and against what:
What a reader must not conclude from a blocked pack:
How to rerun this: the script, the settings, the output folder:
```

The fourth heading is the one people get wrong. A blocked pack does not mean the unit did something wrong; it
means the figures cannot yet be relied on, and the note should say which.

## Done when

The clean month gives nine passes and 9 of 9 against the checkpoint, a faulty month produces evidence and no
figures, both workbooks open in Excel as described, and your note explains both outcomes.

## If something goes wrong

| What you see | What to do |
|---|---|
| `STOPPED: the figures cannot be calculated safely` | Figures were built for a blocked month. Put steps 3 and 4 in the right order |
| `Could not replace ...: it is probably open in Excel` | Close the workbook and run again |
| A figures file exists after a blocked run | The condition tests the wrong thing. It must be `!= "blocked"` |
| Fewer than 9 of 9 match | Do not adjust the figures to fit. Find which line differs and why |
| `FileNotFoundError` on a checkpoint | That month has no checkpoint. Check at least one unit by hand instead |

**Start again:** delete your copy and paste `worked_example.py` again. The delivery folders and the master template
never change.
