# cli.py — the command-line interface (only input/output here).
# Run from the budget-manager folder, for example:
#   python src/budget_manager/cli.py add 18.50 --category food --date 2026-09-04
#   python src/budget_manager/cli.py list --month 2026-09
#   python src/budget_manager/cli.py summary
#   python src/budget_manager/cli.py import data/sample_transactions.csv
#   python src/budget_manager/cli.py backup data/backup.json
#   python src/budget_manager/cli.py undo
#   python src/budget_manager/cli.py --help

import argparse
import sys
from pathlib import Path

from services import add_transaction, filter_transactions, summarize, undo_last
from storage import load_transactions, save_transactions, backup_transactions, read_csv_rows

DATA_FILE = "data/transactions.json"


def build_parser():
    """Describe every command and its arguments (argparse also adds --help)."""
    parser = argparse.ArgumentParser(description="Personal budget manager")
    commands = parser.add_subparsers(dest="command", required=True)

    add = commands.add_parser("add", help="add one transaction")
    add.add_argument("amount", help="positive amount, e.g. 18.50")
    add.add_argument("--category", required=True, help="food, transport, rent, leisure, salary, other")
    add.add_argument("--date", required=True, help="YYYY-MM-DD")
    add.add_argument("--kind", default="expense", help="expense (default) or income")
    add.add_argument("--currency", default="EUR", help="EUR (default), USD or GBP")

    show = commands.add_parser("list", help="list transactions")
    show.add_argument("--month", help="only this month, e.g. 2026-09")
    show.add_argument("--category", help="only this category")

    commands.add_parser("summary", help="income, expenses, balance and totals per category")

    imp = commands.add_parser("import", help="import transactions from a CSV file")
    imp.add_argument("csv_file")

    backup = commands.add_parser("backup", help="save a copy of the data in a NEW file")
    backup.add_argument("destination")

    commands.add_parser("undo", help="remove the last transaction")
    return parser


def main():
    args = build_parser().parse_args()
    transactions = load_transactions(DATA_FILE)

    if args.command == "add":
        new, errors = add_transaction(transactions, args.date, args.kind,
                                      args.category, args.amount, args.currency)
        if errors:
            for error in errors:
                print(f"error: {error}", file=sys.stderr)
            sys.exit(1)
        save_transactions(DATA_FILE, transactions)
        print(f"Added {new['id']}: {new['date']} {new['kind']} {new['category']} "
              f"{new['amount']:.2f} {new['currency']}")

    elif args.command == "list":
        selected = filter_transactions(transactions, args.month, args.category)
        if not selected:
            print("No transactions found.")
        for t in selected:
            print(f"{t['id']} | {t['date']} | {t['kind']} | {t['category']} | "
                  f"{t['amount']:.2f} {t['currency']}")

    elif args.command == "summary":
        s = summarize(transactions)
        print(f"Income:   {s['income']:.2f}")
        print(f"Expenses: {s['expenses']:.2f}")
        print(f"Balance:  {s['balance']:.2f}")
        for category, total in s["by_category"].items():
            print(f"  {category}: {total:.2f}")

    elif args.command == "import":
        if not Path(args.csv_file).exists():
            print(f"error: the file {args.csv_file} does not exist.", file=sys.stderr)
            sys.exit(1)
        rows = read_csv_rows(args.csv_file)
        added = 0
        rejected = 0
        for number, row in enumerate(rows, start=2):        # line 1 is the header
            new, errors = add_transaction(transactions, row.get("date", ""), row.get("kind", ""),
                                          row.get("category", ""), row.get("amount", ""),
                                          row.get("currency", "EUR"))
            if errors:
                rejected += 1
                for error in errors:
                    print(f"Row {number}: {error}", file=sys.stderr)
            else:
                added += 1
        save_transactions(DATA_FILE, transactions)
        print(f"Imported {added} transactions, rejected {rejected}.")

    elif args.command == "backup":
        if Path(args.destination).exists():
            print(f"error: {args.destination} already exists. Choose a new file name "
                  f"so the old backup is not overwritten.", file=sys.stderr)
            sys.exit(1)
        count = backup_transactions(DATA_FILE, args.destination)
        print(f"Backup saved to {args.destination} ({count} transactions).")

    elif args.command == "undo":
        removed = undo_last(transactions)
        if removed is None:
            print("error: there is nothing to undo.", file=sys.stderr)
            sys.exit(1)
        save_transactions(DATA_FILE, transactions)     # the file always matches the real state
        print(f"Removed {removed['id']}.")


if __name__ == "__main__":
    main()
