# Choosing a tool: one page

Pick the **simplest tool that the people who will maintain it can actually run**. Python is a
good choice when it adds clear value, not by default.

## Ask these four questions, in order
1. **Task fit:** Is this a one-off look, or a process that must run again next month?
2. **Maintenance:** Who changes it when the input changes? What can *they* use?
3. **Data access:** Where do the inputs live, and can this tool reach them?
4. **Handover:** Can someone else run it and see what was checked?

## What each tool is for in this course

| Tool | Good at | Watch out for | Where it runs |
|---|---|---|---|
| **Excel formulas / PivotTables** | Quick totals and summaries of one table someone already has open | Manual steps are hard to repeat and to evidence | The workbook |
| **Power Query (in Excel or Power BI)** | Repeatable import and reshaping, **including combining a folder of files with the same columns** [7] | Expects a dedicated folder "without extraneous files" [7]; business checks must be added deliberately | Excel / Power BI desktop |
| **Python in Excel** | Python analysis and charts on a table **inside the workbook** [3] | Runs in Microsoft's cloud; **cannot read local files or the internet** [2]; needs a qualifying licence [1] | Microsoft's cloud |
| **Local Python in VS Code** | Repeatable multi-step processes: controls, exception reports, writing a dated output from a template, calling an external data service | Needs a working local environment and someone who can read the code | Your machine |
| **Power BI** | Shared, interactive reporting on a modelled dataset | Python inside Power BI needs a local Python; scheduled refresh in the Power BI service needs a gateway, a connector your IT team installs [4, 5] | Desktop / service |
| **KNIME** | Visual, documented workflows for teams that prefer nodes to code | Python nodes use KNIME's own environment [6] | KNIME desktop |

**Several files on their own do not justify Python.** Power Query combines a folder of same-shaped
files well. Python adds clear value when the process also needs things like explicit controls with
exception detail, a release decision, a formatted handover output, or reuse by script.

**Two different "Python + Excel" routes (don't confuse them):**
- **Python in Excel:** code lives in cells, runs in Microsoft's cloud, reads the workbook only.
- **Local Python writing Excel:** code runs on your machine, reads files, writes a new `.xlsx`.

## "It depends" is a legitimate answer
If your team maintains Power BI, a clean file handed to Power BI may beat Python inside it.
If nobody on the team will read Python, a well-documented Power Query or KNIME workflow may be
the more sustainable choice even when Python would be faster to write.

Sources (Microsoft and KNIME documentation, checked September 2026):
[1] Python in Excel availability · [2] Open-source libraries and Python in Excel ·
[3] Introduction to Python in Excel · [4] Run Python scripts in Power BI Desktop ·
[5] Use Python in Power Query Editor · [6] KNIME Python integration: bundled packages ·
[7] Import data from a folder with multiple files (Power Query).
**These describe documented product capability, not what your organisation has enabled.**
