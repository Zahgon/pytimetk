import pandas as pd
import polars as pl
import pandas_flavor as pf
import warnings

from typing import List, Optional, Sequence, Tuple, Union

try:  # Optional dependency for GPU acceleration
    import cudf  # type: ignore
    from cudf.core.groupby.groupby import DataFrameGroupBy as CudfDataFrameGroupBy
except ImportError:  # pragma: no cover - cudf optional
    cudf = None  # type: ignore
    CudfDataFrameGroupBy = None  # type: ignore

from pytimetk.utils.checks import (
    check_dataframe_or_groupby,
)
from pytimetk.utils.dataframe_ops import (
    FrameConversion,
    convert_to_engine,
    ensure_row_id_column,
    normalize_engine,
    resolve_pandas_groupby_frame,
    resolve_polars_group_columns,
    restore_output_type,
)
from pytimetk.utils.memory_helpers import reduce_memory_usage
from pytimetk.utils.pandas_helpers import sort_dataframe
from pytimetk.feature_engineering._shift_utils import resolve_shift_values, resolve_shift_columns
from pytimetk.utils.selection import ColumnSelector


@pf.register_groupby_method
@pf.register_dataframe_method
def augment_leads(
    data: Union[
        pd.DataFrame,
        pd.core.groupby.generic.DataFrameGroupBy,
        pl.DataFrame,
        pl.dataframe.group_by.GroupBy,
        "cudf.DataFrame",
        "cudf.core.groupby.groupby.DataFrameGroupBy",
    ],
    date_column: Union[str, ColumnSelector],
    value_column: Union[str, ColumnSelector, Sequence[Union[str, ColumnSelector]]],
    leads: Union[int, Tuple[int, int], List[int], Sequence[Union[int, str]], str] = 1,
    reduce_memory: bool = False,
    engine: Optional[str] = "auto",
) -> Union[pd.DataFrame, pl.DataFrame, "cudf.DataFrame"]:
    """
    Adds lead columns to a pandas or polars DataFrame (or grouped DataFrame).

    Parameters
    ----------
    data : DataFrame or GroupBy (pandas or polars)
        Input tabular data to augment.
    date_column : str or ColumnSelector
        Name of the date column used to determine ordering prior to shifting.
        Accepts tidy selectors for convenience.
    value_column : str, ColumnSelector, or list
        One or more column names/tidy selectors whose lead values will be appended.
    leads : int, tuple, list, or str, optional
        Lead specification. Accepts:

        - int: single lead value
        - tuple(start, end): inclusive range of leads
        - list[int] or list[str]: explicit values/durations
        - str: duration (e.g., ``"3 days"``) converted using ``date_column``
    reduce_memory : bool, optional
        If True, attempts to reduce memory usage (pandas only).
    engine : {"auto", "pandas", "polars", "cudf"}, optional
        Execution engine. When "auto" (default) the backend is inferred from the
        input data type.

    Returns
    -------
    DataFrame
        DataFrame with lead columns appended. The return type matches the input backend.
    """
    pass


def _augment_leads_pandas(
    data: Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy],
    date_column: str,
    value_column: Union[str, List[str]],
    leads: List[int],
) -> pd.DataFrame:
    pass


def _augment_leads_polars(
    data: Union[pl.DataFrame, pl.dataframe.group_by.GroupBy],
    date_column: str,
    value_column: Union[str, List[str]],
    leads: List[int],
    group_columns: Optional[Sequence[str]],
    row_id_column: Optional[str],
) -> pl.DataFrame:
    pass


def _augment_leads_cudf(
    data: Union["cudf.DataFrame", "cudf.core.groupby.groupby.DataFrameGroupBy"],
    date_column: str,
    value_column: Union[str, List[str]],
    leads: List[int],
    group_columns: Optional[Sequence[str]],
    row_id_column: Optional[str],
):
    pass
