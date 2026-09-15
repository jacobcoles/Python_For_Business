# Management dashboard in Excel or Power BI

**The business question:** Can a manager see each unit's result against budget in the tool they already use?

**Worked example:** `worked_example.py` in this folder solves a small version with course data. It builds on
D2-S04 and D2-S06. Open it and click **Run Python File** to see what it produces; its comments explain each step.

**Data it uses:** the checked unit comparison and reporting lines in `case_pack/data/clean/`.

## How to start

1. In the VS Code Explorer, right-click `outputs` and choose **New Folder**; name it `projects` if it is not there
   already. Then right-click `outputs/projects`, choose **New Folder**, and name it after your project, for example
   `my_management_dashboard`.
2. Copy `worked_example.py` into that folder (right-click, **Copy**, then **Paste**) and run your copy. It saves
   its results beside itself, in your folder, and prints the full path it used.
3. Make the first change from your plan (`sessions/D2-S07/learner/project_plan.md`), run it, and check the result.

## Ideas for your change

- Build the report in Power BI or Excel from the CSV, with a title that states the finding.
- Add January as a second month so the report can compare periods.
- Add a unit filter and check one unit's figures by hand.

## Your finished project must show

- The dashboard figures equal the checked source lines.
- The report says what it shows and what it does not.
- A colleague can refresh it from the handover note.
- **Why this tool:** having built it, whether Python was the right choice for this job, or whether Excel, Power BI
  or KNIME would be more sustainable for whoever maintains it.
- **A handover note** with: purpose, inputs, how to run it, what you checked, and known limits. Use the headings in
  `case_pack/starters/handover_note_template.md` (the same ones you used in D1-S08).

Use your own data only if your organisation has approved it and it is available. Never change the files in
`case_pack`: save everything under `outputs/projects/`.
