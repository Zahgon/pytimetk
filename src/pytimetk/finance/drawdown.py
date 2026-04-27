import pandas as pd
import polars as pl
import pandas_flavor as pf
import warnings
from typing import Optional, Sequence, Union

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
def augment_drawdown(
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
    reduce_memory: bool = False,
    engine: Optional[str] = "auto",
) -> Union[pd.DataFrame, pl.DataFrame, "cudf.DataFrame"]:
    """
    Calculate running drawdown statistics for pandas or polars data.

    Parameters
    ----------
    data : DataFrame or GroupBy (pandas or polars)
        Input time-series data. Grouped inputs are processed per group before
        the drawdown metrics are appended.
    date_column : str or ColumnSelector
        Name or selector for the column containing date information.
    close_column : str, ColumnSelector, or list
        Column(s) containing the values used to compute drawdowns. Must resolve
        to a single column.
    reduce_memory : bool, optional
        Attempt to reduce memory usage when operating on pandas data. If a
        polars input is supplied a warning is emitted and no conversion occurs.
    engine : {"auto", "pandas", "polars"}, optional
        Execution engine. ``"auto"`` (default) infers the backend from the
        input data while allowing explicit overrides.

    Returns
    -------
    DataFrame
        DataFrame with the following columns appended:

        - ``{close_column}_peak``
        - ``{close_column}_drawdown``
        - ``{close_column}_drawdown_pct``

        The return type matches the input backend.

    Notes
    -----
    Drawdown measures the peak-to-trough decline of a series. The running peak
    is computed with a cumulative maximum per group (if present) and the
    drawdown percentage is expressed relative to that peak. When the peak is
    zero the percentage drawdown is left as ``NaN`` to avoid division by zero.

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
    # Drawdown - pandas engine
    dd_pd = (
        df
        .groupby("symbol")
        .augment_drawdown(
            date_column="date",
            close_column="close",
        )
    )

    dd_pd.glimpse()
    ```

    ```{python}
    # Drawdown - polars engine
    pl_df = pl.from_pandas(df.query("symbol == 'AAPL'"))
    dd_pl = (
        pl_df
        .tk.augment_drawdown(
            date_column="date",
            close_column="close",
        )
    )

    dd_pl.glimpse()
    ```

    ```{python}
    from pytimetk.utils.selection import contains

    selector_df = (
        df
        .groupby("symbol")
        .augment_drawdown(
            date_column=contains("dat"),
            close_column=contains("clos"),
        )
    )

    selector_df.glimpse()
    ```
    """
    pass


def _augment_drawdown_cudf_dataframe(
    frame: "cudf.DataFrame",
    *,
    date_column: str,
    close_column: str,
    group_columns: Optional[Sequence[str]],
    row_id_column: Optional[str],
) -> "cudf.DataFrame":
    pass


def _augment_drawdown_pandas(
    data: Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy],
    close_column: str,
) -> pd.DataFrame:
    """Pandas implementation of drawdown calculation."""
    pass


def _augment_drawdown_polars(
    data: Union[pl.DataFrame, pl.dataframe.group_by.GroupBy],
    date_column: str,
    close_column: str,
    group_columns: Optional[Sequence[str]],
    row_id_column: Optional[str],
) -> pl.DataFrame:
    """Polars implementation of drawdown calculation."""
    pass
