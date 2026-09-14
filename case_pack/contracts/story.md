# Northbridge Business Services: the case

**This company is fictional.** Its people, units, data and control thresholds are invented for
teaching. The thresholds are not financial policy, and nothing in this pack is an audit.

Every figure on this page comes from a file in `case_pack/`; sources are listed at the end.

## The business
Northbridge Business Services sells support, training and advisory work. It has three
**operating units**. These are reporting units inside one business, not separate companies, so
there is no group accounting to do. Each unit simply reports its own month.

| Unit | Name |
|---|---|
| `N01` | Northbridge Support Services |
| `N02` | Northbridge Training Services |
| `N03` | Northbridge Advisory Services |

Everything is in euros. The reporting month is December 2025. The same process is run again for
January 2026. In December the units exported 119, 119 and 124 transaction lines. Of those,
117, 116 and 121 were posted and count towards the figures. The rest were cancelled.

You are the operations analyst.

## Month-end today
Each unit's administrator exports the month's transactions to a file and sends it in. Then the
analyst does the month-end by hand.

- **Copy and paste.** Three files are pasted into one workbook. Nobody can say afterwards which
  version of which file was pasted, or whether a row was pasted twice.
- **Inconsistent mappings.** Every transaction carries an **account code**, such as `0400`.
  Someone has to decide which report line each code belongs to: revenue, direct cost or overhead.
  That lookup lives in several people's spreadsheets and they do not always agree. A spreadsheet
  that turns `0400` into `400` quietly breaks the lookup. When a unit starts using a new code
  without telling anyone, its amounts simply fall out of the total.
- **A unit forgets to send its export.** Nothing fails when a file does not arrive. The total just
  looks a little low, and someone notices days later, or never.
- **Look-alike records.** The same transaction number is used by different units: 119 numbers
  appear in more than one unit's December file. Removing "duplicates" by number alone would
  delete genuine transactions.
- **No trail of what was checked.** A workbook that was checked looks exactly like one that was
  not. When the manager asks "did you check it?", the only evidence is somebody's memory.

None of this is dishonest. It is ordinary, and it is exactly the kind of process that goes wrong
quietly.

## What the analyst is asked to build
A small, repeatable monthly run that anyone on the team can rerun. It should:

1. read only the files the month is expected to have, and say so when one is missing;
2. map every account code to a report line from **one** mapping table;
3. leave cancelled lines out of the totals but keep them in the file;
4. compare what arrived with the totals each unit says it sent;
5. write a control summary, a list of exceptions and a dated management workbook;
6. state a release status: `ready`, `ready_with_warnings` or `blocked`.

A `blocked` run is a correct result. It means the checks did their job. The deliverable is then
the list of problems and a written decision, not a workbook that looks approved.

## The operations manager's four questions

**1. "Have all three units sent me December?"**
Three exports are expected for December, one per unit. The answer comes from checking that list,
not from looking at a total.

**2. "Can I rely on these figures?"**
Nine checks run before anyone believes a number. The answer is a release status, with every
exception traced to the file and row it came from. It says the figures are fit to use for this
report. It does not say they have been audited.

**3. "Where are we against budget, and what explains it?"**
For December the three units made an operating result of EUR 67,330.86 against a budget of
EUR 67,600.00. That is EUR 269.14 below budget. Close to plan overall, but for a reason worth
knowing:

| | Against budget (EUR) |
|---|---:|
| Revenue | −2,972.11 (below budget) |
| Direct cost | +1,778.66 (spent less than budget) |
| Overhead | +924.31 (spent less than budget) |
| **Operating result** | **−269.14** |

Revenue fell short, and lower costs made up most of the gap. By unit: N01 +1,112.50,
N02 −1,105.17, N03 −276.47. The largest single shortfall is N02 revenue, EUR 2,587.97 below
budget. A plus sign here always means better than budget; a minus sign means worse.

These figures describe what happened. They do not explain why. Finding the reason is a
conversation with the units, not a calculation.

**4. "What might next quarter look like if our assumptions change?"**
The starting point is a **baseline**: each month of January to March 2026 is set equal to the same
month one year earlier. Stated assumptions are then applied to it. One scenario has revenue
10% above the baseline and direct cost 8% above. Another keeps revenue at the baseline, with
direct cost 12% above and overhead 5% above. Each scenario is a what-if. None is a prediction,
and the range between them carries no probability.

## How the story runs through the course

| Course section | The manager's question | Shared result |
|---|---|---|
| Day 1: Copilot and data preparation | "Can you bring the three units' files together correctly, without a copy-and-paste I have to take on trust?" | Posted transactions in one consistent shape, each mapped to its report line |
| Day 1: controls | "Before this goes anywhere: is everything in, and can I use the figures?" | Control summary, exceptions traced to file and row, release status |
| Day 1: reporting | "Can we produce exactly the same pack next month without starting again?" | Dated management workbook and a short note for whoever runs it next |
| Day 2: external data | "For context: what have consumer prices been doing, and how current is that figure?" | A separately labelled external dataset with a record of where and when it was fetched |
| Day 2: visualisation | "Show me what explains the gap to budget in a picture I can read." | An accurate, readable comparison or variance chart |
| Day 2: planning | "If our assumptions change, what could next quarter look like, and what can't this tell me?" | Baseline, scenarios and clearly stated limitations |
| Day 2: integrations, then Days 3–4 projects | "Where should this process live, and who looks after it once you've moved on?" | Tested local and tool-based examples and a reasoned handover route |

## What this case is not
- **Not a fraud story.** The failures are a missing file, an unmapped code, a repeated row. No one
  is hiding anything.
- **Not a compliance exercise.** No regulation is involved. The checks are fictional teaching
  rules, not policy, and passing them is not an audit opinion.
- **Not a causal model.** On Day 2 a real OECD consumer-price series appears. It is **external
  context only**. It is never joined to Northbridge's figures and never feeds the baseline or the
  scenarios. Nothing in Northbridge's results is explained by it.

## Where these figures come from
| Figure | File |
|---|---|
| Unit codes and names | `data/clean/entities.csv` |
| December lines exported (119, 119, 124) and posted (117, 116, 121) | `data/clean/source_controls.csv`, 2025-12 rows |
| Three expected December exports | `data/clean/expected_files.csv`, 2025-12 rows |
| 119 transaction numbers shared between units | The three December transaction files in `data/clean/transactions/` |
| 67,330.86 / 67,600.00 / −269.14 (three-unit totals) | `data/clean/analysis/variance_bridge_2025-12.csv` (first and last steps) |
| The unit split (N01 +1,112.50, N02 −1,105.17, N03 −276.47) | `data/clean/analysis/unit_comparison_2025-12.csv` |
| −2,972.11 / +1,778.66 / +924.31 | `data/clean/analysis/variance_bridge_2025-12.csv` |
| N02 revenue −2,587.97 | `data/clean/analysis/variance_by_line_2025-12.csv` |
| Scenario percentages | `data/clean/scenario_assumptions.csv` (multipliers 1.10, 1.08, 1.12, 1.05) |
| Forecast months, baseline method | `data/clean/planning/` (used on Day 2) |
