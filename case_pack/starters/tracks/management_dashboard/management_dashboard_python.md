# Management dashboard: the data, in Python

The job is in `README.md`. This page covers steps 1 to 4, which produce the checked table. Step 5, the report
itself, is in `management_dashboard_in_other_tools.md`, because Excel or Power BI is usually the better home for it.

**Tool:** a Python script in VS Code, with Microsoft 365 Copilot Chat for the code.
**You will produce:** `dashboard_units.csv`, `preview_variance_by_unit.png` and `dashboard_note.md`.

## Start here

1. Right-click `outputs` > **New Folder**, name it `projects` if it is not there. Right-click `outputs/projects` >
   **New Folder**, name it after your project, for example `december_dashboard`.
2. Right-click `worked_example.py` > **Copy**, then right-click your folder > **Paste**.
3. Open your copy and click **Run Python File**.

**You should see:**

```text
Check: unit results equal the sum of their reporting lines: yes
 period unit                     unit_name  actual_eur  budget_eur  variance_eur
2025-12  N01  Northbridge Support Services    29862.50     28750.0       1112.50
2025-12  N02 Northbridge Training Services    23444.83     24550.0      -1105.17
2025-12  N03 Northbridge Advisory Services    14023.53     14300.0       -276.47
```

and a `Saving into:` line with your own folder. Two files appear in it.

## Step 1: read both files

```python
units = pd.read_csv(f"case_pack/data/clean/analysis/unit_comparison_{PERIOD}.csv", dtype={"period": str})
lines = pd.read_csv(f"case_pack/data/clean/checkpoints/actuals_by_line_{PERIOD}.csv", dtype={"period": str})
```

`dtype={"period": str}` keeps `2025-12` as text. Without it the period can be read as something else and stop
matching later.

`PERIOD` is a setting at the top. Changing it to `2026-01` will fail on the first file, because January has no
ready-made unit comparison. Building it is one of the suggested changes in `README.md`, and it is a better
exercise than it sounds.

## Step 2: prove the two files agree (do not skip this)

**Why:** you are about to publish these figures. The two files come from different places, and if they disagree,
one of them is wrong and you do not yet know which.

```python
from_lines = lines.groupby("entity")["actual_amount"].sum().round(2)
agree = (units.set_index("entity")["operating_result"].round(2) - from_lines).abs().le(0.01).all()
print("Check: unit results equal the sum of their reporting lines:", "yes" if agree else "NO")
if not agree:
    raise SystemExit("STOPPED: the two checked files disagree. Do not publish a dashboard from them.")
```

**Read the last two lines.** The script *stops*. It does not print a warning and carry on, because a warning at the
top of a long output is a warning nobody reads.

The sum works because costs are stored negative, so a unit's operating result is a plain sum of its three lines.

**Ask Copilot** if you want to write it yourself:

> I have two pandas DataFrames. `lines` has entity, report_line and actual_amount, three rows per entity, with
> costs stored as negative numbers. `units` has entity and operating_result, one row per entity. Write a check
> that each entity's operating_result equals the sum of its three actual_amount values within 0.01, prints a
> plain yes or no, and stops the script with a message if they do not agree.

## Step 3: plain column names

`operating_result` and `favourable_variance` are our names. A manager reading a report should see `actual_eur`,
`budget_eur` and `variance_eur`, with the currency in the name so nobody has to ask.

```python
dashboard = units[[...]].rename(columns={
    "entity": "unit", "entity_name": "unit_name", "operating_result": "actual_eur",
    "budget_operating_result": "budget_eur", "favourable_variance": "variance_eur"})
```

Do this once, here, rather than in the report. If the renaming lives in the reporting tool, the next person to
build a report from the same file has to guess the same names again.

## Step 4: save it, and look at it before anyone else does

The file is saved with `float_format="%.2f"` so the CSV holds two decimals rather than the full floating-point
value. The chart is a preview for you, not the deliverable: it exists so you see the shape of the answer before
building a report on it.

**You should see** one bar above zero (N01) and two below (N02 and N03), each labelled with its amount.

## Check your result

| Unit | Actual | Budget | Variance |
|---|---:|---:|---:|
| N01 | 29,862.50 | 28,750.00 | +1,112.50 |
| N02 | 23,444.83 | 24,550.00 | −1,105.17 |
| N03 | 14,023.53 | 14,300.00 | −276.47 |
| Total | 67,330.86 | 67,600.00 | −269.14 |

Compare within EUR 0.01. Add the three variances on a calculator: they must give −269.14. One unit beat budget and
two missed it, and the group is very slightly behind.

## Write the note

Right-click your project folder > **New File**, name it `dashboard_note.md`:

```text
What the month shows, in one sentence a manager would repeat:
The figure I checked by hand, and against what:
What this table does not tell you:
Who reruns this next month, and in which tool:
```

"What this table does not tell you" is the honest part: it shows the result against budget, not why, and three
units at this size can move on one contract.

## Done when

The check prints `yes`, the three units match the table above, the CSV and the chart are in your own folder, and
your note leads with a finding rather than a description.

## If something goes wrong

| What you see | What to do |
|---|---|
| `STOPPED: the two checked files disagree` | The safeguard worked. Print both sides per unit and find which one is out |
| `FileNotFoundError` on `unit_comparison_2026-01.csv` | That file only exists for 2025-12. See the ideas in `README.md` |
| The variances do not add to −269.14 | You are summing the wrong column, or a sign has been flipped somewhere |
| The chart is empty or has no labels | Run it again after the CSV is saved; the chart is drawn from the same table |
| `KeyError` after renaming | The rename ran twice, or a name in the list does not match the source file |

**Start again:** delete your copy and paste `worked_example.py` again. The two source files never change.
