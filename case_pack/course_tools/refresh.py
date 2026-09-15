"""Supplied refresh process for D2-S03 and the external-refresh project track.

Learners do not need to read this file. It reuses the D2-S02 parser and meaning checks, and follows
case_pack/contracts/refresh_policy.md. The one business rule learners write (is saved data still fresh enough?)
can be passed in as `status_rule`; without it the released 35-day policy is used.
"""
from __future__ import annotations

import datetime as dt
import json
import time
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import requests

from case_pack.data.external.oecd_sdmx import (ACCEPT, EXPECTED_CONTENT_TYPE, TIDY_COLUMNS,
                                              NoObservations, build_url, parse_sdmx_json)

SERIES_KEY = "SWE+EA.M.HICP.CPI.PA._T.N.GY"
START_PERIOD, END_PERIOD = "2024-01", "2026-01"
TIMEOUT_SECONDS = 30
MAX_ATTEMPTS = 2                      # retry only after a timeout or HTTP 5xx
RETRY_WAIT_SECONDS = 2
MAX_AGE_DAYS = 35                     # monthly series: older than one cycle is stale


@dataclass
class RefreshResult:
    data_status: str                  # live | cached | stale | unavailable
    refresh_outcome: str              # not_attempted | success | http_error | timeout |
                                      # wrong_content_type | malformed | no_results | invalid
    attempts: int
    retrieved_at_utc: str | None      # of the data returned, never of the failed attempt
    rows: int
    detail: str
    data: pd.DataFrame | None


def utc_text(moment: dt.datetime) -> str:
    return moment.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_utc(text: str) -> dt.datetime:
    return dt.datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)


# ----------------------------------------------------------------------------- cache
def cache_paths(cache_dir: Path) -> tuple[Path, Path]:
    return cache_dir / "oecd_context_cache.csv", cache_dir / "oecd_context_cache.meta.json"


def read_cache(cache_dir: Path) -> tuple[pd.DataFrame, dict] | None:
    data_file, meta_file = cache_paths(cache_dir)
    if not (data_file.exists() and meta_file.exists()):
        return None
    return pd.read_csv(data_file, dtype={"period": "string"}), json.loads(meta_file.read_text())


def write_cache(cache_dir: Path, frame: pd.DataFrame, meta: dict) -> None:
    """Write to temporary files first, then replace. Replace - never append."""
    cache_dir.mkdir(parents=True, exist_ok=True)
    data_file, meta_file = cache_paths(cache_dir)
    tmp_data, tmp_meta = data_file.with_suffix(".csv.tmp"), meta_file.with_suffix(".json.tmp")
    frame.to_csv(tmp_data, index=False, encoding="utf-8", lineterminator="\n")
    tmp_meta.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    tmp_data.replace(data_file)
    tmp_meta.replace(meta_file)


def record_attempt(cache_dir: Path, now_utc: dt.datetime, outcome: str) -> None:
    """A failed attempt updates last_attempt_* only. It never touches retrieved_at_utc."""
    _data_file, meta_file = cache_paths(cache_dir)
    if meta_file.exists():
        meta = json.loads(meta_file.read_text())
        meta['last_attempt_utc'], meta['last_refresh_outcome'] = (utc_text(now_utc), outcome)
        meta_file.write_text(json.dumps(meta, indent=2) + '\n', encoding='utf-8')


def policy_rule(age_in_days: float, max_age_days: float) -> str:
    """The released policy: saved data up to and including the age limit is 'cached', older is 'stale'."""
    return "cached" if age_in_days <= max_age_days else "stale"


def decide_data_status(retrieved_at_utc: str, now_utc: dt.datetime, max_age_days: float = 35, status_rule=None) -> str:
    """Freshness of CACHED data, from the data's own retrieval time: 'cached' or 'stale'."""
    age_in_days = (now_utc - parse_utc(retrieved_at_utc)).total_seconds() / 86400
    rule = status_rule or policy_rule
    return rule(age_in_days, max_age_days)


