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
from pytimetk.utils.memory_helpers import reduce_memory_usage
from pytimetk.utils.pandas_helpers import sort_dataframe
from pytimetk.utils.polars_helpers import collect_lazyframe
from pytimetk.utils.selection import ColumnSelector
from pytimetk.feature_engineering._shift_utils import resolve_shift_columns


@pf.register_groupby_method
@pf.register_dataframe_method
def augment_hurst_exponent(
    data: Union[
        pd.DataFrame,
        pd.core.groupby.generic.DataFrameGroupBy,
        pl.DataFrame,
        pl.dataframe.group_by.GroupBy,
    ],
    date_column: Union[str, ColumnSelector],
    close_column: Union[str, ColumnSelector, Sequence[Union[str, ColumnSelector]]],
    window: Union[int, Tuple[int, int], List[int]] = 100,
    reduce_memory: bool = False,
    engine: Optional[str] = "auto",
) -> Union[pd.DataFrame, pl.DataFrame]:
    """Calculate the Hurst Exponent on a rolling window for a financial time series. Used for detecting trends and mean-reversion.

    Parameters
    ----------
    data : DataFrame or GroupBy (pandas or polars)
        Input time-series data. Grouped inputs are processed per group before
        the exponent is appended.
    date_column : str or ColumnSelector
        Column name or selector containing dates or timestamps.
    close_column : str, ColumnSelector, or list
        Column(s) with closing prices to calculate the Hurst Exponent. Must
        resolve to a single column.
    window : Union[int, Tuple[int, int], List[int]], optional
        Size of the rolling window for Hurst Exponent calculation. Accepts int, tuple (start, end), or list. Default is 100.
    reduce_memory : bool, optional
        If True, reduces memory usage before calculation. Default is False.
    engine : {"auto", "pandas", "polars"}, optional
        Execution engine. ``"auto"`` (default) infers the backend from the
        input data while allowing explicit overrides.

    Returns
    -------
    DataFrame
        DataFrame with added columns:
        - {close_column}_hurst_{window}: Hurst Exponent for each window size

    Notes
    -----
    The Hurst Exponent measures the long-term memory of a time series:

    - H < 0.5: Mean-reverting behavior
    - H ≈ 0.5: Random walk (no persistence)
    - H > 0.5: Trending or persistent behavior
    Computed using a simplified R/S analysis over rolling windows.

    References:

    - https://en.wikipedia.org/wiki/Hurst_exponent

    Examples:
    ---------
    ```{python}
    import pandas as pd
    import polars as pl
    import pytimetk as tk

    df = tk.load_dataset("stocks_daily", parse_dates=["date"])

    df
    ```

    ```{python}
    # Hurst exponent - single stock (pandas)
    hurst_single = (
        df
        .query("symbol == 'AAPL'")
        .augment_hurst_exponent(
            date_column="date",
            close_column="close",
            window=[100, 200],
        )
    )

    hurst_single.glimpse()
    ```

    ```{python}
    # Hurst exponent - grouped pandas engine
    hurst_grouped = (
        df
        .groupby("symbol")
        .augment_hurst_exponent(
            date_column="date",
            close_column="close",
            window=100,
        )
    )

    hurst_grouped.glimpse()
    ```

    ```{python}
    # Hurst exponent - polars engine
    pl_single = pl.from_pandas(df.query("symbol == 'AAPL'"))
    hurst_polars = (
        pl_single
        .tk.augment_hurst_exponent(
            date_column="date",
            close_column="close",
            window=[100, 200],
        )
    )

    hurst_polars.glimpse()
    ```

    ```{python}
    # Hurst exponent - polars grouped
    pl_grouped = pl.from_pandas(df)
    hurst_polars_grouped = (
        pl_grouped
        .group_by("symbol")
        .tk.augment_hurst_exponent(
            date_column="date",
            close_column="close",
            window=100,
        )
    )

    hurst_polars_grouped.glimpse()
    ```

    ```{python}
    from pytimetk.utils.selection import contains

    selector_df = (
        df
        .groupby("symbol")
        .augment_hurst_exponent(
            date_column=contains("dat"),
            close_column=contains("clos"),
            window=100,
        )
    )

    selector_df.glimpse()
    ```
    """
    pass


def _hurst_from_array(values: np.ndarray, min_size: int = 8) -> float:
    pass


def _augment_hurst_exponent_pandas(
    data: Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy],
    close_column: str,
    windows: List[int],
) -> pd.DataFrame:
    """Pandas implementation of Hurst Exponent calculation."""
    pass


def _augment_hurst_exponent_cudf_dataframe(
    frame: "cudf.DataFrame",
    *,
    date_column: str,
    close_column: str,
    windows: List[int],
    group_columns: Optional[Sequence[str]],
    row_id_column: Optional[str],
) -> "cudf.DataFrame":
    pass


def _augment_hurst_exponent_polars(
    data: Union[pl.DataFrame, pl.dataframe.group_by.GroupBy],
    date_column: str,
    close_column: str,
    windows: List[int],
    group_columns: Optional[Sequence[str]],
    row_id_column: Optional[str],
) -> pl.DataFrame:
    """Polars implementation of Hurst Exponent calculation."""
    def hurst_udf(series):
        pass
    def _maybe_over(expr: pl.Expr) -> pl.Expr:
        pass
    pass


def _normalize_windows(window: Union[int, Tuple[int, int], List[int]]) -> List[int]:
    pass
