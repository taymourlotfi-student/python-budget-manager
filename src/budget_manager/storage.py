# storage.py — reading and writing files (persistence).
# Same tools as the professor's cli.py example: json + Path.

import json
from pathlib import Path


def load_transactions(path):
    """Read the list of transactions from a JSON file. Missing file -> []."""
    file = Path(path)
    if file.exists():
        return json.loads(file.read_text())
    return []


def save_transactions(path, transactions):
    """Write the whole list of transactions to a JSON file."""
    file = Path(path)
    file.write_text(json.dumps(transactions, indent=2))


def backup_transactions(path, destination):
    """Copy the transactions into a NEW backup file.

    "x" mode refuses to overwrite an existing file, so an older backup is never lost.
    Returns the number of transactions in the backup (so we can check it).
    """
    transactions = load_transactions(path)
    with open(destination, "x") as output:
        json.dump(transactions, output, indent=2)
    return len(load_transactions(destination))       # verify after copying


def read_csv_rows(path):
    """Read a simple CSV file (first line = header) into a list of dictionaries."""
    lines = Path(path).read_text().strip().split("\n")
    header = lines[0].strip().split(",")
    rows = []
    for line in lines[1:]:
        values = line.strip().split(",")
        rows.append(dict(zip(header, values)))
    return rows
