from _future_ import annotations

from typing import Literal

import pandas as pd


def compute_income_expense_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute total income, total expenses, and net balance.

    Assumptions
    -----------
    - 'amount' is numeric (positive or negative).
    - 'type' column exists and contains 'INCOME' and 'EXPENSE'
      (case-sensitive after cleaning).

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned transactions DataFrame.

    Returns
    -------
    pd.DataFrame
        A DataFrame with:
        - 'label' column: INCOME, EXPENSE, NET
        - 'total_amount' column: aggregated amounts

    Raises
    ------
    KeyError
        If required columns are missing.
    """
    for col in ("amount", "type"):
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column.")

    income_total = df.loc[df["type"] == "INCOME", "amount"].sum()
    expense_total = df.loc[df["type"] == "EXPENSE", "amount"].sum()
    net_total = income_total - expense_total

    summary = pd.DataFrame(
        {
            "label": ["INCOME", "EXPENSE", "NET"],
            "total_amount": [income_total, expense_total, net_total],
        }
    )
    return summary


def summary_by_category(
    df: pd.DataFrame,
    *,
    include_income: bool = True,
    include_expense: bool = True,
) -> pd.DataFrame:
    """
    Group transactions by category and compute total amount.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned transactions DataFrame, expected to contain 'category' and 'amount'.
    include_income : bool, optional
        Whether to include rows with type == 'INCOME', by default True.
    include_expense : bool, optional
        Whether to include rows with type == 'EXPENSE', by default True.

    Returns
    -------
    pd.DataFrame
        Columns:
        - 'category'
        - 'total_amount'
    """
    if "category" not in df.columns:
        raise KeyError("DataFrame must contain 'category' column.")
    if "amount" not in df.columns:
        raise KeyError("DataFrame must contain 'amount' column.")

    filtered = df.copy()
    if "type" in filtered.columns:
        if not include_income:
            filtered = filtered[filtered["type"] != "INCOME"]
        if not include_expense:
            filtered = filtered[filtered["type"] != "EXPENSE"]

    grouped = (
        filtered.groupby("category", dropna=False)["amount"]
        .sum()
        .reset_index(name="total_amount")
        .sort_values("total_amount", ascending=False)
    )
    return grouped.reset_index(drop=True)


def summary_by_month(
    df: pd.DataFrame,
    *,
    period: Literal["M", "Q", "Y"] = "M",
) -> pd.DataFrame:
    """
    Compute periodic (monthly by default) income, expenses, and net balance.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned transactions DataFrame containing 'date', 'amount', and 'type'.
    period : {'M', 'Q', 'Y'}, optional
        Period frequency for grouping:
        - 'M' = month (default)
        - 'Q' = quarter
        - 'Y' = year

    Returns
    -------
    pd.DataFrame
        Columns:
        - 'period'  (string representation of year-month/quarter/year)
        - 'income'
        - 'expense'
        - 'net'

    Raises
    ------
    KeyError
        If required columns are missing.
    """
    for col in ("date", "amount", "type"):
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column.")

    temp = df.copy()
    temp["period"] = temp["date"].dt.to_period(period).astype(str)

    income = (
        temp[temp["type"] == "INCOME"]
        .groupby("period")["amount"]
        .sum()
        .rename("income")
    )

    expense = (
        temp[temp["type"] == "EXPENSE"]
        .groupby("period")["amount"]
        .sum()
        .rename("expense")
    )

    combined = (
        pd.concat([income, expense], axis=1)
        .fillna(0.0)
        .reset_index()
    )
    combined["net"] = combined["income"] - combined["expense"]

    return combined[["period", "income", "expense", "net"]]