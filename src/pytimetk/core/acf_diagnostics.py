from dataclasses import dataclass
from typing import List, Optional, Sequence, Union

import numpy as np
import pandas as pd
import pandas_flavor as pf

from statsmodels.tsa.stattools import acf as sm_acf
from statsmodels.tsa.stattools import ccf as sm_ccf
from statsmodels.tsa.stattools import pacf as sm_pacf

from pytimetk.utils.checks import (
    check_dataframe_or_groupby,
)
from pytimetk.utils.datetime_helpers import resolve_lag_sequence
from pytimetk.utils.selection import resolve_column_selection, ColumnSelector
from pytimetk.feature_engineering._shift_utils import resolve_shift_columns
from pytimetk.utils.dataframe_ops import resolve_pandas_groupby_frame


@dataclass
class _ACFConfig:
    date_column: str
    value_column: str
    ccf_columns: List[str]
    lags: Union[str, int, Sequence[int], np.ndarray, range, slice]


def _prepare_numeric(series: pd.Series) -> pd.Series:
    pass


def _acf_diagnostics_single(frame: pd.DataFrame, config: _ACFConfig) -> pd.DataFrame:
    pass


@pf.register_groupby_method
@pf.register_dataframe_method
def acf_diagnostics(
    data: Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy],
    date_column: Union[str, ColumnSelector],
    value_column: Union[str, ColumnSelector],
    ccf_columns: Optional[Union[str, ColumnSelector, Sequence[Union[str, ColumnSelector]], np.ndarray]] = None,
    lags: Union[str, int, Sequence[int], np.ndarray, range, slice] = 1000,
) -> pd.DataFrame:
    """
    Compute tidy autocorrelation, partial autocorrelation, and optional
    cross-correlation diagnostics for one or more time series.

    Parameters
    ----------
    data : pd.DataFrame or pd.core.groupby.generic.DataFrameGroupBy
        Long-form time series data (optionally grouped via ``groupby``).
    date_column : str
        Name of the datetime column.
    value_column : str
        Numeric column used to compute ACF/PACF diagnostics.
    ccf_columns : str or sequence, optional
        Additional numeric columns to run cross-correlation against
        ``value_column``. Accepts literal column names or tidy selectors created
        with :mod:`pytimetk.utils.selection` (e.g. ``contains("driver")``).
    lags : int, sequence, slice, or str, optional
        Lag specification. Integers mirror ``range(0, lags)``,
        sequences/slices are used verbatim, and strings such as ``"30 days"`` or
        ``"3 months"`` are resolved relative to the supplied index. Defaults to
        ``1000``.

    Returns
    -------
    pd.DataFrame
        Diagnostics with columns:

        - grouping columns (when present)
        - ``metric`` (``"ACF"``, ``"PACF"``, or ``"CCF_<column>"``)
        - ``lag`` (non-negative integer)
        - ``value`` (correlation)
        - ``white_noise_upper`` / ``white_noise_lower`` (95% bounds)

    Examples
    --------
    ```{python}
    import numpy as np
    import pandas as pd
    import pytimetk as tk

    rng = pd.date_range("2020-01-01", periods=40, freq="D")
    df = pd.DataFrame(
        {
            "id": ["A"] * 20 + ["B"] * 20,
            "date": list(rng[:20]) + list(rng[:20]),
            "value": np.sin(np.linspace(0, 4 * np.pi, 40)),
            "driver": np.cos(np.linspace(0, 4 * np.pi, 40)),
        }
    )

    diagnostics = tk.acf_diagnostics(
        data=df.groupby("id"),
        date_column="date",
        value_column="value",
        ccf_columns="driver",
        lags="30 days",
    )
    diagnostics.head()
    ```
    """
    pass
