# Control catalogue and release rules — Northbridge shared case pack

**Version:** `v0.1-draft`. **Owner:** coordinator.
These thresholds are **fictional teaching assumptions**, not financial policy. Every learner-facing
asset that shows them must say so. Proposing a change goes through W4.

## Check states and release decision (DEC-19)

Individual check state — one of exactly four:

| state | meaning |
|---|---|
| `pass` | The check ran and the condition held |
| `fail` | The check ran and the condition did not hold |
| `warning` | The check ran and found something a human should look at, but which does not invalidate the figures |
| `not_run` | The check could **not** be evaluated — missing input, unavailable reference, error |

`not_run` is **never** a pass. An absent check must never render as a blank cell that reads like
success; it renders as `not_run` with the reason.

All nine controls C01–C09 are **required** for this teaching pack (DEC-24).
Thus an unavailable prior-period comparison blocks release even when C01–C08 pass;
an evaluated movement warning permits `ready_with_warnings`.

Release decision, evaluated in this order:

```
if any check with severity=critical has state == "fail":            release = "blocked"
elif any check with required=true has state == "not_run":           release = "blocked"
elif any check has state == "warning":                              release = "ready_with_warnings"
else:                                                               release = "ready"
```

A `blocked` run **still writes its diagnostics** — the control summary and the exception detail —
but must **not** write an apparently approved management workbook. An unresolved `warning` stays
visible in the pack; it is not cleared by rerunning.

## Control summary schema (`control_summary.csv`)

| column | type | meaning |
|---|---|---|
| `check_id` | string | `C01`..`C09` |
| `check_name` | string | Short readable name |
| `severity` | string | `critical` or `review` |
| `scope` | string | What was evaluated, e.g. `2025-12` or `2025-12/N02` |
| `expected` | string | The expected value or condition, as text |
| `observed` | string | What was actually found, as text |
| `tolerance` | string | The tolerance applied, or `n/a` |
| `status` | string | `pass` / `fail` / `warning` / `not_run` |
| `affected_count` | integer | Number of distinct affected **objects** for this check (0 when none) — see *Counting rule* below |
| `detail_ref` | string | Key into `exceptions.csv`, or empty |

## Exception detail schema (`exceptions.csv`)

| column | type | meaning |
|---|---|---|
| `check_id` | string | The check that raised it |
| `severity` | string | `critical` or `review` |
| `source_file` | string | File name, or empty when the defect is the **absence** of a file |
| `source_row` | integer | 1-based data row, or empty when not row-level |
| `entity` | string | Where known |
| `period` | string | Where known |
| `transaction_id` | string | Where known — may be empty for a missing/blank key |
| `issue` | string | What is wrong, in business language |
| `observed_value` | string | The offending value |
| `expected_value` | string | What was required |
| `action_note` | string | What the analyst should do next |

When the business key is itself corrupt or blank, the record is located by `source_file` +
`source_row`. That is why ingestion must attach those two columns (`schemas.md` section 3).

### Counting rule for `affected_count` (DEC-23)
`affected_count` counts the distinct things the check is *about*; the exception detail may list more
rows than that.

| Check | One unit of `affected_count` is |
|---|---|
| `C01` | a missing expected file |
| `C02`, `C08` | a failing `(period, entity)` scope |
| `C03` | a distinct duplicated business key (both occurrences appear in the detail) |
| `C04` | a distinct account code with more than one mapping row |
| `C05`, `C06`, `C07` | an offending source row |
| `C09` | a warned `(entity, report_line)` |

---

## The nine controls

### C01 `completeness_files` — severity **critical**
Every `(period, entity, filename)` row in `expected_files.csv` for the reporting period has a
corresponding file present in the input folder.
- **Pass:** every expected file present.
- **Fail:** one or more expected files missing. One exception row per missing file, with
  `source_file` = the expected filename and `issue` = "expected export not received".
- **not_run:** `expected_files.csv` itself is missing or unreadable.

**This check cannot be satisfied by an aggregate.** A clean-looking total proves nothing about a
file that was never delivered. Fixture-scoped: the tiny fixture's manifest lists **N01 only**.

### C02 `completeness_rows` — severity **critical**
Per `(period, entity)`: raw row count equals `expected_raw_rows`, and posted row count equals
`expected_posted_rows`, from `source_controls.csv`.
- A row counts as posted only if its `status` is **exactly** `posted`. A blank or unknown status is
  therefore not counted, and the posted count genuinely differs from what the unit says it sent:
  that is a `fail` here **as well as** a `C06` failure (DEC-23).
- **Fail:** either count differs. `observed`/`expected` carry both numbers.
- **not_run:** `source_controls.csv` missing, no control row for that `(period, entity)`, or the
  expected source file for that scope is **missing** (reason: "source file missing — see C01").

### C03 `duplicate_business_key` — severity **critical**
No duplicate on the **full** business key `(entity, period, transaction_id)` across all loaded
rows, **including cancelled rows** (the raw key is unique even for cancelled records in clean data).
- **Fail:** one exception row per duplicated key occurrence, each carrying its own
  `source_file`/`source_row` so both sides of the duplicate are visible.
- **No silent de-duplication.** Dropping duplicates to make the count match is a defect.
- Checking `transaction_id` **alone** is wrong: the same ID may legitimately occur in a different
  unit. That false positive is a registered teaching point.

