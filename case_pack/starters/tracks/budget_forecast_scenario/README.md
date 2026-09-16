# Budget and forecast scenarios

> What do finance's assumptions, and your alternative, imply for the first quarter of next year?

A baseline forecast for January to March 2026 already exists. Finance has sent assumptions. Your job is to check
the baseline was built the way it claims, apply the assumptions, and show what changes, with one figure somebody
can check on a calculator.

**You build this in Python.** The method is in `budget_forecast_scenario_python.md`, beside `worked_example.py`.
**After you have built it**, `budget_forecast_scenario_in_other_tools.md` shows the same job elsewhere, and this is
the one track where Power BI can do something Python cannot.

## What you produce

A comparison of the baseline against the original plan and two chosen cases, the assumptions you used written
down, a chart, and a recommendation with its reasoning.

## Data in

| File (paths start at the course folder) | One row is | Columns that matter |
|---|---|---|
| `case_pack/data/clean/history/monthly_actuals_history.csv` | One reporting line for one unit in one past month | `period`, `entity`, `report_line`, `actual_amount` |
| `case_pack/data/clean/planning/baseline_forecast.csv` | One forecast line | `period`, `entity`, `report_line`, `amount`, `source_period`, `data_cutoff` |
| `case_pack/data/clean/scenario_assumptions.csv` | One named scenario | the three multipliers |

History is 324 rows: 36 months from January 2023 to December 2025, three units, three lines each. The baseline is
27 rows: three months, three units, three lines. Costs are negative throughout.

## Data out

| The information | Shape | Where |
|---|---|---|
| Each case's figures | One row per report line, with a column per case | Your project folder |
| The assumptions you chose | The multipliers and the business reason for each | Beside it |
| The comparison | A chart, and one unit and month shown in full | Beside it |

## The steps

1. Read the history, the baseline and the assumptions.
2. Check that the January to March 2026 baseline equals the corresponding January to March 2025 values, using only
   history available through December 2025.
3. Apply the original scenarios, including the neutral one, which must reproduce the baseline exactly.
4. Apply two chosen cases as revenue and cost multipliers.
5. Compare one unit and month in full, and check one line on a calculator.
6. Chart the cases against history, and save the assumptions you used.

## Ask Copilot for

| Step | What to ask for |
|---|---|
| 2 | A comparison of each forecast row against the same month a year earlier, that stops if any row differs |
| 4 | A multiplication of one column by a factor that depends on which reporting line the row is |
| 5 | A table with one row per reporting line and one column per case, for a single unit and month |

## It is right when

**Step 2**, all three must hold: every one of the 27 baseline rows equals the same month one year earlier; the
history has all 36 months to a December 2025 cutoff; nothing after that cutoff is used.

**Step 3**, the neutral scenario with every multiplier at 1.00 reproduces the baseline on all 27 rows.

**Step 5**, for N02 in February 2026, compare within EUR 0.01:

| | Baseline | Original growth | Finance 1.05 / 1.12 |
|---|---:|---:|---:|
| Revenue | 52,688.88 | 57,957.77 | 55,323.32 |
| Direct cost | −19,648.94 | −21,220.86 | −22,006.81 |
| Overhead | −7,650.54 | −7,650.54 | −7,650.54 |
| **Operating result** | **25,389.40** | **29,086.37** | **25,665.97** |

Finance's case is **3,420.40 below** the original growth plan. Multiply 52,688.88 by 1.05 on a calculator: it gives
55,323.32, and that is the check.

## Break it on purpose

Set both finance multipliers to 1.00 and run it. The "scenario" now equals the baseline exactly. If your code
produces anything else at 1.00, it is not applying a multiplier, it is doing something else.

## A note on the rounding

The supplied code rounds each reporting line to cents before adding them into an operating result. Another tool
might multiply and add first and round once at the end. Those two conventions disagree by a cent on some
multiplier pairs and never by more, which is why every figure here is compared **within EUR 0.01** rather than
expected to match exactly.

## Ideas for your change

- Choose your own two cases with a business reason for each, rather than a round number.
- Look at a different unit or month, and say whether the story changes.
- Add a scenario of your own, and be explicit that it is a what-if and not a probability.

## Your finished project must show

- The comparison, the assumptions and the chart.
- **Evidence of a check**: the neutral scenario reproduces the baseline, and one line checked by hand.
- **Why this tool**, having built it.
- **A handover note** using the headings in `case_pack/starters/handover_note_template.md`.

Use your own data only if your organisation has approved it and it is available. Never change the files in
`case_pack`: save everything under `outputs/projects/`.
