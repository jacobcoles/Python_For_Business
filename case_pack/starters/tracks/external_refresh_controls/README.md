# External refresh with controls

> We want published inflation figures beside our own. How current are they, and what do we say when the source is
> down?

External context makes a management pack more useful and more dangerous. The danger is not a wrong number, it is
an old number presented as today's. Your job is to fetch it, check it is what you asked for, record where and when
it came from, and report its age honestly.

**You build this in Python.** The method is in `external_refresh_controls_python.md`, beside `worked_example.py`.
**After you have built it**, `external_refresh_controls_in_other_tools.md` shows the same job elsewhere, and this
is the track where KNIME has a real advantage.

## What you produce

The context table, the response exactly as it was received, a source record saying where and when it came from,
and a status that is honest about its age.

## Data in

| Source | What it is |
|---|---|
| The OECD public statistics API | Consumer price inflation, one series per area, monthly |
| `case_pack/data/external/` | A saved response from that API, its metadata, and fixtures for the failure cases |

Two areas (Sweden and the euro area) and thirteen months, so 26 rows. The settings choose whether to send a real
request or reuse the saved response.

## Data out

| The information | Shape | Where |
|---|---|---|
| The context table | One row per area and month, with the measure named | Your project folder |
| The response as received | Untouched, as evidence | Beside it |
| Where and when it came from | A small record, including the retrieval time | Beside it |
| How fresh it is | One status: live, cached, stale or unavailable | Printed, and in your note |

## The steps

1. Build the request: which areas, which months, which measure.
2. Send it, or reuse the saved response.
3. Check the response is what you asked for before using any of it.
4. Save the table, the response and the source record together.
5. Work out the age from the original retrieval time, and report the status.
6. Say what you would do when the source is unavailable.

## Ask Copilot for

| Step | What to ask for |
|---|---|
| 3 | Checks that the row count, the areas and the measure are what was requested, that stop rather than warn |
| 5 | An age in days between a stored timestamp and now, and a rule turning it into a status |
| 6 | Wording for a note that reports an unavailable source without implying the old figures are current |

## It is right when

The checks pass:

```text
OK: 26 rows = 2 area(s) x 13 month(s).
OK: one measure only: HICP, change over one year, percent (checked for every row).
OK: no area and month appears twice.
```

For **December 2025**, the euro area is **2.0** and Sweden is **2.1**, a gap of **0.1 percentage points**, Sweden
higher. Compare within 0.1 points: the source publishes to one decimal and revises.

The status line names the age and the limit, and the age is measured from when the data was **downloaded**, never
from when you ran the script.

## Break it on purpose

Set the age limit to 1 day and run it again. The same saved data is now `stale`. Nothing about the figures changed;
only the claim you are entitled to make about them did. That is the whole lesson of this track.

## A warning about percentages

2.0 against 2.1 is a gap of **0.1 percentage points**, not "0.1 per cent". They are different claims and the second
one is wrong. Use the word "points" in anything you hand over.

## Ideas for your change

- Change the months or add an area, and check the row count changes as you predicted.
- Rehearse a failure properly. `MODE` offers only `live` and `offline`, so this one needs a small change to the
  script: make it read one of the files in `case_pack/data/external/fixtures/` in place of the saved response, then
  confirm that the checks stop it and **nothing is saved**. The fixtures cover an empty result, a 404, a 500, a
  malformed body and a timeout.
- Document a different approved source with the same three checks.

## Your finished project must show

- The table, the response, the source record and a status.
- **Evidence of a check**: the three checks passed, and you tried a failure case and nothing was saved.
- **Why this tool**, having built it.
- **A handover note** using the headings in `case_pack/starters/handover_note_template.md`, saying plainly what the
  status would be if nobody reran it for two months.

Use your own data only if your organisation has approved it and it is available. Never change the files in
`case_pack`: save everything under `outputs/projects/`.
