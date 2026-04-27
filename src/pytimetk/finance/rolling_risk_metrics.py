import pandas as pd
import polars as pl
import pandas_flavor as pf
import numpy as np
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
from pytimetk.utils.selection import ColumnSelector
from pytimetk.feature_engineering._shift_utils import resolve_shift_columns
from scipy import stats  # For skewness and kurtosis


@pf.register_groupby_method
@pf.register_dataframe_method
def augment_rolling_risk_metrics(
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
    risk_free_rate: float = 0.0,
    benchmark_column: Optional[
        Union[str, ColumnSelector, Sequence[Union[str, ColumnSelector]]]
    ] = None,
    annualization_factor: int = 252,
    metrics: Optional[List[str]] = None,
    reduce_memory: bool = False,
    engine: Optional[str] = "auto",
) -> Union[pd.DataFrame, pl.DataFrame]:
    """The augment_rolling_risk_metrics function calculates rolling risk-adjusted performance
    metrics for a financial time series using either pandas or polars engine, and returns
    the augmented DataFrame with columns for Sharpe Ratio, Sortino Ratio, and other metrics.

    Parameters
    ----------
    data : Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy]
        The input data can be a pandas DataFrame or a pandas DataFrameGroupBy object
        containing the time series data for risk metric calculations.
    date_column : str or ColumnSelector
        The name or selector of the column containing dates or timestamps.
    close_column : str, ColumnSelector, or list
        The column(s) containing closing prices to calculate returns and risk
        metrics from. Must resolve to exactly one column.
    window : int, optional
        The rolling window size for calculations (e.g., 252 for annual). Default is 252.
    risk_free_rate : float, optional
        The assumed risk-free rate (e.g., 0.0 for 0%). Default is 0.0.
    benchmark_column : str, ColumnSelector, or None, optional
        Column containing benchmark returns (e.g., market index) for Treynor
        and Information Ratios. If provided it must resolve to one column.
        Default is None.
    annualization_factor : int, optional
        The factor to annualize returns and volatility (e.g., 252 for daily data). Default is 252.
    metrics : List[str] or None, optional
        The list of risk metrics to calculate. Choose from: 'sharpe_ratio', 'sortino_ratio',
        'treynor_ratio', 'information_ratio', 'omega_ratio', 'volatility_annualized',
        'skewness', 'kurtosis'. Default is None (all metrics).
    reduce_memory : bool, optional
        If True, reduces memory usage of the DataFrame before calculation. Default is False.
    engine : str, optional
        The computation engine to use: 'pandas' or 'polars'. Default is 'pandas'.

    Returns
    -------
    pd.DataFrame
        A pandas DataFrame augmented with columns:
        - {close_column}_sharpe_ratio_{window}: Rolling Sharpe Ratio
        - {close_column}_sortino_ratio_{window}: Rolling Sortino Ratio
        - {close_column}_treynor_ratio_{window}: Rolling Treynor Ratio (if benchmark provided)
        - {close_column}_information_ratio_{window}: Rolling Information Ratio (if benchmark provided)
        - {close_column}_omega_ratio_{window}: Rolling Omega Ratio
        - {close_column}_volatility_annualized_{window}: Rolling annualized volatility
        - {close_column}_skewness_{window}: Rolling skewness of returns
        - {close_column}_kurtosis_{window}: Rolling kurtosis of returns

    Notes
    -----
    This function computes returns from closing prices and calculates rolling risk metrics:

    - Sharpe Ratio: Excess return over risk-free rate divided by volatility
    - Sortino Ratio: Excess return over risk-free rate divided by downside deviation
    - Treynor Ratio: Excess return over risk-free rate divided by beta (requires benchmark)
    - Information Ratio: Excess return over benchmark divided by tracking error (requires benchmark)
    - Omega Ratio: Ratio of gains to losses above/below a threshold
    - Volatility: Annualized standard deviation of returns
    - Skewness: Asymmetry of return distribution
    - Kurtosis: Fat-tailedness of return distribution

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
    # Rolling risk metrics - single stock (pandas)
    risk_single = (
        df
        .query("symbol == 'AAPL'")
        .augment_rolling_risk_metrics(
            date_column="date",
            close_column="adjusted",
            window=252,
        )
    )

    risk_single.glimpse()
    ```

    ```{python}
    # Rolling risk metrics - polars grouped
    pl_df = pl.from_pandas(df)
    risk_polars = (
        pl_df
        .group_by("symbol")
        .tk.augment_rolling_risk_metrics(
            date_column="date",
            close_column="adjusted",
            window=60,
        )
    )

    risk_polars.glimpse()
    ```

    ```{python}
    # Rolling risk metrics - selective pandas metrics
    risk_selected = (
        df
        .groupby("symbol")
        .augment_rolling_risk_metrics(
            date_column="date",
            close_column="adjusted",
            window=252,
            metrics=["sharpe_ratio", "sortino_ratio", "volatility_annualized"],
        )
    )

    risk_selected.glimpse()
    ```

    ```{python}
    from pytimetk.utils.selection import contains

    selector_df = (
        df
        .groupby("symbol")
        .augment_rolling_risk_metrics(
            date_column=contains("dat"),
            close_column=contains("adj"),
            benchmark_column=contains("clos"),
            window=63,
            metrics=["sharpe_ratio"],
        )
    )

    selector_df.glimpse()
    ```
    """
    pass


def _augment_rolling_risk_metrics_pandas(
    data: Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy],
    date_column: str,
    close_column: str,
    windows: List[int],
    risk_free_rate: float,
    benchmark_column: Optional[str],
    annualization_factor: int,
    metrics: List[str],
) -> pd.DataFrame:
    """Pandas implementation of rolling risk metrics calculation with selective metrics."""
    def roll_downside_std(ser, window_size, **kwargs):
        pass
    def roll_omega(ser, window_size, **kwargs):
        pass
    def roll_beta(ser, bench_ser, window_size, **kwargs):
        pass
    pass


def _augment_rolling_risk_metrics_cudf_dataframe(
    frame: "cudf.DataFrame",
    *,
    date_column: str,
    close_column: str,
    windows: List[int],
    risk_free_rate: float,
    benchmark_column: Optional[str],
    annualization_factor: int,
    metrics: List[str],
    group_columns: Optional[Sequence[str]],
    row_id_column: Optional[str],
) -> "cudf.DataFrame":
    pass


def _augment_rolling_risk_metrics_polars(
    data: Union[pl.DataFrame, pl.dataframe.group_by.GroupBy],
    date_column: str,
    close_column: str,
    windows: List[int],
    risk_free_rate: float,
    benchmark_column: Optional[str],
    annualization_factor: int,
    metrics: List[str],
    group_columns: Optional[Sequence[str]],
    row_id_column: Optional[str],
) -> pl.DataFrame:
    pass
