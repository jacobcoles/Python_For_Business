# D1-S04: The working method end to end, with several finance files in VS Code
90 minutes. Northbridge is fictional; amounts are EUR.

**Question:** what did each Northbridge unit earn in December, and where did every number come from?
**Start:** `sessions/D1-S04/learner/staged_notebook.ipynb`. The notebook has its own numbered sections; this guide
says which notebook section to use at each step.
**Output:** `outputs/D1-S04/actuals_by_line.csv`, with 9 rows (3 units × revenue / direct_cost / overhead).

Open the course folder in VS Code and select the course `.virtual-env-folder` as the notebook kernel (see D1-S02).

## 1. Understand the data (slides 1–3, 10 min)
- `case_pack/data/clean/transactions/` holds **four months** of files. `case_pack/data/clean/input_manifest_2025-12.json`
  (in the `clean` folder) names the three December files. Load only those; loading every file in the folder would inflate every total.
- One row is one transaction. `T000001` exists in every unit, so the key is
  **entity + period + transaction_id**.
- `account_code` is **text**. Read as a number, 0400 becomes 400 and no longer matches the mapping.
- Revenue is positive and costs are negative. Only `posted` rows count. A positive amount on a cost line
  is a reversal: keep its sign.

## 2. Load and inspect (slide 4, 15 min)
Run the supplied loading cell in **notebook section 1**. Note the shape (362 rows, shown first), the types (all text on purpose) and
missing values. `source_file` and `source_row` record where each row came from. `source_row` counts **data rows**
(the header is not counted), so in an editor the line number is `source_row + 1`.

## 3. Predict (slide 5)
In **notebook section 2**, enter your predictions **before** any transformation: the number of posted rows, the rows
after the join, and N01's operating result. The cell also shows `source_controls.csv`, each unit's own totals.

## 4. Watch the demonstration (slides 6–7, 15 min)
The instructor builds filter → map → aggregate and explains each safeguard:
- `how="left"` with `indicator=True` keeps unmatched rows visible.
- `validate="many_to_one"` stops the join if the mapping has a duplicated code.

## 5. Build your own (slides 8–9, 30 min)
1. Write a short specification with the D1-S03 template. It should ask for: posted EUR rows only; a
   left join on text `account_code` with `validate="many_to_one"` and `indicator=True`; signed `amount`
   totalled by period/entity/report_line into `actual_amount`; rows ordered revenue, direct_cost,
   overhead within each unit. The loader reads everything as text, so ask for `amount` to be **converted to a number
   after filtering** (never with `abs()`).
2. Ask Copilot. Paste the code into the YOUR TURN cell in **notebook section 3** and **read it before running**.
   Look for file writes, an inner join, or `abs()`.
3. Run the **spot checks** cell (**notebook section 4**). Every line should print `True`. A line comparing with your
   prediction prints `False` if either your code or your prediction is wrong; use the table below to see which:

| Check | Expect |
|---|---|
| Rows after filter | 354 |
| Rows after join | 354 (unchanged) |
| Sum of amount before vs after the join | Identical |
| `_merge` values | All `both` |
| N01 operating result | 29,862.50 |

## 6. Test a known fault (slide 10, 15 min)
**Predict** what `validate="many_to_one"` will do with
`case_pack/data/faulty/F03_duplicate_mapping/account_mapping.csv`. In that file, account `0500` appears twice.
In **notebook section 5**, rerun your join with it: you should get a `MergeError`. Then run the same join once more
without `validate=` to see what happens when nothing stops it.
The rows grow from 354 to 455 and the total drops from 67,330.86 to 26,318.19, with no error.
Restore the clean mapping and **rerun notebook section 3** so `joined` and `by_line` are rebuilt from it. Do **not** delete the duplicate yourself: the mapping owner decides which
row is right. The instructor then shows F04, an unmapped account, where `_merge == "left_only"` rows point to the source row.

## 7. Save, compare and explain (slides 11–12, 5 min)
Run the save-and-compare cell (**notebook section 6**). It writes your CSV and checks it against
`case_pack/data/clean/checkpoints/actuals_by_line_2025-12.csv`: all 9 keys must match, and every amount must
be within EUR 0.01. Then explain to your neighbour:
- how a duplicated reference row can change a plausible total;
- why `source_file` and `source_row` matter;
- why you keep the positive reversal instead of using `abs()`.

## What to keep
Keep the notebook with your predictions, code and check results, and your specification. Your code does not have
to match anyone else's; the checks must pass.

## Troubleshooting
| Symptom | Check first |
|---|---|
| `FileNotFoundError` | The course folder is open in VS Code and the notebook runs from it |
| `ModuleNotFoundError` / wrong results everywhere | The kernel picker shows the course `.virtual-env-folder` |
| `ValueError: You are trying to merge on int64 and object columns` | Your code re-read the CSV without `dtype=str`: use the `rows` table the notebook already loaded |
| Fewer than 354 rows after the join | An inner join dropped unmatched rows: use `how="left"` |
| Totals too small on cost lines | `abs()` or a sign flip was applied before summing |

**Reset:** see `RESET.md`. The input files are never changed.
**Not finished?** Later sessions use the supplied checkpoint file, so nothing depends on finishing this notebook.

## Optional extension
Repeat for January (`period = "2026-01"`, with its own manifest) and compare with
`checkpoints/actuals_by_line_2026-01.csv`.
