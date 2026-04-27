import pandas as pd
import polars as pl

import pandas_flavor as pf
import warnings
from typing import List, Optional, Sequence, Tuple, Union

try:  # Optional cudf dependency
    import cudf  # type: ignore
except ImportError:  # pragma: no cover - cudf optional
    cudf = None  # type: ignore

from pytimetk._polars_compat import ensure_polars_rolling_kwargs
from pytimetk.utils.polars_helpers import collect_lazyframe
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
from pytimetk.utils.selection import ColumnSelector
from pytimetk.feature_engineering._shift_utils import resolve_shift_columns


@pf.register_groupby_method
@pf.register_dataframe_method
def augment_stochastic_oscillator(
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
    k_periods: Union[int, Tuple[int, int], List[int]] = 14,
    d_periods: Union[int, List[int]] = 3,
    reduce_memory: bool = False,
    engine: Optional[str] = "auto",
) -> Union[pd.DataFrame, pl.DataFrame, "cudf.DataFrame"]:
    """
    Calculate Stochastic Oscillator (%K and %D) using pandas or polars backends.

    Parameters
    ----------
    data : DataFrame or GroupBy (pandas or polars)
        Input financial data. Grouped inputs are processed per group before
        the indicators are appended.
    date_column : str or ColumnSelector
        Name of the column containing date information (selectors supported).
    high_column : str or ColumnSelector
        Column containing high prices.
    low_column : str or ColumnSelector
        Column containing low prices.
    close_column : str or ColumnSelector
        Column containing closing prices. Resulting columns are prefixed with
        this name.
    k_periods : int, tuple, or list, optional
        Lookback window(s) for the %K calculation. Accepts a single integer, an
        inclusive tuple range, or an explicit list. Defaults to ``14``.
    d_periods : int or list, optional
        Lookback window(s) for the %D smoothing calculation. Defaults to ``3``.
    reduce_memory : bool, optional
        Attempt to reduce memory usage when operating on pandas data. If a
        polars input is supplied a warning is emitted and no conversion occurs.
    engine : {"auto", "pandas", "polars"}, optional
        Execution engine. ``"auto"`` (default) infers the backend from the
        input data while allowing explicit overrides.

    Returns
    -------
    DataFrame
        DataFrame with %K and %D columns appended for every combination of
        ``k_periods`` and ``d_periods``. The return type matches the input
        backend.

    Notes
    -----
    %K is defined as ``100 * (Close - LowestLow) / (HighestHigh - LowestLow)``
    where LowestLow/HighestHigh span the specified lookback window. %D is the
    rolling mean of %K over ``d_periods``. Division-by-zero scenarios yield
    ``NaN`` values to match the pandas behaviour.

    Examples
    --------
    ```{python}
    import polars as pl
    import pytimetk as tk

    df = tk.load_dataset("stocks_daily", parse_dates=["date"])

    # Pandas example (engine inferred)
    stoch_df = df.groupby("symbol").augment_stochastic_oscillator(
        date_column="date",
        high_column="high",
        low_column="low",
        close_column="close",
        k_periods=[14, 21],
        d_periods=[3, 9],
    )

    # Polars example (method chaining)
    stoch_pl = (
        pl.from_pandas(df.query("symbol == 'AAPL'"))
        .tk.augment_stochastic_oscillator(
            date_column="date",
            high_column="high",
            low_column="low",
            close_column="close",
            k_periods=14,
            d_periods=[3],
        )
    )

    from pytimetk.utils.selection import contains
    selector_demo = (
        df
            .augment_stochastic_oscillator(
                date_column=contains("dat"),
                high_column=contains("high"),
                low_column=contains("low"),
                close_column=contains("clos"),
                k_periods=14,
                d_periods=[3],
            )
    )
    ```
    """
    pass


def _augment_stochastic_cudf_dataframe(
    frame: "cudf.DataFrame",
    *,
    date_column: str,
    high_column: str,
    low_column: str,
    close_column: str,
    k_periods: List[int],
    d_periods: List[int],
    group_columns: Optional[Sequence[str]],
    row_id_column: Optional[str],
) -> "cudf.DataFrame":
    pass


def _augment_stochastic_pandas(
    data,
    high_column: str,
    low_column: str,
    close_column: str,
    k_periods: List[int],
    d_periods: List[int],
) -> pd.DataFrame:
    pass


def _augment_stochastic_polars(
    data: Union[pl.DataFrame, pl.dataframe.group_by.GroupBy],
    date_column: str,
    high_column: str,
    low_column: str,
    close_column: str,
    k_periods: List[int],
    d_periods: List[int],
    group_columns: Optional[Sequence[str]],
    row_id_column: Optional[str],
) -> pl.DataFrame:
    def _maybe_over(expr: pl.Expr) -> pl.Expr:
        pass
    pass


def _normalize_periods(periods: Union[int, Tuple[int, int], List[int]], label: str) -> List[int]:
    pass


def _normalize_d_periods(d_periods: Union[int, List[int]]) -> List[int]:
    pass
