# D2-S05: Planning scenarios for the CFO

**Which planning case should the CFO use for next quarter?**

13:15 to 14:45, 90 minutes. **Tool: a Jupyter notebook in VS Code**, because you check the baseline, change
assumptions and look at charts in stages.

**You will produce:** in `outputs/D2-S05/`, your assumptions (`changed_assumptions.csv`), a scenario chart
(`scenario_figure.png`) and your recommendation (`interpretation.md`).

**All the steps are in the notebook.** This page tells you what you are working with and how to start.

## The question

Finance expects the **direct costs it buys in** (delivery and subcontractors) to **rise about 12%**, and **sales to
grow about 5%**, above the baseline for January to March 2026. Overhead is unchanged. The CFO wants that case compared with the original growth plan and with a less severe case of your own,
and wants to know how much weight to put on the difference.

## Data you will read

| File (in `case_pack/data/clean/`) | What it contains | One row means |
|---|---|---|
| `history/monthly_actuals_history.csv` | What happened, January 2023 to December 2025 | One unit, report line and month |
| `planning/baseline_forecast.csv` | The starting forecast for January to March 2026: the same month one year earlier | One unit, report line and future month |
| `scenario_assumptions.csv` | The original scenarios: baseline, growth, cost_pressure | One scenario and its multipliers |

## Rules for this task

- Fictional EUR data. Revenue is positive, costs are negative; operating result is the sum of the three lines.
- Only information up to December 2025 may be used. January 2026 actuals and the OECD data are not inputs.
- A multiplier scales a baseline amount once: 1.05 means 5% higher. It is not compounded from month to month.
- Overhead stays at 1.00 in your two cases.
- Scenarios are assumptions without probabilities.

## How to start

1. In VS Code choose **File > Open Folder** and open the course folder.
2. Open `sessions/D2-S05/learner/planning_notebook.ipynb`.
3. Choose the course **`.virtual-env-folder`** kernel at the top right of the notebook.
4. Follow the notebook from Step 0 to Step 8. Run cells in order the first time, not **Run All**.

## What the notebook asks of you

| Notebook step | What you do | How you know it worked |
|---|---|---|
| 1 | Load the three tables | 324, 27 and 3 rows |
| 2 | Check the baseline; discuss pattern and trend | Three **OK** lines and a history chart |
| 3 | See how accurate this method was on a past period | An error table for the three lines |
| 4 | Follow one number through a scenario | Two **OK** lines |
| 5 (YOUR CHOICE) | Translate finance's expectations into multipliers; choose and justify your own case | Your two cases saved |
| 6 | Check N02's February figures by calculator | Your sum matches the table |
| 7 | Read the scenario chart; weigh the difference against past errors | Chart saved |
| 8 | Write your recommendation; restart and run all | The same numbers appear again |

## If something goes wrong

| What you see | What to do |
|---|---|
| `Open the course folder in VS Code` in Step 0 | Use **File > Open Folder** and choose the course folder |
| `ModuleNotFoundError` | Choose `.virtual-env-folder` in the kernel picker |
| `NameError` (for example `baseline` is not defined) | Run the earlier cells again from Step 0 |
| `Each multiplier must be a number from 0.5 to 1.5` | Write multipliers like `1.05`, without a percent sign or quotation marks |
| `NOT DONE YET: finance's case still has 1.00` | Change the two finance multipliers in Step 5 and run that cell again. Nothing is saved until you do |
| `PROBLEM: finance expects supplier costs to RISE` | A cost rise is a multiplier **above** 1.00, because costs are stored as negative numbers |

**Start again:** choose **Restart** in the notebook toolbar and run from Step 0. The source data never changes.
