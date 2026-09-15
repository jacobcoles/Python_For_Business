"""Supplied helpers for D1-S04 (combining several finance files).

Learners call these from the notebook. They do not need to read this file.
Every check prints a plain-English OK, PROBLEM or NOT DONE YET message and says what to look at next.
"""
import json
from pathlib import Path

import pandas as pd

CLEAN = Path("case_pack/data/clean")
REPORT_LINES = ["revenue", "direct_cost", "overhead"]


def _say(ok, good, bad):
    print(("OK: " + good) if ok else ("PROBLEM: " + bad))
    return ok


def _not_done(value, name):
    if value is None:
        print(f"NOT DONE YET: `{name}` is still empty. Run your YOUR TURN cell first, then this check.")
        return True
    if not isinstance(value, pd.DataFrame):
        print(f"PROBLEM: `{name}` should be a table (a DataFrame), but it is a {type(value).__name__}. "
              "Ask Copilot to make sure the code stores a table in that name.")
        return True
    return False


def read_manifest(period="2025-12"):
    """Return the manifest: the small file listing which exports belong to the month."""
    return json.loads((CLEAN / f"input_manifest_{period}.json").read_text(encoding="utf-8"))


def load_transactions(manifest):
    """Read exactly the files the manifest lists, as text, and note where each row came from."""
    parts = []
    for relative in manifest["transaction_files"]:
        source = CLEAN / relative
        frame = pd.read_csv(source, dtype=str, keep_default_na=False)
        frame["source_file"] = source.name
        frame["source_row"] = range(1, len(frame) + 1)
        parts.append(frame)
        print(f"Loaded {source.name}: {len(frame)} rows")
    rows = pd.concat(parts, ignore_index=True)
    print(f"Total: {len(rows)} rows from {len(parts)} files")
    return rows


def unit_totals(period="2025-12"):
    """The units' own totals, sent separately from the exports. Used to predict and to check."""
    controls = pd.read_csv(CLEAN / "source_controls.csv", dtype={"period": str})
    table = controls[controls["period"] == period][
        ["entity", "expected_raw_rows", "expected_posted_rows", "expected_posted_amount"]]
    return table.reset_index(drop=True)


def check_posted(posted, period="2025-12"):
    """Step 4 check: only posted EUR rows remain, and amount is now a number."""
    if _not_done(posted, "posted"):
        return
    expected_rows = int(unit_totals(period)["expected_posted_rows"].sum())
    results = [
        _say(set(posted["status"]) == {"posted"},
             "every row has status posted.",
             f"statuses still present: {sorted(set(posted['status']))}. Keep only rows where status is posted."),
        _say(set(posted["currency"]) == {"EUR"},
             "every row is in EUR.",
             f"currencies present: {sorted(set(posted['currency']))}. Keep only EUR rows."),
        _say(len(posted) == expected_rows,
             f"{len(posted)} rows, the same as the units' own count of posted rows ({expected_rows}).",
             f"{len(posted)} rows, but the units say {expected_rows} posted rows. Check the filter."),
        _say(pd.api.types.is_numeric_dtype(posted["amount"]),
             "amount is a number, so it can be added up.",
             "amount is still text. Ask Copilot to convert the amount column to a number after filtering "
             "(for example with pd.to_numeric). Do not use abs(): signs matter."),
    ]
    if pd.api.types.is_numeric_dtype(posted["amount"]):
        expected_total = float(unit_totals(period)["expected_posted_amount"].sum())
        total = round(float(posted["amount"].sum()), 2)
        if (posted["amount"] >= 0).all():
            print("PROBLEM: every amount is positive, so the signs were removed (abs() was used somewhere). "
                  "Costs must stay negative. Go back to Step 4 and convert the amounts without abs().")
        elif abs(total - expected_total) > 0.01:
            print(f"PROBLEM: the posted amounts add up to {total:,.2f} EUR, but the units' own totals add up to "
                  f"{expected_total:,.2f} EUR. Check the filter and the conversion in Step 4.")
        else:
            print(f"OK: the posted amounts add up to {total:,.2f} EUR, the same as the units' own totals.")
    return None


