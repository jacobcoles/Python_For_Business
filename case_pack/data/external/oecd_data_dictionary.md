# Data dictionary: `oecd_context_tidy.csv`

**For learners (D2-S02):** you only need the five fields the notebook lists: `ref_area_name` (the place),
`period` (the month measured), `value` (the change in consumer prices over one year, in percent), `unit_label`
and `retrieved_at_utc` (when it was downloaded). The rest of this page is reference detail for anyone adapting the
series to another source; you do not need it for the session.

---


External management context for Northbridge Business Services. **Context only** — this series is
published inflation background. It is *not* a forecast input and must not be joined into the
Northbridge planning model.

- **Source:** OECD public SDMX API (`sdmx.oecd.org`), dataflow
  `OECD.SDD.TPS:DSD_PRICES_COICOP2018@DF_PRICES_C2018_ALL(1.0)` — *Consumer price indices
  (CPIs,HICPs), COICOP 2018*.
- **Series adopted:** `SWE+EA.M.HICP.CPI.PA._T.N.GY` — 2 series, 25 monthly periods each,
  **50 rows**, period range **2024-01 … 2026-01**.
- **Grain / primary key:** one row per `(series_key, period)`.
- **File format:** UTF-8 CSV, comma separated, `\n` line endings, header row, no thousands
  separators, decimal point.
- **Full provenance:** `oecd_source_metadata.json`. **Expected invariants:** `invariants.json`.
- **Frozen contract:** the column list below is fixed and is consumed unchanged by **D2-S02** and
  **D2-S03**. Do not add, remove or reorder columns without going through the coordinator.

---

## What the endpoint actually returns (read this before parsing)

The OECD endpoint does **not** return a flat list of records. There is no `[{...}, {...}]`
anywhere in the response. It returns an **SDMX-JSON 2.0 data message**, which is a compressed,
code-book-style structure:

```
{
  "meta":   { "schema": ..., "id": ..., "prepared": "2026-09-13T18:26:43Z", ... },
  "data": {
    "structures": [ {                    <- the code book
        "dimensions": { "observation": [ {"id":"REF_AREA","name":"Reference area",
                                          "values":[{"id":"EA","name":"Euro area"},
                                                    {"id":"SWE","name":"Sweden"}]},
                                         ... 8 more, TIME_PERIOD last ] },
        "attributes": { "observation": [ {"id":"DECIMALS",...}, {"id":"OBS_STATUS",...} ] } } ],
    "dataSets": [ {
        "observations": { "1:0:0:0:0:0:0:0:24": [2.1, 0, 0], ... } } ]   <- the data
  },
  "errors": []
}
```

Each **key** in `observations` is a `":"`-joined list of *positions* into the `values` arrays of
`structures[0].dimensions.observation`, in order. Each **value** is an array whose first element
is the observation value and whose remaining elements are positions into the observation
attributes. So `"1:0:0:0:0:0:0:0:24": [2.1, 0, 0]` decodes as
`REF_AREA[1]=SWE`, `FREQ[0]=M`, … `TIME_PERIOD[24]=2025-12`, value `2.1`,
`DECIMALS[0]="Two"`, `OBS_STATUS[0]="Normal value"`.

Three consequences that matter:

1. **The response already carries the English names.** Every dimension value in
   `structures[0]` has both an `id` and a `name`, taken from the same official OECD code lists as
   the structure message. You do not have to guess what `GY` means, and you must not.
2. **The `TIME_PERIOD` values array is not in chronological order.** In the saved snapshot it
   begins `2025-04, 2025-09, 2025-08, 2024-05, 2024-01, …` and ends `2026-01, 2025-12`.
   Never assume position order equals time order — read the period out of the `values`
   entry, then sort the rows yourself. `fetch_oecd.py` sorts by `(ref_area, period)`.
3. **`observations` can be `null`.** A valid query that matches no data returns HTTP 200 with a
   complete message and `"observations": null` — an empty result, not an error.

`?dimensionAtObservation=AllDimensions` is what produces this flat observation dictionary. Without
it the message is nested one level deeper by series.

---

## Columns

