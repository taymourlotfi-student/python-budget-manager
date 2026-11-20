# Design Rationale

I split the program into layers so each file has one job: `cli.py` only reads the command and
prints results, `services.py` holds the budget rules (add, filter, summarize, undo), `storage.py`
only reads and writes files, and `validation.py` checks every input in one place. Because the
business logic in `services.py` never uses `input()`, `print()` or files, I can test it directly
with `assert` without running the command line. All validation happens at the two entry points
(the `add` command and the CSV `import`), and it returns clear messages such as
"Row 5: amount '-12' must be > 0" instead of silently fixing the data, so the user knows exactly
what to correct. The trade-off is a few more files for a small program, but every rule lives in
one obvious place. For `undo`, the program saves the file immediately after removing the
transaction, so the data on disk always matches the real state, even if the program is closed
and opened again.
