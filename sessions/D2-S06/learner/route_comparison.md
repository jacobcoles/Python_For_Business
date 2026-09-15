# Three routes for the same Python step

Read this before Step 4 of the D2-S06 instructions.

| | Clean file from a script | Python step in Power BI Desktop | Python Script node in KNIME |
|---|---|---|---|
| Where Python runs | On the computer of whoever runs the script | Inside Power BI Desktop, using the Python set in its options | Inside KNIME, using its Python Integration environment |
| What comes out | A CSV file anyone can open | A table in the report's model | A table passed to the next node |
| What a colleague needs to use the result | Excel, or any tool that opens a CSV | Power BI Desktop, and the report file | KNIME, and the workflow |
| What a colleague needs to update it | Python, the script and the input files | Power BI Desktop **and** a working Python set up in it | KNIME with Python Integration, and the workflow |
| When the input file moves | Paths inside the course folder keep working | Change the source path in Power BI | Change the path in CSV Reader |
| Good when | The colleague only needs checked figures | The result is part of an existing Power BI report | The team already builds and maintains KNIME workflows |

A Python **visual** in Power BI is different from a Python **step**: the visual returns a picture, not a table.

Nothing in this session sets up automatic refresh. Publishing a report with Python steps to the Power BI service, or
scheduling it, needs separate setup and testing by your organisation.
