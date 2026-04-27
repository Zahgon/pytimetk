import pandas as pd
import numpy as np
import polars as pl
import pandas_flavor as pf

from datetime import datetime, timedelta
from dateutil import parser
from typing import Iterable, List, Sequence, Union
import re

from pytimetk.utils.checks import check_series_or_datetime
from pytimetk.utils.polars_helpers import pandas_to_polars_frequency
from pytimetk.utils.string_helpers import parse_freq_str

_HUMAN_DURATION_PATTERN = re.compile(
    r"^\s*(?P<value>[-+]?\d*\.?\d+)?\s*(?P<unit>[a-zA-Z]+)\s*$"
)

_HUMAN_DURATION_UNITS = {
    # Timedelta-compatible units
    "s": "seconds",
    "sec": "seconds",
    "secs": "seconds",
    "second": "seconds",
    "seconds": "seconds",
    "ms": "milliseconds",
    "millisecond": "milliseconds",
    "milliseconds": "milliseconds",
    "us": "microseconds",
    "microsecond": "microseconds",
    "microseconds": "microseconds",
    "ns": "nanoseconds",
    "nanosecond": "nanoseconds",
    "nanoseconds": "nanoseconds",
    "m": "minutes",
    "min": "minutes",
    "mins": "minutes",
    "minute": "minutes",
    "minutes": "minutes",
    "h": "hours",
    "hr": "hours",
    "hrs": "hours",
    "hour": "hours",
    "hours": "hours",
    "d": "days",
    "day": "days",
    "days": "days",
    "w": "weeks",
    "wk": "weeks",
    "wks": "weeks",
    "week": "weeks",
    "weeks": "weeks",
    # DateOffset-based units
    "month": "months",
    "months": "months",
    "mon": "months",
    "mons": "months",
    "mo": "months",
    "q": "quarters",
    "quarter": "quarters",
    "quarters": "quarters",
    "y": "years",
    "yr": "years",
    "yrs": "years",
    "year": "years",
    "years": "years",
}

_FREQ_ALIAS_PAIRS = [
    ("CBM", "CBME"),
    ("BM", "BME"),
    ("SM", "SME"),
    ("BQ", "BQE"),
    ("BY", "BYE"),
    ("BA", "BYE"),
    ("BAS", "BYS"),
    ("A", "YE"),
    ("AS", "YS"),
    ("M", "ME"),
    ("Q", "QE"),
    ("Y", "YE"),
    ("H", "h"),
    ("T", "min"),
    ("L", "ms"),
    ("U", "us"),
    ("N", "ns"),
]


def parse_human_duration(
    value: Union[
        str, int, float, pd.Timedelta, np.timedelta64, timedelta, pd.DateOffset
    ],
) -> Union[pd.Timedelta, pd.DateOffset]:
    """
    Convert human-friendly duration input into a pandas Timedelta or DateOffset.

    Parameters
    ----------
    value : str or numeric or timedelta-like
        Supported examples include: ``"30 minutes"``, ``"2 hours"``, ``"3 months"``,
        ``"1 year"``, ``pd.Timedelta("7D")``, ``datetime.timedelta(days=2)``.

    Returns
    -------
    Union[pd.Timedelta, pd.DateOffset]
        Returns a Timedelta for fixed-width units (seconds through weeks) and a
        DateOffset for calendar-aware units (months, quarters, years).

    Raises
    ------
    ValueError
        If the input cannot be parsed or represents an unsupported unit.

    Examples
    --------
    ```{python}
    import pytimetk as tk

    tk.parse_human_duration("45 minutes")
    ```

    ```{python}
    tk.parse_human_duration("3 months")
    ```
    """
    pass


def normalize_frequency_alias(freq: str) -> str:
    """
    Normalize deprecated pandas frequency aliases to their modern equivalents.

    Parameters
    ----------
    freq : str
        Frequency string (e.g. ``"M"``, ``"Q-NOV"``, ``"ME"``, ``"3D"``).

    Returns
    -------
    str
        Returns ``freq`` unchanged if it does not match any deprecated alias.
        Otherwise the alias portion is replaced with the new spelling (e.g.
        ``"M" -> "ME"``, ``"Q-NOV" -> "QE-NOV"``).
    """
    def _replace(match: re.Match) -> str:
        pass
    pass


