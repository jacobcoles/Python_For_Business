# D1-S01 participant guide: where we are going

**25 minutes.** No installation and no code.

## Before the session (pre-read, about 7 minutes)
Read `case_pack/contracts/business_primer.md`. It uses eight rows from a fictional company to show
why costs are stored as negative numbers, what a cancelled line does, and what a favourable
variance means. The key points are also covered on the slides, but reading it first makes D1-S03 easier.

## The case
**Northbridge Business Services** is a fictional support, training and advisory business with three units.
You are its operations analyst. Every month the units send transaction exports. You combine them,
check them, compare them with budget and produce a management pack that someone else can rerun.
The full story is in `case_pack/contracts/story.md`.

## The result we are aiming for
A monthly pack that is **checked** (controls with exceptions and a release decision), **rerunnable**
next month, and **handed over** with a note saying what was checked and what its known limitations are.
Code is a means to that, not the goal.

## The working loop you will use all week
```
specify -> generate -> execute -> inspect -> correct -> document
```
You describe the requirement to Microsoft 365 Copilot Chat, copy the code it suggests
into VS Code, run it on your machine, check the result against known figures, correct it, and write
down what you did.

## Choosing a tool
Keep `sessions/D1-S01/learner/tool_choice_aid.md` open all week. In short: choose the
simplest tool that the people who maintain the process can run.

## Discussion (5 min, in pairs)
Read the three scenarios in `sessions/D1-S01/learner/scenarios.md`. For each one, agree which tool you would
recommend and the deciding reason, ready to discuss with the group.

## By the end of this session you can
- describe what the finished pack contains and why it is checked;
- explain why the eight rows give 720.00 and not 1,719.00;
- recommend a tool for a reporting task and justify the choice.
