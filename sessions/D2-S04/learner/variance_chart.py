"""D2-S04: improve a variance chart for a board member. Instructions: sessions/D2-S04/D2-S04_instructions.md

Change the settings under YOUR CHOICES, save (Ctrl+S), run again, and reopen the PNG.
"""
# SUPPLIED: course setup. It lets this file find the course folder, so it works from the Run button or the
# terminal. You do not need to read or change these lines.
import os, sys
from pathlib import Path
COURSE_FOLDER = next(p for p in Path(__file__).resolve().parents if (p / "case_pack").is_dir())
os.chdir(COURSE_FOLDER)
sys.path.insert(0, str(COURSE_FOLDER))
ROOT = COURSE_FOLDER

import pandas as pd
from case_pack.course_tools.settings import require_true_or_false
import matplotlib
matplotlib.use('Agg')   # save the chart to a file instead of opening a window
import matplotlib.pyplot as plt

# ---- YOUR CHOICES: decide which settings help the board member. True/False need a capital letter, no quotes. ----
CHART_TITLE = "December 2025: variance contributions | all three units"   # keep the double quotation marks
SHOW_VALUE_LABELS = False
COLOUR_BY_SIGN = False
SHOW_NET_REFERENCE = False

for name, value in [("SHOW_VALUE_LABELS", SHOW_VALUE_LABELS), ("COLOUR_BY_SIGN", COLOUR_BY_SIGN),
                    ("SHOW_NET_REFERENCE", SHOW_NET_REFERENCE)]:
    require_true_or_false(name, value)

# SUPPLIED: everything below draws and saves the chart. Only the three 'delta' rows are contributions;
# the net reference is their sum, never an extra contribution.
data = pd.read_csv(ROOT/'case_pack/data/clean/analysis/variance_bridge_2025-12.csv')
deltas = data[data['kind'].eq('delta')].copy()
deltas['label'] = deltas['step'].str.replace(' vs budget', '', regex=False)   # labels come from the data
# YOUR TURN: ask Copilot for ONE line that sorts `deltas` so that the largest change comes first, using the size of
# 'value' and ignoring its sign. Paste it below this comment, run the file, and look at what changed.
# Prompt: "I have a pandas DataFrame called deltas with a numeric column 'value'. Give me one line that sorts it so
# the largest absolute value comes first, keeping all columns. Do not change any value."

# ---- end of YOUR TURN ----
values = deltas['value'].tolist()
labels = deltas['label'].tolist()
if SHOW_NET_REFERENCE:
    values.append(round(deltas['value'].sum(), 2))
    labels.append('Net variance\n(reference)')
colours = ['#2874a6' if v >= 0 else '#b14b39' for v in values] if COLOUR_BY_SIGN else ['#4979a4'] * len(values)
if SHOW_NET_REFERENCE:
    colours[-1] = '#595959'
fig, ax = plt.subplots(figsize=(10, 5.5))
bars = ax.bar(labels, values, color=colours)
if SHOW_NET_REFERENCE:
    bars[-1].set_hatch('//')
ax.axhline(0, color='#555555', linewidth=1)
ax.set_title(CHART_TITLE, fontsize=11, pad=15)
ax.set_ylabel('EUR, actual minus budget (positive = favourable)')
ax.yaxis.set_major_formatter(matplotlib.ticker.StrMethodFormatter('{x:,.0f}'))
# Allow room for labels using the actual plotted values, including zero.
span = max(max(values), 0) - min(min(values), 0)
padding = max(span * .25, 1)
ax.set_ylim(min(min(values), 0) - padding, max(max(values), 0) + padding)
if SHOW_VALUE_LABELS:
    for bar, value in zip(bars, values):
        word = 'favourable' if value > 0 else 'unfavourable' if value < 0 else 'no variance'
        ax.annotate(f'{value:+,.2f}\n{word}', (bar.get_x() + bar.get_width()/2, value),
                    xytext=(0, 7 if value >= 0 else -7), textcoords='offset points',
                    ha='center', va='bottom' if value >= 0 else 'top', fontsize=9)
fig.text(.08, .02, 'Fictional Northbridge data. A net reference summarises the contributions; it is not another contribution.', fontsize=8)
fig.tight_layout(rect=(0, .06, 1, 1))
out = ROOT/'outputs/D2-S04'
out.mkdir(parents=True, exist_ok=True)
fig.savefig(out/'variance_chart.png', dpi=160)
plt.close(fig)
print('Saved outputs/D2-S04/variance_chart.png')
expected = {'Revenue vs budget': -2972.11, 'Direct cost vs budget': 1778.66, 'Overhead vs budget': 924.31}
if dict(zip(deltas['step'], deltas['value'].round(2))) == expected:
    print('OK: the three amounts are unchanged; the bars are drawn in this order:', ', '.join(deltas['label']))
else:
    print('PROBLEM: the amounts have changed. Sorting may reorder the rows, but must never change a value.')
print(deltas[['step','value']].to_string(index=False))
print('Net variance:', round(deltas.value.sum(), 2), 'EUR')
