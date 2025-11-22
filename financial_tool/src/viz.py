from _future_ import annotations

from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure


def plot_spending_by_category(
    df: pd.DataFrame,
    *,
    title: str = "Spending by Category",
) -> Figure:
    """
    Create a bar plot of spending by category.

    Assumptions
    -----------
    - 'category' column exists.
    - 'amount' column contains numeric values.
    - Typically used on EXPENSE records, or on absolute amounts.

    Parameters
    ----------
    df : pd.DataFrame
        Transactions DataFrame, usually filtered to expenses.
    title : str, optional
        Plot title, by default "Spending by Category".

    Returns
    -------
    matplotlib.figure.Figure
        The generated matplotlib Figure object.

    Raises
    ------
    KeyError
        If required columns are missing.
    """
    for col in ("category", "amount"):
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column.")

    grouped = (
        df.groupby("category")["amount"]
        .sum()
        .abs()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots()
    grouped.plot(kind="bar", ax=ax)
    ax.set_title(title)
    ax.set_xlabel("Category")
    ax.set_ylabel("Total Amount")
    fig.tight_layout()
    return fig


def plot_balance_over_time(
    periodic_df: pd.DataFrame,
    *,
    title: str = "Net Balance Over Time",
    x_label: str = "Period",
    y_label: str = "Net Amount",
    x_col: str = "period",
    net_col: str = "net",
) -> Figure:
    """
    Plot net balance over time using periodic summary data.

    Typically used with the output of summary_by_month or similar.

    Parameters
    ----------
    periodic_df : pd.DataFrame
        DataFrame containing a time-like column and a 'net' column.
    title : str, optional
        Plot title.
    x_label : str, optional
        X-axis label.
    y_label : str, optional
        Y-axis label.
    x_col : str, optional
        Name of the column to use for x-axis, by default 'period'.
    net_col : str, optional
        Name of the column containing net values, by default 'net'.

    Returns
    -------
    matplotlib.figure.Figure
        The generated matplotlib Figure object.

    Raises
    ------
    KeyError
        If required columns are missing.
    """
    for col in (x_col, net_col):
        if col not in periodic_df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column.")

    fig, ax = plt.subplots()
    ax.plot(
        periodic_df[x_col],
        periodic_df[net_col],
        marker="o",
    )
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    return fig