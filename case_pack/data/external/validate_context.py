"""Shared live semantic guard, implementing invariants.json for a bounded area/window."""
import datetime as dt
from urllib.parse import parse_qs, urlparse
import pandas as pd
try:
    from .oecd_sdmx import TIDY_COLUMNS, DATAFLOW_ID, SOURCE_ID
except ImportError:
    from oecd_sdmx import TIDY_COLUMNS, DATAFLOW_ID, SOURCE_ID


def validate_context(frame, areas=('EA', 'SWE'), start='2024-01', end='2026-01'):
    """Return a readable problem or None. Never pin revised live observation values."""
    if list(frame.columns) != TIDY_COLUMNS:
        return 'columns differ from the frozen tidy contract'
    if frame.empty:
        return 'no observations'
    required = [c for c in TIDY_COLUMNS if c not in ('obs_status', 'obs_status_name')]
    if frame[required].isna().any().any() or frame[required].astype(str).eq('').any().any():
        return 'missing required values'
    constants = {'frequency': 'M', 'methodology': 'HICP', 'measure': 'CPI', 'unit_measure': 'PA',
                 'expenditure': '_T', 'adjustment': 'N', 'transformation': 'GY',
                 'source_id': SOURCE_ID, 'dataflow_id': DATAFLOW_ID}
    for column, expected in constants.items():
        if set(frame[column]) != {expected}:
            return f'{column} does not match {expected}'
    if set(frame.ref_area) != set(areas):
        return 'reference areas differ from requested scope'
    if not pd.api.types.is_numeric_dtype(frame.value) or not frame.value.between(-50, 100).all():
        return 'non-numeric, missing or implausible value (unit change?)'
    if frame.duplicated(['series_key', 'period']).any():
        return 'duplicate series/period'
    periods = set(pd.period_range(start, end, freq='M').astype(str))
    for area, group in frame.groupby('ref_area'):
        if set(group.period.astype(str)) != periods or len(group) != len(periods):
            return 'requested monthly coverage has gaps, duplicates or extra periods'
        if set(group.series_key) != {area + '.M.HICP.CPI.PA._T.N.GY'}:
            return 'series key disagrees with decoded dimensions'
    if frame.retrieved_at_utc.nunique() != 1 or frame.query_url.nunique() != 1:
        return 'provenance is not constant within one retrieval'
    try:
        retrieved = dt.datetime.strptime(str(frame.retrieved_at_utc.iloc[0]), '%Y-%m-%dT%H:%M:%SZ')
        if retrieved.strftime('%Y-%m') <= end:
            return 'retrieval must be later than this historical observation window'
        url = urlparse(str(frame.query_url.iloc[0]))
        params = parse_qs(url.query)
        if url.hostname != 'sdmx.oecd.org' or DATAFLOW_ID not in url.path:
            return 'query provenance is not the adopted OECD dataflow'
        if params.get('startPeriod') != [start] or params.get('endPeriod') != [end]:
            return 'query provenance window does not match requested coverage'
    except (TypeError, ValueError):
        return 'invalid timestamp or query provenance'
    return None
