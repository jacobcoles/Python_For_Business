# D1-S02 participant guide: check that your setup works

**20 minutes.** By the end you will have shown, rather than assumed, that you can run the course code.

Where you are in the story: you are the operations analyst at **Northbridge Business Services**.
Before you touch the month-end figures, you check your tools. That is the same habit this session
is teaching.

---

> **Before the course:** the course folder must already contain a `.virtual-env-folder` created from
> `case_pack/environment/requirements-lock.txt` (steps in `START_HERE.md`). If `.virtual-env-folder` is missing, tell the
> instructor now; do not try to create it during this session.

## Step 1: Open the course folder (3 min)

1. Open **VS Code**.
2. **File → Open Folder...** and choose the **course folder itself** (the one containing
   `case_pack/`, `sessions/` and `outputs/`), not the folder above it or a folder inside it.
3. Open **Microsoft 365 Copilot Chat** in a browser tab and check you are signed in.

**You should see** `case_pack/`, `sessions/` and `outputs/` in the Explorer panel.

> If you open the wrong folder, VS Code will not find the course Python later. This single step causes
> more Day 1 problems than anything else.

---

## Step 2: Choose the course Python (5 min)

VS Code tracks **two** separate settings, and they can disagree:

| Setting | Where | Applies to |
|---|---|---|
| Interpreter | **Ctrl+Shift+P** (Mac: Cmd+Shift+P) → **Python: Select Interpreter** | `.py` scripts |
| Kernel | The picker at the **top right of an open notebook** | `.ipynb` notebooks |

Set **both** to the interpreter inside the course folder's `.virtual-env-folder`. If it is not in the list, choose
**Enter interpreter path...** (for a notebook: **Select Another Kernel → Python Environments**, then the same option)
and pick `.virtual-env-folder\Scripts\python.exe` (Windows) or `.virtual-env-folder/bin/python` (macOS).

**You should see** a path ending in `.virtual-env-folder/bin/python` (macOS) or `.virtual-env-folder\Scripts\python.exe`
(Windows).

---

## Step 3: Run the readiness check (7 min)

In the VS Code **terminal** (the command window at the bottom of VS Code; open it with **View → Terminal**), from the course folder:

```
.virtual-env-folder\Scripts\python.exe case_pack\environment\preflight\smoke_test.py
```
(macOS: `.virtual-env-folder/bin/python case_pack/environment/preflight/smoke_test.py`)

It prints nine checks in five groups (PF-01 to PF-05; PF-01 also confirms you are using Python 3.12) and then a **support block** between two marker lines.

**You should see** a result line starting `RESULT: READY. All checks passed.`, followed by the support block.

**Now read two lines of the support block, not the headline:**

```
in_project_venv : True
working_dir     : ...the course folder...
```

`in_project_venv : True` is the line that matters. A check can find every package and still be using the
wrong Python. **Look for this line, not just the word READY.**

### Paths: why the working directory decides where your file lands
A **path** is a folder route written as text. `case_pack/data/clean/account_mapping.csv` means: open `case_pack`, then
`data`, then `clean`, then the file, exactly as you would click through folders in File Explorer. `/` and `\` both
separate folders; inside Python code this course always uses `/`, which also works on Windows.

Every path in this course is **relative**: it starts from your **working directory**, the folder you are working in.

```
case_pack/data/clean/transactions/transactions_2025-12_N01.csv
```

That path only works if your working directory is the course folder. Run the same code from your
Desktop and it fails, or it saves output somewhere you will not find it.

**Try it:** the readiness check prints `working_dir`. Note what it says. That is where relative paths
start from.

**Tip:** you rarely need to type a path. In VS Code, right-click any file in the Explorer panel → **Copy Relative Path**.

**Three habits for today:** save your file with **Ctrl+S** before running it (a dot on the file's tab means unsaved
changes; **File → Auto Save** avoids this); run everything from the course folder; extract ZIPs into the course folder.

### Find these four things now
| What | Where |
|---|---|
| The data | `case_pack/data/clean/` |
| Your starting files | `sessions/<session>/learner/` |
| Where your output goes | `outputs/`; each exercise names its exact subfolder |
| How to start over | The **Reset** note in the participant guide or `RESET.md` of sessions that have starting files |

---

## Step 4: Four common problems (3 min)

Full table with symptoms and fixes: `case_pack/environment/preflight/expected_output.md`.

| # | Symptom | What to check first |
|---|---|---|
| 1 | `RESULT: NOT READY`, `PF-01` failed | `in_project_venv : False` means the check ran with a different Python. Run the command exactly as shown above, starting with `.virtual-env-folder\Scripts\python.exe`. |
| 2 | `ModuleNotFoundError` | Usually the same cause as problem 1. Check `in_project_venv` **before** you try to install anything. |
| 3 | `FileNotFoundError` | Check `working_dir`. You are probably working from the wrong folder. |
| 4 | Permission or access denied | Retrying will not help. Send your support block to the instructor. |

**Do not run `pip install` to fix a missing package.** On a managed machine it is likely to be
blocked, and a partial install creates a harder problem than the one you started with. Check the
interpreter first; ask second.

---

## Step 5: Report your status (2 min)

Tell the instructor one of:
- **"READY"**: the readiness check passed and `in_project_venv` is `True`; or
- **your support block**: copy everything between the two marker lines and send it.

The support block deliberately contains **no** username, no home path and no credentials. It is
safe to paste into a chat.

If your setup cannot be fixed in this session, you will **work with a partner** whose setup works.
That is a normal outcome: you still do the analysis and make the decisions together.
Tell the instructor now rather than later in the morning.

---

## By the end of this session
- The course folder is open in VS Code, with `case_pack` visible.
- The interpreter **and** the notebook kernel both point at the course `.virtual-env-folder`.
- The readiness check reports `READY` and `in_project_venv : True`.
- You know where the data is, where your output goes and how to reset an exercise.
- You can explain why a relative path depends on the working directory.
