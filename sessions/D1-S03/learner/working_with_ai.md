# Working with AI on a job that takes more than one prompt: one page

The loop in D1-S03 (specify, generate, execute, inspect, correct, document) is one **step** of a real job.
A month-end run, or your project on Days 3 and 4, is ten or twenty of them. This page is about holding that together.
Keep it open alongside `specification_template.md`, which covers what to write in a single prompt and what never to
paste into a chat.

## 1. Split the job before you ask for anything

List the steps first, in business terms, before any code exists. A step belongs on the list when you can say
both of these about it:

- **what it does**, in a sentence a colleague would understand;
- **what it gives back**, which is the thing you can then look at and check.

D1-S08 shows what the finished list looks like: six rows, each one line of Python, each producing something
checkable. You were given that list. On your own work you write it, and it is the most valuable ten minutes of the
job. If you cannot say what a step gives back, it is not one step yet: split it.

Then work one step at a time. Get step one right and checked before asking for step two. A long generated script
that does everything at once is fast to produce and slow to trust.

## 2. The chat does not remember, and does not see your files

Microsoft 365 Copilot Chat knows only what is in the current conversation. It has not seen your data, your folders
or what your last run printed, unless you paste it in. So each prompt carries its own facts: the column names, the
rules that matter, and what you already have in the file.

**Start a new chat when:**

- you move to a different step of the job, and the earlier detail no longer matters;
- the answers have started drifting back to an earlier version of the task, or contradict something agreed twenty
  messages ago;
- you are about to switch data sources, tools or periods.

Before you close a long chat, copy the two or three lines you actually kept into your working record (below).
Everything else in the conversation is scaffolding.

## 3. Keep a working record

One small file beside your work, added to as you go. On Days 3 and 4 it is `worklog.md` in your project
folder. Three columns, one line per step:

| What I asked for | What I kept | What I checked |
|---|---|---|
| N01's December operating result from the eight-row file, posted rows only | The five-line block now in `my_total.py` | Printed the rows used: 7, T008 not among them, total 720.00, matches my prediction |

It takes fifteen seconds per step and it is the only way to write an honest handover note two days later. The
headings in `case_pack/starters/handover_note_template.md` are answered almost entirely from this table, in
particular "what I checked, and how".

## 4. Two prompts worth using every time

Both are cheap, and both work better before you have code than after.

**Let it question you.** Paste your specification or plan and ask:

> Before you write any code: list up to three things in this specification that are ambiguous, missing or
> contradictory, and ask me about them. Do not write code yet.

A near-beginner's specification usually leaves out the thing that matters most, and this is how you find out which.
Answer the questions in the specification itself, so the next person reads a complete one.

**Ask it to argue against its own answer.** After it gives you code or a recommendation:

> What would make this wrong? List the assumptions you made, and the cases where this code would give a plausible
> but incorrect answer.

Treat the reply as a list of things to test, not as a verdict. It is a second pair of eyes, not evidence. Only your
own run against a figure you worked out yourself is evidence, and an assistant will sometimes defend a claim your
run has already disproved.

## 5. Plan up front, adjust as you go

Settle these before you start, because changing them later means redoing the checks:

- the question and who the answer is for;
- the inputs, and what one row means;
- the one figure you will check without trusting your code.

Leave these to be decided as you go: how the code is organised, which library does what, how the output is
formatted, and whether a step needs splitting. When something does change, write one line in the working record
saying what changed and why. That line is what stops the same rethinking happening twice.

## 6. When to stop asking and check it yourself

Three exchanges on the same error is the signal. Go back to something you can see: print the rows actually used,
open the file, count something by hand. Then ask again with that fact in the prompt. Nearly every long, circular
conversation is the assistant guessing at something you could have looked up in ten seconds.
