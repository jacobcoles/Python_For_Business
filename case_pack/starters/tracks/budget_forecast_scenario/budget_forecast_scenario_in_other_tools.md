# Budget and forecast scenarios in Power BI and KNIME

You have built this in Python. This is what the same job looks like elsewhere, and what it would cost you. The job
itself is in `README.md`.

## Fit

| Power BI | KNIME |
|---|---|
| **Good fit, and it can do something Python cannot**: let the reader move the assumption and watch the answer change | **Workable.** The assumptions become visible settings on the canvas rather than a slider |

This is the only one of the six tracks where another tool beats Python at the *analysis* rather than at the
presentation.

## The one thing each does differently in kind

**Power BI: the assumption stops being yours.** In Python you chose 1.05 and 1.12, ran it, and showed somebody the
answer. With a **what-if parameter** (**Modeling > New parameter**, choose **Numeric range**) the reader gets a
slider, and the question changes from "what did you assume?" to "what happens if I assume something else?". For a
conversation with a CFO who does not accept your multipliers, that is a different meeting.

It comes with a specific trap. **A scenario table and a parameter measure are two different mechanisms**, and they
must not be blurred:

| | Step 3's original scenarios | Step 4's chosen case |
|---|---|---|
| What it is | A **calculated table**, computed once when the model refreshes | A **measure** that reads the parameter |
| When it changes | Only on refresh | Every time the slider moves |
| Use it for | Fixed, named, agreed scenarios | The live what-if |

Microsoft's own guidance is that a parameter belongs in a measure: used in a dimension calculation it can compute
incorrectly. So the three supplied scenarios stay tables, and only your own case gets the slider.

**KNIME: the assumption is a node you can see.** A **Double Configuration** node holds each multiplier and feeds it
into the calculation as a flow variable. No slider, so no live conversation, but the assumption sits on the canvas
with a label, rather than being a number buried at the top of a script. For a workflow somebody else reruns next
quarter, visible beats interactive.

## The same steps, where they differ

Steps 1 and 6 are reading files and drawing a chart in every tool. These are the steps that differ.

| Step | In Python you wrote | Power BI | KNIME |
|---|---|---|---|
| 2 Check the baseline | A comparison against the same month a year earlier, that stops | Merge the baseline to the history on the source month, unit and line; a difference column that must be zero on all 27 rows, shown as a card. A refresh cannot stop, so the zero must be visible | **Joiner** on the same key, **Math Formula** for the difference, then a **Rule Engine** that fails the workflow. Closer to Python's behaviour |
| 3 Original scenarios | A function over the baseline | A calculated table per scenario, with the neutral one as the self-test | **Math Formula**, with the neutral scenario as the self-test |
| 4 Your case | Two settings at the top of the file | Two what-if parameters and a measure that reads them | Two **Double Configuration** nodes into flow variables |
| 5 One unit and month | A printed table | A table visual filtered to N02 and February | **Row Filter** and a **Table View** |

**The holdout table stays in Python.** It is supplied demonstration material you read rather than build, and
neither tool route attempts it.

## What it would cost you

**Power BI.** You gain the slider and lose the ability to refuse. Python stops when the baseline check fails; a
refresh cannot, so the check becomes a number somebody has to notice on the page. You also take on the two-
mechanism distinction above, which is a real source of wrong answers when a parameter is used in the wrong place.
Against that: a scenario tool that the audience can drive is worth a great deal, and this is the one track where
that is true.

**KNIME.** The assumptions become part of the documented process, which suits a quarterly rerun by somebody who
did not write it. You give up the live conversation. The arithmetic is Math Formula nodes, which are fine for
three multipliers and unpleasant for thirty.

**Python, which you have built.** Best for the checking, including the holdout evaluation that neither other route
attempts. Worst for the conversation: the assumption is yours, and the reader can only agree or disagree.

**The judgement this track is really asking for:** if the point is to *agree* an assumption with someone, build it
where they can move it. If the point is to *rerun* an agreed assumption reliably, build it where it is written
down. Say which of those your project is for.

## What this has not shown you

Nobody has run the Power BI or KNIME routes on the course machines. The menus and nodes above come from the
vendors' documentation, so treat them as an accurate description of what the tools do, not as tested instructions.

Also note the rounding point in `README.md`: the supplied code rounds each reporting line before adding, while a
measure or a formula node would naturally round once at the end. Compare any figure across tools within EUR 0.01,
not exactly.
