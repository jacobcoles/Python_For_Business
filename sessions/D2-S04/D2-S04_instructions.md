# D2-S04: A chart the board can read

**Can the board understand the budget shortfall?**

11:30 to 12:15, 45 minutes. **Tools: a Python script in VS Code for the chart, and Excel for comparison.** The script
makes a chart that can be reproduced exactly every month; Excel shows what a standard chart already offers.

**You will produce:** `outputs/D2-S04/variance_chart.png` and a short conclusion, `outputs/D2-S04/conclusion.md`.

## The situation

December's operating result was below budget. A board member looks at a plain bar chart of the three contributions
and cannot quickly tell which ones helped, which hurt, or what they add up to. Improve the chart for that reader, and
decide whether this team needs Python for the job at all.

## Data you will read

`case_pack/data/clean/analysis/variance_bridge_2025-12.csv` (paths start at the course folder): December 2025, all
three units, EUR. It has five rows:

| step | kind | value EUR | cumulative EUR |
|---|---|---:|---:|
| Budget operating result | total | 67,600.00 | 67,600.00 |
| Revenue vs budget | delta | -2,972.11 | 64,627.89 |
| Direct cost vs budget | delta | +1,778.66 | 66,406.55 |
| Overhead vs budget | delta | +924.31 | 67,330.86 |
| Actual operating result | total | 67,330.86 | 67,330.86 |

`delta` means a change from budget. `total` rows are the starting and ending results, not contributions.

## Files you will open or run

| File | What it is for |
|---|---|
| `sessions/D2-S04/learner/variance_chart.py` | Draws the chart. You change settings at the top only |
| `sessions/D2-S04/learner/excel_comparison.xlsx` | The same three figures as a standard Excel chart |

## Rules for this task

- Variance means actual minus budget, on signed amounts. Positive is favourable. For a cost,
  `-90 - (-100) = +10`: spending was 10 below budget, which is good.
- The chart shows the three contributions. Their sum (the net) is a summary, never a fourth contribution.
- Keep a zero line and the units. Colour must not be the only way to tell good from bad (printouts are often black
  and white).
- A chart shows how the arithmetic splits; it does not show **why** sales or costs changed.

## How to run the script

Open `variance_chart.py` and click **Run Python File** (the triangle at the top right), or paste into
**Terminal > New Terminal**:

```powershell
.\.virtual-env-folder\Scripts\python.exe sessions\D2-S04\learner\variance_chart.py
```

No chart window opens: the chart is saved as a picture. Open it from the Explorer. After a rerun, close and reopen
the picture tab to see the new version.

## Steps

### Step 1: Run the starting chart (5 minutes)

**Do:** run the script, then open `outputs/D2-S04/variance_chart.png`.

**You should see:** `Saved outputs/D2-S04/variance_chart.png`, the three amounts and `Net variance: -269.14 EUR` in
the terminal, and three plain blue bars in the picture.

Create your notes file: right-click the `outputs/D2-S04` folder in the Explorer, choose **New File**, name it
`conclusion.md`. Write one sentence: what would the board member misread in this chart?

### Step 2: Choose settings for this reader (12 minutes)

**Why:** each setting fixes a different misunderstanding. Choose the ones that fix the problem you wrote down.

| Setting | Changing False to True | Fixes |
|---|---|---|
| `SHOW_VALUE_LABELS` | Writes each amount and the word favourable or unfavourable on its bar | Direction and size are unclear, including in black and white |
| `COLOUR_BY_SIGN` | Colours helpful and harmful changes differently | Faster scanning on screen; not enough on its own for a printout |
| `SHOW_NET_REFERENCE` | Adds a hatched bar showing the net of the three | The reader cannot see the overall result |

You can also replace the text in `CHART_TITLE` with a title that states the finding. Keep the double quotation
marks around it; an apostrophe inside the title is then fine.

**Before you change anything,** add to `conclusion.md` which setting you expect to help most, and why.

