"""D1-S06: run all nine controls, including your two functions. Needs the D1-S06 ZIP from the instructor."""
from pathlib import Path
import sys
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-folder', default='case_pack/data/clean')
    parser.add_argument('--period', default='2025-12')
    parser.add_argument('--output-folder', default='outputs/D1-S06')
    args = parser.parse_args()
    component = Path('outputs/handoffs/D1-S06/report_components.py')
    if not component.exists():
        print('SETUP: cannot find outputs/handoffs/D1-S06/report_components.py. Check that you are running from the course folder and that the D1-S06 ZIP from the instructor was extracted into it.')
        return 2
    sys.path.insert(0, str(component.parent.resolve()))
    import report_components as report
    inputs = report.load_inputs(args.input_folder, args.period)
    controls, exceptions, release = report.run_controls(inputs)
    out = Path(args.output_folder)
    out.mkdir(parents=True, exist_ok=True)
    controls.to_csv(out / 'control_summary.csv', index=False)
    exceptions.to_csv(out / 'exceptions.csv', index=False)
    print(controls[['check_id', 'status', 'affected_count']].to_string(index=False))
    print('Release:', release)
    return 2 if release == 'blocked' else 0


if __name__ == '__main__':
    raise SystemExit(main())
