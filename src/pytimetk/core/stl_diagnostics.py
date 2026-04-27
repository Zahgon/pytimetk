from __future__ import annotations

import math
from typing import Optional, Sequence, Union

import numpy as np
import pandas as pd
import pandas_flavor as pf
from statsmodels.tsa.seasonal import STL

from pytimetk.core.frequency import get_seasonal_frequency, get_trend_frequency
from pytimetk.utils.checks import (
    check_dataframe_or_groupby,
    check_date_column,
    check_value_column,
)
from pytimetk.utils.datetime_helpers import parse_human_duration


def _median_interval(index: pd.Series) -> pd.Timedelta:
    pass


def _duration_to_period(
    duration: Union[pd.Timedelta, pd.DateOffset], index: pd.Series
) -> int:
    pass


def _resolve_period(
    value: Union[str, int, float, pd.Timedelta, pd.DateOffset, None],
    index: pd.Series,
    auto_callable,
) -> int:
    pass


def _stl_diagnostics_single(
    frame: pd.DataFrame,
    date_column: str,
    value_column: str,
    frequency: Union[str, int, float, pd.Timedelta, pd.DateOffset, None],
    trend: Union[str, int, float, pd.Timedelta, pd.DateOffset, None],
    robust: bool,
) -> pd.DataFrame:
    pass


@pf.register_groupby_method
@pf.register_dataframe_method
def stl_diagnostics(
    data: Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy],
    date_column: str,
    value_column: str,
    frequency: Union[str, int, float, pd.Timedelta, pd.DateOffset, None] = "auto",
    trend: Union[str, int, float, pd.Timedelta, pd.DateOffset, None] = "auto",
    robust: bool = True,
) -> pd.DataFrame:
    """
    Generate STL decomposition diagnostics (observed, season, trend, remainder, seasadj).

    Parameters
    ----------
    data : pd.DataFrame or pd.core.groupby.generic.DataFrameGroupBy
        Time series data, optionally grouped.
    date_column : str
        Name of the datetime column.
    value_column : str
        Numeric measure to decompose.
    frequency : str, int, float, pd.Timedelta, pd.DateOffset, optional
        Seasonal period specification. ``"auto"`` (default) infers a period via
        :func:`pytimetk.get_seasonal_frequency`. Strings such as ``"7D"`` or
        ``"30 days"`` are supported.
    trend : str, int, float, pd.Timedelta, pd.DateOffset, optional
        Trend window specification. ``"auto"`` (default) infers a window via
        :func:`pytimetk.get_trend_frequency`.
    robust : bool, optional
        Apply a robust STL fit (down-weights outliers). Defaults to ``True``.

    Returns
    -------
    pd.DataFrame
        Decomposition with columns:

        - grouping columns (if present)
        - ``date``, ``observed``, ``season``, ``trend``, ``remainder``, ``seasadj``

    Examples
    --------
    ```{python}
    import numpy as np
    import pandas as pd
    import pytimetk as tk

    rng = pd.date_range("2020-01-01", periods=180, freq="D")
    values = np.sin(np.linspace(0, 8 * np.pi, len(rng))) + np.random.default_rng(123).normal(scale=0.1, size=len(rng))
    df = pd.DataFrame({"date": rng, "value": values})

    decomposition = tk.stl_diagnostics(
        data=df,
        date_column="date",
        value_column="value",
        frequency="7D",
        trend="30 days",
    )
    decomposition.head()
    ```
    """
    pass
