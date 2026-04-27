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
def augment_roc(
    data: Union[
        pd.DataFrame,
        pd.core.groupby.generic.DataFrameGroupBy,
        pl.DataFrame,
        pl.dataframe.group_by.GroupBy,
    ],
    date_column: Union[str, ColumnSelector],
    close_column: Union[str, ColumnSelector, Sequence[Union[str, ColumnSelector]]],
    periods: Union[int, Tuple[int, int], List[int]] = 1,
    start_index: int = 0,
    reduce_memory: bool = False,
    engine: Optional[str] = "auto",
) -> Union[pd.DataFrame, pl.DataFrame]:
    """
    Add rate-of-change (ROC) columns to a pandas or polars DataFrame.

    Parameters
    ----------
    data : DataFrame or GroupBy (pandas or polars)
        Input financial data. Grouped inputs are expanded per group before
        computing ROC features.
    date_column : str or ColumnSelector
        Name of the column containing date information (tidy selectors supported)
        used to preserve the original ordering.
    close_column : str, ColumnSelector, or list
        Column(s) containing closing prices on which the ROC is computed. Lists or
        multiple selectors compute an ROC per column.
    periods : int, tuple, or list, optional
        Lookback windows used for the denominator term. An integer adds a
        single ROC column, a tuple ``(start, end)`` expands to the inclusive
        range ``start..end``, and a list provides explicit periods. Defaults to
        ``1``.
    start_index : int, optional
        Offset applied to the numerator. When ``0`` (default) the current value
        is used; otherwise the numerator uses ``close.shift(start_index)``.
    reduce_memory : bool, optional
        Attempt to reduce memory usage when operating on pandas data. If used
        with polars inputs a warning is emitted and no conversion is performed.
    engine : {"auto", "pandas", "polars"}, optional
        Execution engine. ``"auto"`` (default) infers the backend from the
        input data type while also accepting explicit overrides.

    Returns
    -------
    DataFrame
        DataFrame with ROC columns appended. The return type matches the input
        backend (pandas or polars).

    Notes
    -----
    Rate of change is defined as ::

        ROC = (Value_t - Value_{t-period}) / Value_{t-period}

    When ``start_index`` is non-zero the numerator is taken from
    ``Value_{t-start_index}`` instead of the current value. The implementation
    safeguards against division by zero by returning ``NaN`` whenever the
    denominator is zero.

    Examples
    --------
    ```{python}
    import polars as pl
    import pytimetk as tk


    df = tk.load_dataset("stocks_daily", parse_dates=["date"])

    # Pandas DataFrame input (engine inferred)
    roc_df = df.groupby("symbol").augment_roc(
        date_column="date",
        close_column="close",
        periods=[22, 63],
        start_index=5,
    )

    # Polars DataFrame input using the tk accessor
    roc_pl = (
        pl.from_pandas(df.query("symbol == 'AAPL'"))
        .tk.augment_roc(
            date_column="date",
            close_column="close",
            periods=(5, 10),
        )
    )

    # Selector example
    from pytimetk.utils.selection import contains

    selector_demo = (
        df
            .augment_roc(
                date_column=contains("dat"),
                close_column=contains("clos"),
                periods=[5, 10],
            )
    )
    ```
    """
    pass


def _augment_roc_cudf_dataframe(
    frame: "cudf.DataFrame",
    *,
    date_column: str,
    close_columns: List[str],
    periods: List[int],
    start_index: int,
    group_columns: Optional[Sequence[str]],
    row_id_column: Optional[str],
) -> "cudf.DataFrame":
    pass


def _augment_roc_pandas(
    data,
    close_columns: List[str],
    periods: List[int],
    start_index: int,
) -> pd.DataFrame:
    pass


def _roc_pandas_series(series: pd.Series, period: int, start_index: int) -> pd.Series:
    pass


def _augment_roc_polars(
    data: Union[pl.DataFrame, pl.dataframe.group_by.GroupBy],
    date_column: str,
    close_columns: List[str],
    periods: List[int],
    start_index: int,
    group_columns: Optional[Sequence[str]],
    row_id_column: Optional[str],
) -> pl.DataFrame:
    pass


def _roc_expression(
    col: str,
    period: int,
    start_index: int,
    groups: Sequence[str],
) -> pl.Expr:
    pass


def _roc_column(col: str, start_index: int, period: int) -> str:
    pass


def _normalize_periods(periods: Union[int, Tuple[int, int], List[int]]) -> List[int]:
    pass
