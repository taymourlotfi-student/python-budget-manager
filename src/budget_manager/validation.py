# validation.py — checks done at the entry points (CLI and CSV import).
# Each function returns a LIST of clear error messages.
# An empty list [] means the data is valid.

from models import KINDS, CATEGORIES, CURRENCIES

# Days in each month (February allows 29, so leap years are accepted).
DAYS_IN_MONTH = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def is_number(text):
    """True if text looks like a number such as 18, 18.5 or 18.50 (no minus sign)."""
    text = text.strip()
    return text != "" and text.replace(".", "", 1).isdigit()


def is_valid_date(text):
    """True if text has the ISO format YYYY-MM-DD with a real month and day."""
    parts = text.strip().split("-")
    if len(parts) != 3:
        return False
    year, month, day = parts
    if len(year) != 4 or len(month) != 2 or len(day) != 2:
        return False
    if not (year.isdigit() and month.isdigit() and day.isdigit()):
        return False
    if not 1 <= int(month) <= 12:
        return False
    return 1 <= int(day) <= DAYS_IN_MONTH[int(month) - 1]


def validate_transaction(date, kind, category, amount, currency):
    """Check every field. Return a list of error messages ([] = all good)."""
    errors = []

    if not is_valid_date(date):
        errors.append(f"date '{date}' is not a valid date in the format YYYY-MM-DD (e.g. 2026-09-04).")

    if kind.strip().lower() not in KINDS:
        errors.append(f"kind '{kind}' must be one of: {', '.join(KINDS)}.")

    if category.strip().lower() not in CATEGORIES:
        errors.append(f"category '{category}' is unknown. Use one of: {', '.join(CATEGORIES)}.")

    if amount.strip().startswith("-"):
        errors.append(f"amount '{amount}' must be > 0 (negative amounts are not allowed).")
    elif not is_number(amount):
        errors.append(f"amount '{amount}' must be a number, e.g. 18.50.")
    elif float(amount) <= 0:
        errors.append(f"amount '{amount}' must be > 0.")

    if currency.strip().upper() not in CURRENCIES:
        errors.append(f"currency '{currency}' must be one of: {', '.join(CURRENCIES)}.")

    return errors
