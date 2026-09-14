# Received after the first run

`account_mapping_updated.csv` is the mapping table with the missing account added, sent
by finance once you queried it.

Do **not** edit the transaction exports. Point your process at this mapping file instead,
rerun, and record in your handover note that the mapping changed and why.

After the correction your January totals must match the clean January checkpoint,
`case_pack/data/clean/checkpoints/actuals_by_line_2026-01.csv` exactly. That is your
independent check that the correction was the right one.
