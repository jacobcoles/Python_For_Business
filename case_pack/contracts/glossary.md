# Glossary: the Northbridge case

Fictional case. If a definition here seems to differ from a participant guide, ask the instructor.
**Common mistake** marks the error people most often make.

**Account code:** The text code on every transaction that says what kind of income or cost it
is, e.g. `0400` Service revenue. There are seven. *Common mistake:* it is text, so `0400` is not `400`.

**Actual:** What really happened: the signed total of posted, mapped transactions for one
period, unit and report line (`actual_amount`). *Common mistake:* cancelled and unmapped rows are never in it.

**Baseline forecast:** Each future month set equal to the same month one year earlier, stated
with the last month of data it used. *Common mistake:* it is a simple starting point, not a prediction.

**Budget:** The planned amount for a period, unit and report line, stored with the same signs as
actuals. *Common mistake:* there is no budget row for operating result; it is worked out.

**Business key:** The three things that together identify one transaction: unit, period and
transaction id. *Common mistake:* a transaction id alone is not unique; other units reuse the same ids.

**Cancelled transaction:** A line with status `cancelled`. It is left out of every total but kept
in the file. *Common mistake:* a blank status is an error, not a cancellation.

**Check state:** The result of one control: `pass`, `fail`, `warning` or `not_run` (could not be
checked). *Common mistake:* `not_run` is never a pass and must never show as an empty cell.

**Control:** One of nine automatic checks (`C01`–`C09`) run before anyone believes a figure.
*Common mistake:* the thresholds are fictional teaching rules, and passing them is not an audit.

**Direct cost:** The cost of delivering the work itself: delivery cost and subcontractors
(`0500`, `0510`). Stored as a negative number.

**Display magnitude:** A cost shown as a positive number in a management table (stored value
× −1). *Common mistake:* same number, different label; never add a displayed value to a stored one.

**Entity / operating unit:** One of Northbridge's three reporting units, `N01`–`N03`, inside one
business. The data column is called `entity`. *Common mistake:* they are not separate legal companies.

**Exception:** One row in the exception list describing one specific problem, where it is
(file and row) and what to do next. *Common mistake:* an exception is a request for action, not a correction.

**Favourable variance:** Actual minus budget on the stored, signed amounts, for each period,
unit and report line. A plus result is better than budget on every line. *Common mistake:* it is not
overspend; "spent more than budget" has the opposite sign and must be labelled `expense_overspend`.

**Mapping:** The table that assigns each account code to exactly one report line.
*Common mistake:* a code listed twice silently doubles its transactions when the tables are joined.

**Movement:** The change in the same measure from the previous month, as an amount and as a
percentage of the previous month's size. *Common mistake:* if last month was zero the percentage is
`not_comparable`, never infinite.

**Operating result:** Revenue + direct cost + overhead, a plain sum because costs are already
negative. *Common mistake:* it is not net profit (no tax, interest or depreciation here), and it is never
stored as a line and added again.

**Overhead:** Running costs not tied to one piece of work: premises and administration
(`0600`, `0610`). Stored as a negative number.

**Period:** A reporting month written `YYYY-MM`, e.g. `2025-12`. *Common mistake:* always a fixed month,
never "last month".

**Posted:** The status meaning a transaction counts. Only posted rows enter totals.

**Provenance:** The record of where a figure came from: file and row for Northbridge data;
source, query and retrieval time for the OECD series.

**Reconciliation:** Comparing the posted total received with the total the unit says it sent; it
passes within EUR 0.01. *Common mistake:* it proves the file arrived intact, not that every row is usable.

**Refund:** Money given back to a customer: a negative amount on a revenue line.
*Common mistake:* it is less revenue, not a cost.

**Release status:** The verdict on the whole pack: `ready`, `ready_with_warnings` or `blocked`.
*Common mistake:* `blocked` is a correct outcome; it must not produce a workbook that looks approved.

**Report line:** One of three headings every account code maps to: `revenue`, `direct_cost`,
`overhead`. *Common mistake:* operating result is not a fourth report line.

**Reversal:** Part of a cost undone, such as a charge corrected after it was recorded: a positive
amount on a cost line. *Common mistake:* it reduces cost; it is not income.

**Revenue:** Income from selling services (`0400`, `0410`, `0420`). Stored as a positive number.

**Scenario:** The baseline multiplied by stated assumptions, e.g. revenue × 1.10. *Common mistake:* it is a
what-if; the range between scenarios carries no probability.

**Signed amount:** A number kept with its plus or minus sign exactly as stored: revenue plus,
costs minus. *Common mistake:* never strip the sign before adding.

**Source row:** The position of a line in its file, counting the first transaction as row 1 (the
header is not counted). Kept with the file name so any problem can be found.

**Tolerance:** The largest difference still treated as a match: EUR 0.01 for reconciliation.
*Common mistake:* a fictional teaching rule, not policy.

**Transaction:** One exported line in a unit's monthly file. *Common mistake:* a refund, a reversal and a
cancellation are each a transaction too.

**Unmapped account:** An account code with no row in the mapping table. It fails a control and
blocks the pack. *Common mistake:* never dropped, never put in "other".
