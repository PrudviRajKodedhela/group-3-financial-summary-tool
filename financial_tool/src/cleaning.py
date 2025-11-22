HERE IS src/cleaning.py
from _future_ import annotations

from typing import Iterable, List

import pandas as pd


REQUIRED_COLUMNS: List[str] = ["date", "amount"]
DEFAULT_TYPE_MAP = {
    "CREDIT": "INCOME",
    "CR": "INCOME",
    "INCOME": "INCOME",
    "DEBIT": "EXPENSE",
    "DR": "EXPENSE",
    "EXPENSE": "EXPENSE",
}


def _ensure_required_columns(df: pd.DataFrame, required: Iterable[str]) -> None:
    """
    Internal helper to validate that required columns exist.

    Raises
    ------
    KeyError
        If any required column is missing.
    """
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise KeyError(f"Missing required column(s): {', '.join(missing)}")


def clean_transactions(
    df: pd.DataFrame,
    *,
    type_map: dict[str, str] | None = None,
    required_columns: Iterable[str] = REQUIRED_COLUMNS,
) -> pd.DataFrame:
    """
    Clean the transactions DataFrame to make it suitable for analysis.

    Cleaning steps:
    - Validate presence of required columns (by default: 'date', 'amount').
    - Parse 'date' column to datetime (invalid -> NaT).
    - Convert 'amount' column to numeric (invalid -> NaN).
    - Standardize 'type' column if present (e.g. CREDIT/DEBIT -> INCOME/EXPENSE).
    - Drop rows with missing required fields after parsing.
    - Return a new DataFrame (no in-place modification).

    Parameters
    ----------
    df : pd.DataFrame
        Raw transactions DataFrame.
    type_map : dict[str, str], optional
        Mapping from raw transaction type values to normalized values.
        If None, a default mapping is used.
    required_columns : Iterable[str], optional
        Columns that must be present and non-null, by default ['date', 'amount'].

    Returns
    -------
    pd.DataFrame
        Cleaned DataFrame ready for summarisation.

    Raises
    ------
    KeyError
        If required columns are missing.
    """
    _ensure_required_columns(df, required_columns)

    cleaned = df.copy()

    # 1. Parse dates
    cleaned["date"] = pd.to_datetime(cleaned["date"], errors="coerce")

    # 2. Convert amount to numeric
    cleaned["amount"] = pd.to_numeric(cleaned["amount"], errors="coerce")

    # 3. Normalize type column, if present
    if "type" in cleaned.columns:
        effective_type_map = type_map or DEFAULT_TYPE_MAP
        cleaned["type"] = (
            cleaned["type"]
            .astype(str)
            .str.strip()
            .str.upper()
            .map(lambda x: effective_type_map.get(x, x))
        )

    # 4. Drop rows missing required values (after conversion)
    required_after = list(required_columns)
    cleaned = cleaned.dropna(subset=required_after)

    # Optional: enforce correct dtypes
    # (We keep it minimal; additional enforcement can be added as needed.)
    return cleaned.reset_index(drop=True)