# Controlled failure fixtures for D2-S03

**Everything in this folder except `http_404_notresultsfound.txt` and `empty_result.json` is a
MOCK response that was written by hand. Mocked responses are not live-source tests.** They
exercise the refresh logic; they prove nothing about the OECD API's current behaviour.

| File | Real or mock? | Simulates | Serve it as |
|---|---|---|---|
| `empty_result.json` | **REAL** OECD response, observations removed (see below) | A valid query that matches no data | HTTP 200, `application/vnd.sdmx.data+json` |
| `http_404_notresultsfound.txt` | **REAL** OECD response, captured 2026-09-13 | An invalid dimension code | HTTP 404, `text/plain` |
| `http_500.json` | MOCK — no OECD 500 was ever observed | A server-side failure | HTTP 500, `application/vnd.sdmx.data+json` |
| `malformed_body.txt` | MOCK | Correct status and content type, truncated JSON | HTTP 200, `application/vnd.sdmx.data+json` |
| `timeout.md` | MOCK (client-side simulation; no body exists) | No response at all | n/a — raise `requests.exceptions.Timeout` |

## How `empty_result.json` was made

It is a genuine OECD-shaped response. The OECD was asked for the adopted series over a period
window that has no data:

```
GET https://sdmx.oecd.org/public/rest/data/OECD.SDD.TPS,DSD_PRICES_COICOP2018@DF_PRICES_C2018_ALL,1.0/SWE+EA.M.HICP.CPI.PA._T.N.GY?startPeriod=1950-01&endPeriod=1950-02&dimensionAtObservation=AllDimensions
Accept: application/vnd.sdmx.data+json; charset=utf-8; version=2
-> HTTP 200, application/vnd.sdmx.data+json; charset=utf-8; version=2, 8892 bytes
```

The OECD itself returned a complete message with **`"observations": null`**. Nothing had to be
removed by hand — the empty result is exactly as the OECD sent it on 2026-09-13T18:32:33Z. The
file is byte-identical to that response body.

## The lesson these fixtures exist to teach

Four different things can go wrong and they need four different guards:

1. **No response** (timeout) — guard: `timeout=` plus `except requests.exceptions.Timeout`.
2. **Bad status** (500, 404) — guard: check `response.status_code` before anything else.
3. **Right status, wrong format** (the 404 above is `text/plain`) — guard: check
   `response.headers["Content-Type"]` before `json.loads()`.
4. **Right status, right format, no data** (`observations: null`) — guard: check the observation
   count after parsing, and treat zero rows as a reportable outcome rather than an empty success.

In every one of the four, a good cache must survive untouched and must keep reporting its own
original `retrieved_at_utc`.
