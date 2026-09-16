# Multi-file reconciliation

> Do our transactions and the settlement extract agree, and where exactly do they not?

Two systems hold what should be the same December transactions for unit N01. They do not match. Your job is to say
exactly which items differ and in what way, and to prove that the differences explain the gap between the two
totals.

**You build this in Python.** The method is in `multi_file_reconciliation_python.md`, beside `worked_example.py`.
**After you have built it**, `multi_file_reconciliation_in_other_tools.md` shows what the same job looks like in
Power BI and KNIME, and what each would cost you. Python suits this track because the result is a file somebody
else checks, not a screen somebody watches.

## What you produce

One row per transaction, from **both** lists, each labelled with what is wrong with it, plus a short note saying
which differences a colleague must chase and which are ours to correct.

## Data in

| File (paths start at the course folder) | One row is | Columns that matter |
|---|---|---|
| `case_pack/data/clean/tiny/transactions_2025-12_N01.csv` | One of our transactions | `transaction_id`, `period`, `entity`, `amount`, `status` |
| `case_pack/starters/tracks/multi_file_reconciliation/settlement_extract_2025-12.csv` | One settled item from the other system | `transaction_id`, `period`, `entity`, `settlement_amount` |

Eight rows on our side, seven on theirs. `amount` and `settlement_amount` are signed: costs are negative.

## Data out

| The information | Shape | Where |
|---|---|---|
| Every item from both lists, with a status | One row per transaction, with both amounts and the difference | Your project folder |
| What you would do about it | A few sentences under headings | A note beside it |

## The steps

1. Read both lists.
2. Keep only our `posted` rows, and turn the amounts into numbers.
3. Stop if either list repeats a transaction, because matching would then be ambiguous.
4. Match the two lists on unit, month and transaction ID, keeping the rows that appear in only one of them.
5. Label every item: matched, missing from settlement, extra in settlement, or amount difference.
6. Prove the two totals reconcile.

## Ask Copilot for

| Step | What to ask for |
|---|---|
| 3 | A check that a combination of columns is unique, that stops the script rather than warning |
| 4 | A join that keeps rows found in only one of the two tables, and tells you which side each row came from |
| 5 | A rule that turns "which side was it on, and how big is the difference" into one of four plain labels |
| 6 | A sentence that adds the differences to one total and shows it equals the other |

## It is right when

Our posted total is **720.00** and theirs is **295.02**, and the four statuses account for the gap exactly:

**720.00 − 500.00 missing + 75.00 extra + 0.02 difference = 295.02**, compare within EUR 0.01.

Five items match, one is missing from the settlement, one is extra in it, and one differs by EUR 0.02.

## Break it on purpose

Change your join so it keeps only rows found in both lists. The totals still print, the script still runs, and the
two problems that matter most vanish without any warning. That is the failure this whole track exists to prevent.

## Ideas for your change

- Work at full-month scale. Note first that you cannot simply point `OUR_FILE` at
  `case_pack/data/clean/transactions/transactions_2025-12_N01.csv`: the settlement extract covers only the
  eight-row file's transactions, so none of the 117 posted rows would match and every one would be reported as
  missing. To do this properly, make your own settlement extract from that month's transactions, change a few
  amounts, drop one row and add one that does not exist, then reconcile against it. Two lists that genuinely
  overlap is the point.
- Change the tolerance and see which items change status.
- Report the totals by status, so the note leads with the money rather than the count.

## Your finished project must show

- The reconciliation, with every item from both lists accounted for.
- **Evidence of a check**: the totals reconcile, and you tried one faulty input.
- **Why this tool**: having built it, whether Python was the right choice here, or whether Excel, Power BI or KNIME
  would be more sustainable for whoever maintains it.
- **A handover note** with purpose, inputs, how to run it, what you checked and the known limits. Use the headings
  in `case_pack/starters/handover_note_template.md`.

Use your own data only if your organisation has approved it and it is available. Never change the files in
`case_pack`: save everything under `outputs/projects/`.
