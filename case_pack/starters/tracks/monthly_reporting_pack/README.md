# Monthly reporting pack

> Can this month's figures be released to management, and if so, what do they receive?

This is the whole month-end process in one track: read the delivery, run the checks, and only then decide whether
anyone may see a figure. A blocked month is a correct outcome, not a failure.

**You build this in Python.** The method is in `monthly_reporting_pack_python.md`, beside `worked_example.py`.
**After you have built it**, `monthly_reporting_pack_in_other_tools.md` explains why this is the one track whose
deliverable Power BI cannot produce, and what to do instead.

## What you produce

The control results and the exceptions, saved whatever the outcome; and either the released figures in the
management workbook, or a workbook that shows the checks and no figures at all.

## Data in

| Folder or file (paths start at the course folder) | What it is |
|---|---|
| `case_pack/data/clean/` | A month's exports, mapping, budget and the units' own totals |
| `input_manifest_<period>.json` inside it | The list of files that belong to that month |
| `case_pack/data/faulty/<fault>/` | The same shape, with one thing wrong, for the blocked case |
| `case_pack/data/clean/checkpoints/actuals_by_line_<period>.csv` | The correct answer, prepared separately, to check against |

The units' own totals do not come from the transaction files. That independence is what lets the checks catch an
incomplete delivery.

## Data out

| The information | Shape | Where |
|---|---|---|
| What the nine checks found | One row per check, plus the exception detail | Your project folder, always |
| The figures, if they may be released | Nine reporting lines | Beside it, only when not blocked |
| The management pack | A workbook built from the released template | Beside it, marked blocked when it is |

## The steps

1. Start with an empty output folder, so no earlier run's figures sit beside this one.
2. Read the month the manifest lists.
3. Run the nine checks, and save their results whatever they say.
4. Only if the month is not blocked, calculate the figures and save them.
5. Produce the pack, showing no figures when blocked.
6. Compare the figures with the month's checkpoint.

## Ask Copilot for

| Step | What to ask for |
|---|---|
| 4 | A condition that tests "not blocked" rather than "is ready", because a third decision exists |
| 5 | The pack call, with the figures left out when the month is blocked |
| 6 | A comparison of two tables of figures within a tolerance, reporting how many of nine match |

## It is right when

**For the clean January delivery**, all nine checks pass, the release decision is `ready`, and:

```text
Check against the checkpoint: 9 of 9 figures match within EUR 0.01
```

**For a faulty delivery**, the control summary and the exceptions are still saved, no figures file is written, and
the workbook is marked blocked and shows no amounts.

The order is the thing being tested: the checks decide, and the figures follow. Never the other way round.

## Break it on purpose

Move the figure calculation above the checks and run a faulty delivery. The figures are produced, saved, and sit
in the folder looking exactly like released ones. Nothing errors. This is how wrong numbers reach management, and
it is why step 3 comes before step 4.

## Ideas for your change

- Run a different month by changing one setting, and say which files change.
- Run a faulty delivery and write the handover for a blocked month, which is the harder note to write.
- Add one sentence per failed check to the pack, so the reader does not have to interpret a code.

## Your finished project must show

- Both outcomes: a released month and a blocked one, each with its evidence.
- **Evidence of a check**: nine of nine against the checkpoint, and a blocked month that produced no figures.
- **Why this tool**, having built it. This track is the one where Python is hardest to replace.
- **A handover note** using the headings in `case_pack/starters/handover_note_template.md`.

Use your own data only if your organisation has approved it and it is available. Never change the files in
`case_pack`: save everything under `outputs/projects/`.
