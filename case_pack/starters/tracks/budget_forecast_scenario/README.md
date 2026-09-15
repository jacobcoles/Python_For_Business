# Budget and forecast scenarios

**The business question:** What do our assumptions imply for next quarter, and how much weight can the difference bear?

**Worked example:** `worked_example.py` in this folder solves a small version with course data. It builds on
D2-S05. Open it and click **Run Python File** to see what it produces; its comments explain each step.

**Data it uses:** the history, baseline forecast and scenario assumptions in `case_pack/data/clean/`.

## How to start

1. In the VS Code Explorer, right-click `outputs` and choose **New Folder**; name it `projects` if it is not there
   already. Then right-click `outputs/projects`, choose **New Folder**, and name it after your project, for example
   `my_budget_forecast_scenario`.
2. Copy `worked_example.py` into that folder (right-click, **Copy**, then **Paste**) and run your copy. It saves
   its results beside itself, in your folder, and prints the full path it used.
3. Make the first change from your plan (`sessions/D2-S07/learner/project_plan.md`), run it, and check the result.

## Ideas for your change

- Compare scenarios for one unit rather than all three.
- Add a scenario with a business reason and explain it to a CFO.
- Look at March instead of February and explain any difference.

## Your finished project must show

- The neutral scenario equals the baseline.
- One scenario figure checked by calculator.
- The chart separates history from assumptions, and no probabilities are claimed.
- **Why this tool:** having built it, whether Python was the right choice for this job, or whether Excel, Power BI
  or KNIME would be more sustainable for whoever maintains it.
- **A handover note** with: purpose, inputs, how to run it, what you checked, and known limits. Use the headings in
  `case_pack/starters/handover_note_template.md` (the same ones you used in D1-S08).

Use your own data only if your organisation has approved it and it is available. Never change the files in
`case_pack`: save everything under `outputs/projects/`.
