# D2-S07: A new sample, then your project

**Test your skills on a new sample, then choose your project**

15:45 to 17:00, 75 minutes. **Tools: a Python script in VS Code with Copilot, then a short written plan.**

**You will produce:** your completed `sessions/D2-S07/learner/my_analysis.py` and `outputs/D2-S07/my_answer.md`
(a small analysis you did yourself), and in `outputs/projects/<your project>/`: your plan for Days 3 and 4
(`plan.md`) and the first line of your working record (`worklog.md`).

## Why this matters

Days 3 and 4 are for your own project. First, a short task on data you have not seen shows you, and the instructor,
which parts you can already do alone and where you want support. Then you choose a project small enough to finish,
check and hand over in two days.

## Part 1: a new monthly sample (20 minutes)

### Data you will read

| File (paths start at the course folder) | What it contains | One row means |
|---|---|---|
| `case_pack/starters/transfer_fixture/transactions_2026-02_N01.csv` | February 2026 transactions for N01 (7 rows) | One transaction |
| `case_pack/starters/transfer_fixture/transactions_2026-02_N02.csv` | February 2026 transactions for N02 (2 rows) | One transaction |
| `case_pack/data/clean/account_mapping.csv` | Which report line each account code belongs to | One account code |

The four account codes in this sample map as follows:

| account_code | account_name | report_line |
|---|---|---|
| 0400 | Service revenue | revenue |
| 0410 | Training revenue | revenue |
| 0500 | Direct delivery cost | direct_cost |
| 0600 | Premises overhead | overhead |

### The file you work in

`sessions/D2-S07/learner/my_analysis.py` already reads both February files and the mapping. You add the analysis at
the end, under `YOUR TURN`, and keep the file: it is one of the two things you hand in.

### The request

For **N01 in February 2026**: what are revenue, direct cost and overhead, and the operating result?

### Rules

- Only N01. The files also contain N02.
- Only `posted` EUR rows count. Leave cancelled rows in the files.
- Keep every sign: a negative revenue row is a refund; a positive cost row is a reversal.
- The reader loads every column as **text**, including `amount`: convert it to a number before adding.
- Match `account_code` as text to the mapping; each code must match exactly once.
- Operating result = revenue + direct cost + overhead (costs are already negative).

### Steps

1. **Open your working file:** `sessions/D2-S07/learner/my_analysis.py`. It already reads both February files and
   the account mapping.
2. **Run it** (click **Run Python File**). **You should see** nine transactions printed, and a line telling you where
   to write your answer.
3. **Predict.** With a calculator and the rules, work out N01's operating result before writing any code. The run in
   step 2 created `outputs/D2-S07`: right-click that folder, choose **New File**, name it `my_answer.md`, and note
   your prediction. Check as you go that each of the four account codes appears exactly once in
   `case_pack/data/clean/account_mapping.csv`.
4. **Ask Copilot** and paste the answer under `YOUR TURN` at the end of `my_analysis.py`:

   > I have two pandas DataFrames. `transactions` has the columns transaction_id, period, entity, account_code,
   > amount, currency, status, source_file and source_row; every column is text. `mapping` has account_code,
   > account_name and report_line, also text. Write short, commented pandas code that keeps only rows for entity
   > "N01", period "2026-02", status "posted" and currency "EUR"; converts amount to a number; attaches report_line
   > from mapping on account_code with a left join that stops with an error if a code appears twice in the mapping;
   > prints the total amount per report_line; and prints the operating result as the sum of all three. Keep signs as
   > they are. Do not read or write files.

   **Read it before running:** is N01 the only unit kept? Is amount converted? Is it a left join?
5. **Run it again**, compare with your prediction, and finish `my_answer.md` under these headings:

   ```text
   Revenue, direct cost, overhead and operating result:
   My prediction, and whether it matched:
   One thing I checked or corrected in Copilot's code:
   ```

Then the instructor shares the answer and asks each person, briefly, which parts they did alone.

## Part 2: choose your project (35 minutes)

### Step 6: Pick a track (10 minutes)

