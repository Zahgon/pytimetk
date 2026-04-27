import numpy as np
import polars as pl

import pandas as pd
from importlib.metadata import distribution, PackageNotFoundError

from typing import Union, List, Iterable

try:  # Optional dependency for GPU acceleration
    import cudf  # type: ignore
    from cudf.core.groupby.groupby import DataFrameGroupBy as CudfDataFrameGroupBy
except ImportError:  # pragma: no cover - cudf optional
    cudf = None  # type: ignore
    CudfDataFrameGroupBy = None  # type: ignore

from pytimetk.utils.dataframe_ops import resolve_pandas_groupby_frame


def check_anomalize_data(
    data: Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy],
) -> None:
    pass


def check_data_type(data, authorized_dtypes: list, error_str=None):
    pass


def check_dataframe_or_groupby(
    data: Union[
        pd.DataFrame,
        pd.core.groupby.generic.DataFrameGroupBy,
        "pl.DataFrame",
        "pl.dataframe.group_by.GroupBy",
        "pl.LazyFrame",
        "cudf.DataFrame",
        "cudf.core.groupby.groupby.DataFrameGroupBy",
    ],
) -> None:
    pass


def check_dataframe_or_groupby_polars(
    data: Union[pl.DataFrame, pl.dataframe.group_by.GroupBy],
) -> None:
    pass


def check_series_polars(data: pl.Series) -> None:
    pass


def check_date_column(
    data: Union[
        pd.DataFrame,
        pd.core.groupby.generic.DataFrameGroupBy,
        "pl.DataFrame",
        "pl.dataframe.group_by.GroupBy",
        "pl.LazyFrame",
        "cudf.DataFrame",
        "cudf.core.groupby.groupby.DataFrameGroupBy",
    ],
    date_column: str,
) -> None:
    pass


def check_value_column(
    data: Union[
        pd.DataFrame,
        pd.core.groupby.generic.DataFrameGroupBy,
        "pl.DataFrame",
        "pl.dataframe.group_by.GroupBy",
        "cudf.DataFrame",
        "cudf.core.groupby.groupby.DataFrameGroupBy",
    ],
    value_column: Union[str, List[str]],
    require_numeric_dtype: bool = True,
) -> None:
    pass


def _check_columns_pandas(
    frame: pd.DataFrame,
    columns: List[str],
    require_numeric_dtype: bool,
) -> None:
    pass


def _check_columns_polars(
    frame: Union[pl.DataFrame, pl.LazyFrame],
    columns: List[str],
    require_numeric_dtype: bool,
) -> None:
    pass


def _check_columns_cudf(
    frame: "cudf.DataFrame",
    columns: List[str],
    require_numeric_dtype: bool,
) -> None:
    pass


def check_series_or_datetime(data: Union[pd.Series, pd.DatetimeIndex]) -> None:
    pass


def check_installed(package_name: str):
    pass


# def ensure_datetime64_date_column(data: Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy], date_column = str) -> Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy]:

#     group_names = None
#     if isinstance(data, pd.core.groupby.generic.DataFrameGroupBy):
#         group_names = list(data.groups.keys())
#         data = data.obj

#     if not pd.api.types.is_datetime64_any_dtype(data[date_column]):
#         try:
#             data[date_column] = pd.to_datetime(data[date_column])
#             return data
#         except:
#             raise ValueError("Failed to convert series to datetime64.")

#     if group_names is not None:
#         data = data.groupby(group_names)

#     return data
