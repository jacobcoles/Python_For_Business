# D1-S03 participant guide: the Copilot working loop

**45 minutes.** You will get code from an AI assistant and check whether it is right.

**Northbridge recap.** You are the operations analyst at Northbridge Business Services, a fictional
support-and-training company with three units, N01–N03. Each unit exports its monthly transactions.
Today you start with the smallest possible piece: **eight rows** from unit N01 for December 2025.

The loop you are practising:

```
specify -> generate -> execute -> inspect -> correct -> document
```

---

## 1. Predict first

Open `case_pack/data/clean/tiny/transactions_2025-12_N01.csv` in VS Code and read the eight rows.
You need three rules, all supplied by the business:

- Revenue is stored **positive**. Costs are stored **negative**. So the operating result is a plain
  sum of the amounts that count.
- Only rows with `status` = **posted** count. A **cancelled** row stays in the file but is excluded.
- A **positive** amount on a cost line is a reversal. Keep its sign.

Before any code exists, work out the operating result you expect and your reasoning. You will put it in the
ACCEPTANCE EXAMPLE section of your specification, and compare it with your neighbour's.

---

## 2. Vague request versus specification

A vague request:

> *"Write Python to total the transactions in my CSV."*

This produces code that runs. It will very probably include the cancelled row, and nothing in the
output will warn you.

Now open `sessions/D1-S03/learner/specification_template.md` and fill it in for this task. A good
specification names the file, the columns (and that `account_code` is text), the three business
rules above, the output, the constraints, and **the number you expect, plus a likely wrong answer to watch for**.

---

## 3. Get code, run it, inspect it (15 min)

1. Paste your filled-in specification into Microsoft 365 Copilot Chat.
2. **Read the code before running it.** Does it write, move or delete any file? Connect to the
   internet? If you did not ask for that, do not run it.
3. Create the file for the code: in the VS Code Explorer, right-click `outputs` → **New File** and type
   `D1-S03/my_total.py` (this also creates the folder). Paste the code, save with **Ctrl+S**, and run it from the
   course folder:
   ```
   .virtual-env-folder\Scripts\python.exe outputs\D1-S03\my_total.py
   ```
4. **Inspect the result; don't just accept it.** Print the rows it used. How many are there? Is `T008` among them?

Compare the printed number with your prediction. Add a short comment at the bottom of `my_total.py` with the number
printed, the check you used, and whether it matches.

> Your code will not look like your neighbour's. That is fine. The result and the check are what
> matter, not the variable names.

---

## 4. Diagnose and correct (10 min)

Two supplied examples show the two ways AI-generated code goes wrong. Work directly in the files in
`sessions/D1-S03/learner/`; to start again, extract them from the course ZIP.

### A. The loud failure
```
.virtual-env-folder\Scripts\python.exe sessions\D1-S03\learner\flawed_example_runtime.py
```
It stops with a long error. **Read the last line first**, then find the line that mentions *your*
file.

Work out which line of the script the error points to. Then add `print(transactions.columns)` above that line and
run it again: what is the column really called?

Ask the AI for the **smallest** correction: one line, not a rewrite. Then run it. A fix only counts
once it has run and given the right answer.

### B. The silent failure
```
.virtual-env-folder\Scripts\python.exe sessions\D1-S03\learner\flawed_example_silent.py
```
No error. It prints a number. **Is it right?**

Compare the printed result and the number of rows used with your prediction from section 1. Which business rule
did the code ignore?

**Make the change** that applies the missing rule. **Run it again** and compare the new number
with your prediction. Then ask the AI to explain the change, and check its explanation against
what actually ran, not against how confident it sounds.

---

## 5. Pair review (5 min)

Take turns to walk your partner through:
1. **one check** you ran and what it showed;
2. **one correction** you made and how you know it worked.

---

## Troubleshooting

| Symptom | What to inspect | Likely correction | Reset |
|---|---|---|---|
| `FileNotFoundError` | `working_dir`: are you in the course folder? | Run from the course folder, not from `outputs/` | Re-open the course folder in VS Code |
| `KeyError: 'Something'` | `print(df.columns)` | Use the column name exactly as it appears | Re-run the supplied example |
| A number, but not the one you predicted | Print the rows actually used; count them | Apply the missing business rule, re-run | Re-read section 1 |
| `IndentationError` | The pasted lines: Python uses the spaces at the start of a line | Paste the whole block at the left margin; don't mix pasted and typed indentation | Re-paste the code |
| Your change makes no difference | The file tab: a dot means unsaved | Save with **Ctrl+S**, then run again | Not needed |
| The AI keeps rewriting everything | Your prompt | Ask for "the smallest change to line N" | Paste only the error and the one line |

**Reset:** extract the two example files again from the course ZIP, and delete `outputs/D1-S03/` to remove your own files.

## By the end of this session you can
- write a specification that includes the business rules and an expected result;
- run AI-generated code and compare its result with your prediction;
- diagnose a failure from its error message;
- find, fix and re-check a silent error.

## Optional extension
Suppose someone "tidies" the data by turning every cost into a positive number *before* summing
(which rows are costs is in `case_pack/data/clean/tiny/account_mapping.csv`, column `report_line`),
then subtracts costs from revenue. Predict the operating result, try it, and explain what happened to
the reversal row `T006`.