Each folder in `case_pack/starters/tracks/` holds four things: a **README** stating the job in one screen, a
**worked example** (a complete, commented script that solves a small version with course data), a **Python guide**
naming every step and prompt, and a short page on how the same job would look in Power BI and KNIME. You build in
Python and adapt the worked example; read the last one afterwards, when you can judge it.

| Folder | What you will build | Built on the session |
|---|---|---|
| `monthly_reporting_pack` | A month of exports checked and written into the management template | D1-S08 |
| `audit_exceptions` | Checks run across several deliveries, with an exception summary | D1-S06 |
| `multi_file_reconciliation` | Two lists matched, with missing, extra and different items reported | D1-S04 |
| `budget_forecast_scenario` | Your own scenarios with a chart and a recommendation | D2-S05 |
| `external_refresh_controls` | An external data refresh with honest status and a source record | D2-S02 and D2-S03 |
| `management_dashboard` | A clean data file feeding an Excel or Power BI report | D2-S04 and D2-S06 |

Open the README of one or two tracks. Run a worked example (open `worked_example.py`, click **Run Python File**) to see
what it produces. You may use your own data instead only if your organisation has approved it and it is available now.

### Step 7: Write your plan, then have it challenged (15 minutes)

1. **Write it (10 minutes).** Create `outputs/projects/<short name>/` (for example `outputs/projects/january_pack/`)
   with **New Folder**, then copy `sessions/D2-S07/learner/project_plan.md` into it and fill it in.
2. **Have Copilot argue against it (5 minutes).** Paste your filled-in plan into Copilot Chat:

   > This is my plan for a two-day piece of work. Do not write any code, and do not tell me it looks good. Ask me the
   > five questions most likely to show that the plan is too large for two days, that my check would not prove what I
   > think it proves, or that I have assumed data or access I may not have. Then name the one part you would cut.

   You will not have a good answer to all five, and that is the point of asking now rather than tomorrow afternoon.
   Write the two you cannot answer into the last section of your plan and take them to Step 8.

### Step 8: Agree the plan with the instructor (10 minutes)

Show your plan. Agree the first small output, how you will check it, and what to leave out.

## Part 3: first run (20 minutes)

### Step 9: Start from the worked example

Copy your track's `worked_example.py` into your project folder (right-click, **Copy**, **Paste**). Run the copy from
there. **You should see** the same output as the original: your starting point works.

Make the smallest first change from your plan, run it again, and note in `plan.md` what you will do first tomorrow.

Then start your working record: right-click your project folder, choose **New File**, name it `worklog.md`, and write
one line for the change you just made, under the three headings **What I asked for · What I kept · What I checked**.
One line per step from here on. It takes seconds and it is what your handover note is written from on Day 4.

## Done when

Part 1: your analysis prints the three report lines and the operating result, and `my_answer.md` records your
prediction, the result and one thing you checked or corrected.
Part 2 and 3: your plan has been through Copilot's challenge and the instructor's review, your copy of a worked
example runs from your own project folder, `worklog.md` has its first line, and tomorrow's first change has a check.

## Check your result (Part 1)

Your instructor gives out the answer after everyone has attempted it, and will ask which parts you did alone. Check
your own work first: add the posted N01 rows with a calculator, and confirm that your code used only N01, only
February 2026 and only posted EUR rows.

## If something goes wrong

| What you see | What to do |
|---|---|
| `TypeError` or a very long number when adding amounts | `amount` is still text. Ask Copilot to convert it with `pd.to_numeric` after filtering |
| `MergeError` | An account code appears twice in the mapping: the safeguard is working. Tell the instructor |
| A worked example cannot find a file after you copied it | Run your copy with the Run button; the setup lines find the course folder |
| You cannot find what a worked example produced | It saves beside itself: look in your own project folder. The run prints `Saving into:` with the full path |
| Your own data cannot be opened | Use the track's course data for now and note the access problem in your plan |

**Start again:** Part 1 changes only your own copy of `my_analysis.py`; delete what you added under `YOUR TURN` and
run it again. The February files and the mapping are never changed.
