"""Supplied helpers for D2-S05 (baseline forecast and scenarios).

Learners call these from the notebook. They do not need to read this file.
Rules: case_pack/contracts/metrics.md (scenario multipliers apply once to each month's baseline; each report line is
rounded to cents before any operating result is summed). The December 2025 cutoff is enforced by the checks.
"""
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import StrMethodFormatter

CLEAN = Path("case_pack/data/clean")
OUT = Path("outputs/D2-S05")
KEY = ["period", "entity", "report_line"]
LINES = ["revenue", "direct_cost", "overhead"]


def load_inputs():
    """Read the three planning tables and print their sizes."""
    history = pd.read_csv(CLEAN / "history/monthly_actuals_history.csv", dtype={"period": str})
    baseline = pd.read_csv(CLEAN / "planning/baseline_forecast.csv", dtype={"period": str, "source_period": str,
                                                                            "data_cutoff": str})
    assumptions = pd.read_csv(CLEAN / "scenario_assumptions.csv")
    print(f"history:     {len(history)} rows (expected 324 = 36 months x 3 units x 3 report lines)")
    print(f"baseline:    {len(baseline)} rows (expected 27 = 3 future months x 3 units x 3 report lines)")
    print(f"assumptions: {len(assumptions)} rows (expected 3 scenarios)")
    return history, baseline, assumptions


def check_baseline(history, baseline):
    """Check the history is complete and each baseline row copies the same month one year earlier."""
    months = set(pd.period_range("2023-01", "2025-12", freq="M").astype(str))
    complete = all(set(group["period"]) == months for _, group in history.groupby(["entity", "report_line"]))
    lookup = history.set_index(KEY)["actual_amount"]
    copied = all(
        row.source_period == f"{int(row.period[:4]) - 1}-{row.period[5:]}"
        and abs(row.amount - lookup[(row.source_period, row.entity, row.report_line)]) < 0.005
        for row in baseline.itertuples())
    cutoff = baseline["data_cutoff"].eq("2025-12").all() and history["period"].max() == "2025-12"
    print("OK: every unit and report line has all 36 months, January 2023 to December 2025." if complete else
          "PROBLEM: some months are missing from the history.")
    print("OK: each of the 27 baseline rows is the same month one year earlier." if copied else
          "PROBLEM: a baseline row does not match its historical month.")
    print("OK: nothing after December 2025 is used." if cutoff else "PROBLEM: data after the December 2025 cutoff.")


def history_chart(history):
    """Show three years of monthly totals for all units, one panel per report line."""
    lines = history.groupby(["period", "report_line"])["actual_amount"].sum().unstack()
    fig, axes = plt.subplots(3, 1, figsize=(10, 7), sharex=True)
    for ax, line in zip(axes, LINES):
        ax.plot(pd.to_datetime(lines.index), lines[line])
        ax.set_title(line.replace("_", " "), loc="left", fontsize=10)
        ax.set_ylabel("EUR")
        ax.yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))
        ax.grid(alpha=.2)
    fig.suptitle("Northbridge observed history, 2023 to 2025 | all three units (costs are negative)")
    fig.tight_layout()
    plt.close(fig)          # the notebook shows the returned figure once
    return fig


def holdout_errors(history):
    """Test the method on a past period: forecast October to December 2025 from 2024, then compare with what happened."""
    actual = history[history["period"].isin(["2025-10", "2025-11", "2025-12"])].copy()
    actual["source_period"] = actual["period"].str.replace("2025", "2024")
    earlier = history.rename(columns={"period": "source_period", "actual_amount": "forecast"})
    test = actual.merge(earlier, on=["source_period", "entity", "report_line"])
    test["size_of_error"] = (test["actual_amount"] - test["forecast"]).abs()
    table = (test.groupby("report_line")["size_of_error"].mean().reindex(LINES).round(2)
             .rename("average size of error (EUR)").reset_index())
    print("Forecast made with a September 2025 cutoff, for October to December 2025 (9 observations per line):")
    return table


def _apply(baseline, assumption_rows):
    records = []
    for b in baseline.itertuples():
        for a in assumption_rows.itertuples():
            factor = Decimal(str(getattr(a, f"{b.report_line}_multiplier")))
            value = (Decimal(str(b.amount)) * factor).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            records.append({"period": b.period, "entity": b.entity, "scenario_id": a.scenario_id,
                            "report_line": b.report_line, "amount": float(value), "data_cutoff": b.data_cutoff})
    return pd.DataFrame(records)


def original_scenarios(baseline, assumptions):
    """Apply the three original scenarios and check the neutral one reproduces the baseline."""
    original = _apply(baseline, assumptions)
    neutral = original[original["scenario_id"] == "baseline"].merge(baseline, on=KEY)
    same = len(neutral) == 27 and (neutral["amount_x"] - neutral["amount_y"]).abs().lt(0.005).all()
    print(f"OK: {len(original)} scenario rows (3 months x 3 units x 3 lines x 3 scenarios)." if len(original) == 81
          else f"PROBLEM: {len(original)} rows, expected 81.")
    print("OK: the neutral 'baseline' scenario (all multipliers 1.00) matches the baseline exactly." if same else
          "PROBLEM: the neutral scenario differs from the baseline.")
    return original