def check_joined(joined, posted):
    """Step 5 check: attaching report lines kept every row, added none and lost no money."""
    if _not_done(joined, "joined") or _not_done(posted, "posted"):
        return
    if "report_line" not in joined.columns:
        print("PROBLEM: `joined` has no report_line column. The mapping file was not attached. "
              "Ask Copilot to join the mapping on account_code.")
        return
    if not (pd.api.types.is_numeric_dtype(posted["amount"]) and pd.api.types.is_numeric_dtype(joined["amount"])):
        print("PROBLEM: amount is still text, so the totals cannot be compared. Go back to Step 4 and convert it.")
        return
    missing = joined["report_line"].isna().sum()
    before = round(float(posted["amount"].sum()), 2)
    after = round(float(joined["amount"].sum()), 2)
    results = [
        _say(len(joined) == len(posted),
             f"{len(joined)} rows before and after attaching report lines, so no row was duplicated or dropped.",
             f"{len(posted)} rows before but {len(joined)} after. More rows usually means an account code "
             "appears twice in the mapping; fewer means rows without a match were dropped (use a left join)."),
        _say(missing == 0,
             "every account code found a report line.",
             f"{missing} rows have no report line: their account code is not in the mapping. "
             "Keep them visible and look at their account_code values."),
        _say(before == after,
             f"the total amount is unchanged ({after:,.2f} EUR).",
             f"the total changed from {before:,.2f} to {after:,.2f} EUR. The join should never change the money."),
    ]
    print("Note: on this clean month these three results look the same whether or not your join keeps unmatched rows "
          "and stops on a duplicated account. Step 7 puts your own join to that test.")
    return None


def check_by_line(by_line, period="2025-12"):
    """Step 6 check: nine lines, and each unit's result matches the unit's own total."""
    if _not_done(by_line, "by_line"):
        return
    needed = {"entity", "report_line", "actual_amount"}
    in_index = needed - set(by_line.columns) - {"actual_amount"}
    if in_index and in_index.issubset(set(by_line.index.names or [])):
        print(f"PROBLEM: {', '.join(sorted(in_index))} are not columns of `by_line`: they are the table's row labels "
              "(its index). Ask Copilot to add .reset_index(), or to group with as_index=False.")
        return
    if not needed.issubset(by_line.columns):
        print(f"PROBLEM: `by_line` needs the columns {sorted(needed)}; it has {list(by_line.columns)}. "
              "Ask Copilot to name the total column actual_amount.")
        return
    ok_rows = _say(len(by_line) == 9,
                   "9 rows: 3 units times revenue, direct_cost and overhead.",
                   f"{len(by_line)} rows instead of 9. Group by period, entity and report_line.")
    totals = unit_totals(period).set_index("entity")["expected_posted_amount"]
    mine = by_line.groupby("entity")["actual_amount"].sum().round(2)
    all_match = True
    for entity, expected in totals.items():
        got = mine.get(entity)
        match = got is not None and abs(got - expected) <= 0.01
        all_match &= match
        if got is None:
            print(f"PROBLEM: there is no {entity} in by_line. Check the filter in Step 4 and the grouping.")
            continue
        _say(match,
             f"{entity} operating result {got:,.2f} EUR matches the unit's own total.",
             f"{entity} operating result is {got:,.2f} EUR but the unit's own total is {expected:,.2f} EUR.")


def faulty_mapping():
    """The mapping finance once sent with account 0500 listed twice."""
    faulty = pd.read_csv("case_pack/data/faulty/F03_duplicate_mapping/account_mapping.csv", dtype=str)
    print("This mapping lists account 0500 twice:")
    print(faulty[faulty["account_code"].duplicated(keep=False)].to_string(index=False))
    return faulty


