# External refresh with controls, in Python

The job is in `README.md`. This is how to build it.

**Tool:** a Python script in VS Code, with Microsoft 365 Copilot Chat for the code.
**You will produce:** `context.csv`, `response.sdmx.json`, `source_record.json` and `refresh_note.md`.

## Start here

1. Right-click `outputs` > **New Folder**, name it `projects` if it is not there. Right-click `outputs/projects` >
   **New Folder**, name it after your project, for example `inflation_context`.
2. Right-click `worked_example.py` > **Copy**, then right-click your folder > **Paste**.
3. Open your copy and click **Run Python File**.

**You should see** three `OK:` lines, three saved filenames, and a `data_status:` line naming the age and the
limit.

The setting `MODE = "offline"` uses the saved response, so this works with no network. `MODE = "live"` sends a real
request.

## Step 1: build the request

```python
AREAS = ["SWE", "EA"]
START, END = "2025-01", "2026-01"
```

`oecd.build_request(AREAS, START, END)` turns these into a URL and the headers that go with it. Two areas and
thirteen months is 26 observations, and that number is what step 3 checks against.

## Step 2: send it, or reuse the saved one

`oecd.get_response(request, MODE)` either sends the request or loads the saved copy. Either way it returns the
response **with its retrieval time attached**, which is the single most important field on this track.

**Why the saved copy exists:** the course must work without network access, and you need a way to rehearse the
failure cases without waiting for a real outage.

## Step 3: check before you use it (the step that matters)

**Why:** a response with status 200 is not necessarily the data you asked for. It can be the right shape and the
wrong series, or missing months, or contain two measures where you expected one. Checking after publishing is too
late.

`oecd.to_table(response, request)` runs three checks and prints them:

```text
OK: 26 rows = 2 area(s) x 13 month(s).
OK: one measure only: HICP, change over one year, percent (checked for every row).
OK: no area and month appears twice.
```

The second is the one people omit. A statistics API can return an index level and an annual rate in the same
response, and averaging them together produces a number that looks plausible and means nothing.

**Ask Copilot** if you want to write your own checks:

> I have a pandas DataFrame with the columns ref_area, period, value and a measure description. Write three checks
> that stop the script with a clear message: that the row count equals the number of areas times the number of
> months I requested; that every row has the same measure description; and that no combination of ref_area and
> period appears twice. Print a plain OK line for each when it passes.

## Step 4: save the table, the response and the record together

`oecd.save_extract(table, response, OUTPUT_FOLDER)` writes three files, and writes **nothing** if a check failed.

| File | Why it exists |
|---|---|
| `context.csv` | The table you used |
| `response.sdmx.json` | The body exactly as received, as evidence |
| `source_record.json` | Where it came from, when it was retrieved, and whether it was live or cached |

Keeping the raw response is what lets somebody months later tell the difference between "the source changed" and
"we processed it wrongly".

## Step 5: work out the age honestly

```python
downloaded = refresh.parse_utc(response["retrieved_at_utc"])
age_days = (dt.datetime.now(dt.timezone.utc) - downloaded).total_seconds() / 86400
status = "live" if MODE == "live" else refresh.policy_rule(age_days, MAX_AGE_DAYS)
```

**Read the first line.** The age comes from `retrieved_at_utc`, the moment the data was **downloaded**. It does not
come from when you ran the script, and it does not reset because you reran it. A saved file gets older every day
whether or not anybody touches it, and the status must say so.

The four statuses:

| Status | Meaning |
|---|---|
| `live` | Fetched just now from the source |
| `cached` | A saved copy, still inside the age limit |
| `stale` | A saved copy, past the age limit. Usable only if you say it is out of date |
| `unavailable` | No usable response. There is no figure to give |

`MAX_AGE_DAYS = 35` is a teaching assumption, not policy.

## Step 6: what to do when it is down

Run it against one of the failure fixtures in `case_pack/data/external/fixtures/`. **Nothing should be saved**, and
the status should be `unavailable`.

The wrong answer is to fall back to the last good copy and present it as current. The right answer is to report
`unavailable`, say when the last good figure was retrieved, and let the reader decide whether an old number is
useful to them.

## Check your result

For December 2025: euro area **2.0**, Sweden **2.1**, gap **0.1 percentage points** with Sweden higher. Compare
within 0.1 points, because the source publishes to one decimal and revises.

The status line should read `cached` with the saved response and a 35-day limit, and name the download time. If you
set `MAX_AGE_DAYS = 1` it should read `stale` with the same data.

**Say "percentage points", not "per cent".** 2.0 against 2.1 differs by 0.1 points. "0.1 per cent" is a different
and wrong claim.

## Write the note

Right-click your project folder > **New File**, name it `refresh_note.md`:

```text
What this series is, in one sentence, and what it is NOT (it is context, not a forecast input):
Where it came from and when it was retrieved:
Its status today, and the limit I applied:
What I would publish if the source were unavailable:
What a reader must not conclude from it:
```

The last heading matters: an inflation rate beside our figures invites the reader to assume a link that this data
does not support.

## Done when

The three checks pass, the three files are in your own folder, the status names the age and the limit, you have
tried a failure case and confirmed nothing was saved, and your note uses the words "percentage points".

## If something goes wrong

| What you see | What to do |
|---|---|
| A connection or timeout error with `MODE = "live"` | The network blocks the source. Use `MODE = "offline"`, and say in your note that you did |
| `PROBLEM: ... rows` | The response is not what was requested. Do not continue; look at the raw response |
| Two measures in the response | The check caught it. Narrow the request rather than filtering afterwards |
| `data_status: stale` unexpectedly | The saved copy is older than the limit. That is correct behaviour, not a bug |
| Nothing was saved | A check failed. That is the design: nothing is saved from a response that did not pass |

**Start again:** delete your copy and paste `worked_example.py` again. The saved response never changes.
