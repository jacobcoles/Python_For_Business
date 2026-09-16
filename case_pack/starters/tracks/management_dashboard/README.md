# Management dashboard

> Which units are above or below budget this month, and by how much?

Management wants one page. You have checked figures in two files that must agree with each other. Your job is to
prove they agree, turn them into a table a report user can read, and only then build the report.

**You build the data in Python.** The method is in `management_dashboard_python.md`, beside `worked_example.py`.
**After you have built it**, `management_dashboard_in_other_tools.md` covers the report itself, which is the one
track where another tool is the natural home for the finished product.

## What you produce

One row per unit with its actual result, its budget and the variance, in plain column names, plus a report or
chart built from it and a sentence saying what it shows.

## Data in

| File (paths start at the course folder) | One row is | Columns that matter |
|---|---|---|
| `case_pack/data/clean/analysis/unit_comparison_2025-12.csv` | One unit's December result against budget | `entity`, `operating_result`, `budget_operating_result`, `favourable_variance` |
| `case_pack/data/clean/checkpoints/actuals_by_line_2025-12.csv` | One reporting line for one unit | `entity`, `report_line`, `actual_amount` |

The second file exists to check the first. Nine reporting lines, three per unit, signed: costs are negative.

## Data out

| The information | Shape | Where |
|---|---|---|
| Each unit's actual, budget and variance | One row per unit, plain column names, 2 decimals | Your project folder |
| A picture of the variance | A chart, or a report page | Beside it, or in the reporting tool |
| What it shows | One or two sentences, with the period and the units of measure | A note beside it |

## The steps

1. Read the unit comparison and the nine checked reporting lines.
2. Confirm each unit's result equals the sum of its three signed lines, and stop if it does not.
3. Build one row per unit with plain column names a report user understands.
4. Save it, and draw the variance so you can see the figures before anyone else does.
5. Build the report from the saved file, and check one figure on the screen against the file.

## Ask Copilot for

| Step | What to ask for |
|---|---|
| 2 | A comparison of two tables' totals that stops the script when they disagree, not one that prints a warning |
| 3 | A rename of technical column names to ones a manager would recognise |
| 4 | A bar chart coloured by sign, with the amounts labelled on the bars |

## It is right when

Every unit's result equals the sum of its three reporting lines within EUR 0.01, and:

| Unit | Actual | Budget | Variance |
|---|---:|---:|---:|
| N01 Northbridge Support Services | 29,862.50 | 28,750.00 | +1,112.50 |
| N02 Northbridge Training Services | 23,444.83 | 24,550.00 | −1,105.17 |
| N03 Northbridge Advisory Services | 14,023.53 | 14,300.00 | −276.47 |
| **Total** | **67,330.86** | **67,600.00** | **−269.14** |

Compare within EUR 0.01. A positive variance is favourable: the unit did better than budget.

## Break it on purpose

Skip step 2 and build the report anyway. Everything works, the page looks finished, and you have no idea whether
the numbers on it are right. A dashboard built on unreconciled figures is worse than no dashboard, because people
believe it.

## Ideas for your change

- Add January as a second month so the report can compare periods. There is no ready-made
  `unit_comparison_2026-01.csv`: build it from `case_pack/data/clean/checkpoints/actuals_by_line_2026-01.csv`
  (group the three lines per unit) and `case_pack/data/clean/budget.csv`, which covers 2026-01. Checking that your
  January units reconcile to their lines is the same test as step 2.
- Add a unit filter to the report and check one unit's figures by hand.
- Show the three reporting lines behind a unit, so a reader can see where the variance came from.

## Your finished project must show

- The table and the report, with a title that states the finding rather than the subject.
- **Evidence of a check**: step 2 passed, and one figure on the screen matched the file.
- **Why this tool**, having built it. This track is the one where that answer is least likely to be Python.
- **A handover note** using the headings in `case_pack/starters/handover_note_template.md`.

Use your own data only if your organisation has approved it and it is available. Never change the files in
`case_pack`: save everything under `outputs/projects/`.
