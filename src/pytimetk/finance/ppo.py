import pandas as pd
import polars as pl

import pandas_flavor as pf
import warnings
from typing import Optional, Sequence, Union

import numpy as np

try:  # Optional cudf dependency
    import cudf  # type: ignore
except ImportError:  # pragma: no cover - cudf optional
    cudf = None  # type: ignore

from pytimetk.utils.checks import (
    check_dataframe_or_groupby,
)
from pytimetk.utils.dataframe_ops import (
    FrameConversion,
    convert_to_engine,
    conversion_to_pandas,
    ensure_row_id_column,
    normalize_engine,
    pandas_groupby_apply,
    resolve_pandas_groupby_frame,
    resolve_polars_group_columns,
    restore_output_type,
)
from pytimetk.utils.memory_helpers import reduce_memory_usage
from pytimetk.utils.pandas_helpers import sort_dataframe
from pytimetk.utils.selection import ColumnSelector
from pytimetk.feature_engineering._shift_utils import resolve_shift_columns


@pf.register_groupby_method
@pf.register_dataframe_method
def augment_ppo(
    data: Union[
        pd.DataFrame,
        pd.core.groupby.generic.DataFrameGroupBy,
        pl.DataFrame,
        pl.dataframe.group_by.GroupBy,
        "cudf.DataFrame",
        "cudf.core.groupby.groupby.DataFrameGroupBy",
    ],
    date_column: Union[str, ColumnSelector],
    close_column: Union[str, ColumnSelector, Sequence[Union[str, ColumnSelector]]],
    fast_period: int = 12,
    slow_period: int = 26,
    reduce_memory: bool = False,
    engine: Optional[str] = "auto",
) -> Union[pd.DataFrame, pl.DataFrame, "cudf.DataFrame"]:
    """
    Calculate the Percentage Price Oscillator (PPO) for pandas or polars data.

    Parameters
    ----------
    data : DataFrame or GroupBy (pandas or polars)
        Financial data to augment with PPO values. Grouped inputs are processed
        per group before the indicator columns are appended.
    date_column : str or ColumnSelector
        Name of the column containing date information (selectors supported).
    close_column : str, ColumnSelector, or list
        Closing price column(s). Selectors resolving to multiple columns return a PPO per column.
    fast_period : int, optional
        Lookback window for the fast EMA.
    slow_period : int, optional
        Lookback window for the slow EMA.
    reduce_memory : bool, optional
        Attempt to reduce memory usage when operating on pandas data.
    engine : {"auto", "pandas", "polars"}, optional
        Execution engine. Defaults to inferring from the input data type.

    Returns
    -------
    DataFrame
        DataFrame with PPO values appended. Matches the backend of the input data.

    Notes
    -----
    The PPO is computed as the percentage difference between a fast and a slow
    exponential moving average (EMA):

        PPO = (EMA_fast - EMA_slow) / EMA_slow * 100

    The implementation follows the common convention of using ``min_periods=0``
    on the EMA calculations to accumulate values from the beginning of the
    series. Division-by-zero scenarios yield ``NaN`` to align with pandas'
    behaviour.

    Examples
    --------
    ```{python}
    import pandas as pd
    import polars as pl
    import pytimetk as tk


    df = tk.load_dataset("stocks_daily", parse_dates=["date"])

    # Pandas example (engine inferred)
    ppo_pd = (
        df.groupby("symbol")
        .augment_ppo(
            date_column="date",
            close_column="close",
            fast_period=12,
            slow_period=26,
        )
    )

    # Polars example using the tk accessor
    ppo_pl = (
        pl.from_pandas(df.query("symbol == 'AAPL'"))
        .tk.augment_ppo(
            date_column="date",
            close_column="close",
            fast_period=12,
            slow_period=26,
        )
    )

    from pytimetk.utils.selection import contains
    selector_demo = (
        df
            .augment_ppo(
                date_column=contains("dat"),
                close_column=contains("clos"),
                fast_period=12,
                slow_period=26,
            )
    )
    ```
    """
    pass


def _augment_ppo_cudf_dataframe(
    frame: "cudf.DataFrame",
    *,
    date_column: str,
    close_column: str,
    fast_period: int,
    slow_period: int,
    group_columns: Optional[Sequence[str]],
    row_id_column: Optional[str],
) -> "cudf.DataFrame":
    pass


def _augment_ppo_pandas(
    data,
    close_column: str,
    fast_period: int,
    slow_period: int,
) -> pd.DataFrame:
    pass


def _calculate_ppo_pandas(df, close_column, fast_period, slow_period):
    pass


def _augment_ppo_polars(
    data: Union[pl.DataFrame, pl.dataframe.group_by.GroupBy],
    date_column: str,
    close_column: str,
    fast_period: int,
    slow_period: int,
    group_columns: Optional[Sequence[str]],
    row_id_column: Optional[str],
) -> pl.DataFrame:
    pass
