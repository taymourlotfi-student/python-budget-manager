# models.py — the transaction schema (what one transaction looks like).
# Every transaction is a dictionary with ALWAYS the same 6 keys,
# so every other file can trust that these keys exist.

KINDS = ["expense", "income"]
CATEGORIES = ["food", "transport", "rent", "leisure", "salary", "other"]
CURRENCIES = ["EUR", "USD", "GBP"]


def make_transaction(transaction_id, date, kind, category, amount, currency):
    """Build one transaction dictionary with the 6 fields of the schema."""
    return {
        "id": transaction_id,
        "date": date,
        "kind": kind,
        "category": category,
        "amount": amount,
        "currency": currency,
    }


def next_id(transactions):
    """Return the next free id: T001, T002, T003..."""
    number = len(transactions) + 1
    for t in transactions:
        used = int(t["id"][1:])          # "T007" -> 7
        if used >= number:
            number = used + 1
    if number < 10:
        return "T00" + str(number)       # 7  -> "T007"
    if number < 100:
        return "T0" + str(number)        # 42 -> "T042"
    return "T" + str(number)             # 123 -> "T123"
