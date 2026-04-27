import pandas as pd
import polars as pl
import numpy as np

import pandas_flavor as pf
import warnings
from typing import List, Optional, Sequence, Tuple, Union
from joblib import Parallel, delayed

try:
    from hmmlearn.hmm import GaussianHMM
except ImportError:  # pragma: no cover - optional dependency
    GaussianHMM = None

import importlib
import importlib.util

_POMEGRANATE_MODEL = None
_POMEGRANATE_DIST = None


def _ensure_pomegranate_available():
    """
    Lazily import pomegranate regardless of major version.
    Returns (HiddenMarkovModel, NormalDistribution) classes.
    """
    pass


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

HMMLEARN_AVAILABLE = GaussianHMM is not None
POMEGRANATE_AVAILABLE = importlib.util.find_spec("pomegranate") is not None


@pf.register_groupby_method
@pf.register_dataframe_method
def augment_regime_detection(
    data: Union[
        pd.DataFrame,
        pd.core.groupby.generic.DataFrameGroupBy,
        pl.DataFrame,
        pl.dataframe.group_by.GroupBy,
    ],
    date_column: Union[str, ColumnSelector],
    close_column: Union[str, ColumnSelector, Sequence[Union[str, ColumnSelector]]],
    window: Union[int, Tuple[int, int], List[int]] = 252,
    n_regimes: int = 2,
    method: str = "hmm",
    step_size: int = 1,
    n_iter: int = 100,
    n_jobs: int = -1,
    reduce_memory: bool = False,
    hmm_backend: str = "auto",
    engine: Optional[str] = "auto",
) -> Union[pd.DataFrame, pl.DataFrame]:
    """Detect regimes in a financial time series using a specified method (e.g., HMM).

    Parameters
    ----------
    data : DataFrame or GroupBy (pandas or polars)
        Input time-series data. Grouped inputs are processed per group before
        the regime labels are appended.
    date_column : str or ColumnSelector
        Column (or selector) containing dates or timestamps.
    close_column : str, ColumnSelector, or list
        Column(s) with closing prices used for regime detection. Must resolve to
        exactly one column.
    window : Union[int, Tuple[int, int], List[int]], optional
        Size of the rolling window to fit the regime detection model. Default is 252.
    n_regimes : int, optional
        Number of regimes to detect (e.g., 2 for bull/bear). Default is 2.
    method : str, optional
        Method for regime detection. Currently supports 'hmm'. Default is 'hmm'.
    step_size : int, optional
        Step size between HMM fits (e.g., 10 fits every 10 rows). Default is 1.
    n_iter : int, optional
        Number of iterations for HMM fitting. Default is 100.
    n_jobs : int, optional
        Number of parallel jobs for group processing (-1 uses all cores). Default is -1.
    reduce_memory : bool, optional
        If True, reduces memory usage. Default is False.
    hmm_backend : {"auto", "pomegranate", "hmmlearn"}, optional
        Backend library used for the HMM implementation. ``"auto"`` (default)
        prefers the faster ``pomegranate`` backend when installed, otherwise
        falls back to ``hmmlearn``.
    engine : {"auto", "pandas", "polars"}, optional
        Execution engine. ``"auto"`` (default) infers the backend from the
        input data while allowing explicit overrides.

    Returns
    -------
    DataFrame
        DataFrame with added columns:
        - {close_column}_regime_{window}: Integer labels for detected regimes (e.g., 0, 1).

    Notes
    -----
    - Uses Hidden Markov Model (HMM) to identify latent regimes based on log returns.
    - Regimes reflect distinct statistical states (e.g., high/low volatility, trending).
    - Requires 'hmmlearn' package. Install with `pip install hmmlearn` or the faster optional `pomegranate` backend via `pip install 'pytimetk[regime_backends]'` (equivalent to `pip install 'pomegranate<1.0'`).

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
    # Regime detection - pandas single stock (requires hmm backend)
    regime_single = (
        df
        .query("symbol == 'AAPL'")
        .augment_regime_detection(
            date_column="date",
            close_column="close",
            window=252,
            n_regimes=2,
        )
    )

    regime_single.glimpse()
    ```

    ```{python}
    # Regime detection - pandas grouped (requires hmm backend)
    regime_grouped = (
        df
        .groupby("symbol")
        .augment_regime_detection(
            date_column="date",
            close_column="close",
            window=[252, 504],
            n_regimes=3,
        )
    )

    regime_grouped.groupby("symbol").tail(1)
    ```

    ```{python}
    # Regime detection - polars engine (requires hmm backend)
    pl_single = pl.from_pandas(df.query("symbol == 'AAPL'"))
    regime_polars = (
        pl_single
        .tk.augment_regime_detection(
            date_column="date",
            close_column="close",
            window=252,
            n_regimes=2,
        )
    )

    regime_polars.glimpse()
    ```

    ```{python}
    # Pomegranate backend with column selectors
    from pytimetk.utils.selection import contains

    selector_demo = (
        df
        .groupby("symbol")
        .augment_regime_detection(
            date_column=contains("dat"),
            close_column=contains("clos"),
            window=252,
            n_regimes=4,
            hmm_backend="pomegranate", # pomegranate<=1.0.0 required
        )
    )

    selector_demo.groupby("symbol").tail(1)
    ```

    ``` {python}
    # Visualizing regimes
    SYMBOLS = ['AAPL', 'AMZN', 'MSFT', 'GOOG', 'NVDA']
    SYMBOL = 'NVDA'

    (
        selector_demo
        .query(f"symbol == '{SYMBOL}'")
        .plot_timeseries(
            date_column="date",
            value_column="close",
            color_column=contains("regime_"),
            smooth=False,
            title=f"{SYMBOL} Close Price with Detected Regimes",
        )
    )
    ```
    """
    pass


def _augment_regime_detection_pandas(
    data: Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy],
    date_column: str,
    close_column: str,
    windows: List[int],
    n_regimes: int,
    step_size: int,
    n_iter: int,
    hmm_backend: str,
    n_jobs: int,
) -> pd.DataFrame:
    """Pandas implementation of regime detection using HMM."""
    def detect_regimes(series, window, n_regimes, step_size, n_iter):
        pass
    pass


def _augment_regime_detection_polars(
    data: Union[pl.DataFrame, pl.dataframe.group_by.GroupBy],
    date_column: str,
    close_column: str,
    windows: List[int],
    n_regimes: int,
    step_size: int,
    n_iter: int,
    hmm_backend: str,
    n_jobs: int,
    group_columns: Optional[Sequence[str]],
    row_id_column: Optional[str],
) -> pl.DataFrame:
    """Polars implementation of regime detection using HMM (via pandas)."""
    pass


def _normalize_windows(window: Union[int, Tuple[int, int], List[int]]) -> List[int]:
    pass
