# D2-S01: Why is this December figure wrong?

09:00 to 09:25, 25 minutes. **Tools: VS Code to open the files, and a calculator.** No code today: this session
recaps Day 1's checking habits on a real mistake.

**You will produce:** a short diagnosis, `outputs/D2-S01/diagnosis.md`.

## The situation

A colleague was asked for N02's December operating result before the monthly pack was ready. They did it in a
spreadsheet: each transaction's account code was looked up in the mapping table, and **rows whose code was not found
were left out**. They sent the manager **EUR 21,754.26**.

In D1-S08 a January delivery was blocked because an account code had no classification. This is a different month
and a different delivery, and you have not seen its figures. Your job: decide whether the manager can use EUR 21,754.26, find what went wrong, and say
which check would have caught it.

## Data you will read

All in `case_pack/data/faulty/F04_unmapped_account/` unless stated (paths start at the course folder).

| File | What it contains | What to look at |
|---|---|---|
| `sessions/D2-S01/learner/broken_result.csv` | The figure the manager received, and how it was produced | One row |
| `source_controls.csv` | Each unit's own totals, sent separately from the exports | The row for 2025-12, N02 |
| `account_mapping.csv` | The mapping this delivery came with | Which account codes it lists |
| `transactions/transactions_2025-12_N02.csv` | N02's December export: 119 transactions | The account code that is missing from the mapping |

## Rules for this task

- Operating result is the sum of a unit's posted EUR amounts: revenue positive, costs negative.
- Every posted transaction must count. A transaction whose account is not in the mapping is a question for finance,
  not a row to leave out.
- Do not change any source file.

## Steps

### Step 1: What was asked, and what is the unit's own figure? (5 minutes)

**Why:** a figure can only be checked against something independent of the calculation that produced it.

Open `source_controls.csv` and find 2025-12, N02. The last column, `expected_posted_amount`, is the unit's own
December total. Compare it with EUR 21,754.26. How big is the difference?

### Step 2: Find the rows that explain the difference (8 minutes)

**Why:** a difference is not a diagnosis until you can name the rows behind it.

1. Open `transactions/transactions_2025-12_N02.csv` **from the VS Code Explorer** (double-clicking a CSV in
   Windows opens Excel, which would strip the leading zero from a code such as `0400`).
2. Open `account_mapping.csv` beside it and note which account codes it lists.
3. Find the transactions whose account code is **not** in that list. Press **Ctrl+F** in the export and search for a
   code to count its rows; VS Code shows the number of matches.
4. Add the amounts of those rows with a calculator. Does your total equal the difference from Step 1?

### Step 3: Name the cause and the check (7 minutes)

Discuss with your neighbour, then write your diagnosis:

- **The join:** what happened to transactions whose account code had no match in the lookup? Why did the spreadsheet
  give no error?
- **The control:** which of the nine checks from D1-S06 would have stopped this figure, and what would it have
  reported?
  (The nine are listed in `case_pack/contracts/controls.md`.)
- **The repair:** what is the correct action, and what should the colleague have told the manager instead?

Create the file: in the Explorer, right-click the `outputs` folder, choose **New Folder**, name it `D2-S01`, then
right-click that folder, choose **New File**, and name it `diagnosis.md`. Write under these headings:

```text
Figure received, and the unit's own figure:
Transactions responsible (unit, account code, how many, total):
Why the lookup gave no error:
The check that would have caught it:
What I would tell the manager:
```

### Step 4: Two ways to run Python with Excel (5 minutes)

The instructor recaps the two routes from D1-S05. Be ready to answer: in which route does Python run **inside** the
workbook, and in which does a script on your computer **write** a workbook? Why does success with one say nothing
about the other?

## Check your result

After you have written your diagnosis:
- N02's own total is **EUR 23,444.83**. The difference is **EUR 1,690.57**.
- One transaction, `T000007`, uses account `0499`, which is missing from the mapping: **1,690.57**, a posted EUR
  revenue line.
- The lookup treated "not found" as "leave out", so the rows vanished silently: the same failure as an inner join.
- **C05 (unmapped accounts)** would have failed and blocked the release. Comparing with the unit's own total (C08)
  shows the gap immediately.
- The manager cannot use EUR 21,754.26. The right message is: "December's N02 figure is missing EUR 1,690.57 of
  posted revenue because account 0499 has no classification. Finance must classify it before the figure is used."

## Done when

Your diagnosis names the gap, the transaction and its amount, why no error appeared, the check that would have
stopped it, and a message the manager could act on.

## If something goes wrong

| What you see | What to do |
|---|---|
| The account codes look like `400` or `499` | The file was opened in Excel, which drops leading zeros. Open it from the VS Code Explorer instead |
| **Ctrl+F** finds nothing | Search inside the open file, not the Explorer. Include the commas, for example `,0499,` |
| Your total does not match the gap | Check that you added only the rows whose code is missing from the mapping, and that you kept the signs |

**Start again:** nothing is changed by this session. Reopen the three files and work through the steps again.

**Optional extension:** the same spreadsheet would have been right for December's N01 and N03. Explain why one
missing code in one unit is enough to stop the whole pack.