def chosen_scenarios(baseline, finance_revenue, finance_direct_cost, my_revenue, my_direct_cost, folder=OUT):
    """Build finance's case and your case from the four settings, save them, and return the results."""
    values = [finance_revenue, finance_direct_cost, my_revenue, my_direct_cost]
    if not all(isinstance(v, (int, float)) and 0.5 <= v <= 1.5 for v in values):
        raise SystemExit("Each multiplier must be a number from 0.5 to 1.5, written like 1.05 (no percent sign).")
    if (finance_revenue, finance_direct_cost) == (1.0, 1.0):
        print("NOT DONE YET: finance's case still has 1.00 for both, so nothing was saved. Translate finance's "
              "expectations into multipliers in Step 5, then run this cell again.")
        return None
    if finance_direct_cost < 1.00:
        print(f"PROBLEM: finance expects supplier costs to RISE, so FINANCE_DIRECT_COST_MULTIPLIER should be above "
              f"1.00. You entered {finance_direct_cost}, which is a fall of {(1 - finance_direct_cost) * 100:.0f}%. "
              "Costs are stored as negative numbers, so a rise means a bigger multiplier, not a smaller one.")
    if finance_revenue < 1.00:
        print(f"PROBLEM: finance expects sales to GROW, so FINANCE_REVENUE_MULTIPLIER should be above 1.00. "
              f"You entered {finance_revenue}.")
    if not (min(finance_revenue, 1.10) <= my_revenue <= max(finance_revenue, 1.10)
            and min(finance_direct_cost, 1.08) <= my_direct_cost <= max(finance_direct_cost, 1.08)):
        print("Note: your own case is not between finance's case and the original growth plan (revenue 1.10, direct "
              "cost 1.08). That is allowed, but give your reason in the recommendation.")
    chosen = pd.DataFrame([
        {"scenario_id": "finance_case", "revenue_multiplier": finance_revenue,
         "direct_cost_multiplier": finance_direct_cost, "overhead_multiplier": 1.00},
        {"scenario_id": "my_case", "revenue_multiplier": my_revenue,
         "direct_cost_multiplier": my_direct_cost, "overhead_multiplier": 1.00}])
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    chosen.to_csv(folder / "changed_assumptions.csv", index=False, float_format="%.4f")
    print(chosen.to_string(index=False))
    print(f"Saved {folder.as_posix()}/changed_assumptions.csv")
    return _apply(baseline, chosen)


def compare_n02_february(baseline, original, chosen):
    """Show N02's February 2026 lines under original growth, finance's case and your case."""
    if chosen is None:
        print("NOT DONE YET: finish Step 5 (the two cases) first, then run this cell again.")
        return None
    def pick(table, scenario):
        rows = table[(table["period"] == "2026-02") & (table["entity"] == "N02") & (table["scenario_id"] == scenario)]
        return rows.set_index("report_line")["amount"].reindex(LINES)
    base = baseline[(baseline["period"] == "2026-02") & (baseline["entity"] == "N02")].set_index("report_line")["amount"]
    table = pd.DataFrame({"baseline": base.reindex(LINES), "original growth": pick(original, "growth"),
                          "finance case": pick(chosen, "finance_case"), "my case": pick(chosen, "my_case")})
    table.loc["operating result"] = table.sum().round(2)
    print("N02, February 2026, EUR. Costs are negative. Operating result is the sum of the three lines.\n")
    print(table.to_string(float_format=lambda x: f"{x:,.2f}"))
    for case in ["finance case", "my case"]:
        change = table.loc["operating result", case] - table.loc["operating result", "original growth"]
        print(f"\n{case}: operating result {change:+,.2f} EUR compared with original growth")
    return table


def scenario_chart(history, original, chosen, folder=OUT):
    """Plot observed 2025 history and next quarter under the three cases; save the picture."""
    if chosen is None:
        print("NOT DONE YET: finish Step 5 (the two cases) first, then run this cell again.")
        return None
    observed = history.groupby("period")["actual_amount"].sum().loc["2025-01":"2025-12"]
    cases = pd.concat([original[original["scenario_id"] == "growth"], chosen], ignore_index=True)
    future = cases.groupby(["period", "scenario_id"])["amount"].sum().unstack()
    labels = {"growth": "original growth", "finance_case": "finance case", "my_case": "my case"}
    styles = {"growth": ("#2874a6", "s"), "finance_case": ("#b14b39", "^"), "my_case": ("#8e44ad", "D")}
    fig, ax = plt.subplots(figsize=(11, 5.5))
    ax.plot(pd.to_datetime(observed.index), observed.values, color="#374151", label="observed history")
    for name in ["growth", "finance_case", "my_case"]:
        colour, marker = styles[name]
        ax.plot(pd.to_datetime(future.index), future[name], color=colour, marker=marker, linestyle="--",
                label=labels[name])
    ax.axvline(pd.Timestamp("2025-12-15"), color="#777777", linestyle=":", label="December 2025 cutoff")
    ax.set_title("Northbridge operating result: 2025 observed, next quarter under three cases | all three units")
    ax.set_ylabel("Operating result, EUR")
    ax.yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))
    ax.legend(fontsize=9)
    ax.grid(alpha=.2)
    fig.text(.08, .015, "Fictional EUR data. Seasonal-naive baseline. The cases are assumptions, not probabilities.",
             fontsize=9)
    fig.tight_layout(rect=(0, .05, 1, 1))
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    fig.savefig(folder / "scenario_figure.png", dpi=150)
    print(f"Saved {folder.as_posix()}/scenario_figure.png")
    plt.close(fig)          # the notebook shows the returned figure once
    return fig