def resolve_lag_sequence(
    lags: Union[str, int, Sequence[int], np.ndarray, range, slice],
    index: Union[pd.Series, pd.DatetimeIndex, Sequence],
    clamp: bool = True,
) -> np.ndarray:
    """
    Normalise lag specifications into a sorted numpy array of non-negative integers.

    Parameters
    ----------
    lags : str, int, Sequence[int], range, slice
        - String durations (e.g. ``"30 days"``, ``"3 months"``) are converted to the
          number of observation lags implied by ``index``.
        - Integers produce a ``range(0, lags)`` style sequence (inclusive).
        - Sequences/ranges/slices are materialised and sorted.
    index : array-like
        A date/time index used to translate duration strings into row counts. The
        index is sorted internally.
    clamp : bool, optional
        If ``True`` (default), lags greater than ``len(index) - 1`` are clipped.

    Returns
    -------
    np.ndarray
        Sorted array of lag integers starting at zero.

    Raises
    ------
    ValueError
        When the input cannot be interpreted or the index is empty.

    Examples
    --------
    ```{python}
    import numpy as np
    import pandas as pd
    import pytimetk as tk

    idx = pd.date_range("2020-01-01", periods=5, freq="D")
    tk.resolve_lag_sequence("3 days", idx)
    ```

    ```{python}
    tk.resolve_lag_sequence([0, 2, 4], idx)
    ```
    """
    def _clamp(sequence: Iterable[int]) -> np.ndarray:
        pass
    pass


@pf.register_series_method
def floor_date(
    idx: Union[pd.Series, pd.DatetimeIndex],
    unit: str = "D",
    engine: str = "pandas",
) -> pd.Series:
    """
    Robust date flooring.

    The `floor_date` function takes a pandas Series of dates and returns a new Series
    with the dates rounded down to the specified unit. It's more robust than the
    pandas `floor` function, which does weird things with irregular frequencies
    like Month which are actually regular.

    Parameters
    ----------
    idx : pd.Series or pd.DatetimeIndex
        The `idx` parameter is a pandas Series or pandas DatetimeIndex object that
        contains datetime values. It represents the dates that you want to round down.
    unit : str, optional
        The `unit` parameter in the `floor_date` function is a string that specifies
        the time unit to which the dates in the `idx` series should be rounded down.
        It has a default value of "D", which stands for day. Other possible values
        for the `unit` parameter could be.
    engine : str, optional
        The `engine` parameter is used to specify the engine to use for calculating
        the floor datetime. It can be either "pandas" or "polars".

        - The default value is "pandas".

        - When "polars", the function will internally use the `polars` library for
          calculating the floor datetime. This can be faster than using "pandas" for
          large datasets.

    Returns
    -------
    pd.Series
        The `floor_date` function returns a pandas Series object containing datetime64[ns] values.

    Examples
    --------
    ```{python}
    import pytimetk as tk
    import pandas as pd

    dates = pd.date_range("2020-01-01", "2020-01-10", freq="1H")
    dates
    ```

    ```{python}
    # Pandas fails to floor Month
    # dates.floor("M") # ValueError: <MonthEnd> is a non-fixed frequency

    # floor_date works as expected
    tk.floor_date(dates, unit="M", engine='pandas')
    ```
    """
    pass


def _floor_date_pandas(
    idx: Union[pd.Series, pd.DatetimeIndex],
    unit: str = "D",
) -> pd.Series:
    """
    Robust date flooring.
    """
    pass


def _floor_date_polars(
    idx: Union[pd.Series, pd.DatetimeIndex],
    unit: str = "D",
) -> pd.Series:
    """
    Robust date flooring.
    """
    pass


@pf.register_series_method
def ceil_date(
    idx: Union[pd.Series, pd.DatetimeIndex],
    unit: str = "D",
) -> pd.Series:
    """
    Robust date ceiling.

    The `ceil_date` function takes a pandas Series of dates and returns a new
    Series with the dates rounded up to the next specified unit. It's more
    robust than the pandas `ceil` function, which does weird things with
    irregular frequencies like Month which are actually regular.

    Parameters
    ----------
    idx : pd.Series or pd.DatetimeIndex
        The `idx` parameter is a pandas Series or pandas DatetimeIndex object
        that contains datetime values. It represents the dates that you want to
        round down.
    unit : str, optional
        The `unit` parameter in the `ceil_date` function is a string that
        specifies the time unit to which the dates in the `idx` series should be
        rounded down. It has a default value of "D", which stands for day. Other
        possible values for the `unit` parameter could be

    Returns
    -------
    pd.Series
        The `ceil_date` function returns a pandas Series object containing
        datetime64[ns] values.

    Examples
    --------
    ```{python}
    import pytimetk as tk
    import pandas as pd

    dates = pd.date_range("2020-01-01", "2020-01-10", freq="1H")
    dates
    ```

    ```{python}
    # Pandas ceil fails on month
    # dates.ceil("M") # ValueError: <MonthEnd> is a non-fixed frequency

    # Works on Month
    tk.ceil_date(dates, unit="M")
    ```
    """
    pass


