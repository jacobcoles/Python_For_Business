# Audit exceptions and data validation

**The business question:** Which deliveries can be relied on, and exactly which records need attention?

**Worked example:** `worked_example.py` in this folder solves a small version with course data. It builds on
D1-S06. Open it and click **Run Python File** to see what it produces; its comments explain each step.

**Data it uses:** the clean December delivery in `case_pack/data/clean/` and the faulty deliveries in `case_pack/data/faulty/` (each folder's README says what is wrong).

## How to start

1. In the VS Code Explorer, right-click `outputs` and choose **New Folder**; name it `projects` if it is not there
   already. Then right-click `outputs/projects`, choose **New Folder**, and name it after your project, for example
   `my_audit_exceptions`.
2. Copy `worked_example.py` into that folder (right-click, **Copy**, then **Paste**) and run your copy. It saves
   its results beside itself, in your folder, and prints the full path it used.
3. Make the first change from your plan (`sessions/D2-S07/learner/project_plan.md`), run it, and check the result.

## Ideas for your change

- Add the remaining faulty deliveries and explain each result.
- Write one extra check with Copilot (for example: no single transaction above EUR 10,000) and test it on a case you built by hand.
- Summarise the exceptions by unit for an audit manager.

## Your finished project must show

- The clean delivery passes every check.
- Each faulty delivery fails the check that matches its README.
- Every exception names its file and row.
- **Why this tool:** having built it, whether Python was the right choice for this job, or whether Excel, Power BI
  or KNIME would be more sustainable for whoever maintains it.
- **A handover note** with: purpose, inputs, how to run it, what you checked, and known limits. Use the headings in
  `case_pack/starters/handover_note_template.md` (the same ones you used in D1-S08).

Use your own data only if your organisation has approved it and it is available. Never change the files in
`case_pack`: save everything under `outputs/projects/`.
