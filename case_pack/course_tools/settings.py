"""Supplied setting checks, so a mistyped setting stops with a plain sentence instead of behaving oddly.

Learners do not need to read this file. The rule it enforces is the one on the course start page:
text settings need quotation marks; True, False and numbers never do.
"""


def _stop(message):
    raise SystemExit("STOPPED: " + message)


def require_true_or_false(name, value):
    """A yes/no setting. Catches the common `"False"`, which Python treats as true."""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        _stop(f'{name} is the text "{value}", not a yes/no value. Write {name} = True or {name} = False, '
              "with a capital letter and no quotation marks. "
              f'(Python treats any text, even "False", as true, so the run would not do what the file says.)')
    _stop(f"{name} must be True or False, with a capital letter and no quotation marks.")


def require_number(name, value, low=None, high=None):
    """A number setting. Catches quotation marks and values outside the allowed range."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        _stop(f"{name} must be a number written without quotation marks, for example {name} = 35.")
    if low is not None and high is not None and not (low <= value <= high):
        _stop(f"{name} must be between {low} and {high}. You wrote {value}.")
    return value


def require_choice(name, value, choices):
    """A text setting with a fixed list of values."""
    allowed = ", ".join(f'"{c}"' for c in choices)
    if not isinstance(value, str):
        _stop(f"{name} must be one of {allowed}, with the quotation marks.")
    if value not in choices:
        _stop(f'{name} is "{value}", which is not one of {allowed}. Check the spelling and the quotation marks.')
    return value
