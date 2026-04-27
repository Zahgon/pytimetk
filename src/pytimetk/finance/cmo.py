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
def augment_cmo(
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
    Calculate the Chande Momentum Oscillator (CMO) using pandas or polars backends.

    Parameters
    ----------
    data : DataFrame or GroupBy (pandas or polars)
        Input financial data. Grouped inputs are processed per group before the
        indicator columns are appended.
    date_column : str or ColumnSelector
        Name or selector for the column containing date information.
    close_column : str, ColumnSelector, or list
        Column(s) containing closing prices. Selectors/lists must resolve to a
        single column.
    periods : int, tuple, or list, optional
        Lookback window(s) applied to the CMO calculation. Accepts a single
        integer, an inclusive tuple range, or an explicit list. Defaults to ``14``.
    reduce_memory : bool, optional
        Attempt to reduce memory usage when operating on pandas data. If a
        polars input is supplied a warning is emitted and no conversion occurs.
    engine : {"auto", "pandas", "polars"}, optional
        Execution engine. ``"auto"`` (default) infers the backend from the
        input data while allowing explicit overrides.

    Returns
    -------
    DataFrame
        DataFrame with ``{close_column}_cmo_{period}`` columns appended for
        every requested period. The return type matches the input backend.

    Notes
    -----
    The Chande Momentum Oscillator (CMO) compares the magnitude of recent gains
    to recent losses over the supplied lookback window. Values range from -100
    (all losses) to +100 (all gains). Division-by-zero cases are guarded by
    returning ``NaN`` which matches the pandas behaviour.

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
    # Chande Momentum Oscillator - pandas engine
    cmo_pd = (
        df
        .groupby("symbol")
        .augment_cmo(
            date_column="date",
            close_column="close",
            periods=[14, 28],
        )
    )

    cmo_pd.glimpse()
    ```

    ```{python}
    # Chande Momentum Oscillator - polars engine
    pl_df = pl.from_pandas(df.query("symbol == 'AAPL'"))
    cmo_pl = (
        pl_df
        .tk.augment_cmo(
            date_column="date",
            close_column="close",
            periods=14,
        )
    )

    cmo_pl.glimpse()
    ```

    ```{python}
    from pytimetk.utils.selection import contains

    selector_df = (
        df
        .augment_cmo(
            date_column=contains("dat"),
            close_column=contains("clos"),
            periods=14,
        )
    )

    selector_df.glimpse()
    ```
    """
    pass


def _augment_cmo_cudf_dataframe(
    frame: "cudf.DataFrame",
    *,
    date_column: str,
    close_column: str,
    periods: List[int],
    group_columns: Optional[Sequence[str]],
    row_id_column: Optional[str],
) -> "cudf.DataFrame":
    pass


def _augment_cmo_pandas(
    data: Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy],
    close_column: str,
    periods: List[int],
) -> pd.DataFrame:
    pass


def _calculate_cmo_pandas(series: pd.Series, period=14):
    # Calculate the difference in closing prices
    pass


def _augment_cmo_polars(
    data: Union[pl.DataFrame, pl.dataframe.group_by.GroupBy],
    date_column: str,
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
