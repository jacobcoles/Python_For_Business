# Budget and forecast scenarios in Python

The job is in `README.md`. This is how to build it.

**Tool:** a Python script in VS Code, with Microsoft 365 Copilot Chat for the code.
**You will produce:** `changed_assumptions.csv`, `scenario_figure.png` and `scenario_note.md`.

## Start here

1. Right-click `outputs` > **New Folder**, name it `projects` if it is not there. Right-click `outputs/projects` >
   **New Folder**, name it after your project, for example `q1_scenarios`.
2. Right-click `worked_example.py` > **Copy**, then right-click your folder > **Paste**.
3. Open your copy and click **Run Python File**.

**You should see** three `OK:` lines from the baseline check, a table of average errors, the neutral-scenario
confirmation, then the N02 February comparison and two saved files.

## Step 1: read the three inputs

`planning.load_inputs()` reads all three and prints their sizes, which are the first thing to check:

```text
history:     324 rows (expected 324 = 36 months x 3 units x 3 report lines)
baseline:    27 rows (expected 27 = 3 future months x 3 units x 3 report lines)
assumptions: 3 rows (expected 3 scenarios)
```

If a count is wrong, stop there. Everything downstream is built on these.

## Step 2: check the baseline was built the way it claims

**Why:** the baseline is a **seasonal naive** forecast, which means each future month is simply a copy of the same
month one year earlier. That is a modest method, and it is honest as long as it really is what was done. This step
proves it.

`planning.check_baseline(history, baseline)` prints three lines:

```text
OK: every unit and report line has all 36 months, January 2023 to December 2025.
OK: each of the 27 baseline rows is the same month one year earlier.
OK: nothing after December 2025 is used.
```

So January 2026 equals January 2025, February 2026 equals February 2025, March 2026 equals March 2025, for every
unit and every reporting line, and the cutoff is December 2025.

**This is an equality check, not a measure of how good the forecast is.** Those are two different questions, and
confusing them is the most common mistake on this track:

| Question | How it is answered | Where |
|---|---|---|
| Was the baseline built as described? | Every row equals its month a year earlier. Yes or no | Step 2, and it must pass |
| How well has this method done before? | Forecast a period that already happened, compare with what happened | The holdout table, below |

A small error would not prove the baseline was built correctly, and a correctly built baseline can still forecast
badly. Keep them apart.

## The holdout table: supplied, to read rather than build

`planning.holdout_errors(history)` answers the second question, and you do not need to implement it:

```text
Forecast made with a September 2025 cutoff, for October to December 2025 (9 observations per line):
report_line  average size of error (EUR)
    revenue                      2747.84
direct_cost                      1241.81
   overhead                       183.55
```

Read it as: had we used this method three months ago, revenue would have been out by about 2,700 EUR a month on
average. That is the honest scale of the uncertainty around every figure below, and it is worth one sentence in
your note. Overhead is nearly flat and predicts well; revenue does not.

## Step 3: the original scenarios, and the one that must change nothing

`planning.original_scenarios(baseline, assumptions)` applies the three supplied scenarios and checks the neutral
one:

```text
OK: the neutral 'baseline' scenario (all multipliers 1.00) matches the baseline exactly.
```

**Why this matters more than it looks:** it is a self-test of your own arithmetic. A scenario with every multiplier
at 1.00 must reproduce the baseline on all 27 rows. If it does not, the multiplication is being applied to the
wrong column, or twice, or to the wrong rows, and every other scenario is wrong in the same way.

## Step 4: your two cases

The settings at the top are multipliers. Overhead stays at 1.00 in both.

```python
FINANCE_REVENUE, FINANCE_DIRECT_COST = 1.05, 1.12
MY_REVENUE, MY_DIRECT_COST = 1.07, 1.10
```

**Ask Copilot** if you want to apply them yourself:

> I have a pandas DataFrame `baseline` with the columns period, entity, report_line and amount, where report_line
> is revenue, direct_cost or overhead and costs are negative. Write code that multiplies each row's amount by a
> factor chosen by its report_line, from a dictionary of multipliers, and returns a new DataFrame. Do not change
> the sign of any row and do not modify the original.

**Read it before pasting.** A cost multiplier above 1.00 must make the cost **bigger**, which means more negative.
If your direct cost gets smaller when you raise the multiplier, the sign is being handled twice.

## Step 5: one unit and month, in full

`planning.compare_n02_february(baseline, original, chosen)` prints the table in `README.md`. Check one cell by
hand: 52,688.88 × 1.05 = 55,323.32.

**Why one unit and month rather than a total:** a total hides compensating errors. One line, checked on a
calculator, is worth more than a page of figures nobody has touched.

## Step 6: chart and save the assumptions

The chart puts history and the cases on the same axis, so the size of the change is visible against the size of
normal monthly movement. `changed_assumptions.csv` records what you chose. A scenario without its assumptions
written down cannot be defended a week later.

## Check your result

For N02, February 2026, compare within EUR 0.01:

| | Baseline | Original growth | Finance 1.05 / 1.12 | Your case 1.07 / 1.10 |
|---|---:|---:|---:|---:|
| Revenue | 52,688.88 | 57,957.77 | 55,323.32 | 56,377.10 |
| Direct cost | −19,648.94 | −21,220.86 | −22,006.81 | −21,613.83 |
| Overhead | −7,650.54 | −7,650.54 | −7,650.54 | −7,650.54 |
| **Operating result** | **25,389.40** | **29,086.37** | **25,665.97** | **27,112.73** |

Finance's case is 3,420.40 below the original growth plan; yours is 1,973.64 below it.

## Write the note

Right-click your project folder > **New File**, name it `scenario_note.md`:

```text
The assumptions I chose, and the business reason for each:
What finance's case means for the quarter, in one sentence:
The line I checked by hand, and what I got:
How much of this difference is smaller than the method's own average error:
What I am NOT claiming (these are what-ifs, not probabilities):
```

The fourth heading is the honest one. Revenue's average error is about 2,700 EUR a month, so a difference of a few
hundred between two cases is inside the noise and should not drive a decision on its own.

## Done when

The three baseline checks pass, the neutral scenario reproduces the baseline, your N02 February figures match the
table, you have checked one line by hand, and your note separates what you chose from what you know.

## If something goes wrong

| What you see | What to do |
|---|---|
| `PROBLEM: a baseline row does not match its historical month` | Do not continue. The baseline is not what it claims |
| `PROBLEM: the neutral scenario differs from the baseline` | Your multiplication is wrong. Check it is applied once, to `amount`, per report line |
| Costs shrink when you raise the cost multiplier | The sign is being handled twice. Multiply the signed amount and leave the sign alone |
| A figure is one cent from the table | Expected. Compare within EUR 0.01; see the rounding note in `README.md` |
| `KeyError` on a multiplier | The report line names must be revenue, direct_cost and overhead exactly |

**Start again:** delete your copy and paste `worked_example.py` again. The three input files never change.