def check_faulty_join(joined_faulty, posted):
    """Step 7 check: what your own join did with the faulty mapping."""
    if joined_faulty is None:
        print("OK: your join stopped instead of producing a table, which is the safeguard working. "
              "A duplicated account code cannot silently copy transactions.")
        return
    if _not_done(posted, "posted"):
        return
    rows = len(joined_faulty)
    total = round(float(joined_faulty["amount"].sum()), 2) if pd.api.types.is_numeric_dtype(joined_faulty["amount"]) else None
    if rows > len(posted):
        print(f"PROBLEM: your join has no safeguard. It produced {rows} rows from {len(posted)}, and the total became "
              f"{total:,.2f} EUR instead of {round(float(posted['amount'].sum()), 2):,.2f} EUR, with no error at all. "
              'Add validate="many_to_one" to your join in Step 5 and try again.')
    else:
        print(f"PROBLEM: the join returned {rows} rows. Check that you used the faulty mapping in this cell.")


def duplicate_mapping_demo(posted):
    """Step 7: what a mapping with account 0500 listed twice does, with and without the safeguard."""
    if _not_done(posted, "posted"):
        return
    if not pd.api.types.is_numeric_dtype(posted["amount"]):
        print("NOT DONE YET: amount in `posted` is still text, so totals cannot be compared. Finish Step 4 first.")
        return
    faulty = pd.read_csv("case_pack/data/faulty/F03_duplicate_mapping/account_mapping.csv", dtype=str)
    print("The faulty mapping lists account 0500 twice:")
    print(faulty[faulty["account_code"].duplicated(keep=False)].to_string(index=False))
    print()
    print("1) With the safeguard validate='many_to_one':")
    try:
        posted.merge(faulty, on="account_code", how="left", validate="many_to_one")
        print("   no error (unexpected)")
    except pd.errors.MergeError as error:
        print(f"   STOPPED with an error: {error}")
    print("2) Without the safeguard:")
    silent = posted.merge(faulty, on="account_code", how="left")
    print(f"   no error, but {len(posted)} rows became {len(silent)} rows,")
    print(f"   and the total became {silent['amount'].sum():,.2f} EUR instead of {posted['amount'].sum():,.2f} EUR.")


def compare_with_checkpoint(by_line, period="2025-12"):
    """Step 8: compare with the checkpoint, the correct result prepared separately by the course team."""
    if _not_done(by_line, "by_line"):
        return None
    checkpoint = pd.read_csv(CLEAN / "checkpoints" / f"actuals_by_line_{period}.csv", dtype={"period": str})
    mine = by_line[["entity", "report_line", "actual_amount"]].rename(columns={"actual_amount": "your_amount"})
    table = checkpoint.rename(columns={"actual_amount": "checkpoint_amount"}).merge(
        mine, on=["entity", "report_line"], how="outer")
    table["difference"] = (table["your_amount"] - table["checkpoint_amount"]).round(2)
    table["match"] = table["difference"].abs().le(0.01).map({True: "yes", False: "NO"})
    matched = (table["match"] == "yes").sum()
    _say(matched == 9 and len(table) == 9,
         "all 9 figures match the checkpoint within EUR 0.01.",
         f"{matched} of 9 figures match. Look at the rows marked NO below.")
    return table[["entity", "report_line", "checkpoint_amount", "your_amount", "difference", "match"]]


def save(by_line, path="outputs/D1-S04/actuals_by_line.csv"):
    """Save your nine lines in business order for later sessions."""
    if _not_done(by_line, "by_line"):
        return
    order = {name: i for i, name in enumerate(REPORT_LINES)}
    tidy = by_line.sort_values(["entity", "report_line"], key=lambda s: s.map(order) if s.name == "report_line" else s)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tidy.to_csv(path, index=False, float_format="%.2f")
    print(f"Saved {path.as_posix()} ({len(tidy)} rows)")
