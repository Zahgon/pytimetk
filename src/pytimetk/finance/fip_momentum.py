import pandas as pd
import polars as pl
import numpy as np
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
def augment_fip_momentum(
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
    window: Union[int, List[int]] = 252,
    reduce_memory: bool = False,
    engine: Optional[str] = "auto",
    fip_method: str = "original",
    skip_window: int = 0,  # new parameter to skip the first n periods
) -> Union[pd.DataFrame, pl.DataFrame, "cudf.DataFrame"]:
    """
    Calculate the "Frog In The Pan" (FIP) momentum metric over one or more rolling windows
    using either the pandas or polars engine, augmenting the DataFrame with FIP columns.

    The FIP momentum is defined as:

    - For `fip_method = 'original'`: FIP = Total Return * (percent of negative returns - percent of positive returns)
    - For `fip_method = 'modified'`: FIP = sign(Total Return) * (percent of positive returns - percent of negative returns)

    An optional parameter, `skip_window`, allows you to skip the first n periods (e.g., one month)
    to mitigate the effects of mean reversion.

    Parameters
    ----------
    data : Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy]
        Input pandas DataFrame or grouped DataFrame containing time series data.
    date_column : str or ColumnSelector
        Name or selector for the column with dates or timestamps.
    close_column : str, ColumnSelector, or list
        Column(s) with closing prices to calculate returns. Must resolve to a
        single column.
    window : Union[int, List[int]], optional
        Size of the rolling window(s) as an integer or list of integers (default is 252).
    reduce_memory : bool, optional
        If True, reduces memory usage of the DataFrame. Default is False.
    engine : str, optional
        Computation engine: 'pandas' or 'polars'. Default is 'pandas'.
    fip_method : str, optional
        Type of FIP calculation:
        - 'original': Original FIP calculation (default) where negative FIP indicates greater momentum.
        - 'modified': Modified FIP where positive FIP indicates greater momentum.
    skip_window : int, optional
        Number of initial periods to skip (set to NA) for each rolling calculation. Default is 0.

    Returns
    -------
    pd.DataFrame
        DataFrame augmented with FIP momentum columns:

        - {close_column}_fip_momentum_{w}: Rolling FIP momentum for each window w


    Notes
    -----

    - For 'original', a positive FIP may indicate inconsistency in the trend.
    - For 'modified', a positive FIP indicates stronger momentum in the direction of the trend (upward or downward).

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
    # FIP Momentum - pandas engine
    fip_df = (
        df
        .query("symbol == 'AAPL'")
        .augment_fip_momentum(
            date_column="date",
            close_column="close",
            window=252,
        )
    )

    fip_df.glimpse()
    ```

    ```{python}
    # FIP Momentum - polars engine
    pl_df = pl.from_pandas(df)
    fip_polars = (
        pl_df
        .group_by("symbol")
        .tk.augment_fip_momentum(
            date_column="date",
            close_column="close",
            window=[63, 252],
            fip_method="modified",
        )
    )

    fip_polars.glimpse()
    ```

    ```{python}
    from pytimetk.utils.selection import contains

    selector_df = (
        df
        .augment_fip_momentum(
            date_column=contains("dat"),
            close_column=contains("clos"),
            window=252,
        )
    )

    selector_df.glimpse()
    ```
    """
    pass


def _augment_fip_momentum_pandas(
    data: Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy],
    close_column: str,
    windows: List[int],
    fip_method: str,
    skip_window: int,
) -> pd.DataFrame:
    def calc_fip(ser, window, fip_method):
        pass
    pass


def _augment_fip_momentum_cudf_dataframe(
    frame: "cudf.DataFrame",
    *,
    date_column: str,
    close_column: str,
    windows: List[int],
    fip_method: str,
    skip_window: int,
    group_columns: Optional[Sequence[str]],
    row_id_column: Optional[str],
) -> "cudf.DataFrame":
    pass


def _compute_fip_series(
    returns: np.ndarray,
    window: int,
    fip_method: str,
    skip_window: int,
) -> np.ndarray:
    pass


def _augment_fip_momentum_polars(
    data: Union[pl.DataFrame, pl.dataframe.group_by.GroupBy],
    date_column: str,
    close_column: str,
    windows: List[int],
    fip_method: str,
    skip_window: int,
    group_columns: Optional[Sequence[str]],
    row_id_column: Optional[str],
) -> pl.DataFrame:
    def fip_calc(values: np.ndarray, w: int, method: str) -> float:
        pass
    def _maybe_over(expr: pl.Expr) -> pl.Expr:
        pass
    pass
