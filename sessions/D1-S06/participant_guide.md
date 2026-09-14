# D1-S06: Data quality, controls and reconciliation
45 minutes. Northbridge is fictional; tolerances are teaching assumptions, not policy.

**Question:** can we release December's figures, and if not, exactly what must the units fix?
**Start:** `sessions/D1-S06/learner/control_stubs.py`. Use `control_exploration.ipynb` if you prefer a notebook.
**Output:** `outputs/D1-S06/<run>/control_summary.csv` and `exceptions.csv`.

Run every command from the course folder in the VS Code terminal. On macOS, use `.virtual-env-folder/bin/python`
and forward slashes instead.

## 1. What a control is (slides 1–3, 8 min)
A control is a check that is written once, runs every month, and records a tolerance, a status, the failed records and
a release decision. Northbridge has nine controls:
- **C01–C08** are critical. Any `fail` blocks release.
- **C09**, the movement review, is a review warning only.

A status is `pass`, `fail` or `not_run` (the check could not run, for example because a file was missing).
**`not_run` is never a pass.**

## 2. Demonstration: run the supplied controls (slide 4, 8 min)
1. Extract the D1-S06 ZIP from the instructor (**`component_handout.zip`**, which contains the supplied control code).
   In Windows, right-click the ZIP → **Extract All** and set the destination to your **course folder** (the one
   containing `case_pack` and `sessions`). Windows suggests a new folder named after the ZIP: remove that part.
2. Check that `outputs/handoffs/D1-S06/report_components.py` exists.
3. Run `.virtual-env-folder\Scripts\python.exe sessions\D1-S06\learner\run_controls.py`.

Because your two functions are unfinished, C03 and C08 show `not_run`. C09 also shows `not_run`, because it only runs
when C01 to C08 pass. The output ends with `Release: blocked`.

## 3. Task 1: `duplicate_rows(rows)` (slide 5)
Return **every** occurrence of a duplicated full key (`entity`, `period`, `transaction_id`), keeping
`source_file` and `source_row`.
- `transaction_id` alone is not the key: `T000001` appears in all three units.
- Do not return only "the extra one", and never delete duplicates. The unit decides which row is genuine.

## 4. Task 2: `reconciliation_status(observed, expected)` (slide 6)
Return `"pass"` if the difference is at most EUR 0.01 (inclusive), otherwise `"fail"`.
**Predict first** against a control total of 14,023.53: observed 14,023.54 / 14,023.55 / 14,023.52 / 14,023.51.
Beware floating point: `abs(14023.54 - 14023.53) <= 0.01` is `False` in Python. Compare in cents or with `Decimal`.

## 5. Test, then run clean and faulty inputs (slide 7; 20 min in total for sections 3 to 5)
1. Run the self-test: `.virtual-env-folder\Scripts\python.exe sessions\D1-S06\learner\control_stubs.py`. Every line should say `ok`.
2. Run the clean data: `.virtual-env-folder\Scripts\python.exe sessions\D1-S06\learner\run_controls.py --output-folder outputs\D1-S06\clean`.
   You should see all `pass` and `Release: ready`.
3. Run the two faulty sets, each into its own folder:
   ```
   .virtual-env-folder\Scripts\python.exe sessions\D1-S06\learner\run_controls.py --input-folder case_pack\data\faulty\F02_duplicate_record --output-folder outputs\D1-S06\F02
   .virtual-env-folder\Scripts\python.exe sessions\D1-S06\learner\run_controls.py --input-folder case_pack\data\faulty\F06_reconciliation_mismatch --output-folder outputs\D1-S06\F06
   ```

## 6. Read the exception reports (slide 8, 7 min)
Open each `exceptions.csv`. `source_row` counts data rows without the header, so row 42 is line 43 in an editor.
Discuss with your neighbour before the group review:
- which checks failed, and why one problem can cause several checks to fail;
- which source file and rows you would send to the unit;
- why C03's `affected_count` is 1 while two rows are listed.

## 7. Explain (slide 9, 2 min)
- Why is a failed critical check different from a C09 review warning?
- Why can `not_run` never count as a pass?
- What would you send N01 about F02?

## What to keep
Your completed `control_stubs.py` and the three output folders (`clean`, `F02`, `F06`).

## Troubleshooting
| Symptom | Check first |
|---|---|
| `SETUP: cannot find outputs/handoffs/D1-S06/...` | You are running from the course folder, and the ZIP was extracted into the course folder (not inside `sessions/`) |
| C03 or C08 still `not_run` | You saved `control_stubs.py`, and your function returns a value, not `None` |
| `reconciliation_status must return pass or fail` | You return exactly the strings `"pass"` or `"fail"` |
| +0.01 gives `fail` | Floating point: compare `round(x*100)` values or use `Decimal` |

**Reset:** see `RESET.md`. The instructor can share a worked solution after your attempt.

## Optional extension
The movement review (C09) warns only when **both** `abs(movement) > 100.00` **and** `abs(movement %) > 20%`.
Work out the nine small cases in `case_pack/data/clean/boundary/README.md` on paper.
