# External-data refresh and cache policy

## For learners (D2-S03)

A refresh reruns yesterday's request. It reports two separate facts: what happened this time (`refresh_outcome`) and
how fresh the data you are handing over is (`data_status`: live, cached, stale or unavailable). A saved copy keeps
the date it was actually downloaded, whatever happens today, and a copy older than 35 days is stale. That is all you
need for the session; the two tables below give the detail. The rest of this page is the author's record of how the
policy was settled and tested.

---

## The policy record (DEC-22)

**Version:** `v0.1-draft` · **Owner:** coordinator (settled on behalf of the external-source owner,
whose package P5 is closed). Consumed by **D2-S03** and the *external refresh* project track.

This is a **manual, rerunnable refresh**. It is not a scheduled service and must never be described
as one (DEC-11).

## Two separate facts, never merged
Every refresh run reports both:

| Field | Question it answers | Values |
|---|---|---|
| `refresh_outcome` | What happened when we tried to fetch **this run**? | `not_attempted`, `success`, `http_error`, `timeout`, `network_error`, `wrong_content_type`, `malformed`, `no_results`, `invalid` |
| `data_status` | How fresh is the data we are **handing over**? | `live`, `cached`, `stale`, `unavailable` |

A failed attempt changes `refresh_outcome`. It **never** changes the age of the data. The data's age
is always measured from its own original `retrieved_at_utc`.

## `data_status` rules
Let `age = now_utc - retrieved_at_utc` of the data being returned. `MAX_AGE = 35 days` — the series
is monthly, so a cache older than about one publication cycle is stale.

| Situation | `data_status` |
|---|---|
| This run fetched, parsed and validated successfully and wrote the cache | `live` |
| Data returned from cache and `age <= MAX_AGE` | `cached` |
| Data returned from cache and `age > MAX_AGE` | `stale` |
| No valid data could be returned (fetch failed and no cache exists) | `unavailable` |

A refresh that fails while a cache exists returns the cache with its **original** timestamp:
`cached` or `stale` by age, plus the failure in `refresh_outcome`. Yesterday's data does not become
today's data because we tried again today.

## What each failure is, and how it is detected (in this order)
| Order | Guard | `refresh_outcome` on failure | Real or mock fixture |
|---|---|---|---|
| 1 | `requests.get(..., timeout=...)` raises `Timeout` | `timeout` | mock (`fixtures/timeout.md`) |
| 1b | Another request exception (DNS, connection, TLS/proxy) before an HTTP response | `network_error` | mocked connection failure; W4-21 |
| 2 | `status_code == 404` with body `NoResultsFound` | `no_results` | **real** (`fixtures/http_404_notresultsfound.txt`) |
| 3 | any other `status_code != 200` | `http_error` | mock (`fixtures/http_500.json`) |
| 4 | `Content-Type` lacks `application/vnd.sdmx.data+json` | `wrong_content_type` | — |
| 5 | body is not parseable SDMX-JSON | `malformed` | mock (`fixtures/malformed_body.txt`) |
| 6 | parses, but zero observations (`"observations": null`) | `no_results` | **real** (`fixtures/empty_result.json`) |
| 7 | parses, but fails the live invariants in `data/external/invariants.json` | `invalid` | — |

## Retries
At most **2 attempts in total**, and only after `timeout` or an HTTP `5xx`. Wait 2 seconds between
attempts. **No retry** on `4xx`, wrong content type, malformed body or no results — repeating will
not change the answer. Never generate load on the live API to manufacture failures; failure cases
are tested with fixtures.

`network_error` is not an HTTP status and is not retried automatically. Preserve and return the
last good cache with its original timestamp, or report unavailable without cache. Check client
network/proxy settings; do not disable TLS verification. Cache files are assumed untampered in
this bounded teaching workflow; crash-consistent two-file transactions and corruption recovery
are workplace hardening, not implemented guarantees.

## Writing the cache safely
1. Validate **before** writing. Only a `success` may write.
2. Write the tidy CSV and its metadata to temporary files in the same folder, then replace the
   cache files. A failed or malformed response can therefore never replace a good cache.
3. **Replace, never append.** The cache is the full validated extract; a rerun must not accumulate
   duplicate `(ref_area, period)` rows.
4. The metadata sidecar (`*.meta.json`) records: `retrieved_at_utc` (of the cached data),
   `query_url`, `row_count`, `last_attempt_utc`, `last_refresh_outcome`.
   `last_attempt_*` may change on a failed run; `retrieved_at_utc` may not.

## Testing
All state checks take an explicit `now_utc` so tests are deterministic. Mocked responses are
labelled as mocks and are **not** evidence about the live API. The live path is tested separately
and its date recorded.

## Adapting to another approved source
Recheck, in writing, before reusing this pattern: meaning of the series, access and reuse terms,
response format and content type, schema and units, request limits, and provenance fields.
