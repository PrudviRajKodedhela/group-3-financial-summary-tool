"""
Top-level package for the Financial Transactions Analysis Tool.

This module exposes the most common functions for convenience.
"""

from .io_utils import read_transactions
from .cleaning import clean_transactions
from .summary import (
    compute_income_expense_summary,
    summary_by_category,
    summary_by_month,
)
from .viz import (
    plot_spending_by_category,
    plot_balance_over_time,
)

_all_ = [
    "read_transactions",
    "clean_transactions",
    "compute_income_expense_summary",
    "summary_by_category",
    "summary_by_month",
    "plot_spending_by_category",
    "plot_balance_over_time",
]