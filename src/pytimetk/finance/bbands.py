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
from pytimetk.utils.selection import ColumnSelector
from pytimetk.feature_engineering._shift_utils import resolve_shift_columns


@pf.register_groupby_method
@pf.register_dataframe_method
def augment_bbands(
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
    periods: Union[int, Tuple[int, int], List[int]] = 20,
    std_dev: Union[int, float, List[float]] = 2,
    reduce_memory: bool = False,
    engine: Optional[str] = "auto",
) -> Union[pd.DataFrame, pl.DataFrame, "cudf.DataFrame"]:
    """
    Calculate Bollinger Bands for pandas or polars data.

    Parameters
    ----------
    data : DataFrame or GroupBy (pandas or polars)
        Input financial data. Grouped inputs are processed per group before the
        bands are appended.
    date_column : str or ColumnSelector
        Name/selector for the column containing date information. Supports tidy
        selectors such as ``contains("date")``.
    close_column : str, ColumnSelector, or list
        Column(s) containing the prices used to compute the moving average and
        standard deviation. Selectors or lists must resolve to a single column.
    periods : int, tuple, or list, optional
        Rolling window lengths. An integer adds a single window, a tuple
        ``(start, end)`` expands to every integer in the inclusive range, and a
        list provides explicit windows. Defaults to ``20``.
    std_dev : float, int, or list, optional
        Number(s) of standard deviations used when constructing the upper and
        lower bands. Integers are converted to floats. Defaults to ``2``.
    reduce_memory : bool, optional
        Attempt to reduce memory usage when operating on pandas data. If a
        polars input is supplied a warning is emitted and no conversion occurs.
    engine : {"auto", "pandas", "polars"}, optional
        Execution engine. ``"auto"`` (default) infers the backend from the
        input data while allowing explicit overrides.

    Returns
    -------
    DataFrame
        DataFrame with middle/upper/lower band columns appended for each
        ``period`` and ``std_dev`` combination. The return type matches the
        input backend (pandas or polars).

    Notes
    -----
    The middle band is the rolling mean of ``close_column``. The upper band is
    the middle band plus ``std_dev`` times the rolling standard deviation, and
    the lower band subtracts the same quantity. Rolling statistics are
    calculated with a minimum window equal to ``period`` which matches the
    behaviour of the pandas implementation.

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
    # Bollinger Bands - pandas engine
    bbands_df = (
        df
        .groupby("symbol")
        .augment_bbands(
            date_column="date",
            close_column="close",
            periods=[20, 40],
            std_dev=[1.5, 2.0],
        )
    )

    bbands_df.glimpse()
    ```

    ```{python}
    # Bollinger Bands - polars engine
    pl_df = pl.from_pandas(df.query("symbol == 'AAPL'"))
    bbands_pl = (
        pl_df
        .tk.augment_bbands(
            date_column="date",
            close_column="close",
            periods=(10, 15),
            std_dev=2,
        )
    )

    bbands_pl.glimpse()
    ```

    ```{python}
    from pytimetk.utils.selection import contains

    selector_demo = (
        df
        .augment_bbands(
            date_column=contains("dat"),
            close_column=contains("clos"),
            periods=20,
            std_dev=2,
        )
    )

    selector_demo.glimpse()
    ```
    """
    pass


def _augment_bbands_cudf_dataframe(
    frame: "cudf.DataFrame",
    *,
    date_column: str,
    close_column: str,
    periods: List[int],
    std_dev: List[float],
    group_columns: Optional[Sequence[str]],
    row_id_column: Optional[str],
) -> "cudf.DataFrame":
    pass


def _augment_bbands_pandas(
    data,
    close_column: str,
    periods: List[int],
    std_dev: List[float],
) -> pd.DataFrame:
    pass


def _augment_bbands_polars(
    data: Union[pl.DataFrame, pl.dataframe.group_by.GroupBy],
    date_column: str,
    close_column: str,
    periods: List[int],
    std_dev: List[float],
    group_columns: Optional[Sequence[str]],
    row_id_column: Optional[str],
) -> pl.DataFrame:
    pass


def _normalize_periods(periods: Union[int, Tuple[int, int], List[int]]) -> List[int]:
    pass


def _normalize_std_dev(std_dev: Union[int, float, List[float]]) -> List[float]:
    pass


def _format_sd(sd: float) -> str:
    pass
