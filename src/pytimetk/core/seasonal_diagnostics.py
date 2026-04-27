from __future__ import annotations

import pandas as pd
import pandas_flavor as pf

from typing import List, Sequence, Union

from pytimetk.feature_engineering import augment_timeseries_signature
from pytimetk.utils.checks import (
    check_dataframe_or_groupby,
)
from pytimetk.utils.selection import ColumnSelector
from pytimetk.feature_engineering._shift_utils import resolve_shift_columns

_SEASONAL_FEATURE_MAP = {
    "second": "second",
    "minute": "minute",
    "hour": "hour",
    "wday.lbl": "wday_lbl",
    "wday_lbl": "wday_lbl",
    "week": "yweek",
    "month.lbl": "month_lbl",
    "month_lbl": "month_lbl",
    "quarter": "quarter",
    "year": "year",
}

_FEATURE_PERIOD_SECONDS = {
    "second": 1,
    "minute": 60,
    "hour": 3600,
    "wday.lbl": 86400,
    "week": 604800,
    "month.lbl": 2629800,  # ~30.44 days
    "quarter": 7889400,  # 3 months
    "year": 31557600,  # 365.25 days
}

_AUTO_FEATURE_BANDS = [
    (60, ["second", "minute", "hour", "wday.lbl", "week", "month.lbl"]),
    (3600, ["minute", "hour", "wday.lbl", "week", "month.lbl"]),
    (86400, ["hour", "wday.lbl", "week", "month.lbl", "quarter", "year"]),
    (604800, ["wday.lbl", "week", "month.lbl", "quarter", "year"]),
    (2678400, ["week", "month.lbl", "quarter", "year"]),
]


def _normalise_feature_name(feature: str) -> str:
    pass


def _auto_seasonal_features(index: pd.Series) -> List[str]:
    def has_two_periods(name: str) -> bool:
        pass
    pass


def _resolve_feature_set(
    feature_set: Union[str, Sequence[str], None],
    index: pd.Series,
) -> List[str]:
    pass


def _seasonal_diagnostics_single(
    frame: pd.DataFrame,
    date_column: str,
    value_column: str,
    feature_set: List[str],
) -> pd.DataFrame:
    pass


@pf.register_groupby_method
@pf.register_dataframe_method
def seasonal_diagnostics(
    data: Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy],
    date_column: Union[str, ColumnSelector],
    value_column: Union[str, ColumnSelector],
    feature_set: Union[str, Sequence[str], None] = "auto",
) -> pd.DataFrame:
    """
    Prepare seasonal feature diagnostics akin to ``tk_seasonal_diagnostics``.

    Parameters
    ----------
    data : pd.DataFrame or pd.core.groupby.generic.DataFrameGroupBy
        Time series data (long format) or grouped data.
    date_column : str
        Name of the datetime column.
    value_column : str
        Numeric measure to analyse.
    feature_set : str or sequence, optional
        One or more of ``["second", "minute", "hour", "wday.lbl", "week",
        "month.lbl", "quarter", "year"]``. The special value ``"auto"``
        selects features based on the timestamp scale and overall history.

    Returns
    -------
    pd.DataFrame
        Tidy data with:

        - grouping columns (when present)
        - ``date`` (or the supplied ``date_column``)
        - the original ``value_column``
        - ``seasonal_feature`` (e.g. ``"hour"``)
        - ``seasonal_value`` (the actual categorical value for that observation)

    Examples
    --------
    ```{python}
    import numpy as np
    import pandas as pd
    import pytimetk as tk

    rng = pd.date_range("2020-01-01", periods=48, freq="H")
    df = pd.DataFrame(
        {
            "id": ["A"] * 24 + ["B"] * 24,
            "date": list(rng[:24]) + list(rng[:24]),
            "value": np.random.default_rng(123).normal(size=48),
        }
    )

    diagnostics = tk.seasonal_diagnostics(
        data=df.groupby("id"),
        date_column="date",
        value_column="value",
        feature_set=["hour", "wday.lbl"],
    )
    diagnostics.head()
    ```

    ```{python}
    from pytimetk.utils.selection import contains

    selector_diagnostics = tk.seasonal_diagnostics(
        data=df,
        date_column=contains("dat"),
        value_column=contains("val"),
        feature_set=["hour"],
    )
    selector_diagnostics.head()
    ```
    """
    pass
