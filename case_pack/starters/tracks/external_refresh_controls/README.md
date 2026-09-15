# External data refresh with controls

**The business question:** Can we refresh external context each month and always say honestly how current it is?

**Worked example:** `worked_example.py` in this folder solves a small version with course data. It builds on
D2-S02 and D2-S03. Open it and click **Run Python File** to see what it produces; its comments explain each step.

**Data it uses:** the OECD consumer-price series (live, or the response saved on 2026-09-13 in `case_pack/data/external/`).

## How to start

1. In the VS Code Explorer, right-click `outputs` and choose **New Folder**; name it `projects` if it is not there
   already. Then right-click `outputs/projects`, choose **New Folder**, and name it after your project, for example
   `my_external_refresh_controls`.
2. Copy `worked_example.py` into that folder (right-click, **Copy**, then **Paste**) and run your copy. It saves
   its results beside itself, in your folder, and prints the full path it used.
3. Make the first change from your plan (`sessions/D2-S07/learner/project_plan.md`), run it, and check the result.

## Ideas for your change

- Change the months and explain what the checks confirm.
- Run the refresh live on an approved network and record the outcome, including a failure.
- Write the checks you would need for a different approved source.

## Your finished project must show

- The table passes its meaning checks and is saved with its source record.
- The retrieval time is the original download time.
- A failed request is reported, never hidden.
- **Why this tool:** having built it, whether Python was the right choice for this job, or whether Excel, Power BI
  or KNIME would be more sustainable for whoever maintains it.
- **A handover note** with: purpose, inputs, how to run it, what you checked, and known limits. Use the headings in
  `case_pack/starters/handover_note_template.md` (the same ones you used in D1-S08).

Use your own data only if your organisation has approved it and it is available. Never change the files in
`case_pack`: save everything under `outputs/projects/`.