# ----------------------------------------------------------------------------- validation
def validate(frame: pd.DataFrame) -> str | None:
    """Check the full shared schema, dimensions, units, coverage and provenance."""
    from case_pack.data.external.validate_context import validate_context
    return validate_context(frame, areas=SERIES_KEY.split(".")[0].split("+"),
                            start=START_PERIOD, end=END_PERIOD)


# ----------------------------------------------------------------------------- fetch
def try_fetch(now_utc: dt.datetime, get, sleep) -> tuple[str, int, pd.DataFrame | None, str]:
    """Returns (refresh_outcome, attempts, frame_or_None, detail)."""
    params = {"startPeriod": START_PERIOD, "endPeriod": END_PERIOD,
              "dimensionAtObservation": "AllDimensions"}
    url = build_url(SERIES_KEY)
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            response = get(url, headers={"Accept": ACCEPT}, params=params, timeout=TIMEOUT_SECONDS)
        except requests.exceptions.Timeout:
            if attempt < MAX_ATTEMPTS:
                sleep(RETRY_WAIT_SECONDS)
                continue
            return "timeout", attempt, None, f"no response within {TIMEOUT_SECONDS}s"
        except requests.exceptions.RequestException as exc:
            return "network_error", attempt, None, f"request failed ({type(exc).__name__}); no HTTP response"
        if response.status_code == 404 and "NoResultsFound" in response.text:
            return "no_results", attempt, None, "HTTP 404 NoResultsFound"
        if response.status_code != 200:
            if 500 <= response.status_code < 600 and attempt < MAX_ATTEMPTS:
                sleep(RETRY_WAIT_SECONDS)
                continue
            return "http_error", attempt, None, f"HTTP {response.status_code}"
        content_type = response.headers.get("Content-Type", "")
        if EXPECTED_CONTENT_TYPE not in content_type:
            return "wrong_content_type", attempt, None, f"Content-Type {content_type!r}"
        try:
            frame = parse_sdmx_json(response.content, getattr(response, "url", url), utc_text(now_utc))
        except NoObservations:
            return "no_results", attempt, None, "HTTP 200 with zero observations"
        except (ValueError, KeyError, IndexError, TypeError) as exc:
            return "malformed", attempt, None, f"could not parse SDMX-JSON ({type(exc).__name__})"
        problem = validate(frame)
        if problem:
            return "invalid", attempt, None, problem
        return "success", attempt, frame, f"{len(frame)} rows"
    raise AssertionError("unreachable")


def refresh(cache_dir: Path, now_utc: dt.datetime, *, attempt_fetch: bool = True,
            get=requests.get, sleep=time.sleep, max_age_days: float = 35, status_rule=None) -> RefreshResult:
    """One manual refresh. `now_utc`, `get` and `sleep` are parameters so tests are deterministic."""
    if attempt_fetch:
        outcome, attempts, frame, detail = try_fetch(now_utc, get, sleep)
    else:
        outcome, attempts, frame, detail = "not_attempted", 0, None, "refresh not requested"

    if outcome == "success":
        meta = {"retrieved_at_utc": utc_text(now_utc), "query_url": frame["query_url"].iloc[0],
                "row_count": int(len(frame)), "last_attempt_utc": utc_text(now_utc),
                "last_refresh_outcome": "success"}
        write_cache(cache_dir, frame, meta)
        return RefreshResult("live", outcome, attempts, meta["retrieved_at_utc"], len(frame), detail, frame)

    if attempt_fetch:
        record_attempt(cache_dir, now_utc, outcome)
    cached = read_cache(cache_dir)
    if cached is None:
        return RefreshResult("unavailable", outcome, attempts, None, 0, detail, None)
    frame, meta = cached
    status = decide_data_status(meta["retrieved_at_utc"], now_utc, max_age_days, status_rule)
    age = now_utc - parse_utc(meta["retrieved_at_utc"])
    return RefreshResult(status, outcome, attempts, meta["retrieved_at_utc"], len(frame),
                         f"{detail}; cache age {age.days} days", frame)


