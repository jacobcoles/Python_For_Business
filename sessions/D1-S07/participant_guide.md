# D1-S07: Reporting automation into an existing template
45 minutes. Northbridge is fictional; amounts are EUR.

**Question:** can we put the checked December figures, or the reasons they are blocked, into the pack that
management already reads, without changing the master template?
**Start:** `sessions/D1-S07/learner/writer_scaffold.py`.
**Master template (input only):** `case_pack/templates/northbridge_reporting_template.xlsx`.
**Output:** `outputs/D1-S07/run-01/Northbridge_Management_Pack_2025-12_r01.xlsx` and
`outputs/D1-S07/run-02/Northbridge_Management_Pack_2025-12_r01_BLOCKED.xlsx`.

Run commands from the course folder in the VS Code terminal (macOS: `.virtual-env-folder/bin/python` and forward slashes).

## 1. The template and what goes in each sheet (slides 1–2, 7 min)
Extract the D1-S07 ZIP from the instructor (**`component_handout.zip`**, which contains the supplied code that writes the workbook).
In Windows, right-click the ZIP → **Extract All** and set the destination to your **course folder** (the one
containing `case_pack` and `sessions`). Windows suggests a new folder named after the ZIP: remove that part.

Open the master template
in Excel **without saving it**. It has five sheets:

| Sheet | Receives | Sign |
|---|---|---|
| Summary | Period (C3), status (C4), one row per unit | Costs shown **positive** |
| ByLine | The 9 reporting lines | **Signed**, as stored |
| Controls | The control summary | n/a |
| Exceptions | Failed records | n/a |
| ReadMe | Inputs, run details, how to rerun | n/a |

Summary cell **C14** contains the formula `=ROUND(G12-(D12-E12-F12),2)`. It should display 0.00.

## 2. Predict (slide 3)
If Python reads C14 back from a saved file, what will it see? What will Excel show? Discuss with your neighbour.

## 3. The supplied function that writes the workbook (slides 4–5, 10 min demonstration)
`report.write_workbook(output_folder, inputs, release_status, control_summary, exceptions, summary)`
does the following:
- opens the master and saves a **new** file for the period;
- refuses to overwrite the master or an existing output;
- when the status is `"blocked"`, writes no figures, writes the full control results and exceptions, and adds
  `_BLOCKED` to the name.

To read its full description, temporarily add `help(report.write_workbook)` as the first line under
`if __name__ == "__main__":` in `writer_scaffold.py` and run the script.

## 4. Your turn (slide 6, 18 min)
`writer_scaffold.py` already loads the supplied functions and prepares the December `summary` and a
`read_control_run(name)` helper that returns `(inputs, controls, exceptions)`. Three settings at the top of the file
(`CONTROL_RUN`, `RELEASE`, `OUTPUT_FOLDER`) choose which run the script performs.
1. Ask Copilot to complete `populate_and_save(inputs, controls, exceptions, release, output_folder)` so that it
   calls `report.write_workbook` and returns the saved path. **Read the code first.** It must not save to the
   template path, hard-code `"ready"`, or build a new workbook from scratch.
2. Run the script with the default settings (`clean_2025-12`, `ready`, `outputs/D1-S07/run-01`):
   `.virtual-env-folder\Scripts\python.exe sessions\D1-S07\learner\writer_scaffold.py`
3. Open the file in Excel and check the Summary figures:

| Unit | Revenue | Direct cost | Overhead | Operating result |
|---|---:|---:|---:|---:|
| N01 | 68,197.95 | 28,059.68 | 10,275.77 | 29,862.50 |
| N02 | 50,612.03 | 19,556.86 | 7,610.34 | 23,444.83 |
| N03 | 38,117.91 | 17,554.80 | 6,539.58 | 14,023.53 |
| Total | 156,927.89 | 65,171.34 | 24,425.69 | **67,330.86** |

   C14 shows **0.00**. The formatting matches the master. ByLine is signed.
4. Run the script again without changing anything. It should refuse, with `FileExistsError`, and name the existing file. If Excel has the
   file open on Windows, close it before any deliberate replacement.

## 5. Inspect the blocked pack (slide 7, 8 min)
Change the three settings to `CONTROL_RUN = "F03_duplicate_mapping"`, `RELEASE = "blocked"` and
`OUTPUT_FOLDER = Path("outputs/D1-S07/run-02")`, then run the script again. Check that:
- the filename ends `_BLOCKED`;
- Summary says **"Figures withheld: release blocked."** and ByLine has no figures;
- Controls shows C04 `fail`;
- Exceptions lists `account_mapping.csv` rows 4 and 8, where code 0500 is mapped twice (data rows without the header:
  lines 5 and 9 in an editor).

A file that saves is **not** an approved file.

## 6. Handover (slide 8, 2 min)
Write `outputs/D1-S07/handover.md` with **inputs · period · output file · release status · how to rerun**.
Then answer: why is preserving a formula different from calculating it? Why is "it saved" not numerical proof?

## What to keep
Your completed `writer_scaffold.py`, both workbooks and `handover.md`. Mention in the handover note whether Excel
showed 0.00 in C14, or that it was not checked in Excel.

## Troubleshooting
| Symptom | Check first |
|---|---|
| `SETUP: cannot find outputs/handoffs/D1-S07/...` | You are running from the course folder, and the ZIP was extracted into it |
| `FileExistsError` | This is the protection working. Change `OUTPUT_FOLDER` to a new run folder |
| `PermissionError` on save (Windows) | The output file is open in Excel: close it |
| Costs negative on Summary / formatting lost | Your code wrote cells itself or used `Workbook()`: call `write_workbook` instead |

**Reset:** see `RESET.md`. The master template is never changed.

## Optional extension
Add `run_number=2` to write a second revision next to the first, and explain when you would use this
instead of `overwrite=True`.
