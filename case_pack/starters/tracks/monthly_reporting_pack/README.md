# Monthly reporting pack

**The business question:** Each month, turn the units' exports into a checked management pack, or a clearly blocked one.

**Worked example:** `worked_example.py` in this folder solves a small version with course data. It builds on
D1-S06 to D1-S08. Open it and click **Run Python File** to see what it produces; its comments explain each step.

**Data it uses:** the month's exports, mapping, budget and the units' own totals in `case_pack/data/clean/` (December 2025 and January 2026), and the faulty deliveries in `case_pack/data/faulty/`.

## How to start

1. In the VS Code Explorer, right-click `outputs` and choose **New Folder**; name it `projects` if it is not there
   already. Then right-click `outputs/projects`, choose **New Folder**, and name it after your project, for example
   `my_monthly_reporting_pack`.
2. Copy `worked_example.py` into that folder (right-click, **Copy**, then **Paste**) and run your copy. It saves
   its results beside itself, in your folder, and prints the full path it used.
3. Make the first change from your plan (`sessions/D2-S07/learner/project_plan.md`), run it, and check the result.

## Ideas for your change

- Run January instead of December and explain which files change.
- Run a faulty delivery (for example `F01_missing_source`) and write the handover for a blocked month.
- Add one sentence per failed check to the ReadMe sheet.

## Your finished project must show

- The released figures match the checkpoint for that month.
- A faulty delivery produces a blocked pack with no figures.
- The master template is unchanged.
- **Why this tool:** having built it, whether Python was the right choice for this job, or whether Excel, Power BI
  or KNIME would be more sustainable for whoever maintains it.
- **A handover note** with: purpose, inputs, how to run it, what you checked, and known limits. Use the headings in
  `case_pack/starters/handover_note_template.md` (the same ones you used in D1-S08).

Use your own data only if your organisation has approved it and it is available. Never change the files in
`case_pack`: save everything under `outputs/projects/`.
