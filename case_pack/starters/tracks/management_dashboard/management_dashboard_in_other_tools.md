# Management dashboard in Power BI and KNIME

You have built the checked table in Python. This track is the one where the finished product usually belongs
somewhere else, so this page covers step 5 as well as the comparison. The job itself is in `README.md`.

## Fit

| Power BI | KNIME |
|---|---|
| **The native answer.** This is the tool's actual purpose, and the only track here where another tool beats Python at the deliverable | **Preparation, not the reporting surface.** It would do steps 1 to 4 well and steps 5 poorly |

This is the clearest "why this tool" answer of the six tracks, and it is worth noticing that the answer is not
Python. Python made the file. Something else should show it.

## The one thing each does differently in kind

**Power BI: the reader asks their own questions.** Your chart answers one question and stops. A report with a unit
slicer answers "and what about N02 on its own?" without you being in the room. That is not a nicer chart, it is a
different relationship with the reader, and it is the reason this deliverable belongs in a reporting tool. It is
also why step 2 matters so much: once a reader can slice, they will find any figure that does not add up.

**KNIME: it would rather hand you a file than a page.** You can build a view, but the workflow's natural output is
a clean table for something else to display. Which is exactly what the Python script already did, so KNIME would
be replacing a script with a picture of a script and gaining little here. That is a legitimate finding: the tool
is good, and this is not its job.

## Step 5 in Excel or Power BI

Both read the file you made. Neither should recompute anything in it.

**Excel:** **Data > From Text/CSV**, choose `dashboard_units.csv`, **Load**. Insert a bar chart on `variance_eur`
by `unit`. Enough for three units, and everyone can open it.

**Power BI Desktop:** **Home > Get data > Text/CSV**, choose the same file, **Load**. Then a **Clustered bar chart**
with `unit` on the axis and `variance_eur` as the value; conditional formatting on the bar colour by whether the
value is negative; a **Card** for total variance; a **Slicer** on `unit`.

**Check one figure on the screen against the file before you show it to anybody.** N02 should read −1,105.17. This
is the step people skip, and it is the one that catches a mis-set filter or an accidental aggregation.

## The same steps, where they differ

| Step | In Python you wrote | Power BI | KNIME |
|---|---|---|---|
| 2 Prove the files agree | A groupby, a comparison and `raise SystemExit` | A query grouping the lines and a card that must read 0. Power Query cannot stop a refresh, so the zero must be visible on the page | **GroupBy**, **Joiner**, then a **Rule Engine** that fails the workflow, which is closer to the Python behaviour |
| 3 Plain column names | `rename` | Rename in Power Query, not in the visual: a visual-level rename does not travel to the next report | **Column Rename** |
| 4 See it before publishing | A saved PNG | The canvas is the preview | **Bar Chart** node |
| 5 The report | Not attempted | The deliverable | Possible, but not what it is for |

## What it would cost you

**Power BI.** You gain the interactive page and lose the ability to stop. Python refuses to save when the files
disagree; a refresh cannot refuse in the same way, so the reconciliation becomes a number on the page that
somebody must notice. Put it somewhere it cannot be missed, and say what it means in words rather than leaving a
bare 0. Sharing beyond your own machine needs a licence and somewhere to publish, and scheduled refresh needs the
source file where the service can reach it.

**KNIME.** It would do the checking well and the showing poorly. Choosing it here would mean building a workflow
whose last node writes the same CSV the script already writes.

**Python, which you have built.** It produced a checked file and a picture. It cannot answer a question the reader
thinks of afterwards, and that is the limit that matters for a management pack.

**The judgement this track is really asking for:** prepare in one tool, present in another, and be clear about
which did which. The failure mode to avoid is letting the reporting tool quietly recompute the figures, because
then you have two versions of the truth and no check between them.

## What this has not shown you

Nobody has run the Power BI or KNIME routes on the course machines. The menus and nodes above come from the
vendors' documentation, so treat them as an accurate description of what the tools do, not as tested instructions.
