# D1-S05: Python in Excel
45 minutes. Northbridge is fictional; amounts are EUR, costs stored negative.

**Business task:** use Python inside a workbook for one checked analysis and one chart, and decide
when an ordinary workbook feature would have been enough.

**Starting file:** `sessions/D1-S05/learner/northbridge_slice.xlsx` (keep it unchanged).
**Code to enter:** `sessions/D1-S05/learner/workbook_python.txt`.
**Your files:** `outputs/D1-S05/`.

## Before you start (what Python in Excel is)
- Code runs in a Microsoft cloud container, not on your machine.
- It reads workbook data only through `xl()`. It cannot open local files or the internet.
- Results live in cells created with `=PY(...)`.
- Included with Microsoft 365 Business and Enterprise plans on Windows, Mac and Excel for the web. It needs an internet
  connection. If a cell shows `#BLOCKED!`, the feature is off or your Office is activated in shared-computer mode.
  Your organisation may still have to enable it. If you cannot insert a Python cell, tell the instructor.

## 1. Make a working copy and inspect the data (3 min)
Open the starting file and use **File → Save As**: browse to the course folder's `outputs` folder, create a new
folder called `D1-S05`, and save the copy there as `northbridge_exercise.xlsx`. The **Inputs** sheet holds the table
**NorthbridgeLines**, which has nine rows: three units (N01–N03) × revenue / direct_cost / overhead.

**Predict:** what is each unit's operating result (the sum of its three signed lines)?

## 2. First Python cell: the analysis (7 min)
1. On a new sheet, select cell **A1**. Then choose **Formulas → Insert Python**, or type `=PY(`.
2. Enter the first block from `workbook_python.txt`:
   ```python
   lines = xl("NorthbridgeLines[#All]", headers=True)
   unit_result = lines.groupby("entity", as_index=False)["actual_amount"].sum()
   unit_result = unit_result.rename(columns={"actual_amount": "operating_result"})
   unit_result
   ```
3. Press **Ctrl+Enter**.
4. Change the output type to **Excel values**, using the formula-bar output menu or right-click → **Python Output**.
   The result fills the cells below and to the right (Excel calls this "spilling").

**Check:** N01 **29,862.50**, N02 **23,444.83**, N03 **14,023.53**. These match this morning's result.

## 3. Second Python cell: the chart (5 min)
Select a cell **below** the first result, for example **A6**, and enter the second block (the bar chart).
Press **Ctrl+Enter**. The cell shows a **card icon**: the chart is an image object. Click the card to preview it, or right-click the cell → **Display Plot over Cells** for a large chart you can move and resize.

If you get a `NameError`, your cell is probably above or to the left of the first cell. Python cells
calculate left to right, then top to bottom.

*AI route:* you can ask Microsoft 365 Copilot Chat to write this code from a short specification and paste it into
the Python cells. Read the code it writes and apply the same check.

## 4. Change an input and check (7 min)
**Predict** what happens when you add EUR 100 to N01 revenue (68,197.95 → 68,297.95).
Make the change and wait for the Python cells to recalculate.

**Check:** N01 = **29,962.50**, the N02 and N03 results are unchanged, and the chart bar moves.
Restore 68,197.95 by copying it from the untouched starting file. Then save, close and reopen your copy,
and confirm the results are still there.

## 5. Discuss: was Python needed? (3 min)
For this simple sum, a PivotTable or `SUMIFS` would be enough. Python in Excel is worth using when
the analysis needs pandas, statistics or specialised charts, but the data and the audience stay in
Excel. Use local Python in VS Code when the job needs several files, repeated runs, controls, or a
formatted output file.

## What to keep
Your saved `northbridge_exercise.xlsx` with both Python cells. Be ready to explain why the code needs no file path.

## If you have no Python in Excel access
Tell the instructor the exact failure, for example the Insert Python button is missing or a cell shows `#BLOCKED!`.
Work with someone who has access. The instructor can show the same numbers with local Python; note that you did
not run Python in Excel yourself.

## Optional extension
Try a different chart of the same checked table, for example a horizontal bar or a sorted chart,
without changing the numbers.
