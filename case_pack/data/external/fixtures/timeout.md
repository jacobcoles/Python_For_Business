# Fixture: timeout — MOCK, not a live-source test

There is no file to serve for this one. A timeout is the **absence** of a response, so it is
simulated in the client, never by pointing at the live OECD API.

**Never create this case by hammering sdmx.oecd.org.** The OECD Terms & Conditions reserve the
right to limit or suspend access by IP address, and deliberately overloading the service to
manufacture a teaching failure would be a misuse of a public good.

## How the D2-S03 exercise simulates it

Set the timeout to a value the network cannot meet, on a request that is otherwise identical to
the real one:

```python
import requests
try:
    response = requests.get(QUERY_URL, headers=HEADERS, params=PARAMS, timeout=0.001)
except requests.exceptions.Timeout:
    ...  # this is the branch under test
```

`requests` raises `requests.exceptions.Timeout` (a subclass of `requests.exceptions.RequestException`).
No `response` object exists, so `response.status_code` is not available — that is the point of the
drill. A `try/except` that only guards `json.loads()` will not catch this.

An offline alternative, for a classroom with no network at all:

```python
import requests
from unittest.mock import patch
with patch("requests.get", side_effect=requests.exceptions.Timeout("mock timeout")):
    ...
```

## Expected handling

1. Catch `requests.exceptions.Timeout` explicitly and report refresh status **`unavailable (timeout)`**.
2. Leave the existing cache exactly as it is — same bytes, same `retrieved_at_utc`.
3. Report the cache's **original** fetch timestamp, not today's date. A failed attempt today does
   not make yesterday's data fresh.
4. Retry at most once or twice, with a pause, and then stop. Do not loop.
