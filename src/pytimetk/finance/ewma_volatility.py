import pandas as pd
import polars as pl
import numpy as np

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
from pytimetk.utils.polars_helpers import collect_lazyframe
from pytimetk.utils.memory_helpers import reduce_memory_usage
from pytimetk.utils.pandas_helpers import sort_dataframe
from pytimetk.utils.selection import ColumnSelector
from pytimetk.feature_engineering._shift_utils import resolve_shift_columns


@pf.register_groupby_method
@pf.register_dataframe_method
def augment_ewma_volatility(
    data: Union[
        pd.DataFrame,
        pd.core.groupby.generic.DataFrameGroupBy,
        pl.DataFrame,
        pl.dataframe.group_by.GroupBy,
    ],
    date_column: Union[str, ColumnSelector],
    close_column: Union[str, ColumnSelector, Sequence[Union[str, ColumnSelector]]],
    decay_factor: float = 0.94,
    window: Union[int, Tuple[int, int], List[int]] = 20,
    reduce_memory: bool = False,
    engine: Optional[str] = "auto",
) -> Union[pd.DataFrame, pl.DataFrame]:
    """Calculate Exponentially Weighted Moving Average (EWMA) volatility for a financial time series.

    Parameters
    ----------
    data : DataFrame or GroupBy (pandas or polars)
        Input time-series data. Grouped inputs are processed per group before
        the indicator is appended.
    date_column : str or ColumnSelector
        Column name or selector containing dates or timestamps.
    close_column : str, ColumnSelector, or list
        Column(s) with closing prices to calculate volatility. Must resolve to
        a single column.
    decay_factor : float, optional
        Smoothing factor (lambda) for EWMA, between 0 and 1. Higher values give more weight to past data. Default is 0.94 (RiskMetrics standard).
    window : Union[int, Tuple[int, int], List[int]], optional
        Size of the rolling window to initialize EWMA calculation. For each window value the EWMA volatility is only computed when at least that many observations are available.
        You may provide a single integer or multiple values (via tuple or list). Default is 20.
    reduce_memory : bool, optional
        If True, reduces memory usage before calculation. Default is False.
    engine : {"auto", "pandas", "polars", "cudf"}, optional
        Execution engine. ``"auto"`` (default) infers the backend from the
        input data while allowing explicit overrides.

    Returns
    -------
    DataFrame
        DataFrame with added columns:
        - {close_column}_ewma_vol_{window}_{decay_factor}: EWMA volatility calculated using a minimum number of periods equal to each specified window.

    Notes
    -----
    EWMA volatility emphasizes recent price movements and is computed recursively as:

        σ²_t = (1 - λ) * r²_t + λ * σ²_{t-1}

    where r_t is the log return. By using the `min_periods` (set to the provided window value) we ensure that the EWMA is only calculated after enough observations have accumulated.

    References:

    - https://www.investopedia.com/articles/07/ewma.asp

    Examples
    --------
    ```{python}
    import pandas as pd
    import polars as pl
    import pytimetk as tk

    df = tk.load_dataset("stocks_daily", parse_dates=["date"])

    df
    ```

    ```{python}
    # EWMA Volatility - single stock (pandas)
    ewma_single = (
        df
        .query("symbol == 'AAPL'")
        .augment_ewma_volatility(
            date_column="date",
            close_column="close",
            decay_factor=0.94,
            window=[20, 50],
        )
    )

    ewma_single.glimpse()
    ```

    ```{python}
    # EWMA Volatility - grouped pandas engine
    ewma_grouped = (
        df
        .groupby("symbol")
        .augment_ewma_volatility(
            date_column="date",
            close_column="close",
            decay_factor=0.94,
            window=[20, 50],
        )
    )

    ewma_grouped.glimpse()
    ```

    ```{python}
    # EWMA Volatility - polars engine
    pl_single = pl.from_pandas(df.query("symbol == 'AAPL'"))
    ewma_polars = (
        pl_single
        .tk.augment_ewma_volatility(
            date_column="date",
            close_column="close",
            decay_factor=0.94,
            window=[20, 50],
        )
    )

    ewma_polars.glimpse()
    ```

    ```{python}
    # EWMA Volatility - polars grouped
    pl_df_full = pl.from_pandas(df)
    ewma_polars_grouped = (
        pl_df_full
        .group_by("symbol")
        .tk.augment_ewma_volatility(
            date_column="date",
            close_column="close",
            decay_factor=0.94,
            window=[20, 50],
        )
    )

    ewma_polars_grouped.glimpse()
    ```

    ```{python}
    from pytimetk.utils.selection import contains

    selector_df = (
        df
        .augment_ewma_volatility(
            date_column=contains("dat"),
            close_column=contains("clos"),
            window=20,
        )
    )

    selector_df.glimpse()
    ```
    """
    pass


def _augment_ewma_volatility_pandas(
    data: Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy],
    close_column: str,
    decay_factor: float,
    windows: List[int],
) -> pd.DataFrame:
    """Pandas implementation of EWMA volatility calculation with varying minimum periods."""
    pass


def _augment_ewma_volatility_cudf_dataframe(
    frame: "cudf.DataFrame",
    *,
    date_column: str,
    close_column: str,
    decay_factor: float,
    windows: List[int],
    group_columns: Optional[Sequence[str]],
    row_id_column: Optional[str],
) -> "cudf.DataFrame":
    pass


def _augment_ewma_volatility_polars(
    data: Union[pl.DataFrame, pl.dataframe.group_by.GroupBy],
    date_column: str,
    close_column: str,
    decay_factor: float,
    windows: List[int],
    group_columns: Optional[Sequence[str]],
    row_id_column: Optional[str],
) -> pl.DataFrame:
    """Polars implementation of EWMA volatility calculation with varying minimum periods."""
    def _maybe_over(expr: pl.Expr) -> pl.Expr:
        pass
    pass


def _normalize_windows(window: Union[int, Tuple[int, int], List[int]]) -> List[int]:
    pass
