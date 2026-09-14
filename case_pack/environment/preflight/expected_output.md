# Readiness check: what a good result looks like, and what to do if it isn't

Run the check from the course folder, in the VS Code terminal (**View → Terminal**):

```
Windows:  .virtual-env-folder\Scripts\python.exe case_pack\environment\preflight\smoke_test.py
macOS:    .virtual-env-folder/bin/python case_pack/environment/preflight/smoke_test.py
```

## A good result
The check runs nine checks in five groups (PF-01 to PF-05) and ends like this (your folder names will differ):

```
  [PASS] PF-01 Python interpreter: Python 3.12.x from the project .virtual-env-folder.
  [PASS] PF-02 Working directory: the working directory looks like the course folder root ...
  [PASS] PF-03 import pandas: version ...
  [PASS] PF-04 Course data folder: found via a relative path ...
  [PASS] PF-05 Write / read / delete: created, read and deleted a file under 'outputs/preflight_tmp'.

RESULT: READY. All checks passed. You can continue to D1-S03.

----- COPY FROM HERE -----
...
working_dir     : C:\Course
in_project_venv : True
result          : READY (0 failed, 0 warning(s), 9 checks)
----- COPY TO HERE -----
```

The word READY is not enough on its own: `in_project_venv` must also say `True`. That line shows the check ran
with the course's own Python.

The check only reads and writes a small temporary file inside `outputs/`, then deletes it. You can run it as often
as you like.

## If it is not READY

| # | What you see | What to check first |
|---|---|---|
| 1 | `RESULT: NOT READY`, PF-01 failed, `in_project_venv : False` | The command ran with a different Python. Run it exactly as shown above, starting with `.virtual-env-folder\Scripts\python.exe`. If PF-01 says the Python version is not 3.12, the environment needs to be recreated with Python 3.12 (see `START_HERE.md`). |
| 2 | `ModuleNotFoundError`, or PF-03 failed | Usually the same cause as row 1. Check `in_project_venv` before anything else, and do not install packages yourself. |
| 3 | `FileNotFoundError`, or PF-02 or PF-04 failed | You are not in the course folder. In VS Code use **File → Open Folder** on the course folder (the one containing `case_pack` and `sessions`), open a new terminal and run the command again. |
| 4 | PF-05 failed, or "Permission denied" / "Access is denied" | Something on your computer is blocking files from being written, often a synced OneDrive or Teams folder or a security setting. Retrying will not help. Move the course folder to a local folder such as `C:\Course`, or send your support block to the instructor. |

## Sending the support block
Copy everything between `COPY FROM HERE` and `COPY TO HERE` and send it to the instructor. It contains no
username, home folder or passwords, so it is safe to paste into a chat.
