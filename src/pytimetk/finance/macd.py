import numpy as np
import pandas as pd
import polars as pl
import pandas_flavor as pf
import warnings

from typing import List, Optional, Sequence, Union

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
def augment_macd(
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
    signal_period: int = 9,
    reduce_memory: bool = False,
    engine: Optional[str] = "auto",
) -> Union[pd.DataFrame, pl.DataFrame, "cudf.DataFrame"]:
    """
    Calculate MACD for a given financial instrument using either pandas or polars engine.

    Parameters
    ----------
    data : DataFrame or GroupBy (pandas or polars)
        Input financial data.
    date_column : str or ColumnSelector
        Name of the column containing date information (tidy selectors supported).
    close_column : str or ColumnSelector
        Name of the column containing closing price data. Selector inputs must
        resolve to a single column.
    fast_period : int, optional
        Number of periods for the fast EMA in MACD calculation.
    slow_period : int, optional
        Number of periods for the slow EMA in MACD calculation.
    signal_period : int, optional
        Number of periods for the signal line EMA in MACD calculation.
    reduce_memory : bool, optional
        Whether to reduce memory usage of the data before performing the calculation.
    engine : {"auto", "pandas", "polars", "cudf"}, optional
        Computation engine to use. Defaults to infer from the input data type.

    Returns
    -------
    DataFrame
        DataFrame with MACD line, signal line, and MACD histogram added. Matches
        the backend of the input data.

    Notes
    -----
    The MACD (Moving Average Convergence Divergence) is a
    trend-following momentum indicator that shows the relationship
    between two moving averages of a security’s price. Developed by
    Gerald Appel in the late 1970s, the MACD is one of the simplest
    and most effective momentum indicators available.

    MACD Line: The MACD line is the difference between two
    exponential moving averages (EMAs) of a security’s price,
    typically the 12-day and 26-day EMAs.

    Signal Line: This is usually a 9-day EMA of the MACD line. It
    acts as a trigger for buy and sell signals.

    Histogram: The MACD histogram plots the difference between the
    MACD line and the signal line. A histogram above zero indicates
    that the MACD line is above the signal line (bullish), and
    below zero indicates it is below the signal line (bearish).

    Crossovers: The most common MACD signals are when the MACD line
    crosses above or below the signal line. A crossover above the
    signal line is a bullish signal, indicating it might be time to
    buy, and a crossover below the signal line is bearish,
    suggesting it might be time to sell.


    Examples
    --------

    ```{python}
    import pandas as pd
    import polars as pl
    import pytimetk as tk

    df = tk.load_dataset("stocks_daily", parse_dates = ['date'])

    df
    ```

    ```{python}
    # MACD pandas engine
    df_macd = (
        df
            .groupby('symbol')
            .augment_macd(
                date_column = 'date',
                close_column = 'close',
                fast_period = 12,
                slow_period = 26,
                signal_period = 9,
                engine = "pandas"
            )
    )

    df_macd.glimpse()
    ```

    ```{python}
    # MACD polars engine
    pl_df = pl.from_pandas(df)
    df_macd = (
        pl_df
            .group_by('symbol')
            .tk.augment_macd(
                date_column = 'date',
                close_column = 'close',
                fast_period = 12,
                slow_period = 26,
                signal_period = 9,
            )
    )

    df_macd.glimpse()
    ```

    ```{python}
    from pytimetk.utils.selection import contains

    (
        df
            .groupby('symbol')
            .augment_macd(
                date_column = contains('dat'),
                close_column = contains('clos'),
                fast_period = 12,
                slow_period = 26,
                signal_period = 9,
            )
    )
    ```

    """
    pass


def _augment_macd_pandas(
    data,
    close_column,
    fast_period,
    slow_period,
    signal_period,
):
    """
    Internal function to calculate MACD using Pandas.
    """
    pass


def _calculate_macd_pandas(df, close_column, fast_period, slow_period, signal_period):
    """
    Calculate MACD, Signal Line, and MACD Histogram for a DataFrame.
    """
    pass


def _augment_macd_polars(
    data,
    date_column,
    close_column,
    fast_period,
    slow_period,
    signal_period,
    group_columns,
    row_id_column,
):
    """
    Internal function to calculate MACD using Polars.
    """
    pass


def _augment_macd_cudf_dataframe(
    frame: "cudf.DataFrame",
    *,
    date_column: str,
    close_column: str,
    fast_period: int,
    slow_period: int,
    signal_period: int,
    group_columns: Optional[Sequence[str]],
    row_id_column: Optional[str],
) -> "cudf.DataFrame":
    pass
