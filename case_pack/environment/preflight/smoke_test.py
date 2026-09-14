#!/usr/bin/env python3
r"""
D1-S02 readiness check for "Python for Business with Copilot".

Run it from the course folder:

    .virtual-env-folder\Scripts\python.exe case_pack\environment\preflight\smoke_test.py   (Windows)
    .virtual-env-folder/bin/python case_pack/environment/preflight/smoke_test.py     (macOS)

What it checks
    1. Which Python is running, and whether it is the project's .virtual-env-folder.
    2. The current working directory, and whether relative paths will resolve.
    3. That every package the course needs imports, and at which version.
    4. That the course data folder resolves through a RELATIVE path.
    5. That this account may create, read and delete a file inside the course folder.

It prints a copyable support report at the end. The report contains no secrets, no
account names and no absolute home paths: everything under the user's home directory
is shown as "~/...".

Exit code 0 = ready for D1-S03.  Exit code 1 = at least one blocking problem.
Warnings never change the exit code. The script is safe to run repeatedly.

Nothing in this file shells out, so no shell quoting is involved and a course folder
whose path contains spaces is handled correctly.
"""

from __future__ import annotations

import importlib
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

# --------------------------------------------------------------------------------------
# Settings used by the checks. You do not need to change these.
# --------------------------------------------------------------------------------------

REPO_MARKERS = ("case_pack", "sessions")        # folders that show we are in the course folder
DATA_DIR_RELATIVE = "case_pack/data/clean"      # checked via a RELATIVE path, on purpose
TEMP_DIR_RELATIVE = "outputs/preflight_tmp"      # outputs/ is where the course saves your work
VENV_DIR_NAME = ".virtual-env-folder"

# package import name -> version the course was tested with
REQUIRED_PACKAGES = {
    "pandas":     "2.3.3",
    "openpyxl":   "3.1.5",
    "requests":   "2.34.2",
    "matplotlib": "3.11.2",
    "ipykernel":  "7.3.0",      # what VS Code needs to run a notebook on this interpreter
}

CHECK_IDS = {
    "interpreter": "PF-01",
    "cwd":         "PF-02",
    "packages":    "PF-03",
    "data":        "PF-04",
    "write":       "PF-05",
}

# --------------------------------------------------------------------------------------
# Result collection
# --------------------------------------------------------------------------------------

PASS, WARN, FAIL = "PASS", "WARN", "FAIL"
_results: list[tuple[str, str, str, str]] = []   # (check_id, name, status, detail)


def record(check_id: str, name: str, status: str, detail: str) -> None:
    _results.append((check_id, name, status, detail))
    print(f"  [{status:4}] {check_id} {name}: {detail}")


def redact(text: str) -> str:
    """Replace the user's home directory with '~' so the report can be pasted publicly."""
    try:
        home = str(Path.home())
    except Exception:                              # very unusual
        return text
    out = text.replace(home, "~")
    # Windows reports the same path with either separator; cover both.
    return out.replace(home.replace("\\", "/"), "~").replace(home.replace("/", "\\"), "~")


def rel_or_redacted(path: Path) -> str:
    """Show a path relative to the working directory when possible, else redacted."""
    try:
        return str(path.relative_to(Path.cwd()))
    except ValueError:
        return redact(str(path))


# --------------------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------------------

