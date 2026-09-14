# Specification template: write this BEFORE you ask for code

Copy the block below into a new file (for example `outputs/D1-S03/specification.txt`), complete it, then paste it
into Microsoft 365 Copilot Chat.
A vague request gets plausible code. A specification gets code you can check.

```
TASK
  One sentence: what result do I need, for whom?

INPUT
  File(s):          <relative path from the course folder>
  Columns:          <name: meaning, type>   (say which columns are TEXT, e.g. codes with leading zeros)
  One row means:    <what a single row represents, e.g. one transaction>

BUSINESS RULES
  1. <which rows count, which do not>
  2. <sign convention: how revenue and costs are stored>
  3. <how the result is calculated>

OUTPUT
  What:             <the figure(s) or table>
  Format:           <printed / CSV at outputs/... / rounded to 2 decimals>

CONSTRAINTS
  - Use pandas. Keep it short and readable; no functions or classes unless needed.
  - Read and print only. Do not write, move or delete any file.
  - Do not invent columns that are not listed above.

ACCEPTANCE EXAMPLE
  For this input I expect: <a number you worked out by hand, and how>
  A wrong answer I want to avoid: <the likely mistake and its value>

ALSO
  Explain each step in one line, and list any assumption you made.
```

## Before you paste anything into an AI chat
- **Synthetic course data only.** Never paste real customer, employee or financial records unless
  your organisation has explicitly approved that tool for that data.
- **Never paste secrets** such as passwords, API keys, connection strings or access tokens.
- **Read generated code before you run it.** Look for anything that writes, moves, deletes or
  overwrites files, or connects to the internet. If you did not ask for it, do not run it.
