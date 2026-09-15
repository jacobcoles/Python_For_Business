"""Fetch one small, official OECD consumer-price series as external management context.

Northbridge Business Services reports in EUR and operates in Sweden. This script pulls the
harmonised consumer-price inflation rate (HICP, all items, year-on-year %) for Sweden and the
euro area from the OECD's public SDMX API.

This series is CONTEXT ONLY. It is never joined into the Northbridge planning model.

The endpoint returns SDMX-JSON 2.0 -- NOT a flat list of records. See oecd_data_dictionary.md.
Run from the repository root:  .virtual-env-folder/bin/python case_pack/data/external/fetch_oecd.py
"""

from __future__ import annotations

import datetime as dt
import json
import pathlib
import sys

import requests

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from oecd_sdmx import TIDY_COLUMNS, NoObservations, parse_sdmx_json  # noqa: E402  one shared parser

# --- Bounded query parameters: these are the only things a learner should change --------------
AGENCY_ID = "OECD.SDD.TPS"
DATAFLOW_ID = "DSD_PRICES_COICOP2018@DF_PRICES_C2018_ALL"
DATAFLOW_VERSION = "1.0"
SERIES_KEY = "SWE+EA.M.HICP.CPI.PA._T.N.GY"   # 8 dimensions, "+" means "either of these"
START_PERIOD = "2024-01"
END_PERIOD = "2026-01"

BASE_URL = "https://sdmx.oecd.org/public/rest/data"
ACCEPT = "application/vnd.sdmx.data+json; charset=utf-8; version=2"
EXPECTED_CONTENT_TYPE = "application/vnd.sdmx.data+json"
TIMEOUT_SECONDS = 60          # always set a timeout; a hung request is not a failure you can see
SOURCE_ID = "OECD.SDD.TPS"    # SDMX agency that publishes the dataflow

HERE = pathlib.Path(__file__).resolve().parent
RAW_BODY = HERE / "raw" / "oecd_prices_c2018_hicp_swe_ea.sdmx.json"
RAW_SIDECAR = HERE / "raw" / "oecd_prices_c2018_hicp_swe_ea.request.json"
TIDY_CSV = HERE / "oecd_context_tidy.csv"

def build_url() -> str:
    return f"{BASE_URL}/{AGENCY_ID},{DATAFLOW_ID},{DATAFLOW_VERSION}/{SERIES_KEY}"


def fetch() -> tuple[requests.Response, str]:
    """Make the request, then check status and content type BEFORE parsing anything."""
    retrieved_at_utc = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    params = {"startPeriod": START_PERIOD, "endPeriod": END_PERIOD,
              "dimensionAtObservation": "AllDimensions"}
    response = requests.get(build_url(), headers={"Accept": ACCEPT}, params=params,
                            timeout=TIMEOUT_SECONDS)
    if response.status_code != 200:
        raise SystemExit(f"OECD request failed: HTTP {response.status_code} for {response.url}")
    content_type = response.headers.get("Content-Type", "")
    if EXPECTED_CONTENT_TYPE not in content_type:
        raise SystemExit(f"Unexpected Content-Type {content_type!r}; refusing to parse.")
    return response, retrieved_at_utc


def main() -> None:
    response, retrieved_at_utc = fetch()
    RAW_BODY.parent.mkdir(parents=True, exist_ok=True)
    RAW_BODY.write_bytes(response.content)
    RAW_SIDECAR.write_text(json.dumps({
        "url": response.url, "http_method": "GET",
        "request_headers_sent": {"Accept": ACCEPT},
        "http_status": response.status_code,
        "response_content_type": response.headers.get("Content-Type"),
        "response_bytes": len(response.content),
        "retrieved_at_utc": retrieved_at_utc,
        "raw_body_file": RAW_BODY.name,
    }, indent=2) + "\n", encoding="utf-8")

    try:
        frame = parse_sdmx_json(response.content, response.url, retrieved_at_utc)
    except NoObservations as exc:
        raise SystemExit(f"{exc} Nothing was written.")
    frame.to_csv(TIDY_CSV, index=False, encoding="utf-8", lineterminator="\n")
    print(f"HTTP {response.status_code}  {response.headers.get('Content-Type')}  "
          f"{len(response.content)} bytes")
    print(f"retrieved_at_utc : {retrieved_at_utc}")
    print(f"query            : {response.url}")
    print(f"raw body         -> {RAW_BODY.relative_to(pathlib.Path.cwd())}")
    print(f"tidy csv         -> {TIDY_CSV.relative_to(pathlib.Path.cwd())}  "
          f"({len(frame)} rows, {len(frame.columns)} columns)")
    print(f"periods          : {frame['period'].min()} .. {frame['period'].max()}  "
          f"series: {sorted(frame['series_key'].unique())}")


if __name__ == "__main__":
    sys.exit(main())
