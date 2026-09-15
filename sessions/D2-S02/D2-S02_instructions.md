# D2-S02: Euro-area inflation from the OECD

**Was euro-area inflation higher than Sweden's, and how current is that figure?**

09:25 to 10:30, 65 minutes. **Tool: a Jupyter notebook in VS Code**, because you look at the response in stages
before trusting it.

**You will produce:** in `outputs/D2-S02/`, a checked table (`context.csv`), the response exactly as received
(`response.sdmx.json`), a source record (`source_record.json`) and your answer (`answer.md`).

**All the steps are in the notebook.** This page tells you what you are working with and how to start.

## The question

Northbridge's largest subcontractor invoices from Sweden, so the manager keeps Swedish and euro-area consumer prices
side by side as background when reading the monthly pack. This month the question is: **was consumer-price inflation
in the euro area higher or lower than in Sweden in December 2025, was December typical, and how current is that
figure?**

It is background only. It does not explain Northbridge's own costs and is not a forecast input.

## Data and files

| File (paths start at the course folder) | What it is |
|---|---|
| `sessions/D2-S02/learner/query_notebook.ipynb` | The notebook with every step |
| `case_pack/data/external/oecd_data_dictionary.md` | What each field of the OECD series means |
| `case_pack/data/external/raw/oecd_prices_c2018_hicp_swe_ea.sdmx.json` | A response saved on 2026-09-13, used when you work offline |

## Rules for this task

- Compare the same month and the same measure for both places.
- The value is the percentage change in consumer prices compared with the same month a year earlier. It is not a
  euro amount and not a monthly rise.
- The difference between two percentages is in **percentage points**.
- A saved response keeps its original retrieval time. Never label it as live.
- Do not change anything in `case_pack/data/external`.

## How to start

1. In VS Code choose **File > Open Folder** and open the course folder.
2. Open `sessions/D2-S02/learner/query_notebook.ipynb`.
3. Choose the course **`.virtual-env-folder`** kernel at the top right of the notebook.
4. Open Microsoft 365 Copilot Chat in your browser.
5. Follow the notebook from Step 0 to Step 9.

## What the notebook asks of you

| Notebook step | What you do | How you know it worked |
|---|---|---|
| 1 and 2 | Read what an API is and what the number means | You can say what 2.1 means, including its unit |
| 3 (YOUR CHOICE) | Choose the months to request | The endpoint, parameters and expected row count print |
| 4 | Get the response: saved, or live after the demonstration | Status 200 and the retrieval time print |
| 5 | Look at the raw response and decode one number by hand | You can explain the key the cell decodes, such as `0:0:0:0:0:0:0:0:0` |
| 6 | Turn it into a table | Three **OK** lines |
| 7 (YOUR TURN) | Ask Copilot to put Sweden and the euro area side by side, with the gap | Two **OK** lines |
| 8 | Save the table with its source record | Three files saved |
| 9 | Write your answer, then check it | Your answer names the gap, whether December was typical, and live or cached |

## If something goes wrong

| What you see | What to do |
|---|---|
| `Open the course folder in VS Code` in Step 0 | Use **File > Open Folder** and choose the course folder |
| `ModuleNotFoundError` | Choose `.virtual-env-folder` in the kernel picker |
| `NameError` (for example `request` is not defined) | Run the earlier cells again from Step 0 |
| `PROBLEM: START and END must be between ...` | Use months from `"2024-01"` to `"2026-01"` |
| `SyntaxError: leading zeros in decimal integer literals...` | A month lost its quotation marks. Write `START = "2025-09"` |
| `PROBLEM: write the months as text with quotation marks` | Same cause: months are text, so they need quotation marks |
| `LIVE REQUEST FAILED` | Record the message, set `MODE = "offline"`, run that cell again, and continue |

**Start again:** choose **Restart** in the notebook toolbar and run from Step 0.
