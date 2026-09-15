"""Supplied helpers for D2-S02 (requesting OECD data) and reuse in projects.

Learners call these from the notebook. They do not need to read this file.
The parser and the meaning checks are the shared, tested ones in case_pack/data/external.
"""
import datetime as dt
import json
from pathlib import Path

import pandas as pd
import requests

from case_pack.data.external.oecd_sdmx import ACCEPT, EXPECTED_CONTENT_TYPE, build_url, parse_sdmx_json, NoObservations
from case_pack.data.external.validate_context import validate_context

EXTERNAL = Path("case_pack/data/external")
AREA_NAMES = {"SWE": "Sweden", "EA": "Euro area"}
FIRST_MONTH, LAST_MONTH = "2024-01", "2026-01"
SERIES_REST = ".M.HICP.CPI.PA._T.N.GY"
SHORT_COLUMNS = ["ref_area", "ref_area_name", "period", "value", "unit_label", "retrieved_at_utc"]


def _problem(message):
    """In a notebook a raised SystemExit prints two extra lines of noise, so say it plainly and return None."""
    print("PROBLEM: " + message)
    return None


def _months(start, end):
    return list(pd.period_range(start, end, freq="M").astype(str))


def build_request(areas, start, end):
    """Put the request together from its parts and print it. Nothing is sent yet."""
    areas = list(areas)
    unknown = [a for a in areas if a not in AREA_NAMES]
    if not areas or unknown:
        return _problem('AREAS must list "SWE", "EA" or both, for example ["SWE", "EA"].')
    for month in (start, end):
        if not (isinstance(month, str) and len(month) == 7 and month[4] == "-"):
            return _problem('write the months as text with quotation marks, like START = "2025-12".')
    if not FIRST_MONTH <= start <= end <= LAST_MONTH:
        return _problem(f"START and END must be between {FIRST_MONTH} and {LAST_MONTH}, with START not after END. "
                        f"You asked for {start} to {end}.")
    series_key = "+".join(areas) + SERIES_REST
    request = {
        "areas": areas, "start": start, "end": end,
        "url": build_url(series_key),
        "params": {"startPeriod": start, "endPeriod": end, "dimensionAtObservation": "AllDimensions"},
        "headers": {"Accept": ACCEPT},
    }
    print("Endpoint (the address):", request["url"])
    print("Parameters (your choices):")
    for name, value in request["params"].items():
        print(f"  {name} = {value}")
    print("Header (the format we ask for):", ACCEPT)
    print(f"Expected rows: {len(areas)} area(s) x {len(_months(start, end))} month(s) = "
          f"{len(areas) * len(_months(start, end))}")
    return request


