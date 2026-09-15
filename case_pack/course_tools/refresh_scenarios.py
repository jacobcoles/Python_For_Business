"""Supplied controlled scenarios for D2-S03. No network requests are made here.

Each scenario builds a saved copy (cache) from the response saved on 2026-09-13, moves the clock forward by a fixed
number of days, then simulates today's request failing. Simulated responses are labelled fixtures in
case_pack/data/external/fixtures; they test our decisions, not the live OECD service.
"""
import datetime as dt
import json
import shutil
import tempfile
from pathlib import Path

import requests

from case_pack.course_tools import refresh as R

EXT = Path("case_pack/data/external")
FIX = EXT / "fixtures"
SNAPSHOT_TIME = dt.datetime(2026, 9, 13, 18, 33, 16, tzinfo=dt.timezone.utc)
SDMX = "application/vnd.sdmx.data+json; charset=utf-8; version=2"
CASES = [("A", 3, "server_error"), ("B", 30, "server_error"), ("C", 36, "server_error"), ("D", None, "timeout")]


class _FakeResponse:
    def __init__(self, status, content_type, body, url):
        self.status_code, self.content, self.url, self.text = status, body, url, body.decode("utf-8", "replace")
        self.headers = {"Content-Type": content_type}


class _Server:
    """Plays a fixed sequence of responses instead of contacting the OECD."""
    def __init__(self, *script):
        self.script, self.calls = list(script), 0

    def get(self, url, headers=None, params=None, timeout=None):
        name = self.script[min(self.calls, len(self.script) - 1)]
        self.calls += 1
        if name == "timeout":
            raise requests.exceptions.Timeout("simulated")
        if name == "server_error":
            return _FakeResponse(500, SDMX, (FIX / "http_500.json").read_bytes(), url)
        request = json.loads((EXT / "raw/oecd_prices_c2018_hicp_swe_ea.request.json").read_text())
        return _FakeResponse(200, SDMX, (EXT / "raw/oecd_prices_c2018_hicp_swe_ea.sdmx.json").read_bytes(), request["url"])


def _no_wait(_seconds):
    pass


def run(status_rule, max_age_days=35, keep_example_in=None):
    """Run cases A to D with the learner's rule. Returns one dictionary per case."""
    rows = []
    work = Path(tempfile.mkdtemp())
    try:
        for case, age, today in CASES:
            cache = work / case
            if age is not None:
                R.refresh(cache, SNAPSHOT_TIME, get=_Server("success").get, sleep=_no_wait)
            now = SNAPSHOT_TIME + dt.timedelta(days=age if age is not None else 3)
            try:
                result = R.refresh(cache, now, get=_Server(today, today).get, sleep=_no_wait,
                                   max_age_days=max_age_days, status_rule=status_rule)
                status = result.data_status
            except (TypeError, ValueError) as problem:
                result, status = None, f"rule error: {problem}"
            if status is not None and status not in ("cached", "stale", "unavailable"):
                raise SystemExit(
                    f'STOPPED: your rule returned {status!r} for case {case}. It must return exactly "cached" or '
                    '"stale", in lower case and with the quotation marks.')
            meta_file = R.cache_paths(cache)[1]
            meta = json.loads(meta_file.read_text()) if meta_file.exists() else {}
            rows.append({"case": case, "age": "no saved copy" if age is None else f"{age} days",
                         "today": "server error (HTTP 500)" if today == "server_error" else "no answer (timeout)",
                         "refresh_outcome": result.refresh_outcome if result else "?",
                         "data_status": status if status is not None else "NOT DONE YET",
                         "retrieved_at_utc": meta.get("retrieved_at_utc", "none"),
                         "last_attempt_utc": meta.get("last_attempt_utc", R.utc_text(now))})
            if keep_example_in and case == "B":
                target = Path(keep_example_in)
                if target.exists():
                    shutil.rmtree(target)
                shutil.copytree(cache, target)
    finally:
        shutil.rmtree(work)
    return rows


def print_table(rows, max_age_days):
    print(f"CONTROLLED SCENARIOS (no network). Age limit: {max_age_days} days\n")
    print(f"{'Case':<5}{'Saved copy age':<16}{'Today':<26}{'refresh_outcome':<17}{'data_status':<15}retrieved_at_utc")
    for row in rows:
        print(f"{row['case']:<5}{row['age']:<16}{row['today']:<26}{row['refresh_outcome']:<17}"
              f"{row['data_status']:<15}{row['retrieved_at_utc']}")
