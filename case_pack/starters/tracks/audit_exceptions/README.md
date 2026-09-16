# Audit exceptions

> Across several monthly deliveries, which ones may be released, and what exactly must each unit correct?

Six deliveries have arrived. One is clean. The others each carry a single, different fault. Your job is to run the
same checks over all of them and produce one page a reviewer can act on, without opening six folders.

**You build this in Python.** The method is in `audit_exceptions_python.md`, beside `worked_example.py`.
**After you have built it**, `audit_exceptions_in_other_tools.md` shows what the same job looks like in Power BI
and KNIME. Python suits this track because the checks already exist and the job is to run them many times.

## What you produce

One summary row per delivery saying whether it may be released and which checks did not pass, and one combined
list of every exception found, each labelled with the delivery it came from.

## Data in

| Folder (paths start at the course folder) | What it is |
|---|---|
| `case_pack/data/clean/` | December's correct delivery |
| `case_pack/data/faulty/F01_missing_source/` | A promised file never arrived |
| `case_pack/data/faulty/F02_duplicate_record/` | One transaction was delivered twice |
| `case_pack/data/faulty/F04_unmapped_account/` | An account code is missing from the mapping |
| `case_pack/data/faulty/F07_large_genuine_movement/` | A big but genuine month-on-month movement |
| `case_pack/data/faulty/F08_wrong_currency/` | A row is not in EUR |

All six are December 2025. Each folder holds a month's transactions, the mapping, the budget and the units' own
totals. The nine checks are supplied; you do not write them.

## Data out

| The information | Shape | Where |
|---|---|---|
| Whether each delivery may be released | One row per delivery, with the checks that did not pass and a count | Your project folder |
| Every exception, traceable to its delivery | One row per exception, with a delivery column | Beside it |
| What to tell the units | A short note naming the first case to chase | Beside it |

## The steps

1. List the deliveries to test, each with its reporting period.
2. For each one: read it, run the nine checks, and keep the release decision.
3. Record one summary row per delivery.
4. Collect every exception, labelled with the delivery it came from.
5. Confirm the clean delivery is released and no faulty one is released as ready.
6. Decide which case to chase first, and say why.

## Ask Copilot for

| Step | What to ask for |
|---|---|
| 2 | A loop over a dictionary of folder and period, calling two supplied functions and keeping their results |
| 3 | A row built from the results, with the failing check names joined into one readable cell |
| 4 | A way to add a column naming the source before combining several tables into one |
| 5 | A check that reads the release decisions and states plainly whether anything faulty slipped through |

## It is right when

| Delivery | Release | Checks not passing | Exceptions |
|---|---|---|---:|
| clean | `ready` | none | 0 |
| F01_missing_source | `blocked` | C01 fail, C02 not_run, C08 not_run, C09 not_run | 1 |
| F02_duplicate_record | `blocked` | C02 fail, C03 fail, C08 fail, C09 not_run | 4 |
| F04_unmapped_account | `blocked` | C05 fail, C09 not_run | 1 |
| F07_large_genuine_movement | `ready_with_warnings` | C09 warning | 1 |
| F08_wrong_currency | `blocked` | C07 fail, C09 not_run | 1 |

**8 exception rows in total.** F07 is the one to understand: a warning is not a failure, and it is released.

## Break it on purpose

Combine the exceptions without adding the delivery column. The count is unchanged and nothing errors, but nobody
can tell which unit to contact. An exception you cannot trace is not an exception, it is a rumour.

## Ideas for your change

- Add another faulty folder from `case_pack/data/faulty/` and predict its result before you run it.
- Group the exceptions by unit instead of by delivery, so one unit's message covers everything.
- Sort the summary so the worst delivery is first, and say what "worst" means.

## Your finished project must show

- The summary and the exception list, with every exception traceable to its delivery.
- **Evidence of a check**: the clean delivery released, no faulty delivery released as ready.
- **Why this tool**, having built it.
- **A handover note** using the headings in `case_pack/starters/handover_note_template.md`.

Use your own data only if your organisation has approved it and it is available. Never change the files in
`case_pack`: save everything under `outputs/projects/`.
