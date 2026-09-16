# External refresh with controls, in Power BI and KNIME

You have built this in Python. This is what the same job looks like elsewhere, and what it would cost you. The job
itself is in `README.md`.

## Fit

| Power BI | KNIME |
|---|---|
| **Workable, with one real compromise** that goes to the heart of this track | **Good fit**, and the best of the three at the part that matters: what happens when the source is down |

## The one thing each does differently in kind

**KNIME: the HTTP call is configuration, and failure is a visible path.** A **GET Request** node takes the URL and
the headers in a dialog. No library, no code. Better than that: the response status arrives as a **column**, so it
is data you can branch on with ordinary nodes, and **Try** and **Catch** nodes turn "the source is down" into a
second route drawn on the canvas, going to the saved copy and setting the status to unavailable. In Python that
behaviour is an exception handler somebody has to read to find. In KNIME it is a line on a diagram, and the
reviewer can see it without opening anything.

**Power BI: refresh is the whole model, and that is the problem here.** **Get data > Web** will fetch the series
happily. The difficulty is that this track is not really about fetching, it is about *age*, and Power BI's
refresh model works against you:

- a refresh **replaces** the data, so there is no natural "keep yesterday's copy and mark it stale";
- the retrieval time is therefore always "now", which is the one value this track says you must not use;
- if the source is down, the refresh fails and the report keeps showing the previous figures with no visible sign
  that anything went wrong. That is precisely the outcome the whole track exists to prevent.

**The compromise:** let Python or KNIME fetch, check and write `context.csv` and `source_record.json`, and have
Power BI read those two files. The retrieval time is then a real column from the record, the status is a measure
comparing it to today, and the report shows an honest age rather than the time of the last refresh. Say on the
page that Power BI displays this data and did not fetch it.

## The same steps, where they differ

| Step | In Python you wrote | Power BI | KNIME |
|---|---|---|---|
| 1 and 2 Request and send | `build_request` and `get_response` | **Get data > Web**, with the header set in the advanced options, or read the file another route wrote | **GET Request** node: URL and headers in a dialog, no library |
| 3 Check before using | Three checks that stop | Query steps that compare the row count and the measure; a card that must read as expected, because a refresh cannot stop | **Rule Engine** on the same three facts, failing the workflow |
| 4 Save with the record | Three files, or nothing | Not its job. Read the record that another route wrote | **CSV Writer** for the table and the record, after the checks pass |
| 5 Age and status | Age from `retrieved_at_utc` | A measure: days between the retrieval column and today. **Never `now()` alone**, which would always say zero | **Date&Time Difference** and a **Rule Engine** |
| 6 When it is down | The status becomes unavailable and nothing is saved | The refresh fails and the old data stays on screen, silently, unless you have built the status from a stored retrieval time | **Try** and **Catch** nodes: an explicit branch to the saved copy, with the status set accordingly |

## What it would cost you

**Power BI.** You gain a shared, always-available page and lose the ability to refuse to publish. Everything about
freshness has to be rebuilt as something visible on the page, because the tool has no way to stop. Done carefully
it is honest; done carelessly it is the most misleading of the three routes, because a stale report looks exactly
like a current one. Scheduled refresh also needs the source reachable from the service, and a gateway if the files
live on a desktop.

**KNIME.** The closest to what this track is teaching: checks that fail the run, a visible failure branch, and
files written only after the checks pass. The costs are the install, and that a workflow does not run itself
without a scheduler.

**Python, which you have built.** It refuses to save bad data, keeps the raw response as evidence, and computes
the age from the right timestamp. It has no audience: somebody must run it and pass the result on.

**The judgement this track is really asking for:** whichever tool you choose, the age must come from when the data
was **downloaded**, and the reader must see it. A tool that cannot show that honestly is the wrong tool for
external data, however good its charts are.

## What this has not shown you

Nobody has run the Power BI or KNIME routes on the course machines. The nodes and menus above come from the
vendors' documentation, so treat them as an accurate description of what the tools do, not as tested instructions.
In particular, no scheduled refresh, gateway or automatic caching behaviour has been tested here, so do not
promise a colleague a self-updating report on the strength of this page.
