import math
from typing import List, Optional, Sequence, Union

import pandas as pd
import pandas_flavor as pf
import plotly.graph_objects as go
from plotly.subplots import make_subplots

try:  # Optional dependency for seamless polars support
    import polars as pl
except ImportError:  # pragma: no cover - optional import
    pl = None

from pytimetk.core.seasonal_diagnostics import seasonal_diagnostics
from pytimetk.utils.selection import ColumnSelector, resolve_column_selection
from pytimetk.utils.dataframe_ops import resolve_pandas_groupby_frame
from pytimetk.utils.plot_helpers import hex_to_rgba


@pf.register_groupby_method
@pf.register_dataframe_method
def plot_seasonal_diagnostics(
    data: Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy],
    date_column: Union[str, ColumnSelector],
    value_column: Union[str, ColumnSelector],
    feature_set: Union[str, Sequence[str], None] = "auto",
    facet_vars: Optional[Union[str, Sequence[str], ColumnSelector]] = None,
    facet_ncols: Optional[int] = 1,
    geom: str = "box",
    geom_color: str = "#2c3e50",
    geom_outlier_color: str = "#2c3e50",
    title: str = "Seasonal Diagnostics",
    x_lab: str = "",
    y_lab: str = "",
    width: Optional[int] = None,
    height: Optional[int] = None,
    plotly_dropdown: bool = False,
    plotly_dropdown_x: float = 1.05,
    plotly_dropdown_y: float = 1.05,
) -> go.Figure:
    """
    Visualize seasonal patterns using box or violin plots grouped by seasonality
    features (hour, weekday, month, etc.). Works with pandas or polars inputs.

    Parameters
    ----------
    data : pd.DataFrame or pd.core.groupby.generic.DataFrameGroupBy
        Time series data (long format) or grouped data. Polars DataFrames are supported.
    date_column : str or ColumnSelector
        Datetime column used to compute the seasonal features.
    value_column : str or ColumnSelector
        Numeric column plotted on the y-axis.
    feature_set : str or sequence, optional
        One or more of ``["second", "minute", "hour", "wday.lbl", "week",
        "month.lbl", "quarter", "year"]``. ``"auto"`` selects a sensible subset.
    facet_vars : str, sequence, or ColumnSelector, optional
        Additional categorical columns to facet by. They are treated as grouping
        columns for the diagnostics.
    facet_ncols : int, optional
        Number of facet columns when ``plotly_dropdown`` is ``False``. Defaults to 2.
    geom : {"box", "violin"}, optional
        Plotting geometry for each seasonal feature. Defaults to ``"box"``.
    geom_color : str, optional
        Primary color for the box/violin geometry. Defaults to ``"#2c3e50"``.
    geom_outlier_color : str, optional
        Outlier color for box plots. Defaults to ``"#2c3e50"``.
    title : str, optional
        Plot title.
    x_lab, y_lab : str, optional
        Axis labels.
    width, height : int, optional
        Figure dimensions in pixels. Height defaults to a sensible value based on
        the number of facets.
    plotly_dropdown : bool, optional
        When ``True`` and facet combinations exist, render a dropdown to switch
        between them.
    plotly_dropdown_x, plotly_dropdown_y : float, optional
        Dropdown position (only used when ``plotly_dropdown`` is ``True``).

    Returns
    -------
    plotly.graph_objects.Figure
        Figure containing one subplot per seasonal feature for each facet.

    Examples
    --------
    ```{python}
    import pytimetk as tk

    df = tk.load_dataset("taylor_30_min", parse_dates=["date"]).assign(
        month_name=lambda d: d["date"].dt.month_name()
    )

    fig = tk.plot_seasonal_diagnostics(
        data=df,
        date_column="date",
        value_column="value",
        feature_set="auto",
        geom="box",
    )
    fig
    ```

    ```{python}
    # Dropdown example, using tidy selectors
    from pytimetk.utils.selection import contains

    fig_dropdown = tk.plot_seasonal_diagnostics(
        data=df,
        date_column="date",
        value_column=contains("value"),
        feature_set="auto",
        facet_vars="month_name",
        plotly_dropdown=True,
    )
    fig_dropdown
    ```
    """
    def _resolve_single_selector(selector, data_obj, label: str) -> str:
        pass
    def _format_facet_label(row) -> str:
        pass
    pass
