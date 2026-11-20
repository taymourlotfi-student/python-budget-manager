# test_budget.py — tests with assert: one normal case + boundary cases.
# Run from the budget-manager folder:  python src/budget_manager/test_budget.py

from services import add_transaction, filter_transactions, summarize, undo_last
from storage import load_transactions, save_transactions
from validation import validate_transaction


def test_add_normal_expense():
    # Normal case: a valid expense is added with all 6 fields and id T001.
    transactions = []
    new, errors = add_transaction(transactions, "2026-09-04", "expense", "food", "18.50")
    assert errors == []
    assert new == {"id": "T001", "date": "2026-09-04", "kind": "expense",
                   "category": "food", "amount": 18.5, "currency": "EUR"}
    assert len(transactions) == 1


def test_negative_amount_rejected():
    # Boundary: a negative amount is rejected and the list does not change.
    transactions = []
    new, errors = add_transaction(transactions, "2026-09-04", "expense", "food", "-5")
    assert new is None
    assert errors == ["amount '-5' must be > 0 (negative amounts are not allowed)."]
    assert transactions == []


def test_zero_amount_rejected():
    # Boundary: 0 is not a valid amount (must be > 0).
    errors = validate_transaction("2026-09-04", "expense", "food", "0", "EUR")
    assert errors == ["amount '0' must be > 0."]


def test_unknown_category_and_bad_date():
    # Boundary: unknown category and impossible month give two clear messages.
    errors = validate_transaction("2026-13-01", "expense", "pizza", "10", "EUR")
    assert len(errors) == 2
    assert errors[0].startswith("date '2026-13-01'")
    assert errors[1].startswith("category 'pizza' is unknown")


def test_day_that_does_not_exist():
    # Boundary: September has 30 days, so 2026-09-31 is rejected; 2026-09-30 is fine.
    assert validate_transaction("2026-09-30", "expense", "food", "5", "EUR") == []
    errors = validate_transaction("2026-09-31", "expense", "food", "5", "EUR")
    assert errors[0].startswith("date '2026-09-31'")


def test_text_amount_rejected():
    # Malformed input: an amount that is not a number.
    errors = validate_transaction("2026-09-04", "expense", "food", "abc", "EUR")
    assert errors == ["amount 'abc' must be a number, e.g. 18.50."]


def test_summary_and_filter():
    transactions = []
    add_transaction(transactions, "2026-09-01", "income", "salary", "1500")
    add_transaction(transactions, "2026-09-04", "expense", "food", "18.50")
    add_transaction(transactions, "2026-10-02", "expense", "rent", "650")
    summary = summarize(transactions)
    assert summary == {"income": 1500.0, "expenses": 668.5, "balance": 831.5,
                       "by_category": {"food": 18.5, "rent": 650.0}}
    assert len(filter_transactions(transactions, month="2026-09")) == 2
    assert len(filter_transactions(transactions, category="rent")) == 1


def test_save_and_load_round_trip():
    # Persistence: what we save is exactly what we load back.
    # (The test file is overwritten every run; .gitignore keeps it off GitHub.)
    path = "data/test_round_trip.json"
    transactions = []
    add_transaction(transactions, "2026-09-04", "expense", "food", "18.50")
    save_transactions(path, transactions)
    assert load_transactions(path) == transactions


def test_undo_last():
    transactions = []
    add_transaction(transactions, "2026-09-04", "expense", "food", "10")
    removed = undo_last(transactions)
    assert removed["id"] == "T001"
    assert transactions == []
    assert undo_last(transactions) is None  # nothing left to undo


if __name__ == "__main__":
    test_add_normal_expense()
    test_negative_amount_rejected()
    test_zero_amount_rejected()
    test_unknown_category_and_bad_date()
    test_day_that_does_not_exist()
    test_text_amount_rejected()
    test_summary_and_filter()
    test_save_and_load_round_trip()
    test_undo_last()
    print("All 9 tests passed.")
