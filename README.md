# Personal Budget Manager

A small command-line tool to add, list and report income and expenses.
Data is saved in `data/transactions.json`, so it is still there the next time you run the tool.

## 1. Setup

You only need Python 3 (no extra packages).
Open a terminal **inside the `budget-manager` folder** (all commands below are run from there).
On Mac, write `python3` instead of `python` in every command.

```
python --version
```

## 2. Run

```
python src/budget_manager/cli.py --help
```

| Command | What it does |
|---|---|
| `add AMOUNT --category C --date YYYY-MM-DD [--kind expense/income] [--currency EUR]` | add one transaction |
| `list [--month YYYY-MM] [--category C]` | show transactions, optionally filtered |
| `summary` | total income, total expenses, balance, expenses per category |
| `import FILE.csv` | add all valid rows of a CSV file and report the invalid ones |
| `backup FILE.json` | save a copy of the data in a NEW file (never overwrites) |
| `undo` | remove the last transaction (the file is updated too) |

Allowed values: kind = `expense`, `income` · category = `food`, `transport`, `rent`, `leisure`, `salary`, `other` · currency = `EUR`, `USD`, `GBP`.

## 3. Example

```
python src/budget_manager/cli.py import data/sample_transactions.csv
python src/budget_manager/cli.py add 18.50 --category food --date 2026-09-15
python src/budget_manager/cli.py add 2000 --kind income --category salary --date 2026-10-01
python src/budget_manager/cli.py list --month 2026-09
python src/budget_manager/cli.py summary
python src/budget_manager/cli.py backup data/backup-2026-09.json
python src/budget_manager/cli.py undo
```

The import prints which rows were rejected and why, for example:

```
Row 5: amount '-12' must be > 0 (negative amounts are not allowed).
Row 6: category 'pizza' is unknown. Use one of: food, transport, rent, leisure, salary, other.
Imported 4 transactions, rejected 6.
```

Invalid data is never saved. Error messages go to the error output (stderr).
A successful command ends with exit code 0. A failed `add`, `backup` or `undo`, or a CSV file
that does not exist, ends with exit code 1. `import` skips the invalid rows, reports them,
and saves the valid ones.

## 4. Test

```
python src/budget_manager/test_budget.py
```

Expected output: `All 9 tests passed.`
The tests cover one normal case (adding a valid expense) and boundary / malformed cases:
negative amount, amount 0, amount `abc`, unknown category, month 13, 31 September,
summary totals, filtering, undo, and a save → load round-trip.

## 5. Known limitations

- Only one currency per transaction; totals do not convert between currencies.
- Dates are checked for format and real month/day, but 29 February is accepted every year.
- The CSV reader is simple: values must not contain commas.
- `undo` removes only the most recent transaction, one at a time.
- If `data/transactions.json` is edited by hand and broken, the program stops with Python's error.