### C04 `mapping_cardinality` — severity **critical**
`account_mapping.csv` has **exactly one** row per `account_code`.
- **Fail:** any code appearing more than once. `affected_count` = number of offending codes.
- **Must be evaluated before the mapping join.** A duplicated mapping row multiplies transaction
  rows in a many-to-one join and silently inflates totals; detecting it afterwards means the
  inflated figure may already have been believed.

### C05 `unmapped_accounts` — severity **critical**
Every posted transaction's `account_code` resolves to a row in `account_mapping.csv`.
- **Fail:** one exception row per unmapped **source row**, with `source_file`, `source_row`,
  `transaction_id` and the offending `account_code`.
- Unmapped rows are **never** dropped, never bucketed into "other", never defaulted to `overhead`.
- The unmapped **amount** must remain visible in the exception detail so its size is known.

### C06 `required_values` — severity **critical**
For every loaded row: `transaction_id`, `period`, `entity`, `account_code`, `amount`, `currency`,
`status` are non-blank; `amount` parses as a number; `status` is exactly `posted` or `cancelled`;
`period` matches the filename period; `entity` matches the filename entity.
- **Fail:** one exception row per offending source row, naming the offending column.
- A blank `status` is **not** an implicit cancellation. A blank `amount` is **not** zero.

### C07 `currency_supported` — severity **critical**
Every loaded row has `currency == "EUR"`.
- **Fail:** one exception row per offending source row.
- **No conversion is attempted, ever.** There is no rate in this pack and guessing one would be
  fabrication. The correct analyst action is to return the row to the unit that exported it.

### C08 `reconciliation_posted_amount` — severity **critical**
Per `(period, entity)`: the signed sum of `amount` over **every row with `status == "posted"`,
exactly as exported**, equals `expected_posted_amount` from `source_controls.csv`.
- **Tolerance:** `abs(difference) <= 0.01` EUR passes (DEC-18).
- **Fail:** difference beyond tolerance. `observed`, `expected` and the signed difference are all
  reported.
- **not_run:** no control row for that `(period, entity)`, the expected source file for that scope
  is **missing** (see `C01`), **or** any value needed to form the total is
  unusable — a blank or unparseable `amount`, or a blank or unknown `status` (the row cannot be
  classified as posted or not; see `C06`). A total that cannot be computed is
  `not_run` with the reason, **never** a pass and never a sum that quietly treats blank as zero.

**Scope note — this is a file-integrity check, not a business-validity check.** It is deliberately
computed *before* currency filtering and *before* the mapping join, over the rows as received. It
answers one question: "did we receive intact what the unit says it sent?"
That is why an unsupported-currency row (`C07`) or an unmapped account (`C05`) fails its own check
while `C08` still passes — each defect is visible in exactly one place instead of cascading. A
duplicated record (`C03`) does change the received total, so `C08` fails alongside it; controls are
allowed to overlap when the underlying defect genuinely affects both.

`source_controls.csv` is generated from the **pre-corruption truth** and is never updated by a
faulty variant. That independence is what gives the check its power.

### C09 `movement_review` — severity **review** (produces `warning`, never `fail`)
Per `(entity, report_line)`, current reporting period vs the immediately prior period, on
`actual_amount` (signed, posted, mapped).
- **Warning when:** `abs(current - prior) > 100.00` **AND** `abs(movement_pct) > 0.20`.
  Both comparisons are **strict** `>`. A movement of exactly EUR 100.00, or of exactly 20.0%, does
  **not** warn — that boundary is deliberately exercised by a fixture.
- **`prior == 0` special case:** if `abs(current) > 100.00`, raise a warning with
  `issue = "new activity — no prior-period comparison"`, `observed_value` = the absolute movement,
  and `movement_pct` reported as **`not_comparable`**. Never infinity, never a fabricated percent.
- **not_run:** prior-period actuals unavailable, **or any of `C01`–`C08` is not `pass`** for the
  reporting period (DEC-23). Movement is reviewed only on figures that passed every critical control;
  reviewing movement on unmapped, duplicated or unreconciled figures produces warnings that mean
  nothing — for example, dropping F10's unmapped rows would raise a false −30.16% warning on N02
  revenue. One period-wide `C09` summary row, `affected_count` 0, reason stated in `observed`.
- A warning is a **request to look**, not a correction instruction. A large, genuine, fully
  reconciled movement stays a warning and the pack releases as `ready_with_warnings`. Inventing a
  data correction to silence it is a defect.

---

## Fixtures and expected reactions
The named fixtures (`data/faulty/`, `data/clean/boundary/`) and their expected control reactions are
**instructor-only** and live in `case_pack/validation/control_fault_map.md`, with the observed detail
in `case_pack/validation/fault_manifest.csv`. They are kept out of this file because this contract
ships to learners and the reactions are the answers to the D1-S06 and D1-S08 exercises (W4-07).

Cancelled rows, revenue refunds and cost reversals occur in `data/clean/` as ordinary business facts
and are proven by the tiny oracle and by `C02`'s posted-row count, not by a fault fixture.

## A blocked run is a correct outcome
When a control fails, the process has worked. The learner deliverable in that case is: the control
summary, the exception detail, and a written statement of what is wrong and what they would do —
**not** a workbook that looks approved. D1-S08 depends on this: its named fault should block the
pack, and a supplied clean recovery copy is then used to practise workbook creation.
