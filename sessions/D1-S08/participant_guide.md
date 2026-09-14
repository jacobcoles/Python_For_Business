# D1-S08: Guided end-to-end exercise, the January pack
75 minutes. Northbridge is fictional; amounts are EUR.

**Question:** January's exports have arrived. Can management use the figures? Run the whole process,
decide, and hand over a note that a colleague could act on.
**Start:** `sessions/D1-S08/learner/monthly_pack.py`.
**Inputs:** `case_pack/data/faulty/F10_january_unmapped_account/`, period `2026-01`.
**Output:** `outputs/D1-S08/attempt-01/`, `outputs/D1-S08/attempt-02/` and `outputs/D1-S08/handover.md`.

Run commands from the course folder in the VS Code terminal (macOS: `.virtual-env-folder/bin/python` and forward slashes).

## 1. Brief and setup (slide 1, 5 min)
Extract the D1-S08 ZIP from the instructor (**`component_handout.zip`**, which contains the supplied steps you will combine).
In Windows, right-click the ZIP → **Extract All** and set the destination to your **course folder** (the one
containing `case_pack` and `sessions`). Windows suggests a new folder named after the ZIP: remove that part.

Then run
`.virtual-env-folder\Scripts\python.exe sessions\D1-S08\learner\monthly_pack.py`. It should print `Inputs ready` and `Result: None`.
The run is controlled by two settings at the top of the file: `ATTEMPT` (the output folder name) and `MAPPING_FILE`.
The script refuses to reuse an existing attempt folder, so earlier evidence is never overwritten.
You do not need to have finished any earlier exercise.

## 2. Plan and specify (slides 2–3, 10 min)
The supplied code from the ZIP (imported as `components`) gives you `load_inputs`, `run_controls`, `expected_exports`, `build_actuals`,
`build_summary` and `write_workbook`. Write a short specification with the D1-S03 template covering:
- the inputs: folder, period and an optional `mapping_file`;
- the steps in order: load → run controls → **always** write `control_summary.csv` and `exceptions.csv` → if the
  release is not `"blocked"`, build actuals and summary **and write `actuals_by_line.csv`** → write the workbook
  (with `summary=None` when blocked);
- what the function returns: `(release_status, workbook_path)`;
- what it must not do: edit the raw exports, hard-code a release status, or delete rows that cause problems;
- your **prediction**: which controls must pass before January figures can be released?

## 3. Build and run (slides 4–5, 35 min)
1. Ask Copilot to implement `run_month(input_folder, period, output_folder, mapping_file=None)` from your
   specification. **Read the code.** Does it build figures before checking the release? Does it hard-code `"ready"`?
2. Run the script (with `ATTEMPT = "attempt-01"`). It writes to `outputs/D1-S08/attempt-01`.
3. Open `control_summary.csv` and `exceptions.csv`. Answer: **may management use these figures, and why?**

A blocked result is the correct outcome here. Record the failing check, the source file, the rows and the amounts.
Do not "fix" it by filtering rows out.

## 4. Apply the correction (slide 6)
Once you have diagnosed the problem, read `late_delivery/README.md` inside the input folder. Finance has sent
`account_mapping_updated.csv`. **Do not edit the exports.** Change the two settings at the top of the script and
run it again, so attempt-01 stays as evidence:
```python
ATTEMPT = "attempt-02"
MAPPING_FILE = Path("case_pack/data/faulty/F10_january_unmapped_account/late_delivery/account_mapping_updated.csv")
```

## 5. Validate the release (slide 7, 15 min)
You should now see `ready` and a workbook without `_BLOCKED`. Compare your figures with the January reference file,
which was produced separately from your code. Create `outputs/D1-S08/compare.py`, paste the code below, save, and run
`.virtual-env-folder\Scripts\python.exe outputs\D1-S08\compare.py`. Both lines should print `True`.
```python
import pandas as pd
mine = pd.read_csv("outputs/D1-S08/attempt-02/actuals_by_line.csv", dtype={"period": str})
expected = pd.read_csv("case_pack/data/clean/checkpoints/actuals_by_line_2026-01.csv", dtype={"period": str})
compare = expected.merge(mine, on=["period", "entity", "report_line"], how="outer", suffixes=("_expected", "_mine"), indicator=True)
print("all 9 keys:", len(compare) == 9 and (compare["_merge"] == "both").all())
print("within 0.01:", (compare["actual_amount_mine"] - compare["actual_amount_expected"]).abs().le(0.01).all())
```
In Excel, check that the Summary formatting is intact and C14 shows 0.00. If Excel is unavailable, write "not checked in Excel".

## 6. Hand over (slide 8, part of the 15 min)
Write `outputs/D1-S08/handover.md`:
1. Purpose and period
2. Input folder and the **reference correction**: what changed, who supplied it, and why
3. The exact command or call to rerun
4. The controls run and the release decision, for **both** attempts
5. Output locations
6. Known limitations

## 7. Peer explanation and preview (slide 9, 10 min)
Swap notes with a partner. Could they rerun your process from the note alone? Do they understand what the status means?
Walk your partner through one prediction, one change and one check. Then the instructor previews the project tracks.

## What to keep
Both attempt folders, your specification, `compare.py` and `handover.md`. A correctly explained blocked first run,
plus a checked corrected run, is the complete result.

## Troubleshooting
| Symptom | Check first |
|---|---|
| `SETUP: cannot find outputs/handoffs/D1-S08/...` | You are running from the course folder, and the ZIP was extracted into it |
| A released pack from the original inputs | Your code builds figures too early: check the release status **before** building figures |
| `... already exists: keep it as evidence` / `FileExistsError` | Set `ATTEMPT` to a new name; never overwrite the blocked evidence |
| The attempt-02 workbook is still `_BLOCKED`, or `actuals_by_line.csv` is missing | The corrected mapping was not passed: check `MAPPING_FILE` and that `run_month` passes it to `load_inputs`; check that your `run_month` writes `actuals_by_line.csv` when the release is not blocked (step 4 in its description) |

**Reset:** see `RESET.md`.

## Optional extension
Run the clean January inputs (`case_pack/data/clean`, `2026-01`) into another folder and confirm they give the same
figures as your corrected run.
