# Multi-file reconciliation in Python

The job is in `README.md`. This is how to build it. Read that first, then work through these steps.

**Tool:** a Python script in VS Code, with Microsoft 365 Copilot Chat for the code.
**You will produce:** `reconciliation.csv` and `reconciliation_note.md` in your own project folder.

## Start here

1. In the VS Code Explorer, right-click `outputs` and choose **New Folder**. Name it `projects` if it is not there
   already. Right-click `outputs/projects`, **New Folder**, and name it after your project, for example
   `n01_reconciliation`.
2. Right-click `worked_example.py` in this folder, choose **Copy**, then right-click your new folder and choose
   **Paste**.
3. Open your copy and click **Run Python File** (the triangle at the top right).

**You should see** a table of eight rows, then the totals. The eight is a coincidence worth untangling: our
file has eight transactions but only **seven** of them are posted, and the result has eight rows because those
seven are joined by one item that exists only in the settlement.

```text
Our posted total: 720.00   Their total: 295.02
Check: 720.00 - 500.00 missing + 75.00 extra + 0.02 differences = 295.02, their total 295.02
```

and a line starting `Saving into:` with the full path of your own folder. If it saved somewhere else, you ran the
original rather than your copy.

That is the finished result. The rest of this page explains how it gets there, so you can change it.

## Step 1: read both lists

The two settings near the top name the files:

```python
OUR_FILE = "case_pack/data/clean/tiny/transactions_2025-12_N01.csv"
THEIR_FILE = "case_pack/starters/tracks/multi_file_reconciliation/settlement_extract_2025-12.csv"
```

Both are read with `dtype=str`, so every column arrives as text. That is deliberate: `transaction_id` and
`entity` must stay text, and reading everything as text means nothing is converted by accident.

## Step 2: keep our posted rows, and convert the amounts

Our file has eight rows; one of them, `T008`, is `cancelled` and must not count. The line that does this is:

```python
ours = ours[ours["status"] == "posted"].copy()
ours["our_amount"] = pd.to_numeric(ours["amount"])
```

**Why the conversion is separate:** the amounts were read as text, and text cannot be added. Convert **after**
filtering, so a bad value in a row you do not need cannot stop the run.

The settlement extract has no status column. Every row in it has been settled.

## Step 3: stop if either list repeats a transaction

**Why:** if `T004` appeared twice on one side, a match would be ambiguous and every total after it would be wrong.
A check that stops is better than a note nobody reads.

**Ask Copilot:**

> I have two pandas DataFrames, `ours` and `theirs`. Write a short loop that checks each one for duplicate
> combinations of the columns period, entity and transaction_id, and stops the script with a clear message naming
> which file is at fault. Use `raise SystemExit`. Do not delete any rows.

**Read it before you run it.** It must not drop rows. `drop_duplicates` is the wrong answer here: deciding which
copy is genuine belongs to whoever sent the file.

## Step 4: match the two lists (the step that matters)

**Why:** this is where the exercise is won or lost. An ordinary join keeps only the transactions found in both
lists, which silently discards exactly the two problems you are looking for.

**Ask Copilot:**

> I have two pandas DataFrames with the columns period, entity and transaction_id in common. `ours` also has
> our_amount, `theirs` also has their_amount. Merge them so that rows appearing in only one of the two are kept,
> and add a column saying which side each row came from. Then add a column `difference` = their_amount minus
> our_amount, rounded to 2 decimals.

**Read it before you paste it.** Check `how="outer"`. If you see `how="inner"`, or no `how` at all, it is wrong:
say so in the chat and ask again. The supplied answer is:

```python
both = ours[KEY + ["our_amount"]].merge(theirs[KEY + ["their_amount"]], on=KEY, how="outer", indicator=True)
```

**You should see** 8 rows after this step: 5 in both, 1 only on our side, 1 only on theirs, and 1 in both with a
difference.

## Step 5: label every item

Four labels, from two facts: which side the row was on, and how big the difference is.

| Which side | Difference | Label |
|---|---|---|
| Ours only | none to compute | missing from settlement |
| Theirs only | none to compute | extra in settlement |
| Both | at most EUR 0.01 | matched |
| Both | more than EUR 0.01 | amount difference |

`TOLERANCE_EUR = 0.01` is a setting at the top. It is a teaching assumption, not company policy.

## Step 6: prove the totals reconcile

**Why:** a list of statuses is not evidence. The evidence is that the differences you found add up to the gap
between the two totals, with nothing left over.

**You should see:**

```text
Our posted total: 720.00   Their total: 295.02
Check: 720.00 - 500.00 missing + 75.00 extra + 0.02 differences = 295.02, their total 295.02
```

Check it on a calculator once, by hand. If the last two figures differ, an item has been counted twice or not at
all, and the status labels are wrong somewhere.

## Check your result

| Item | Status | Our amount | Their amount |
|---|---|---:|---:|
| T001, T003, T005, T006, T007 | matched | | |
| T002 | missing from settlement | 500.00 | |
| T004 | amount difference | −400.00 | −399.98 |
| T990901 | extra in settlement | | 75.00 |

Five matched, one missing, one extra, one differing by EUR 0.02. Totals 720.00 and 295.02, compare within EUR 0.01.

## Write the note

Right-click your project folder, choose **New File**, name it `reconciliation_note.md`, and write under these
headings:

```text
Items a colleague must chase, and who:
Items that are ours to correct:
The one item I checked by hand, and what I got:
What I would do if the two lists disagreed by much more:
```

`T002` and `T990901` are the ones somebody has to explain. `T004` at two cents is a rounding or fee difference and
is probably yours to write off, but say so rather than leaving it silent.

## Done when

The run prints the reconciliation and the check line, every item from both lists has a status, you have checked one
figure by hand, and your note names who chases what.

## If something goes wrong

| What you see | What to do |
|---|---|
| `KeyError: 'amount'` | A column name is not what you assumed. Add `print(ours.columns)` above the failing line |
| `TypeError` when adding amounts | The amount is still text. `pd.to_numeric` has not run, or ran before the filter |
| Only 5 or 6 rows in the result | The join kept only matching rows. Check `how="outer"` |
| `STOPPED: ... lists a transaction twice` | The safeguard worked. Look at the file it names before going further |
| The check line's two totals differ | An item is counted twice or missed. Print the rows for each status and add them up |
| `FileNotFoundError` | Run from the course folder, or use the Run Python File button |

**Start again:** delete your copy and paste `worked_example.py` again. The two source files never change.