def check_interpreter() -> None:
    cid = CHECK_IDS["interpreter"]
    exe = Path(sys.executable)          # NOT resolved: a venv python is a symlink to the
                                        # base interpreter and resolving it hides the venv.
    print(f"  ---- interpreter: {redact(str(exe))}")
    print(f"  ---- environment: {redact(str(Path(sys.prefix)))}")
    print(f"  ---- version    : {sys.version.splitlines()[0]}")
    print(f"  ---- platform   : {platform.system()} {platform.release()} ({platform.machine()})")

    if sys.version_info[:2] != (3, 12):
        record(cid, "Python version", FAIL,
               f"Python {platform.python_version()} is running, but this course uses Python 3.12. "
               f"Create the '{VENV_DIR_NAME}' environment with Python 3.12 (see START_HERE.md).")
        return

    expected_venv = (Path.cwd() / VENV_DIR_NAME).resolve()
    running_prefix = Path(sys.prefix).resolve()
    if running_prefix == expected_venv:
        record(cid, "Python interpreter", PASS,
               f"Python {platform.python_version()} from the project {VENV_DIR_NAME}.")
    elif expected_venv.exists():
        # A correct environment exists in this folder and is not the one running.  That is
        # unambiguous and fixable in one step, so it BLOCKS rather than warns: otherwise the
        # script prints READY while reporting package versions the course was never tested
        # against, which is the single most confusing way for D1-S02 to fail.
        record(cid, "Python interpreter", FAIL,
               f"Running Python {platform.python_version()} from "
               f"'{redact(str(running_prefix))}', but this course folder has its own "
               f"'{VENV_DIR_NAME}' and that is what the course was tested with. "
               f"Re-run with '{VENV_DIR_NAME}/bin/python' (macOS/Linux) or "
               f"'{VENV_DIR_NAME}\\Scripts\\python.exe' (Windows), or select that "
               f"interpreter in VS Code. See troubleshooting row 1 (wrong interpreter/kernel).")
    else:
        record(cid, "Python interpreter", WARN,
               f"Running Python {platform.python_version()}; no '{VENV_DIR_NAME}' was found "
               f"in the working directory, so the interpreter could not be confirmed. "
               f"See troubleshooting row 1 (wrong interpreter/kernel).")


def check_working_directory() -> None:
    cid = CHECK_IDS["cwd"]
    cwd = Path.cwd()
    print(f"  ---- working dir: {redact(str(cwd))}")
    missing = [m for m in REPO_MARKERS if not (cwd / m).is_dir()]
    if not missing:
        record(cid, "Working directory", PASS,
               "the working directory looks like the course folder root "
               f"(found: {', '.join(REPO_MARKERS)}).")
    else:
        record(cid, "Working directory", FAIL,
               f"expected folder(s) {', '.join(missing)} were not found here. Relative paths "
               "in the course materials will not resolve. Open the course folder itself and "
               "run the command again from there. "
               "See troubleshooting row 3 (file not found / wrong working directory).")


def check_packages() -> None:
    cid = CHECK_IDS["packages"]
    for name, expected in REQUIRED_PACKAGES.items():
        try:
            module = importlib.import_module(name)
        except Exception as exc:
            record(cid, f"import {name}", FAIL,
                   f"{type(exc).__name__}: {exc}. "
                   "See troubleshooting row 2 (missing package).")
            continue
        found = getattr(module, "__version__", None)
        if found is None:
            try:
                from importlib.metadata import version as _v
                found = _v(name)
            except Exception:
                found = "unknown"
        if found == expected:
            record(cid, f"import {name}", PASS, f"version {found}.")
        else:
            record(cid, f"import {name}", WARN,
                   f"version {found} is installed; the course was tested with {expected}. "
                   "Results should still match, but report this version if a number differs.")


def check_data_folder() -> None:
    cid = CHECK_IDS["data"]
    target = Path(DATA_DIR_RELATIVE)               # deliberately relative
    resolved = target.resolve()
    print(f"  ---- data path  : '{DATA_DIR_RELATIVE}' -> {rel_or_redacted(resolved)}")
    if not target.exists():
        record(cid, "Course data folder", FAIL,
               f"the relative path '{DATA_DIR_RELATIVE}' does not exist from the current "
               "working directory. Either the working directory is wrong, or this copy of "
               "the course folder is incomplete. "
               "See troubleshooting row 3 (file not found / wrong working directory).")
        return
    if not target.is_dir():
        record(cid, "Course data folder", FAIL,
               f"'{DATA_DIR_RELATIVE}' exists but is not a folder.")
        return
    try:
        entries = sorted(p.name for p in target.iterdir() if not p.name.startswith("."))
    except PermissionError as exc:
        record(cid, "Course data folder", FAIL,
               f"the folder exists but could not be listed ({type(exc).__name__}). "
               "See troubleshooting row 4 (access restricted).")
        return
    if entries:
        preview = ", ".join(entries[:5]) + (" ..." if len(entries) > 5 else "")
        record(cid, "Course data folder", PASS,
               f"found via a relative path, {len(entries)} item(s): {preview}")
    else:
        record(cid, "Course data folder", WARN,
               "the folder was found but is empty, so the course download may be incomplete. "
               "Tell the instructor.")


