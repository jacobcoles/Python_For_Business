# D1-S02 setup notes (for your own reference)

Keep a copy of these details, for example in `outputs/D1-S02/setup_notes.txt`. They are what the instructor will ask
for if you need help later.

## From the support block
Copy these three lines from your readiness check:

```
executable      :
in_project_venv :
working_dir     :
```

`in_project_venv` must say `True`. If it says `False`, fix that before anything else, because every later exercise
depends on it.

## Where things are
| What | Where |
|---|---|
| December transaction file for unit N01 | `case_pack/data/clean/transactions/transactions_2025-12_N01.csv` |
| Account mapping table | `case_pack/data/clean/account_mapping.csv` |
| Your exercise output | `outputs/<session>/`, named in each participant guide |
| How to reset an exercise | The **Reset** note in the participant guide, or `RESET.md` in `learner/` |

## Discuss with your neighbour
- Before running the check, what do you expect it to report? Afterwards, did it match, and if not, which check differed?
- Why would `case_pack/data/clean/account_mapping.csv` not be found if the same code ran from your Desktop?