def get_response(request, mode="offline"):
    """Get the response: "live" sends the request now; "offline" uses the response saved on 2026-09-13."""
    if request is None:
        print("NOT DONE YET: there is no request yet. Correct the settings in the cell above and run it again.")
        return None
    if mode == "live":
        try:
            reply = requests.get(request["url"], params=request["params"], headers=request["headers"], timeout=30)
        except requests.exceptions.RequestException as problem:
            print(f"LIVE REQUEST FAILED: {type(problem).__name__}. No data was received.")
            print('Record this, set MODE = "offline" and run this cell again. Do not retry repeatedly.')
            return None
        response = {
            "mode": "live", "status": reply.status_code,
            "content_type": reply.headers.get("Content-Type", "missing"), "body": reply.content,
            "query_url": reply.url, "retrieved_at_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
    elif mode == "offline":
        metadata = json.loads((EXTERNAL / "oecd_source_metadata.json").read_text(encoding="utf-8"))
        saved = pd.read_csv(EXTERNAL / "oecd_context_tidy.csv", dtype={"period": str})
        response = {
            "mode": "offline", "status": metadata["query"]["http_status"],
            "content_type": metadata["query"]["response_content_type"],
            "body": (EXTERNAL / metadata["query"]["raw_body_file"]).read_bytes(),
            "query_url": metadata["query"]["full_query_url"], "retrieved_at_utc": saved["retrieved_at_utc"].iloc[0],
        }
        print("SAVED RESPONSE, not a new request. It answered a wider request for SWE and EA, 2024-01 to 2026-01.")
    else:
        return _problem('MODE must be "offline" or "live", with the quotation marks.')
    print("Status code:", response["status"], "(200 means OK)")
    print("Content type:", response["content_type"])
    print("Size of the body:", f"{len(response['body']):,} bytes")
    print("Retrieved at (UTC):", response["retrieved_at_utc"])
    if response["status"] != 200:
        print("PROBLEM: the source did not answer OK, so nothing below can be trusted. "
              'Record the status code and switch to MODE = "offline".')
        return None
    if EXPECTED_CONTENT_TYPE not in response["content_type"]:
        print("PROBLEM: the body is not in the expected SDMX-JSON format. Do not use it.")
        return None
    return response


def peek(response):
    """Show the start of the body and decode one observation by hand, before any table is made."""
    if response is None:
        print("NOT DONE YET: there is no usable response. Run the previous step first.")
        return
    message = json.loads(response["body"].decode("utf-8"))
    text = response["body"].decode("utf-8")
    print("The first 300 characters of the body, exactly as received:\n")
    print(text[:300], "...\n")
    print("Top-level sections:", list(message.keys()), "  inside 'data':", list(message["data"].keys()))
    structure = message["data"]["structures"][0]
    dimensions = structure["dimensions"]["observation"]
    print("\n'structures' holds the MEANING: the list of dimensions and their possible values.")
    for position, dimension in enumerate(dimensions):
        values = [v["id"] for v in dimension["values"]]
        shown = ", ".join(values[:3]) + (" ..." if len(values) > 3 else "")
        print(f"  position {position}: {dimension['id']:<15} values: {shown}")
    observations = message["data"]["dataSets"][0]["observations"]
    key, record = next(iter(observations.items()))
    print(f"\n'dataSets' holds the NUMBERS. There are {len(observations)} observations. The first one is:")
    print(f'  "{key}": {record}')
    print("\nThe key is a list of positions, one per dimension. Decoded:")
    for position, index in enumerate(key.split(":")):
        dimension = dimensions[position]
        value = dimension["values"][int(index)]
        print(f"  {dimension['id']:<15} position {index} -> {value['id']} ({value.get('name', '')})")
    print(f"\nSo the number {record[0]} is that area's consumer-price change over one year, in percent, for that month.")


def to_table(response, request):
    """Turn the body into a table with one row per area and month, then check its meaning."""
    if request is None or response is None:
        print("NOT DONE YET: there is no usable response. Run the earlier steps first.")
        return None
    try:
        frame = parse_sdmx_json(response["body"], response["query_url"], response["retrieved_at_utc"])
    except NoObservations:
        print("PROBLEM: the request worked but returned no observations. Check the months you asked for.")
        return None
    if response["mode"] == "offline":
        problem = validate_context(frame)
        frame = frame[frame["ref_area"].isin(request["areas"]) &
                      frame["period"].between(request["start"], request["end"])].reset_index(drop=True)
    else:
        problem = validate_context(frame, areas=tuple(request["areas"]), start=request["start"], end=request["end"])
    if problem:
        print(f"PROBLEM: the data failed a meaning check: {problem}. Do not use it.")
        return None
    expected_rows = len(request["areas"]) * len(_months(request["start"], request["end"]))
    print(f"OK: {len(frame)} rows = {len(request['areas'])} area(s) x "
          f"{len(_months(request['start'], request['end']))} month(s)." if len(frame) == expected_rows else
          f"PROBLEM: {len(frame)} rows, expected {expected_rows}.")
    print("OK: one measure only: HICP, change over one year, percent (checked for every row).")
    print("OK: no area and month appears twice.")
    return frame


def check_gaps(gaps, table):
    """Check the YOUR TURN table: one row per month, Sweden and euro area side by side, gap = EA minus SWE."""
    if gaps is None:
        print("NOT DONE YET: `gaps` is still empty. Paste Copilot's code into the YOUR TURN cell and run it.")
        return
    if table is None or set(table["ref_area"]) != {"SWE", "EA"}:
        print("PROBLEM: this comparison needs both areas. Set AREAS = [\"SWE\", \"EA\"] in Step 3 and rerun from there.")
        return
    if not isinstance(gaps, pd.DataFrame):
        print(f"PROBLEM: `gaps` should be a table (DataFrame), but it is a {type(gaps).__name__}.")
        return
    frame = gaps.reset_index() if "period" not in gaps.columns else gaps
    needed = {"period", "SWE", "EA", "gap"}
    if not needed.issubset(frame.columns):
        print(f"PROBLEM: `gaps` needs the columns period, SWE, EA and gap; it has {list(frame.columns)}.")
        return
    expected = table.pivot(index="period", columns="ref_area", values="value")
    expected = (expected["EA"] - expected["SWE"]).round(2)
    mine = frame.set_index("period")["gap"].round(2)
    months_ok = len(mine) == len(expected)
    print(f"OK: one row per month ({len(mine)})." if months_ok else
          f"PROBLEM: {len(mine)} rows, expected {len(expected)} months.")
    if not months_ok:
        return
    difference = mine.reindex(expected.index).sub(expected).abs()
    if difference.le(0.001).all():
        print("OK: gap is euro area minus Sweden, in percentage points, for every month.")
    elif mine.reindex(expected.index).add(expected).abs().le(0.001).all():
        print("PROBLEM: the gap is the wrong way round. It should be the euro area minus Sweden, not Sweden minus "
              "the euro area.")
    elif difference.max() > 1:
        print("PROBLEM: the gap should be one rate subtracted from the other, in percentage points (for example "
              "2.0 - 2.1 = -0.1), not a percentage change between them.")
    else:
        print("PROBLEM: some gaps differ from euro area minus Sweden. Compare one month by hand.")


def save_extract(table, response, folder="outputs/D2-S02"):
    """Save the table, the untouched response body and a source record, so anyone can see where it came from."""
    if table is None or response is None:
        print("NOT DONE YET: there is no checked table to save.")
        return
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    table.to_csv(folder / "context.csv", index=False)
    (folder / "response.sdmx.json").write_bytes(response["body"])
    record = {
        "data_status": "live" if response["mode"] == "live" else "cached",
        "source": "OECD public SDMX API, dataflow DSD_PRICES_COICOP2018@DF_PRICES_C2018_ALL",
        "query_url": response["query_url"],
        "retrieved_at_utc": response["retrieved_at_utc"],
        "rows_kept": {"areas": sorted(set(table["ref_area"])), "from": table["period"].min(),
                      "to": table["period"].max(), "row_count": len(table)},
        "meaning": "Harmonised consumer prices (HICP), percentage change over one year, monthly, not seasonally adjusted",
        "use": "External context only. Not a Northbridge forecast input.",
    }
    (folder / "source_record.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(f"Saved in {folder.as_posix()}:")
    print("  context.csv          the table you used")
    print("  response.sdmx.json   the body exactly as received (evidence)")
    print("  source_record.json   where and when it came from, and whether it is live or cached")
