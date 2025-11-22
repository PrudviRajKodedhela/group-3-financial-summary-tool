from _future_ import annotations

from pathlib import Path
from typing import Union

import pandas as pd


PathLike = Union[str, Path]


def read_transactions(path: PathLike, *, encoding: str = "utf-8") -> pd.DataFrame:
    """
    Read the financial transactions dataset from a CSV file.

    Parameters
    ----------
    path : str or pathlib.Path
        Path to the CSV file.
    encoding : str, optional
        File encoding, by default "utf-8".

    Returns
    -------
    pd.DataFrame
        Raw transactions DataFrame.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    ValueError
        If the file cannot be parsed as CSV.
    """
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"Transactions file not found: {file_path}")

    try:
        df = pd.read_csv(file_path, encoding=encoding)
    except Exception as exc:  # pragma: no cover (defensive)
        raise ValueError(f"Failed to read CSV from {file_path}") from exc

    if df.empty:
        # Not necessarily an error, but in most analytical workflows it is useful to warn early.
        # We surface it as a ValueError to catch misconfigured paths / bad inputs in tests or notebooks.
        raise ValueError(f"Transactions file {file_path} is empty.")

    return df