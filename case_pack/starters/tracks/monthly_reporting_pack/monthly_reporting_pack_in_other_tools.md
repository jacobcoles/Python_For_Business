# Monthly reporting pack in Power BI and KNIME

You have built this in Python. This is the one track where the honest answer is that one of the other tools cannot
produce the deliverable at all, and saying so clearly is more useful than a workaround. The job is in `README.md`.

## Fit

| Power BI | KNIME |
|---|---|
| **Not the right tool for this deliverable.** It cannot fill the formatted management workbook. It can do something else worth doing, described below | **Workable, as a hybrid**: nodes for the process, one Python step for the workbook |

## Why Power BI cannot do this one

The deliverable is a **formatted Excel workbook**, built from a master template with five sheets, protected
layout and a cross-check formula. Power BI produces reports and models; it does not write into somebody else's
`.xlsx` and preserve its formatting. No amount of configuration changes that, and it is not a gap in the tool: it
was never meant to do it.

**So change the deliverable rather than the rules.** A genuinely good Power BI project on this track is a
**release-status report page**:

- a table of the nine checks with their statuses;
- the exceptions behind them, one click away;
- a banner reading the release decision;
- and, the interesting part, **figures that disappear when the month is blocked**. A measure that returns blank
  unless the release decision permits figures reproduces the control gate natively, in the tool's own idiom.

That is the same rule your Python enforces, expressed in a different mechanism, and it is worth building. It just
is not the management workbook.

**Do not rebuild the nine checks in Power Query.** They are a business asset with an agreed definition. A second
implementation can drift from the first, and nobody would know which was right. Run them where they are defined
and import the results.

## The one thing each does differently in kind

**Power BI: the gate becomes a property of the display, not of the process.** In Python the gate is an ordering
decision: the figures are never *calculated* for a blocked month. In Power BI the figures exist in the model and
a measure decides whether to show them. The outcome on screen is the same and the guarantee is weaker, because
the numbers are one click from being exposed by somebody building a new visual. Worth saying out loud in a
handover.

**KNIME: the gate is a wire.** An **IF Switch** or a **Rule Engine** sends the month down one of two paths, and
the canvas shows a blocked month taking the other route. That is the clearest picture of this process any of the
three tools produces. For the workbook itself, use a **Python Script** node running the same supplied writer:
filling a formatted template is the one part nodes do badly, and a workflow that calls Python for one step is not
a failure of either tool.

## The same steps, where they differ

| Step | In Python you wrote | Power BI | KNIME |
|---|---|---|---|
| 1 Fresh output folder | `fresh_output_folder` | Not applicable: a refresh replaces the model | A **Delete Files/Folders** node, or write to a dated folder |
| 2 and 3 Read and check | The manifest reader and the nine checks | **Not here.** Import `control_summary.csv` and `exceptions.csv` | A **Python Script** node calling the same supplied functions |
| 4 Figures only if not blocked | `if release != "blocked"` | A measure returning blank unless the decision permits figures | **IF Switch** on the decision: a visible branch |
| 5 Produce the pack | `write_pack` | A report page instead of a workbook | **Python Script** node with the supplied writer |
| 6 Check against the checkpoint | A comparison within EUR 0.01 | A card that must read 9 | **Joiner** and a **Rule Engine** that fails the workflow |

## What it would cost you

**Power BI.** You gain a page management can open themselves, and give up the artefact they currently receive. If
the workbook is a requirement, this route cannot meet it, and the correct project finding is to say so. You also
take on the weaker guarantee described above.

**KNIME.** You gain a picture of a process that is genuinely hard to follow in code, especially the gate. You keep
Python for the workbook, so you have not removed the dependency, only wrapped it. Somebody maintaining it needs
both tools.

**Python, which you have built.** The only route that produces the deliverable and enforces the gate by never
calculating the figures at all. Hardest to hand to somebody who does not read code, which is the honest cost.

**The judgement this track is really asking for:** start from what management actually receives. If it is that
workbook, the tool question is already decided. If it turns out they would rather have a page they can open
themselves, that is a different requirement and a different project, and finding that out is a better outcome than
building either one on an assumption.

## What this has not shown you

Nobody has run the Power BI or KNIME routes on the course machines. The nodes, menus and measure behaviour above
come from the vendors' documentation, so treat them as an accurate description of what the tools do, not as tested
instructions.