25 columns. Columns 1–16 and 20–25 are **constant across all 50 rows in this snapshot** (the query
fixes them); they are repeated on every row so that a single row is self-describing and a row
lifted into a slide still carries its own provenance. Only `ref_area*`, `series_key`, `period` and
`value` vary.

| # | Column | Type | Nullable | Allowed values / code list | Unit | Notes |
|---:|---|---|---|---|---|---|
| 1 | `ref_area` | string | no | `SWE`, `EA` — `OECD:CL_AREA(1.1)` | — | Reference area code. |
| 2 | `ref_area_name` | string | no | `Sweden`, `Euro area` | — | Decoded from CL_AREA, not from the code string. |
| 3 | `frequency` | string | no | `M` — `SDMX:CL_FREQ(2.1)` | — | Dimension id in the DSD is `FREQ`. |
| 4 | `frequency_name` | string | no | `Monthly` | — | |
| 5 | `methodology` | string | no | `HICP` — `OECD.SDD.TPS:CL_METHODOLOGY_PRI(1.0)` | — | **Load-bearing.** `N` (National) is a *different statistic* — see below. |
| 6 | `methodology_name` | string | no | `Eurostat harmonised index of consumer prices (HICP)` | — | |
| 7 | `measure` | string | no | `CPI` — `OECD.SDD.TPS:CL_MEASURE_PRI(1.0)` | — | The other live code is `IT_W` (item weights). |
| 8 | `measure_name` | string | no | `Consumer price index` | — | |
| 9 | `unit_measure` | string | no | `PA` — `OECD:CL_UNIT_MEASURE(1.7)` | — | **Load-bearing.** `IX` would be index levels (~120), not a rate. |
| 10 | `unit_label` | string | no | `Percent per annum` | — | The unit of `value`. |
| 11 | `expenditure` | string | no | `_T` — `OECD:CL_COICOP_18(1.1)` | — | All items. |
| 12 | `expenditure_name` | string | no | `Total` | — | |
| 13 | `adjustment` | string | no | `N` — `OECD:CL_ADJUSTMENT(1.0)` | — | |
| 14 | `adjustment_name` | string | no | `Neither seasonally adjusted nor calendar adjusted` | — | |
| 15 | `transformation` | string | no | `GY` — `OECD:CL_TRANSFORMATION(1.0)` | — | **Load-bearing.** `G1` would be month-on-month. |
| 16 | `transformation_name` | string | no | `Growth rate, over 1 year` | — | |
| 17 | `series_key` | string | no | `SWE.M.HICP.CPI.PA._T.N.GY`, `EA.M.HICP.CPI.PA._T.N.GY` | — | Columns 1,3,5,7,9,11,13,15 joined by `.` in DSD order. Part 1 of the primary key. |
| 18 | `period` | string | no | ISO `YYYY-MM`, `^[0-9]{4}-(0[1-9]\|1[0-2])$`, `2024-01`…`2026-01` | month | **Observation period.** Part 2 of the primary key. Keep as text — `2024-01` is a month, not a date, and Excel will mangle it. |
| 19 | `value` | float | no | finite; ≈ −50 … 100 sanity band | percent per annum | The published figure, exactly as returned. **Not rounded by this pack.** |
| 20 | `obs_status` | string | no | `A` — `SDMX:CL_OBS_STATUS(2.2)` | — | Other codes exist upstream (e.g. provisional, estimated); only `A` appears here. |
| 21 | `obs_status_name` | string | no | `Normal value` | — | |
| 22 | `source_id` | string | no | `OECD.SDD.TPS` | — | SDMX agency id that publishes the dataflow. |
| 23 | `dataflow_id` | string | no | `DSD_PRICES_COICOP2018@DF_PRICES_C2018_ALL` | — | Version `1.0` is in `query_url` and in the metadata file. |
| 24 | `query_url` | string | no | the exact request URL | — | Identical on every row. Makes any single row reproducible. |
| 25 | `retrieved_at_utc` | string | no | ISO-8601 UTC, `YYYY-MM-DDTHH:MM:SSZ` | — | **Retrieval time.** Always later than `period`. Identical on every row. Changes on every rerun; nothing else should. |

### Two-row example

