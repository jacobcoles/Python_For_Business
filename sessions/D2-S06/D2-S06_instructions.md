# D2-S06: Python in a script, Power BI and KNIME

**Where should this Python step live: in a script, in Power BI, or in KNIME?**

15:00 to 15:45, 45 minutes. **Tools: VS Code, then Power BI Desktop, then KNIME Analytics Platform.** You run the
same small Python step in all three, then decide which route suits a colleague.

**You will produce:** `outputs/D2-S06/unit_results.csv` from VS Code, the same table inside Power BI and KNIME
(KNIME also saves `outputs/D2-S06/knime_unit_results.csv`), and a short decision note
`outputs/D2-S06/route_decision.md`.

## Why this matters

A checked Python result can reach colleagues in different ways: as a clean file they import, as a step inside a
Power BI report, or as a node in a KNIME workflow. Each route changes **where Python runs** and **who must keep it
working**. Doing the same step three ways makes those differences concrete.

## Data you will read

`case_pack/data/clean/checkpoints/actuals_by_line_2025-12.csv` (paths start at the course folder): the nine checked
December reporting lines, three per unit. Columns: `period` (text, for example 2025-12), `entity` (N01 to N03),
`report_line` (revenue, direct_cost or overhead) and `actual_amount` (signed EUR). Costs are already negative, so a
unit's operating result is the sum of its three lines.

Power BI and KNIME need the **full** path to this file: right-click it in the VS Code Explorer and choose
**Copy Path**.

## Files you will open or run

| File | What it is for |
|---|---|
| `sessions/D2-S06/learner/compare_routes.py` | Where you write and test the Python step in VS Code |
| `sessions/D2-S06/learner/route_comparison.md` | A comparison table to read before you decide |

## Rules for this task

- One row per unit and month, with a column `operating_result`.
- Do not add a total row, and never treat a missing reporting line as zero.
- Every route must give the same three operating results, within EUR 0.01. Step 1 prints them; compare Steps 2 and 3
  against what you got there.
- Power BI and KNIME give Python the input table already named **`dataset`**. Your step must create a table named
  **`result`**.

## Steps

### Step 1: Write the step once, in VS Code (8 minutes)

**Why:** you test the logic where it is easiest to see errors, before putting it inside another application.

**Do:** open `compare_routes.py` and ask Copilot:

> I have a pandas DataFrame called `dataset` with the columns period, entity, report_line and actual_amount.
> Write one or two lines of pandas that create a DataFrame called `result` with one row per period and entity, where
> operating_result is the sum of actual_amount. Use only `dataset` and `pd`. Do not read or write files.

Paste the lines under `YOUR TURN`, replacing `result = None`. Save and click **Run Python File**, or run:

```powershell
.\.virtual-env-folder\Scripts\python.exe sessions\D2-S06\learner\compare_routes.py
```

**You should see:** two OK lines and `Saved outputs/D2-S06/unit_results.csv`. Keep your lines visible: you will copy
them into Power BI and KNIME.

### Step 2: Run the same step inside Power BI Desktop (12 minutes)

**Why:** here Python runs as one transformation step inside the report, and its result becomes a table in the model.

1. Open Power BI Desktop with a blank report. Choose **Home > Get data > Text/CSV**, paste the full path of the
   checkpoint CSV, and choose **Transform Data**. The Power Query editor opens.
2. Make sure `period` stays text: click the small type icon at the left of the `period` heading and choose **Text**.
   If asked, choose **Replace current**. `actual_amount` should show as a decimal number.
3. Choose **Transform > Run Python script**. Paste the lines between the two `COPY` markers in `compare_routes.py`
   (that is `import pandas as pd` and your own lines), then **OK**. Do not paste the lines that read the CSV file:
   Power BI already supplies the table as `dataset`.
4. Power BI now asks about **privacy levels**, because a script can combine sources. For this synthetic course file,
   choose **Public** and **Save**, unless your organisation tells you otherwise. Real data may need a different level.
5. Power BI lists the tables your script produced. Click **Table** next to `result`.
6. **You should see:** three rows with `period`, `entity` and `operating_result`, matching Step 1. Then choose
   **Home > Close & Apply**.
