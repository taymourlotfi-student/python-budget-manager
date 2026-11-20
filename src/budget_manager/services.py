# services.py — the budget logic (business rules).
# No input(), no print(), no files here: only data in -> data out.
# That is why these functions are easy to test.

from models import make_transaction, next_id
from validation import validate_transaction


def add_transaction(transactions, date, kind, category, amount, currency="EUR"):
    """Validate the data and add a new transaction to the list.

    Returns (new_transaction, []) when it worked,
    or (None, errors) when the data is invalid (the list is NOT changed).
    """
    errors = validate_transaction(date, kind, category, amount, currency)
    if errors:
        return None, errors

    new = make_transaction(
        next_id(transactions),
        date.strip(),
        kind.strip().lower(),
        category.strip().lower(),
        round(float(amount), 2),
        currency.strip().upper(),
    )
    transactions.append(new)
    return new, []


def filter_transactions(transactions, month=None, category=None):
    """Keep only the transactions of one month ("2026-09") and/or one category."""
    result = []
    for t in transactions:
        if month is not None and not t["date"].startswith(month):
            continue
        if category is not None and t["category"] != category.lower():
            continue
        result.append(t)
    return result


def summarize(transactions):
    """Return total income, total expenses, balance and expenses per category."""
    income = 0
    expenses = 0
    by_category = {}
    for t in transactions:
        if t["kind"] == "income":
            income += t["amount"]
        else:
            expenses += t["amount"]
            by_category[t["category"]] = by_category.get(t["category"], 0) + t["amount"]

    return {
        "income": round(income, 2),
        "expenses": round(expenses, 2),
        "balance": round(income - expenses, 2),
        "by_category": {k: round(v, 2) for k, v in by_category.items()},
    }


def undo_last(transactions):
    """Remove the last transaction and return it (or None if the list is empty)."""
    if not transactions:
        return None
    return transactions.pop()
