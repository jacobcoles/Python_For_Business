# Audit exceptions in Python

The job is in `README.md`. This is how to build it.

**Tool:** a Python script in VS Code, with Microsoft 365 Copilot Chat for the code.
**You will produce:** `delivery_summary.csv`, `all_exceptions.csv` and `action_note.md` in your own project folder.

## Start here

1. In the VS Code Explorer, right-click `outputs` > **New Folder**, name it `projects` if it is not there. Right-click
   `outputs/projects` > **New Folder**, name it after your project, for example `december_audit`.
2. Right-click `worked_example.py` in this folder > **Copy**, then right-click your folder > **Paste**.
3. Open your copy and click **Run Python File**.

**You should see** a six-row table ending:

```text
Check: clean delivery released as ready: yes
```

and a line starting `Saving into:` with your own folder's full path.

That is the finished result. The rest of this page explains how it gets there.

## Step 1: list the deliveries

The setting at the top is a dictionary: folder on the left, reporting period on the right.

```python
DELIVERIES = {
    "case_pack/data/clean": "2025-12",
    "case_pack/data/faulty/F01_missing_source": "2025-12",
    ...
}
```

To add a delivery, add a line. Everything else adapts. Keep the period with the folder rather than assuming it,
because a delivery for a different month is exactly the kind of thing this process should catch.

## Step 2: run the nine checks over each one

**Why:** the checks are not yours to write. They are supplied, they are the same nine every month, and running them
unchanged over every delivery is the whole point. Rewriting them per delivery would defeat it.

Two supplied functions do the work:

```python
inputs = northbridge.load_inputs(folder, period)
controls, exceptions, release = northbridge.run_controls(inputs)
```

`controls` is a table of nine rows with a `status` each. `exceptions` is the detail. `release` is one of `ready`,
`ready_with_warnings` or `blocked`.

**Ask Copilot** if you want to build the loop yourself:

> I have a dictionary `DELIVERIES` of folder path to period string. For each entry, call
> `northbridge.load_inputs(folder, period)` then `northbridge.run_controls(inputs)`, which returns three things:
> a controls DataFrame, an exceptions DataFrame and a release string. Collect the results into a list. Do not
> change the two function calls and do not write your own checks.

## Step 3: one summary row per delivery

The row needs the delivery name, the period, the release decision, the checks that did not pass, and how many
exceptions there were. The awkward part is the third one: several checks can fail at once, and a list inside a
table cell is unreadable.

```python
not_passing = controls.loc[controls["status"] != "pass", ["check_id", "status"]]
"checks_not_passing": ", ".join(f"{c} {s}" for c, s in not_passing.itertuples(index=False)) or "none"
```

**Read that carefully.** It tests `!= "pass"`, not `== "fail"`. A check that could not run is not a pass, and a
summary that only counts failures would call F01's delivery clean apart from one problem, when in fact three
checks never ran at all.

## Step 4: combine the exceptions, keeping the source

**Why:** this is the step the whole track turns on. Six exception tables combined without labels is one useless
table.

```python
all_exceptions.append(exceptions.assign(delivery=name))
```

`assign` adds the column as the table goes into the list, before anything is combined. Add it afterwards and you
no longer know which rows came from where.

## Step 5: confirm nothing faulty slipped through

**You should see:**

```text
Check: clean delivery released as ready: yes
Check: release decision for each faulty delivery (only a warning may still be released): F01_missing_source
blocked, F02_duplicate_record blocked, F04_unmapped_account blocked, F07_large_genuine_movement
ready_with_warnings, F08_wrong_currency blocked
```

**F07 is released.** That is correct, and it is the most important line on the page. Its movement is large but
genuine, so the check raises a warning rather than a failure, and a warning does not stop a release. If your
process blocks F07, it is too strict and units will start ignoring it.

## Step 6: decide what to chase first

Right-click your project folder > **New File**, name it `action_note.md`, and write under these headings:

```text
The delivery I would chase first, and why:
The evidence for it (delivery, check, unit, file, row or amount):
A delivery that is blocked but is not the units' fault:
Why F07 is released even though something changed a lot:
Message to one unit:
```

A useful message names the delivery, the check, and the row or amount, and asks the unit to confirm a correction.
It does not correct their export for them.

## Check your result

| Delivery | Release | Checks not passing | Exceptions |
|---|---|---|---:|
| clean | `ready` | none | 0 |
| F01_missing_source | `blocked` | C01 fail, C02 not_run, C08 not_run, C09 not_run | 1 |
| F02_duplicate_record | `blocked` | C02 fail, C03 fail, C08 fail, C09 not_run | 4 |
| F04_unmapped_account | `blocked` | C05 fail, C09 not_run | 1 |
| F07_large_genuine_movement | `ready_with_warnings` | C09 warning | 1 |
| F08_wrong_currency | `blocked` | C07 fail, C09 not_run | 1 |

8 exception rows in total. F02 produces 4 from three failing checks: C02 the row count, **C03 twice** because a
duplicate is reported by listing every copy, and C08 the total. One repeated transaction, four pieces of evidence.

## Done when

All six deliveries appear with the decisions above, every exception row names its delivery, and your note picks a
first case with evidence behind it.

## If something goes wrong

| What you see | What to do |
|---|---|
| `FileNotFoundError` naming a faulty folder | Check the folder name against `case_pack/data/faulty/`; they are case-sensitive |
| One delivery missing from the summary | An entry in `DELIVERIES` is missing its comma, so two keys merged |
| `KeyError: 'delivery'` when reading the exceptions | The column was added after combining rather than before |
| Every delivery shows `blocked` | Look at the clean one first: if that is blocked too, the input folder is wrong |
| The exception count is 0 everywhere | You are reading `controls` where you want `exceptions` |

**Start again:** delete your copy and paste `worked_example.py` again. The six delivery folders never change.
