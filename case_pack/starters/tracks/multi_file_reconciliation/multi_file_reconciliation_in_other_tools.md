# Multi-file reconciliation in Power BI and KNIME

You have built this in Python. This is what the same job looks like elsewhere, and what it would cost you. The job
itself is in `README.md`.

## Fit

| Power BI | KNIME |
|---|---|
| **Good fit.** Power Query was built for exactly this: matching two tables and keeping what does not match | **Good fit**, and the easiest of the three to explain to somebody who does not read code |

Either would do this job well. The question is not capability, it is who maintains it afterwards.

## The one thing each does differently in kind

**Power BI: the merge is a step you can reopen.** In Python, `how="outer"` is four characters inside a line, and
the only way to see what it did is to run the script and look. In Power Query the merge is a named step in a list
down the right-hand side. You can click it, change **Full Outer** to **Inner** in a dropdown, watch the row count
fall from 8 to 5, and change it back. The thing that silently loses your two most important rows becomes a
dropdown with a label on it.

**KNIME: the unmatched rows come out on their own wires.** Switch on **Output unmatched rows to separate ports** in
the Joiner and the node grows three outputs: *Join result*, *Left unmatched rows*, *Right unmatched rows*. Two of
your four statuses are then simply which wire a row left by. You do not classify them; you look at where they went.
The remaining split, matched against amount difference, is still yours to make with a Rule Engine on the tolerance.

That is the honest version. It is not "KNIME gives you all four statuses free". It gives you two, visibly, and the
separate ports are an option you must switch on: by default everything leaves by one port, as in pandas.

## The same steps, where they differ

Steps 1 and 2 are the same idea everywhere: read two files, keep the posted rows, make the amounts numeric. These
are the steps that differ.

| Step | In Python you wrote | Power BI | KNIME |
|---|---|---|---|
| 3 Stop on duplicates | A loop and `raise SystemExit` | Group by the key and check every count is 1, or use **Keep Duplicates** to show them. Power Query has no natural "stop the refresh" | **Duplicate Row Filter** to see them, or a **Rule Engine** that fails the workflow |
| 4 Match both lists | `merge(..., how="outer", indicator=True)` | **Home > Merge Queries**, join kind **Full Outer**, then expand the second table's columns | **Joiner**, with **Output unmatched rows to separate ports** switched on |
| 5 Label the items | A function over the merge indicator and the difference | **Add Column > Conditional Column**, testing whether each amount column is null and whether the difference exceeds the tolerance | **Rule Engine** on the same two facts, or **Concatenate** the three ports back together with a label each |
| 6 Prove the totals | A printed sentence | Card visuals for the two totals and a matrix of counts by status | **GroupBy** and a **Table View** |

## What it would cost you

**Power BI.** The result is a report, not a file. If a colleague needs `reconciliation.csv` to send to the other
system's owner, somebody has to export it, and an export from a visual can reflect that visual's filters and
grouping rather than the underlying table. Check the exported row count against the source before sending it.
Refreshing on a schedule needs the files in a place the service can reach, and a gateway if they stay on a
desktop. Against that: anybody in the team who already opens Power BI can maintain it without reading code.

**KNIME.** The workflow is a picture of the process, which is the best handover of the three: a colleague can see
the shape before opening anything. It writes a CSV directly, so the deliverable is the same as Python's. The costs
are that KNIME must be installed and kept current on every machine that runs it, and that a workflow is harder to
put under version control or to diff than a script.

**Python, which you have already built.** Smallest to hand over as a file, hardest to hand over as a process: it
needs somebody who will read it.

**The judgement this track is really asking for:** all three produce the same eight rows. Choose on who reruns it
next month and what they can already use, then say so in your handover note.

## What this has not shown you

Nobody has run the Power BI or KNIME routes on the course machines. The menus and nodes above come from the
vendors' documentation, so treat them as an accurate description of what the tools do, not as tested instructions.
Reading this is not the same as having built it: if you want to claim one of these routes is better for your team,
build the smallest version of it first.