def freq_to_dateoffset(freq_str):
    pass


def freq_to_timedelta(freq_str):
    pass


def parse_end_date(date_str):
    pass


@pf.register_series_method
def week_of_month(
    idx: Union[pd.Series, pd.DatetimeIndex],
    engine: str = "pandas",
) -> pd.Series:
    """
    The "week_of_month" function calculates the week number of a given date
    within its month.

    Parameters
    ----------
    idx : pd.Series or pd.DatetimeIndex
        The parameter "idx" is a pandas Series object that represents a specific
        date for which you want to determine the week of the month.
    engine : str, optional
        The `engine` parameter is used to specify the engine to use for
        calculating the week of the month. It can be either "pandas" or "polars".

        - The default value is "pandas".

        - When "polars", the function will internally use the `polars` library
        for calculating the week of the month. This can be faster than using
        "pandas" for large datasets.


    Returns
    -------
    pd.Series
        The week of the month for a given date.

    Examples
    --------
    ```{python}
    import pytimetk as tk
    import pandas as pd

    dates = pd.date_range("2020-01-01", "2020-02-28", freq="1D")
    dates
    ```

    ```{python}
    # Works on DateTimeIndex
    tk.week_of_month(dates, engine='pandas')
    ```

    ```{python}
    # Works on DateTimeIndex
    tk.week_of_month(dates, engine='polars')
    ```

    ```{python}
    # Works on Pandas Series
    dates.to_series().week_of_month()
    ```

    ```{python}
    # Works on Pandas Series
    dates.to_series().week_of_month(engine='polars')
    ```

    """
    pass


def _week_of_month_pandas(idx: Union[pd.Series, pd.DatetimeIndex]) -> pd.Series:
    """
    The "week_of_month" function calculates the week number of a given date within its month.
    """
    pass


def _week_of_month_polars(idx: Union[pd.Series, pd.DatetimeIndex]) -> pd.Series:
    """
    The "week_of_month" function calculates the week number of a given date within its month.
    """
    pass


@pf.register_series_method
def is_holiday(
    idx: Union[str, datetime, List[Union[str, datetime]], pd.Series],
    country_name: str = "UnitedStates",
    country: str = None,
    engine: str = "pandas",
) -> pd.Series:
    """
    Check if a given list of dates are holidays for a specified country.

    Note: This function requires the `holidays` package to be installed.

    Parameters
    ----------
    idx : Union[str, datetime, List[Union[str, datetime]], pd.Series]
        The dates to check for holiday status.
    country_name (str, optional):
        The name of the country for which to check the holiday status. Defaults
        to 'UnitedStates' if not specified.
    country (str, optional):
        An alternative parameter to specify the country for holiday checking,
        overriding country_name.
    engine : str, optional
        The `engine` parameter is used to specify the engine to use for
        generating the boolean series. It can be either "pandas" or "polars".

        - The default value is "pandas".

        - When "polars", the function will internally use the `polars` library
          for generating a boolean of holidays or not holidays. This can be
          faster than using "pandas" for long series.

    Returns:
    -------
    pd.Series:
        Series containing True if the date is a holiday, False otherwise.

    Raises:
    -------
    ValueError:
        If the specified country is not found in the holidays package.

    Examples:
    --------
    ```{python}
    import polars as pl
    import pytimetk as tk

    tk.is_holiday('2023-01-01', country_name='UnitedStates')
    ```

    ```{python}
    # List of dates
    tk.is_holiday(['2023-01-01', '2023-01-02', '2023-01-03'], country_name='UnitedStates')
    ```

    ```{python}
    # Polars Series
    tk.is_holiday(pl.Series(['2023-01-01', '2023-01-02', '2023-01-03']), country_name='UnitedStates')
    ```
    """
    pass


def _is_holiday_pandas(
    idx: Union[str, datetime, List[Union[str, datetime]], pd.DatetimeIndex, pd.Series],
    country_name: str = "UnitedStates",
    country: str = None,
) -> pd.Series:
    # This function requires the holidays package to be installed
    pass


def _is_holiday_polars(
    idx: Union[str, datetime, List[Union[str, datetime]], pd.Series],
    country_name: str = "UnitedStates",
    country: str = None,
) -> pd.Series:
    # This function requires the holidays package to be installed
    pass


def is_datetime_string(x: Union[str, pd.Series, pd.DatetimeIndex]) -> bool:
    pass


def detect_timeseries_columns(
    data: pd.DataFrame, verbose: bool = False
) -> pd.DataFrame:
    pass


def has_timeseries_columns(data: pd.DataFrame, verbose: bool = False) -> bool:
    pass


def get_timeseries_colname(data: pd.DataFrame, verbose: bool = False) -> str:
    pass
