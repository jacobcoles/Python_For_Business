# Multi-file reconciliation

**The business question:** Do two systems agree on the same transactions, and what exactly differs?

**Worked example:** `worked_example.py` in this folder solves a small version with course data. It builds on
D1-S04. Open it and click **Run Python File** to see what it produces; its comments explain each step.

**Data it uses:** N01's eight December transactions in `case_pack/data/clean/tiny/` and a settlement extract from another system in this folder.

## How to start

1. In the VS Code Explorer, right-click `outputs` and choose **New Folder**; name it `projects` if it is not there
   already. Then right-click `outputs/projects`, choose **New Folder**, and name it after your project, for example
   `my_multi_file_reconciliation`.
2. Copy `worked_example.py` into that folder (right-click, **Copy**, then **Paste**) and run your copy. It saves
   its results beside itself, in your folder, and prints the full path it used.
3. Make the first change from your plan (`sessions/D2-S07/learner/project_plan.md`), run it, and check the result.

## Ideas for your change

- Report totals by status as well as item by item.
- Change the tolerance and explain which items change status.
- Reconcile a second pair of files that you have prepared by hand, with known differences.

## Your finished project must show

- Every item from both files appears exactly once.
- The totals on each side are explained by the statuses.
- A repeated transaction stops the reconciliation.
- **Why this tool:** having built it, whether Python was the right choice for this job, or whether Excel, Power BI
  or KNIME would be more sustainable for whoever maintains it.
- **A handover note** with: purpose, inputs, how to run it, what you checked, and known limits. Use the headings in
  `case_pack/starters/handover_note_template.md` (the same ones you used in D1-S08).

Use your own data only if your organisation has approved it and it is available. Never change the files in
`case_pack`: save everything under `outputs/projects/`.
