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
def augment_atr(
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
    periods: Union[int, Tuple[int, int], List[int]] = 20,
    normalize: bool = False,
    reduce_memory: bool = False,
    engine: Optional[str] = "auto",
) -> Union[pd.DataFrame, pl.DataFrame, "cudf.DataFrame"]:
    """
    Calculate Average True Range (ATR) or Normalised ATR for pandas or polars data.

    Parameters
    ----------
    data : DataFrame or GroupBy (pandas or polars)
        Input financial data. Grouped inputs are processed per group before the
        indicators are appended.
    date_column : str or ColumnSelector
        Name of the column containing date information. Accepts tidy selectors.
    high_column, low_column, close_column : str or ColumnSelector
        Column names/selectors used to compute the true range and ATR.
    periods : int, tuple, or list, optional
        Rolling window lengths. Accepts an integer, an inclusive tuple range,
        or an explicit list. Defaults to ``20``.
    normalize : bool, optional
        When ``True``, report the normalised ATR (``ATR / close * 100``). Defaults
        to ``False``.
    reduce_memory : bool, optional
        Attempt to reduce memory usage when operating on pandas data. If a
        polars input is supplied a warning is emitted and no conversion occurs.
    engine : {"auto", "pandas", "polars"}, optional
        Execution engine. ``"auto"`` (default) infers the backend from the
        input data while allowing explicit overrides.

    Returns
    -------
    DataFrame
        DataFrame with ``{close_column}_atr_{period}`` (or ``_natr_`` when
        ``normalize=True``) columns appended for each requested period. The
        return type matches the input backend.

    Notes
    -----
    The Average True Range (ATR) follows Wilder's definition, using the maximum
    of the intra-period range, the high-to-previous-close distance, and the
    low-to-previous-close distance. When ``normalize=True`` the ATR is scaled
    by the close price and expressed as a percentage (often called NATR). Both
    pandas and polars implementations guard against division by zero by
    returning ``NaN`` when the denominator is zero.

    Examples
    --------
    ```{python}
    import pandas as pd
    import polars as pl
    import pytimetk as tk


    df = tk.load_dataset("stocks_daily", parse_dates=["date"])

    # Pandas example (engine inferred)
    atr_pd = (
        df.groupby("symbol")
        .augment_atr(
            date_column="date",
            high_column="high",
            low_column="low",
            close_column="close",
            periods=[14, 28],
            normalize=False,
        )
    )

    # Polars example using the tk accessor
    atr_pl = (
        pl.from_pandas(df.query("symbol == 'AAPL'"))
        .tk.augment_atr(
            date_column="date",
            high_column="high",
            low_column="low",
            close_column="close",
            periods=14,
            normalize=True,
        )
    )

    # Selector example
    from pytimetk.utils.selection import contains
    selector_example = (
        df
            .augment_atr(
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


def _augment_atr_pandas(
    data: Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy],
    high_column: str,
    low_column: str,
    close_column: str,
    periods: List[int],
    normalize: bool,
) -> pd.DataFrame:
    """Pandas implementation of ATR/NATR calculation."""
    pass


def _augment_atr_polars(
    data: Union[pl.DataFrame, pl.dataframe.group_by.GroupBy],
    date_column: str,
    high_column: str,
    low_column: str,
    close_column: str,
    periods: List[int],
    normalize: bool,
    group_columns: Optional[Sequence[str]],
    row_id_column: Optional[str],
) -> pl.DataFrame:
    """Polars implementation of ATR/NATR calculation."""
    def _maybe_over(expr: pl.Expr) -> pl.Expr:
        pass
    pass


def _augment_atr_cudf_dataframe(
    frame: "cudf.DataFrame",
    *,
    date_column: str,
    high_column: str,
    low_column: str,
    close_column: str,
    periods: List[int],
    normalize: bool,
    group_columns: Optional[Sequence[str]],
    row_id_column: Optional[str],
) -> "cudf.DataFrame":
    pass


def _normalize_periods(periods: Union[int, Tuple[int, int], List[int]]) -> List[int]:
    pass
