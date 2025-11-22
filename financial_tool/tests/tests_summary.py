from _future_ import annotations

import pandas as pd
import pytest

from src.summary import (
    compute_income_expense_summary,
    summary_by_category,
    summary_by_month,
)


def _sample_clean_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": pd.to_datetime(
                ["2024-01-01", "2024-01-02", "2024-02-01", "2024-02-15"]
            ),
            "amount": [1000, -50, 2000, -100],
            "type": ["INCOME", "EXPENSE", "INCOME", "EXPENSE"],
            "category": ["Salary", "Groceries", "Salary", "Utilities"],
        }
    )


def test_compute_income_expense_summary() -> None:
    df = _sample_clean_df()
    summary = compute_income_expense_summary(df)

    assert set(summary["label"]) == {"INCOME", "EXPENSE", "NET"}
    income = summary.loc[summary["label"] == "INCOME", "total_amount"].iloc[0]
    expense = summary.loc[summary["label"] == "EXPENSE", "total_amount"].iloc[0]
    net = summary.loc[summary["label"] == "NET", "total_amount"].iloc[0]

    assert income == 3000
    assert expense == -150
    assert net == income - expense


def test_summary_by_category() -> None:
    df = _sample_clean_df()
    cat_summary = summary_by_category(df)

    assert "category" in cat_summary.columns
    assert "total_amount" in cat_summary.columns
    assert set(cat_summary["category"]) == {"Salary", "Groceries", "Utilities"}


def test_summary_by_month() -> None:
    df = _sample_clean_df()
    monthly = summary_by_month(df)

    assert set(monthly.columns) == {"period", "income", "expense", "net"}
    # Expect two periods: 2024-01 and 2024-02
    assert set(monthly["period"]) == {"2024-01", "2024-02"}