7. In the report, add a **Table** visual with `entity` and `operating_result`, and check the three amounts again.

If Power BI reports a Python error or cannot find Python, see the table at the end.

### Step 3: Run the same step inside KNIME (12 minutes)

**Why:** here Python runs as one node in a visual workflow, between a reader and a writer.

1. In KNIME Analytics Platform, create a new empty workflow. From the **Node repository**, drag in **CSV Reader**,
   **Python Script** and **CSV Writer**. Connect them in that order by dragging from each output port (the small
   triangle on the right of a node) to the next node's input port.
2. Double-click **CSV Reader**, browse to (or paste the full path of) the checkpoint CSV, check the preview shows nine
   rows, and click **OK**. Right-click the node and choose **Execute**.
3. Double-click **Python Script**. Replace the example code with these lines, putting **your lines from Step 1** where
   shown:

   ```python
   import knime.scripting.io as knio          # KNIME's link between the workflow and Python
   import pandas as pd
   dataset = knio.input_tables[0].to_pandas()  # the table arriving from CSV Reader

   # your lines from Step 1 go here, creating `result`

   knio.output_tables[0] = knio.Table.from_pandas(result)   # send result to the next node
   ```

   Click **OK**, then right-click the node and choose **Execute**. Right-click it again and open its output table.
   **You should see:** three rows with the same three figures you got in Step 1.
4. Double-click **CSV Writer**. Set the output file to the full path of your course folder's
   `outputs\D2-S06\knime_unit_results.csv` (use **Copy Path** on the `outputs\D2-S06` folder, then add the file name),
   allow it to overwrite an existing file, click **OK**, and **Execute**. Step 1 created that folder; if it is not
   there, run `compare_routes.py` first.

### Step 4: Decide the route (8 minutes)

**Do:** read `route_comparison.md`, then right-click `outputs/D2-S06` in the VS Code Explorer, choose **New File**,
name it `route_decision.md`, and write under these headings:

```text
The three results I compared, and whether they matched:
Where Python ran in each route:
The colleague I have in mind, and what they need to do each month:
The route I recommend, and who would keep it working:
What I have not tested (for example scheduled refresh in the Power BI service):
```

If you want help weighing the routes, ask Copilot:

> My colleague needs [describe: view the monthly result / update it themselves / reuse it in a workflow]. Compare
> handing over a checked CSV file, a Python step inside Power BI Desktop, and a Python Script node in KNIME, in terms
> of who must install and maintain Python and what happens when the file moves. Do not assume automatic refresh or
> any service we have not tested.

## Check your result

All three routes should give the same figures: **N01 29,862.50 · N02 23,444.83 · N03 14,023.53**, for 2025-12.

## Done when

All three routes agree with those figures, and your note names a route, its owner and what remains untested.

## If something goes wrong

| What you see | What to do |
|---|---|
| VS Code: `PROBLEM: an operating result differs` | The lines must sum `actual_amount` per `period` and `entity` only |
| Power BI: no **Run Python script** option, or "Python is not installed" | Python scripting is not set up in Power BI. Tell the instructor; the setting is **File > Options and settings > Options > Python scripting** |
| Power BI: `No module named 'pandas'` | Power BI is using a Python without pandas. The instructor checks the Python scripting setting |
| Power BI: `period` shows as a date | Change its type to **Text** before **Run Python script**, then run the script step again |
| Power BI: `name 'dataset' is not defined` | You pasted the lines into the wrong place. They go in **Transform > Run Python script** |
| KNIME: `No module named 'knime'` in VS Code | The KNIME lines only work inside KNIME's Python Script node, not in VS Code |
| KNIME: the Python Script node shows a red cross | Open it, read the error at the bottom of the editor, and check `result` is created before the last line |
| KNIME or Power BI cannot find the CSV | Use **Copy Path** in VS Code: these applications need the full path, not the course-relative one |

**Start again:** in VS Code restore `compare_routes.py` from the course download. Close Power BI without saving and
create a new KNIME workflow. The source data never changes.

**Optional extension:** in Power BI, add a **Python visual** with `entity`, `report_line` and `actual_amount`, and
use Copilot to write a bar chart of each unit's total from `dataset`. Notice that a Python visual returns a picture,
not a table other visuals can use.
