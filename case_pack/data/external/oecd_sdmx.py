"""Shared OECD SDMX-JSON parsing for D2-S02 and D2-S03 (one parser, two sessions).

Factored out of fetch_oecd.py by the coordinator on 2026-09-13 so the refresh process in D2-S03 can
reuse EXACTLY the parser D2-S02 teaches.  The only behavioural change: an empty result raises
`NoObservations` instead of exiting the program, so a caller can report it as a status.
Regression check: re-parsing the frozen raw snapshot reproduces oecd_context_tidy.csv byte for byte.
"""
from __future__ import annotations

import datetime as dt
import json
import pathlib

import pandas as pd
import requests

AGENCY_ID = "OECD.SDD.TPS"
DATAFLOW_ID = "DSD_PRICES_COICOP2018@DF_PRICES_C2018_ALL"
DATAFLOW_VERSION = "1.0"
BASE_URL = "https://sdmx.oecd.org/public/rest/data"
ACCEPT = "application/vnd.sdmx.data+json; charset=utf-8; version=2"
EXPECTED_CONTENT_TYPE = "application/vnd.sdmx.data+json"
SOURCE_ID = "OECD.SDD.TPS"


class NoObservations(ValueError):
    """The request succeeded and the message parsed, but it contains zero observations."""


# Frozen column contract. D2-S02 and D2-S03 both depend on this exact list and order.
TIDY_COLUMNS = [
    "ref_area", "ref_area_name", "frequency", "frequency_name",
    "methodology", "methodology_name", "measure", "measure_name",
    "unit_measure", "unit_label", "expenditure", "expenditure_name",
    "adjustment", "adjustment_name", "transformation", "transformation_name",
    "series_key", "period", "value", "obs_status", "obs_status_name",
    "source_id", "dataflow_id", "query_url", "retrieved_at_utc",
]


def build_url(series_key: str) -> str:
    return f"{BASE_URL}/{AGENCY_ID},{DATAFLOW_ID},{DATAFLOW_VERSION}/{series_key}"


def parse_sdmx_json(raw: bytes, query_url: str, retrieved_at_utc: str) -> pd.DataFrame:
    """Turn one SDMX-JSON 2.0 data message into one row per (series key, period).

    Shape of the message: data.structures[0].dimensions.observation lists the 9 dimensions in
    order (8 series dimensions + TIME_PERIOD), each with its allowed values and English names.
    data.dataSets[0].observations is a dict whose KEY is a ":"-joined list of positions into
    those value lists, and whose VALUE is [observation_value, attribute positions...].
    """
    message = json.loads(raw.decode("utf-8"))
    structure = message["data"]["structures"][0]
    dims = structure["dimensions"]["observation"]
    obs_attrs = structure["attributes"]["observation"]
    status_pos = next((i for i, a in enumerate(obs_attrs) if a["id"] == "OBS_STATUS"), None)

    # A valid query that matches nothing still returns HTTP 200 and a full message, but with
    # "observations": null. That is an empty result, not a crash and not a failure of the request.
    observations = message["data"]["dataSets"][0].get("observations") or {}
    if not observations:
        raise NoObservations("OECD returned 0 observations for this query.")

    rows = []
    for key, observation in observations.items():
        codes = {d["id"]: d["values"][int(p)] for d, p in zip(dims, key.split(":"))}
        status = {"id": "", "name": ""}
        if status_pos is not None and len(observation) > status_pos + 1:
            status = obs_attrs[status_pos]["values"][observation[status_pos + 1]]
        rows.append({
            "ref_area": codes["REF_AREA"]["id"], "ref_area_name": codes["REF_AREA"]["name"],
            "frequency": codes["FREQ"]["id"], "frequency_name": codes["FREQ"]["name"],
            "methodology": codes["METHODOLOGY"]["id"],
            "methodology_name": codes["METHODOLOGY"]["name"],
            "measure": codes["MEASURE"]["id"], "measure_name": codes["MEASURE"]["name"],
            "unit_measure": codes["UNIT_MEASURE"]["id"],
            "unit_label": codes["UNIT_MEASURE"]["name"],
            "expenditure": codes["EXPENDITURE"]["id"],
            "expenditure_name": codes["EXPENDITURE"]["name"],
            "adjustment": codes["ADJUSTMENT"]["id"],
            "adjustment_name": codes["ADJUSTMENT"]["name"],
            "transformation": codes["TRANSFORMATION"]["id"],
            "transformation_name": codes["TRANSFORMATION"]["name"],
            "series_key": ".".join(codes[d["id"]]["id"] for d in dims if d["id"] != "TIME_PERIOD"),
            "period": codes["TIME_PERIOD"]["id"],      # observation period, NOT retrieval time
            "value": float(observation[0]),
            "obs_status": status["id"], "obs_status_name": status["name"],
            "source_id": SOURCE_ID, "dataflow_id": DATAFLOW_ID,
            "query_url": query_url, "retrieved_at_utc": retrieved_at_utc,
        })
    frame = pd.DataFrame(rows, columns=TIDY_COLUMNS)
    return frame.sort_values(["ref_area", "period"]).reset_index(drop=True)
