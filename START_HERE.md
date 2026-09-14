# Start here: the Northbridge course folder

Northbridge Business Services is a fictional company and all of its data is synthetic, in EUR. The `case_pack`
folder holds the shared Northbridge data, templates and background documents used in every session.

## Course setup (once, before Day 1: organiser or participant)
Unzip the course download to a **local** folder such as `C:\Course`. Avoid OneDrive, SharePoint or Teams-synced
folders: syncing can lock files while scripts write to them. When Windows **Extract All** suggests a folder name,
check you don't end up with a folder inside a folder of the same name. The **course folder** is the one that
directly contains `case_pack`, `sessions` and `outputs`.

Every command in the course expects a Python environment called `.virtual-env-folder` **inside this course folder**.
It is not included in the download. Create it from the course folder using Python 3.12:

```
Windows:  py -3.12 -m venv .virtual-env-folder          (if py is not recognised: python -m venv .virtual-env-folder,
                                                     after checking that python --version shows 3.12)
          .virtual-env-folder\Scripts\python.exe -m pip install -r case_pack\environment\requirements-lock.txt
macOS:    python3.12 -m venv .virtual-env-folder
          .virtual-env-folder/bin/python -m pip install -r case_pack/environment/requirements-lock.txt
```
Then run the readiness check (see below). The result line must say `RESULT: READY` **and** the support block must
show `in_project_venv : True`.
On a managed machine where installing software is blocked, IT must provide this environment before the course.

## Starting
Open the whole course folder in VS Code (**File → Open Folder**). Run everything from the course folder,
not from a session subfolder. The readiness check is `case_pack/environment/preflight/smoke_test.py`;
`sessions/D1-S02/participant_guide.md` explains how to run it and what to do if it is not READY.
After setup, do not install any other packages, and do not work around your organisation's IT controls.

## Where things are
- **Slides:** `slides/Day1_slides.pdf`
- **Pre-read:** `case_pack/contracts/business_primer.md`
- **Each session:** `sessions/<session>/participant_guide.md`, with starting files in `sessions/<session>/learner/`
- **Data (read only):** `case_pack/data/`. Never change these files.
- **Your work:** the `outputs/` folder, which starts empty

## Files handed out during Day 1
Sessions D1-S06, D1-S07 and D1-S08 each start with a small ZIP file of ready-made code from the instructor
(`component_handout.zip`). Extract it into the course folder itself: in Windows **Extract All**, remove the
suggested `component_handout` folder name from the destination. Each ZIP contains everything that session needs,
so you can start it even if you did not finish the previous exercise.

## How the exercises work
This package does not include the instructor's solutions or answer files. An empty "YOUR TURN" cell or function
is intentional, not a broken installation. For each exercise: predict the result, make the change, check the output
and explain it, then ask for a worked answer if you need one. Use only the supplied synthetic data with AI tools;
never paste personal or confidential data.

Python in Excel (code inside a workbook cell, run in Microsoft's cloud) is different from local Python that writes
an Excel file. If you cannot use Python in Excel, work with someone who can and tell the instructor the error you saw.

You edit the starting files in `sessions/<session>/learner/` directly. To start an exercise again, extract that
file again from the course ZIP.
