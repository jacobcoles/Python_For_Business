# Day 2: start here

Continue in the **same course folder** you used on Day 1. Nothing from Day 1 needs to be finished: each session
starts from its own supplied files.

| Time | Session | Instructions |
|---|---|---|
| 09:00 | Why is this December figure wrong? | `sessions/D2-S01/D2-S01_instructions.md` |
| 09:25 | Euro-area inflation from the OECD | `sessions/D2-S02/D2-S02_instructions.md` |
| 10:45 | When today's refresh fails | `sessions/D2-S03/D2-S03_instructions.md` |
| 11:30 | A chart the board can read | `sessions/D2-S04/D2-S04_instructions.md` |
| 13:15 | Planning scenarios for the CFO | `sessions/D2-S05/D2-S05_instructions.md` |
| 15:00 | Python in a script, Power BI and KNIME | `sessions/D2-S06/D2-S06_instructions.md` |
| 15:45 | A new sample, then your project | `sessions/D2-S07/D2-S07_instructions.md` |

Breaks: 10:30 to 10:45, lunch 12:15 to 13:15, 14:45 to 15:00.

## How a session works

- **One instructions file per session**, named in the table above. Open it and press **Ctrl+Shift+V** to read it
  comfortably. It names the tool to use, the data to read, the rules and the steps in order.
- **Starting files** are in `sessions/<session>/learner/`. You edit them in place.
- **Everything you produce** goes in `outputs/`, one folder per session. Scripts create those folders. Nothing reads
  from `outputs/`, so you can delete anything there and run the session again.
- **Code you see is labelled** `SUPPLIED` (run it, no need to read it), `READ` (the comments explain it) or
  `YOUR TURN` (paste Copilot's code there, after reading it).
- **Checks** print `OK`, `PROBLEM` (with what to look at) or `NOT DONE YET`. On a PROBLEM, change that one thing and
  run again.
- **Settings** are the named values at the top of a script or cell that you change. Text needs quotation marks
  (`CASE = "clean"`); `True`, `False` and numbers never do (`MAX_AGE_DAYS = 35`). A wrong one stops the run with a
  sentence saying which it is.
- **Expected answers** appear under **Check your result**, after the step that asks you to work them out.
- **Data in `case_pack` is read only.** Never change it.

## Paths, in three habits

| When you need... | Do this |
|---|---|
| A path in **Python code** | Right-click the file in the Explorer > **Copy Relative Path**, and use `/` between folders |
| A path for **Power BI, KNIME or Excel** | Right-click the file > **Copy Path** (the full path) |
| To **run** a script | Open it and click **Run Python File**, or paste the command from the instructions |

If a file seems locked, close it in Excel; if your course folder is in OneDrive, wait for syncing to finish.

## If you get stuck

- `case_pack/contracts/glossary.md` explains the business terms and the tool and Python words.
- `sessions/D1-S01/learner/tool_choice_aid.md`: which tool suits which job.
- `sessions/D1-S03/learner/working_with_ai.md`: how to hold a job together across many prompts.
- Every session ends with an **If something goes wrong** table and a **Start again** line.

**AI tools:** use only the course's synthetic data with Copilot. Never paste personal, confidential or real financial
data unless your organisation has approved that tool for it.
