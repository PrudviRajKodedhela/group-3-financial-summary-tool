from _future_ import annotations

from io import StringIO

import pandas as pd
import pytest

from src.io_utils import read_transactions
from pathlib import Path


def test_read_transactions_success(tmp_path: Path) -> None:
    # Arrange
    csv_content = "date,amount,type,category\n2024-01-01,100,INCOME,Salary\n"
    file_path = tmp_path / "transactions.csv"
    file_path.write_text(csv_content, encoding="utf-8")

    # Act
    df = read_transactions(file_path)

    # Assert
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert list(df.columns) == ["date", "amount", "type", "category"]


def test_read_transactions_missing_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        read_transactions(tmp_path / "missing.csv")


def test_read_transactions_empty_file(tmp_path: Path) -> None:
    file_path = tmp_path / "empty.csv"
    file_path.write_text("", encoding="utf-8")

    with pytest.raises(ValueError):
        read_transactions(file_path)