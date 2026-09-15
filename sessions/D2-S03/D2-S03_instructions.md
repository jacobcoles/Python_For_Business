# D2-S03: When today's refresh fails

**What can we report when today's refresh fails?**

10:45 to 11:30, 45 minutes. **Tool: Python scripts in VS Code**, because a refresh is rerun the same way each time.

**You will produce:** your freshness rule in `freshness_rule.py`, and an operator note `outputs/D2-S03/operator_note.md`.

## Why this matters

In D2-S02 a single request fetched a small OECD table and saved it with the time it was downloaded. A real process
reruns that request every month: a **refresh**. (If you have not done D2-S02, that is all you need to know here.) Sometimes the
request fails. A saved copy from last time (a **cache**) may still be useful, but only if it is honestly labelled
with its original download date and is not too old. The refresh process is supplied. You write the one business
rule inside it that decides whether a saved copy is still fresh enough, and then see what that rule does when
requests fail.

## Files you will open or run

| File (paths start at the course folder) | What it is for |
|---|---|
| `case_pack/contracts/refresh_policy.md` | The course's refresh policy. Read the first two tables |
| `sessions/D2-S03/learner/freshness_rule.py` | Your rule, plus a small test. You edit this file |
| `sessions/D2-S03/learner/refresh_scenarios.py` | Runs four controlled failure scenarios with your rule. You change one setting |

The scenarios use the response saved on 2026-09-13 and **simulated** failures. They make no internet requests, so they
test our decisions, not the OECD service.

## Rules for this task

Every refresh reports two separate facts:

| Field | Question it answers | Possible values |
|---|---|---|
| `refresh_outcome` | What happened when we tried this time? | `success`, `http_error`, `timeout`, ... |
| `data_status` | How fresh is the data we hand over? | `live`, `cached`, `stale`, `unavailable` |

- A successful request gives `live` data.
- If the request fails and a saved copy exists: `cached` if it is **at most** 35 days old, `stale` if older.
- If the request fails and there is no saved copy: `unavailable`.
- A failed attempt never changes the saved copy's original download time (`retrieved_at_utc`). Only the time of the
  last attempt changes.
- The 35-day limit is a course policy for a monthly series, not a workplace rule.

## How to run a file

Open it and click **Run Python File** (the triangle at the top right), or paste the command into
**Terminal > New Terminal**.

## Steps

### Step 1: Predict the four cases (8 minutes)

**Why:** deciding the labels yourself first shows whether the policy is clear to you.

In each case below, **today's request fails**:

| Case | Age of the saved copy | Today's request |
|---|---|---|
| A | 3 days | server error (HTTP 500) |
| B | 30 days | server error (HTTP 500) |
| C | 36 days | server error (HTTP 500) |
| D | no saved copy | no answer (timeout) |

**Do:** in the Explorer, right-click the `outputs` folder, choose **New Folder**, name it `D2-S03`; right-click that
folder, choose **New File**, name it `operator_note.md`. Copy the table in, add columns `data_status` and
`date shown to the manager`, and fill them with your prediction.

### Step 2: Write the freshness rule (YOUR TURN, 10 minutes)

**Why:** this one decision is what separates an honest refresh from one that passes off old data as current.

**Do:** open `freshness_rule.py`. The description inside the function says exactly what it receives and must return.
Replace `return None` with your rule. If you want help, ask Copilot:

> Write the body of a Python function data_status_for_saved_data(age_in_days, max_age_days). Return "cached" if
> age_in_days is less than or equal to max_age_days, otherwise return "stale". Give me only the line or two inside
> the function.

Save, then run the file:

```powershell
.\.virtual-env-folder\Scripts\python.exe sessions\D2-S03\learner\freshness_rule.py
```

**You should see:** four lines ending in `ok`. If the 35-day line says `CHECK`, look at the boundary: "at most 35"
includes exactly 35.

### Step 3: Run the scenarios and compare with your prediction (10 minutes)

**Do:** run `refresh_scenarios.py`:

```powershell
.\.virtual-env-folder\Scripts\python.exe sessions\D2-S03\learner\refresh_scenarios.py
```

**You should see:** a table of the four cases with `refresh_outcome`, `data_status` and `retrieved_at_utc`.
Compare it with your prediction and note any difference in your operator note.

Then open `outputs/D2-S03/example_cache/`. It holds case B's saved copy: a CSV with the data and a `.meta.json` file.
In the `.meta.json` file, compare `retrieved_at_utc` (when the data was downloaded) with `last_attempt_utc` (when we
last tried). Why must these two stay separate?

### Step 4: Test a stricter policy (7 minutes)

**Why:** a manager asks, "what if we only accepted data up to 20 days old?"

**Predict** which case changes. Then set `MAX_AGE_DAYS = 20` near the top of `refresh_scenarios.py`, save and run.

Note in your operator note which case changed and what stayed the same. Then **set it back to 35**, save and run
again. Changing a setting in an exercise does not change the course policy.

### Step 5: Finish the operator note (10 minutes)

Add these headings under your prediction table:

```text
What the scenarios showed, and any prediction I corrected:
What changed at a 20-day limit, and what did not:
What I would tell the manager about case C:
The date that must not change after a failed attempt, and why:
How to rerun the scenarios:
One thing to check before using this with another data source:
```

## Check your result

After you have run the scenarios:
- A **cached**, B **cached**, C **stale**, D **unavailable**. A to C keep `retrieved_at_utc` 2026-09-13T18:33:16Z; D has none.
- At a 20-day limit only **B** changes, from cached to **stale**. The outcomes, the dates and the data values do not change.
- For case C, a good message is: "Today's refresh failed. The latest data we hold was downloaded on 13 September and is
  older than our 35-day limit, so treat it as out of date until a refresh succeeds."

## Done when

Your rule passes its four tests, your note compares prediction with the scenarios, explains the 20-day change and
gives a manager-ready message for case C.

## If something goes wrong

| What you see | What to do |
|---|---|
| `NOT DONE YET` in the data_status column | Save `freshness_rule.py` after replacing `return None`, then run the scenarios again |
| `rule error: ...` | Your rule must return the text `"cached"` or `"stale"`, with quotation marks and in lower case |
| `STOPPED: MAX_AGE_DAYS must be a number` | The setting is a number, so it takes no quotation marks: `MAX_AGE_DAYS = 35` |
| Nothing changed at a 20-day limit | Your rule probably uses the number 35 instead of `max_age_days` |
| `IndentationError` | The line inside the function must start with four spaces, like `return None` did |
| `ModuleNotFoundError` | VS Code is not using the course Python. Select `.virtual-env-folder` (see D1-S02) |

**Start again:** restore `freshness_rule.py` from the course download. The scenarios create and remove their own
temporary files.

**Optional extension:** on an approved network, set `RUN_LIVE_REFRESH = True` and run once. Look at the printed
outcome and at `outputs/D2-S03/live_cache/`. If it fails, record the outcome: that is the process working. Set it back
to `False`. A script you run by hand is rerunnable, but it is not a scheduled service: nothing runs it for you.
