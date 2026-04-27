import numpy as np
import pandas as pd
import polars as pl

import pandas_flavor as pf
import warnings
from typing import List, Optional, Sequence, Tuple, Union

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
    ensure_row_id_column,
    normalize_engine,
    resolve_pandas_groupby_frame,
    resolve_polars_group_columns,
    restore_output_type,
    conversion_to_pandas,
)
from pytimetk.utils.memory_helpers import reduce_memory_usage
from pytimetk.utils.pandas_helpers import sort_dataframe
from pytimetk.utils.polars_helpers import collect_lazyframe
from pytimetk.utils.selection import ColumnSelector
from pytimetk.feature_engineering._shift_utils import resolve_shift_columns


@pf.register_groupby_method
@pf.register_dataframe_method
def augment_rsi(
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
    periods: Union[int, Tuple[int, int], List[int]] = 14,
    reduce_memory: bool = False,
    engine: Optional[str] = "auto",
) -> Union[pd.DataFrame, pl.DataFrame, "cudf.DataFrame"]:
    """
    Calculate the Relative Strength Index (RSI) for pandas or polars data.

    Parameters
    ----------
    data : DataFrame or GroupBy (pandas or polars)
        Financial data to augment. Grouped inputs are processed per group
        before RSI columns are appended.
    date_column : str or ColumnSelector
        Name of the column containing date information. Accepts tidy selectors
        such as ``contains("date")``.
    close_column : str, ColumnSelector, or list
        Column name(s) containing the closing prices used to compute RSI. Lists
        (or multiple selectors) generate an RSI for each column.
    periods : int, tuple, or list, optional
        Lookback window(s) used when computing RSI. Accepts an integer, an
        inclusive tuple range, or a list of explicit periods. Defaults to ``14``.
    reduce_memory : bool, optional
        Attempt to reduce memory usage when operating on pandas data. If a
        polars input is supplied a warning is emitted and no conversion occurs.
    engine : {"auto", "pandas", "polars", "cudf"}, optional
        Execution engine. ``"auto"`` (default) infers the backend from the
        input data while allowing explicit overrides.

    Returns
    -------
    DataFrame
        DataFrame with ``{close_column}_rsi_{period}`` columns appended. The
        return type matches the input backend.

    Notes
    -----
    RSI follows Wilder's formulation, separating gains and losses before
    computing smoothed averages and forming the ratio. Values range from 0 to
    100, with extreme readings typically interpreted as overbought or
    oversold. Division-by-zero cases yield ``NaN`` which mirrors pandas
    behaviour.

    Examples
    --------
    ```{python}
    import pandas as pd
    import polars as pl
    import pytimetk as tk


    df = tk.load_dataset("stocks_daily", parse_dates=["date"])

    # Pandas example (engine inferred)
    rsi_pd = (
        df.groupby("symbol")
        .augment_rsi(
            date_column="date",
            close_column="close",
            periods=[14, 28],
        )
    )

    # Polars example using the tk accessor
    rsi_pl = (
        pl.from_pandas(df.query("symbol == 'AAPL'"))
        .tk.augment_rsi(
            date_column="date",
            close_column=["close"],
            periods=14,
        )
    )
    
    # Selector example
    from pytimetk.utils.selection import contains
    selector_demo = (
        df
            .augment_rsi(
                date_column=contains("dat"),
                close_column=contains("clos"),
                periods=[14],
            )
    )
    ```
    """
    pass


def _augment_rsi_pandas(
    data: Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy],
    close_columns: List[str],
    periods: List[int],
) -> pd.DataFrame:
    pass


def _augment_rsi_polars(
    data: Union[pl.DataFrame, pl.dataframe.group_by.GroupBy],
    date_column: str,
    close_columns: List[str],
    periods: List[int],
    group_columns: Optional[Sequence[str]],
    row_id_column: Optional[str],
) -> pl.DataFrame:
    def _maybe_over(expr: pl.Expr) -> pl.Expr:
        pass
    pass


def _augment_rsi_cudf_dataframe(
    frame: "cudf.DataFrame",
    *,
    date_column: str,
    close_columns: List[str],
    periods: List[int],
    group_columns: Optional[Sequence[str]],
    row_id_column: Optional[str],
) -> "cudf.DataFrame":
    pass


def _calculate_rsi_pandas(series: pd.Series, period=14):
    # Calculate the difference in closing prices
    pass
def _normalize_periods(periods: Union[int, Tuple[int, int], List[int]]) -> List[int]:
    pass
