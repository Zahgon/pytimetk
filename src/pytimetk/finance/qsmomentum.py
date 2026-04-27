import pandas as pd
import numpy as np
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
def augment_qsmomentum(
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
    roc_fast_period: Union[int, Tuple[int, int], List[int]] = 21,
    roc_slow_period: Union[int, Tuple[int, int], List[int]] = 252,
    returns_period: Union[int, Tuple[int, int], List[int]] = 126,
    reduce_memory: bool = False,
    engine: Optional[str] = "auto",
) -> Union[pd.DataFrame, pl.DataFrame, "cudf.DataFrame"]:
    """
    Calculate Quant Science Momentum (QSM) for pandas or polars inputs.

    Parameters
    ----------
    data : DataFrame or GroupBy (pandas or polars)
        Input financial data. Grouped inputs are processed per group before the
        momentum columns are appended.
    date_column : str or ColumnSelector
        Name or selector for the column containing date information.
    close_column : str, ColumnSelector, or list
        Column(s) containing closing prices used to compute QSM. Must resolve
        to exactly one column.
    roc_fast_period : int, tuple, or list, optional
        Lookback window(s) for the fast Rate of Change (ROC). Accepts a single
        integer, an inclusive tuple range, or a list of explicit periods.
    roc_slow_period : int, tuple, or list, optional
        Lookback window(s) for the slow ROC component.
    returns_period : int, tuple, or list, optional
        Lookback window(s) used when calculating the rolling standard deviation
        of returns.
    reduce_memory : bool, optional
        Attempt to reduce memory usage when operating on pandas data. If a
        polars input is supplied a warning is emitted and no conversion occurs.
    engine : {"auto", "pandas", "polars", "cudf"}, optional
        Execution engine. ``"auto"`` (default) infers the backend from the
        input data while allowing explicit overrides.

    Returns
    -------
    DataFrame
        DataFrame with ``{close_column}_qsmom_{fast}_{slow}_{returns}`` columns
        appended for every valid combination. The return type matches the input
        backend.

    Notes
    -----
    QSM measures the difference between slow and fast ROC values normalised by
    the rolling volatility of returns. Only combinations where ``fast < slow``
    and ``returns_period <= slow`` are evaluated. If no combinations satisfy
    these rules a ``ValueError`` is raised to surface the configuration issue.

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
    # QS Momentum - pandas engine
    qsm_pd = (
        df
        .groupby("symbol")
        .augment_qsmomentum(
            date_column="date",
            close_column="close",
            roc_fast_period=[5, 21],
            roc_slow_period=252,
            returns_period=126,
        )
    )

    qsm_pd.glimpse()
    ```

    ```{python}
    # QS Momentum - polars engine
    pl_df = pl.from_pandas(df)
    qsm_pl = (
        pl_df
        .group_by("symbol")
        .tk.augment_qsmomentum(
            date_column="date",
            close_column="close",
            roc_fast_period=[5, 21],
            roc_slow_period=252,
            returns_period=126,
        )
    )

    qsm_pl.glimpse()
    ```

    ```{python}
    from pytimetk.utils.selection import contains

    selector_df = (
        df
        .groupby("symbol")
        .augment_qsmomentum(
            date_column=contains("dat"),
            close_column=contains("clos"),
            roc_fast_period=21,
            roc_slow_period=252,
            returns_period=126,
        )
    )

    selector_df.glimpse()
    ```
    """
    pass


def _calculate_qsmomentum_pandas(
    close, roc_fast_period, roc_slow_period, returns_period
):
    pass


def _calculate_qsmomentum_polars(
    close, roc_fast_period, roc_slow_period, returns_period
):
    pass
def _augment_qsmomentum_pandas(
    data: Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy],
    close_column: str,
    combos: Sequence[Tuple[int, int, int]],
) -> pd.DataFrame:
    pass


def _augment_qsmomentum_polars(
    data: Union[pl.DataFrame, pl.dataframe.group_by.GroupBy],
    date_column: str,
    close_column: str,
    combos: Sequence[Tuple[int, int, int]],
    group_columns: Optional[Sequence[str]],
    row_id_column: Optional[str],
) -> pl.DataFrame:
    def _maybe_over(expr: pl.Expr) -> pl.Expr:
        pass
    pass


def _augment_qsmomentum_cudf_dataframe(
    frame: "cudf.DataFrame",
    *,
    date_column: str,
    close_column: str,
    combos: Sequence[Tuple[int, int, int]],
    group_columns: Optional[Sequence[str]],
    row_id_column: Optional[str],
) -> "cudf.DataFrame":
    pass


def _normalize_periods(
    periods: Union[int, Tuple[int, int], List[int]],
    label: str,
) -> List[int]:
    pass
