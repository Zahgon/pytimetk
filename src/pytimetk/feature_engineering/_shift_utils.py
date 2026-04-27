from __future__ import annotations

from typing import List, Sequence, Tuple, Union

import pandas as pd

from pytimetk.utils.datetime_helpers import resolve_lag_sequence
from pytimetk.utils.dataframe_ops import resolve_pandas_groupby_frame
from pytimetk.utils.selection import ColumnSelector, resolve_column_selection
from pytimetk.utils.checks import check_value_column, check_date_column

try:  # Optional dependency
    import polars as pl
except ImportError:  # pragma: no cover - optional import
    pl = None

try:  # Optional cudf dependency
    import cudf  # type: ignore
    from cudf.core.groupby.groupby import DataFrameGroupBy as CudfGroupBy  # type: ignore
except ImportError:  # pragma: no cover - optional import
    cudf = None  # type: ignore
    CudfGroupBy = None  # type: ignore


def _extract_date_series(
    data,
    date_column: str,
) -> pd.Series:
    pass


def _resolve_selector_frame(
    data,
) -> pd.DataFrame:
    pass


def _resolve_single_column(frame: pd.DataFrame, selector, label: str) -> str:
    pass


def _resolve_multi_columns(frame: pd.DataFrame, selector, label: str) -> List[str]:
    pass


def resolve_shift_columns(
    data,
    date_column: Union[str, ColumnSelector],
    value_column: Union[str, ColumnSelector, Sequence[Union[str, ColumnSelector]]],
    *,
    require_numeric: bool = False,
) -> Tuple[str, List[str]]:
    pass


def resolve_shift_values(
    spec: Union[int, Tuple[int, int], List[int], Sequence[Union[int, str]], str],
    *,
    label: str,
    data,
    date_column: str,
) -> List[int]:
    def _coerce_single(value) -> List[int]:
        pass
    pass
