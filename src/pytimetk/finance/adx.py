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
def augment_adx(
    data: Union[
        pd.DataFrame,
        pd.core.groupby.generic.DataFrameGroupBy,
        pl.DataFrame,
        pl.dataframe.group_by.GroupBy,
        "cudf.DataFrame",
        "cudf.core.groupby.groupby.DataFrameGroupBy",
    ],
    date_column: Union[str, ColumnSelector],
    high_column: Union[str, ColumnSelector],
    low_column: Union[str, ColumnSelector],
    close_column: Union[str, ColumnSelector],
    periods: Union[int, Tuple[int, int], List[int]] = 14,
    reduce_memory: bool = False,
    engine: Optional[str] = "auto",
) -> Union[pd.DataFrame, pl.DataFrame, "cudf.DataFrame"]:
    """
    Calculate Average Directional Index (ADX), +DI, and -DI using pandas or polars backends.

    Parameters
    ----------
    data : DataFrame or GroupBy (pandas or polars)
        Input financial data. Grouped inputs are processed per group before the
        indicators are appended.
    date_column : str or ColumnSelector
        Name of the column containing date information (tidy selectors supported).
    high_column, low_column, close_column : str or ColumnSelector
        Column names used to compute the indicator. Selectors must resolve to a
        single column each.
    periods : int, tuple, or list, optional
        Lookback windows for smoothing. Accepts an integer, a tuple specifying
        an inclusive range, or a list of explicit periods. Defaults to ``14``.
    reduce_memory : bool, optional
        Attempt to reduce memory usage when operating on pandas data. If a
        polars input is supplied a warning is emitted and no conversion occurs.
    engine : {"auto", "pandas", "polars"}, optional
        Execution engine. ``"auto"`` (default) infers the backend from the
        input data while allowing explicit overrides.

    Returns
    -------
    DataFrame
        DataFrame with the following columns appended for each ``period``:

        - ``{close_column}_plus_di_{period}``
        - ``{close_column}_minus_di_{period}``
        - ``{close_column}_adx_{period}``

        The return type matches the input backend.

    Notes
    -----
    The implementation follows Wilder's smoothing approach using exponential
    moving averages with ``alpha = 1 / period`` for the true range (TR) and
    directional movement (+DM, -DM) components. Division by zero is guarded by
    returning ``NaN`` when the denominator is zero.

    Examples
    --------
    ```{python}
    import pytimetk as tk

    df = tk.load_dataset("stocks_daily", parse_dates=["date"])

    # Pandas example (engine inferred)
    adx_df = (
        df.groupby("symbol")
        .augment_adx(
            date_column="date",
            high_column="high",
            low_column="low",
            close_column="close",
            periods=[14, 28],
        )
    )

    adx_df.glimpse()
    ```

    ```{python}
    # Polars example (method chaining)
    import polars as pl

    pl_df = pl.from_pandas(df.query("symbol == 'AAPL'"))

    adx_pl = pl_df.tk.augment_adx(
        date_column="date",
        high_column="high",
        low_column="low",
        close_column="close",
        periods=14,
    )

    adx_pl.glimpse()

    # Selector example
    from pytimetk.utils.selection import contains
    demo = (
        df
            .augment_adx(
                date_column=contains("dat"),
                high_column=contains("high"),
                low_column=contains("low"),
                close_column=contains("clos"),
                periods=14,
            )
    )
    ```
    """
    pass


def _augment_adx_pandas(
    data,
    high_column: str,
    low_column: str,
    close_column: str,
    periods: List[int],
) -> pd.DataFrame:
    pass


def _augment_adx_cudf_dataframe(
    frame: "cudf.DataFrame",
    *,
    date_column: str,
    high_column: str,
    low_column: str,
    close_column: str,
    periods: List[int],
    group_columns: Optional[Sequence[str]],
    row_id_column: Optional[str],
) -> "cudf.DataFrame":
    pass


def _augment_adx_polars(
    data: Union[pl.DataFrame, pl.dataframe.group_by.GroupBy],
    date_column: str,
    high_column: str,
    low_column: str,
    close_column: str,
    periods: List[int],
    group_columns: Optional[Sequence[str]],
    row_id_column: Optional[str],
) -> pl.DataFrame:
    def _maybe_over(expr: pl.Expr) -> pl.Expr:
        pass
    pass


def _normalize_periods(periods: Union[int, Tuple[int, int], List[int]]) -> List[int]:
    pass