def check_write_access() -> None:
    cid = CHECK_IDS["write"]
    temp_dir = Path(TEMP_DIR_RELATIVE)
    probe = temp_dir / "preflight_write_probe.txt"
    payload = f"preflight write probe {datetime.now(timezone.utc).isoformat(timespec='seconds')}"
    try:
        temp_dir.mkdir(parents=True, exist_ok=True)      # safe on a repeat run
        probe.write_text(payload, encoding="utf-8")
        read_back = probe.read_text(encoding="utf-8")
        if read_back != payload:
            record(cid, "Write / read / delete", FAIL,
                   "a file was written but read back with different contents.")
            return
    except PermissionError as exc:
        record(cid, "Write / read / delete", FAIL,
               f"permission denied creating '{TEMP_DIR_RELATIVE}' ({exc.__class__.__name__}). "
               "The course folder may be in a location your account or device policy protects. "
               "See troubleshooting row 4 (access restricted).")
        return
    except OSError as exc:
        record(cid, "Write / read / delete", FAIL,
               f"could not write inside '{TEMP_DIR_RELATIVE}': {type(exc).__name__}: {exc}. "
               "See troubleshooting row 4 (access restricted).")
        return
    finally:
        try:
            probe.unlink()                                # safe on a repeat run
        except FileNotFoundError:
            pass
        except OSError:
            pass
    still_there = probe.exists()
    if still_there:
        record(cid, "Write / read / delete", WARN,
               f"wrote and read '{rel_or_redacted(probe)}' but could not delete it. "
               "Delete it by hand before the next run.")
    else:
        record(cid, "Write / read / delete", PASS,
               f"created, read and deleted a file under '{TEMP_DIR_RELATIVE}'.")


# --------------------------------------------------------------------------------------
# Support report
# --------------------------------------------------------------------------------------

def support_report() -> str:
    fails = [r for r in _results if r[2] == FAIL]
    warns = [r for r in _results if r[2] == WARN]
    exe = redact(str(Path(sys.executable)))
    cwd = redact(str(Path.cwd()))
    versions = []
    for name in REQUIRED_PACKAGES:
        mod = sys.modules.get(name)
        versions.append(f"{name}={getattr(mod, '__version__', 'not-imported') if mod else 'not-imported'}")

    lines = [
        "----- COPY FROM HERE -----",
        "course      : Python for Business with Copilot - D1-S02 readiness check",
        f"report_utc  : {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        f"os          : {platform.system()} {platform.release()} ({platform.machine()})",
        f"python      : {platform.python_version()} ({platform.python_implementation()})",
        f"executable  : {exe}",
        f"environment : {redact(str(Path(sys.prefix)))}",
        f"working_dir : {cwd}",
        f"in_project_venv : {Path(sys.prefix).resolve() == (Path.cwd() / VENV_DIR_NAME).resolve()}",
        f"packages    : {', '.join(versions)}",
        f"data_path   : {DATA_DIR_RELATIVE} (relative)",
        f"result      : {'BLOCKED' if fails else 'READY'} "
        f"({len(fails)} failed, {len(warns)} warning(s), {len(_results)} checks)",
    ]
    for cid, name, status, detail in _results:
        if status != PASS:
            lines.append(f"{status.lower():4} {cid} {name}: {detail}")
    lines.append("----- COPY TO HERE -----")
    return redact("\n".join(lines))


# --------------------------------------------------------------------------------------

def main() -> int:
    print("=" * 78)
    print(" Python for Business with Copilot - readiness check (D1-S02)")
    print("=" * 78)

    print("\n1. Python interpreter")
    check_interpreter()
    print("\n2. Working directory")
    check_working_directory()
    print("\n3. Required packages")
    check_packages()
    print("\n4. Course data folder (relative path)")
    check_data_folder()
    print("\n5. Write / read / delete inside the course folder")
    check_write_access()

    fails = [r for r in _results if r[2] == FAIL]
    warns = [r for r in _results if r[2] == WARN]

    print("\n" + "-" * 78)
    if fails:
        print(f"RESULT: NOT READY - {len(fails)} blocking problem(s), {len(warns)} warning(s).")
        print("Work through the failed checks above, then run this script again.")
        print("If you cannot clear them, paste the support report below to your instructor.")
    elif warns:
        print(f"RESULT: READY, with {len(warns)} warning(s). You can continue to D1-S03.")
        print("Mention the warnings to your instructor if a number you produce looks wrong.")
    else:
        print("RESULT: READY. All checks passed. You can continue to D1-S03.")
    print("-" * 78 + "\n")

    print(support_report())
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
