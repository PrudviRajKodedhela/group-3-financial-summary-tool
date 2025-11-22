from _future_ import annotations

import pandas as pd

from src.viz import plot_spending_by_category, plot_balance_over_time
from src.summary import summary_by_month


def test_plot_spending_by_category_returns_figure() -> None:
    df = pd.DataFrame(
        {
            "category": ["Groceries", "Groceries", "Rent"],
            "amount": [-50, -100, -800],
        }
    )
    fig = plot_spending_by_category(df)
    # Basic sanity check
    assert fig is not None
    assert hasattr(fig, "axes")


def test_plot_balance_over_time_returns_figure() -> None:
    df = pd.DataFrame(
        {
            "date": pd.to_datetime(["2024-01-01", "2024-02-01"]),
            "amount": [1000, -200],
            "type": ["INCOME", "EXPENSE"],
            "category": ["Salary", "Groceries"],
        }
    )
    monthly = summary_by_month(df)
    fig = plot_balance_over_time(monthly)

    assert fig is not None
    assert hasattr(fig, "axes")