from _future_ import annotations

import pandas as pd
import pytest

from src.cleaning import clean_transactions


def test_clean_transactions_basic() -> None:
    raw = pd.DataFrame(
        {
            "date": ["2024-01-01", "invalid", "2024-01-03"],
            "amount": ["100", "abc", "200"],
            "type": ["credit", "debit", "INCOME"],
            "category": ["Salary", "Groceries", "Bonus"],
        }
    )

    cleaned = clean_transactions(raw)

    # One invalid row should be dropped (invalid date/amount)
    assert len(cleaned) == 2

    # Types should be normalized
    assert set(cleaned["type"].unique()) <= {"INCOME", "EXPENSE"}

    # Dtypes should be parsed
    assert pd.api.types.is_datetime64_any_dtype(cleaned["date"])
    assert pd.api.types.is_numeric_dtype(cleaned["amount"])


def test_clean_transactions_missing_required_column() -> None:
    raw = pd.DataFrame({"amount": [100, 200]})
    with pytest.raises(KeyError):
        clean_transactions(raw)