| ref_area | ref_area_name | frequency | frequency_name | methodology | methodology_name | measure | measure_name | unit_measure | unit_label | expenditure | expenditure_name | adjustment | adjustment_name | transformation | transformation_name | series_key | period | value | obs_status | obs_status_name | source_id | dataflow_id | query_url | retrieved_at_utc |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SWE | Sweden | M | Monthly | HICP | Eurostat harmonised index of consumer prices (HICP) | CPI | Consumer price index | PA | Percent per annum | `_T` | Total | N | Neither seasonally adjusted nor calendar adjusted | GY | Growth rate, over 1 year | SWE.M.HICP.CPI.PA._T.N.GY | 2025-12 | 2.1 | A | Normal value | OECD.SDD.TPS | DSD_PRICES_COICOP2018@DF_PRICES_C2018_ALL | `https://sdmx.oecd.org/public/rest/data/OECD.SDD.TPS,DSD_PRICES_COICOP2018@DF_PRICES_C2018_ALL,1.0/SWE+EA.M.HICP.CPI.PA._T.N.GY?startPeriod=2024-01&endPeriod=2026-01&dimensionAtObservation=AllDimensions` | 2026-09-13T18:33:16Z |
| EA | Euro area | M | Monthly | HICP | Eurostat harmonised index of consumer prices (HICP) | CPI | Consumer price index | PA | Percent per annum | `_T` | Total | N | Neither seasonally adjusted nor calendar adjusted | GY | Growth rate, over 1 year | EA.M.HICP.CPI.PA._T.N.GY | 2026-01 | 1.7 | A | Normal value | OECD.SDD.TPS | DSD_PRICES_COICOP2018@DF_PRICES_C2018_ALL | *(same URL)* | 2026-09-13T18:33:16Z |

Read those two rows as: **in December 2025, consumer prices in Sweden were 2.1% higher than in
December 2024; in January 2026, consumer prices across the euro area were 1.7% higher than in
January 2025.**

---

## What this indicator measures — in plain language

The Harmonised Index of Consumer Prices tracks what a typical *household* pays for a fixed,
representative basket of goods and services — food, rent, energy, transport, restaurants,
haircuts, and so on. The number in the `value` column is the **year-on-year percentage change**
in that basket's cost: how much more expensive the same basket is this month than it was in the
same month twelve months ago. "Harmonised" means every country builds it to one agreed European
definition, which is why Sweden and the euro area can sit in the same table and be compared
honestly. It is compiled by Statistics Sweden and Eurostat; the OECD redisseminates it.

For Northbridge, this is background. It tells you roughly what the general price environment
looked like around the reporting period — useful when someone in a review asks "was this a
high-inflation month?" or "how does our cost movement compare with what was happening generally?"

### Three things it does **not** tell you

1. **It does not tell you what happened to Northbridge's costs.** HICP is a *household* basket,
   weighted by what consumers spend. Northbridge's costs are salaries, subcontracted delivery,
   premises and software. Those move on their own schedule and can rise while HICP falls. A 2.1%
   HICP reading is not a 2.1% cost increase for N01–N03, and nothing in this file supports
   inferring one.
2. **It does not explain or predict Northbridge's revenue, costs or variances.** There is no
   causal link established here and none may be asserted. This series is deliberately *not*
   joined to the planning model, and the seasonal-naive baseline does not use it. Putting it on
   the same chart as a variance does not make it an explanation.
3. **It does not describe your own currency, region or timing exposure.** The euro-area figure is
   a 20-country aggregate; no single country, city or supplier experienced exactly that number.
   Sweden's figure is a national average. Neither figure is an exchange-rate effect — Northbridge
   reports in EUR but a Swedish HICP reading says nothing about SEK/EUR. And both are published
   with a lag, so the most recent month you can see is not the month you are closing.

### One more trap, specific to this dataset

Ask the same OECD dataflow for Sweden in 2025-12 with `methodology=N` (National) instead of
`HICP` and you get **0.2982668**, not **2.1**. Both are real, both are OECD, and they differ by
almost two percentage points. The Swedish national CPI (KPI) includes owner-occupier mortgage
interest costs, so falling policy rates drag it down; HICP excludes them. Changing one character
in the series key changes the story. This is exactly why every code in this file is decoded from
the official OECD code lists and carried alongside its meaning, rather than being assumed from the
look of the code.
