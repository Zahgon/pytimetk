import pandas as pd
import pandas_flavor as pf
import plotly.graph_objects as go
import statsmodels.formula.api as smf

from typing import Any, Dict, List, Optional, Union

try:  # Optional dependency for seamless polars support
    import polars as pl
except ImportError:  # pragma: no cover - optional import
    pl = None

from pytimetk.utils.dataframe_ops import resolve_pandas_groupby_frame
from pytimetk.utils.selection import ColumnSelector, resolve_column_selection


SERIES_COLUMN = "__regression_series__"
VALUE_COLUMN = "__regression_value__"


def _to_pandas(data: Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy]):
    pass


def _resolve_date_column(
    data: Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy],
    selector: Union[str, ColumnSelector],
) -> str:
    pass


def _prepare_long_frame(
    df: pd.DataFrame,
    date_column: str,
    response_column: str,
    fitted_values: pd.Series,
    group_columns: List[str],
) -> pd.DataFrame:
    pass


def _fit_group(
    df: pd.DataFrame,
    date_column: str,
    formula: str,
    show_summary: bool,
    group_label: Optional[str],
    model_kwargs: Dict[str, Any],
    group_columns: List[str],
) -> pd.DataFrame:
    pass


@pf.register_groupby_method
@pf.register_dataframe_method
def plot_time_series_regression(
    data: Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy],
    date_column: Union[str, ColumnSelector],
    formula: str,
    show_summary: bool = False,
    model_kwargs: Optional[Dict[str, Any]] = None,
    **plot_kwargs: Any,
) -> go.Figure:
    """
    Fit a linear regression using a formula and visualise observed vs fitted
    values over time using :func:`pytimetk.plot_timeseries`.

    Parameters
    ----------
    data : DataFrame or GroupBy
        Long-format time series data or grouped data via ``DataFrame.groupby``.
        Polars inputs are automatically converted to pandas.
    date_column : str or ColumnSelector
        Datetime column used on the x-axis.
    formula : str
        Patsy/Statsmodels formula passed to :func:`statsmodels.formula.api.ols`.
    show_summary : bool, optional
        Print statsmodels regression summaries (per group when grouped).
    model_kwargs : dict, optional
        Extra keyword arguments forwarded to :func:`statsmodels.formula.api.ols`.
        Use this to pass ``eval_env`` when formulas depend on outer scope names.
    **plot_kwargs : dict, optional
        Additional keyword arguments forwarded to :func:`pytimetk.plot_timeseries`
        (faceting, dropdowns, theme overrides, etc.).

    Returns
    -------
    plotly.graph_objects.Figure
        Plotly figure showing observed vs fitted values over time.

    Examples
    --------
    ```{python}
    import numpy as np
    import pytimetk as tk

    df = tk.load_dataset("taylor_30_min", parse_dates=["date"]).assign(
        trend=lambda d: np.arange(len(d))
    )

    fig = tk.plot_time_series_regression(
        data=df,
        date_column="date",
        formula="value ~ trend",
        title="Observed vs Fitted",
    )
    fig
    ```

    ```{python}
    # Grouped example
    df["half"] = np.where(df["trend"] < df["trend"].median(), "H1", "H2")
    fig_grouped = tk.plot_time_series_regression(
        data=df.groupby("half"),
        date_column="date",
        formula="value ~ trend",
        facet_ncol=1,
    )
    fig_grouped
    ```

    ```{python}
    # Example with additional time-series features (trend + day/hour effects)
    df_features = df.assign(
        dow=lambda d: d["date"].dt.dayofweek,
        hour=lambda d: d["date"].dt.hour,
    )

    fig_features = tk.plot_time_series_regression(
        data=df_features,
        date_column="date",
        formula="value ~ trend + C(dow) + C(hour)",
        facet_ncol=1,
        color_lab="Series",
    )
    fig_features
    ```
    """
    pass
