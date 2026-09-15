"""D2-S03: the one business rule you write. Instructions: sessions/D2-S03/D2-S03_instructions.md

Run this file to test your rule. Then run refresh_scenarios.py to see it used in a refresh.
"""


def data_status_for_saved_data(age_in_days, max_age_days):
    """Decide how to label a saved copy of the data when today's request has failed.

    age_in_days:   how old the saved copy is, measured from when it was originally downloaded (for example 30.0)
    max_age_days:  the oldest a saved copy may be and still be reported as usable (the course policy is 35)
    Return "cached" if age_in_days is less than or equal to max_age_days, otherwise return "stale".
    """
    # YOUR TURN: replace the line below with your rule (one or two lines).
    return None


# SUPPLIED: a quick test of your rule. You do not need to change anything below.
if __name__ == "__main__":
    examples = [(3, 35, "cached"), (35, 35, "cached"), (36, 35, "stale"), (20, 20, "cached")]
    for age, limit, expected in examples:
        got = data_status_for_saved_data(age, limit)
        if got is None:
            print(f"{age} days old, limit {limit}: not written yet (YOUR TURN)")
        else:
            verdict = "ok" if got == expected else f"CHECK: expected {expected}"
            print(f"{age} days old, limit {limit}: {got}   {verdict}")