**Do:** change your chosen settings, save with **Ctrl+S**, run, and reopen the picture. `True` and `False` start with
a capital letter and have no quotation marks. You may try several combinations.

If you want a second opinion, ask Copilot:

> A board member cannot tell from a bar chart which of three budget variances were favourable, or what they add up to.
> The contributions are revenue -2,972.11 EUR, direct cost +1,778.66 EUR and overhead +924.31 EUR, and the chart may
> be printed in black and white. My options are: value labels with the words favourable/unfavourable, colour by sign,
> and a separate net reference bar. Which combination would you recommend and what is one trade-off? Do not change
> any amounts or suggest reasons for the variances.

Decide for yourself after reading the advice.

### Step 3 (YOUR TURN): Order the bars, and see whether it helps (5 minutes)

**Why:** a board reader looks for the biggest item first. Whether sorting helps depends on the data, and finding that
out is part of the judgement.

**Do:** in the script, find `YOUR TURN` above the chart code, copy the prompt beside it into Copilot, paste the single
line it gives you, save and run.

**You should see:** `OK: the three amounts are unchanged; the bars are drawn in this order: ...`. Compare the picture
with the one before. If nothing moved, that is a real finding, not a failure: say why in your conclusion.

### Step 4: Check your chart (8 minutes)

**Why:** a clearer chart is worthless if it shows the wrong numbers.

**Do:** compare each amount in the picture with the table above. With a calculator, check that the three
contributions add up to the net, and that the budget plus the net equals the actual result. Read the smallest text
at normal size. Would the board member now read direction and overall result correctly, even printed without colour?
If not, change a setting and run again.

### Step 5: Compare with Excel (8 minutes)

Open `sessions/D2-S04/learner/excel_comparison.xlsx`. It shows the same three figures as a standard Excel chart.
Look for two minutes, then add to `conclusion.md`: **could this Excel chart serve the board with less maintenance, or
does your Python chart give a specific improvement? Name the difference you actually see.**
Power BI and KNIME are compared in D2-S06.

### Step 6: Finish your conclusion (7 minutes)

Complete `conclusion.md` under these headings:

```text
The misreading I wanted to prevent, and the settings I chose:
Whether sorting the bars changed anything, and why:
Did it work? What I checked:
The net result against budget, in one sentence:
Excel or Python for this board, and why:
What this chart does not prove:
```

## Check your result

After you have written your conclusion:
- -2,972.11 + 1,778.66 + 924.31 = **-269.14**, and 67,600.00 - 269.14 = **67,330.86**.
- Revenue is the only unfavourable contribution. The two cost lines together offset EUR 2,702.97 of it, leaving
  the result EUR 269.14 below budget.
- Value labels with words are the setting that still works in black and white.
- "Revenue contributed most to the shortfall" is supported by the chart. "Revenue fell because of weaker demand" is not.

## Done when

Your chart shows the correct amounts, fixes the misreading you named, and your conclusion gives a reasoned tool choice
and one limit.

## If something goes wrong

| What you see | What to do |
|---|---|
| `SyntaxError: unterminated string literal` | The title lost a quotation mark. Keep the double quotation marks at both ends |
| `STOPPED: ... is the text "False"` | A True/False setting was given quotation marks. Write `True` or `False` with a capital letter and no quotation marks |
| `NameError: name 'true' is not defined` | `True` and `False` start with a capital letter |
| The picture did not change | Save the script (a dot on its tab means unsaved), run again, then close and reopen the picture tab |
| An amount looks different from the table | Undo edits outside the settings (Ctrl+Z), save and run again. Never edit the CSV |

**Start again:** restore `variance_chart.py` from the course download and run it.

**Optional extension:** `case_pack/data/clean/analysis/unit_comparison_2025-12.csv` has the variance split by unit.
Sketch on paper a chart that answers "which unit caused the shortfall?", including its title and what the bars mean.
