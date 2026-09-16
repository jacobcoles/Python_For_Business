# Audit exceptions in Power BI and KNIME

You have built this in Python. This is what the same job looks like elsewhere, and what it would cost you. The job
itself is in `README.md`.

## Fit

| Power BI | KNIME |
|---|---|
| **Workable, once you put the boundary in the right place.** It presents control results well. It should not be made to run the nine checks | **Good fit**, and the clearest demonstration of the one thing KNIME does better than a script |

## The one thing each does differently in kind

**KNIME: repetition becomes a shape, not a construct.** In Python you wrote a `for` loop and had to hold in your
head that the body runs six times. In KNIME you build the body **once**, as ordinary nodes, and put a loop start
before it and a loop end after it. The canvas shows one reader and one set of checks; the loop nodes say "do this
for each row of the list". Nothing is repeated on screen, and nothing has to be imagined. Use
**Table Row To Variable Loop Start** to drive it from the list of deliveries, and **Loop End (2 Ports)** to collect
both streams at once, the summary row on one port and that delivery's exceptions on the other. The plain
**Loop End** collects one table per pass, which is not enough here.

**Power BI: the summary is a matrix, and the detail is one click away.** Your CSV has one row per delivery with the
failing checks squashed into a text cell, because a table cell cannot hold a list. Power BI does not have that
problem: a matrix with deliveries down the side and the nine checks across the top shows every result at once,
coloured by status, and clicking a cell can drill into the exceptions behind it. For a reviewer scanning six
deliveries, that is a genuinely better artefact than the CSV.

**But it must not run the checks.** The nine controls are a business asset with an agreed definition. Rebuilding
them as Power Query steps would give you a second implementation that can drift from the first, and nobody would
know which was right. Run them where they are defined and import `delivery_summary.csv` and `all_exceptions.csv`.
Say so on the report page, so no reader believes Power BI performed the checks.

## The same steps, where they differ

Step 1 is a list of folders in every tool. Step 6 is a person deciding. These are the steps that differ.

| Step | In Python you wrote | Power BI | KNIME |
|---|---|---|---|
| 2 Run the checks | A loop calling two supplied functions | **Not here.** Run them upstream; import the two result files | A **Python Script** node calling the same two supplied functions, inside the loop |
| 3 Summary row | A dictionary appended per pass | A query grouping the imported results by delivery | First port of **Loop End (2 Ports)** |
| 4 Combine exceptions with their source | `assign(delivery=name)` before concatenating | Already a column in the imported file | Second port of the same **Loop End (2 Ports)**; the delivery arrives as a flow variable |
| 5 Confirm nothing slipped through | A printed sentence | A card showing the count of faulty deliveries not blocked, which must read 0 | A **Rule Engine** that fails the workflow if any faulty delivery is `ready` |

## What it would cost you

**Power BI.** You gain a reviewer's page that is genuinely better than a CSV, and lose the ability to say the
report did the checking. The report is only as current as the last time somebody ran the checks and refreshed it,
so the page must show when the checks ran, not when the report refreshed. Those are two different timestamps and
confusing them is the failure mode here.

**KNIME.** Adding a seventh delivery is a row in a table, not a code change, and the workflow picture explains
itself to an auditor better than either alternative. The costs are the install, and that the Python Script node
inside the loop still needs the supplied helpers on the machine: you have not removed Python, you have wrapped it.

**Python, which you have built.** The loop is four lines and runs anywhere the course environment runs. It
produces files rather than a view, which is the right output if the next step is emailing a unit.

**The judgement this track is really asking for:** the checks belong in one place whatever you choose. The tool
question is only about how the results are shown, and who has to open what to see them.

## What this has not shown you

Nobody has run the Power BI or KNIME routes on the course machines. The nodes and menus above come from the
vendors' documentation, so treat them as an accurate description of what the tools do, not as tested instructions.
