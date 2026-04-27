import pandas as pd
import pandas_flavor as pf
import numpy as np
import polars as pl

from typing import Union

from pytimetk.utils.checks import check_series_or_datetime, check_series_polars
from pytimetk.utils.datetime_helpers import floor_date


# to convert irregular frequency into its regular counterpart
IRREGULAR_TO_REGULAR = {
    "A-DEC": "Y",
    "Q-DEC": "Q",
    "W-SUN": "W",
    "B": "D",
    "BM": "M",
    "BME": "M",
    "BQ": "Q",
    "BQE": "Q",
    "BA": "A",
    "BYE": "Y",
    "BY": "Y",
    "BMS": "MS",
    "BQS": "QS",
    "BYS": "YS",
    "BAS": "AS",
}


def get_unit_and_scale(freq_median_seconds, engine="pandas"):
    # Use time series frequency table
    def lookup_freq(unit, type="freq"):
        pass
    pass


def _get_frequency_summary_polars(idx: pl.Series, force_regular: bool = False):
    pass


def _get_frequency_summary_pandas(
    idx: Union[pd.Series, pd.DatetimeIndex], force_regular: bool = False
):
    # common checks
    pass


def get_frequency_summary(
    idx: Union[pd.Series, pd.DatetimeIndex],
    force_regular: bool = False,
    engine: str = "pandas",
):
    """
    More robust version of pandas inferred frequency.

    Parameters
    ----------
    idx : pd.Series or pd.DateTimeIndex
        The `idx` parameter is either a `pd.Series` or a `pd.DateTimeIndex`. It
        represents the index of a pandas DataFrame or Series, which contains
        datetime values.
    force_regular : bool, optional
        The `force_regular` parameter is a boolean flag that determines whether
        to force the frequency to be regular. If set to `True`, the function
        will convert irregular frequencies to their regular counterparts. For
        example, if the inferred frequency is 'B' (business days), it will be
        converted to 'D' (calendar days). The default value is `False`.

    Returns
    -------
    pd.DataFrame
        A pandas DataFrame with the following columns:
        - `freq_inferred_unit`: The inferred frequency of the time series from `pandas`.
        - `freq_median_timedelta`: The median time difference between consecutive
           observations in the time series.
        - `freq_median_scale`: The median time difference between consecutive
           observations in the time series, scaled to a common unit.
        - `freq_median_unit`: The unit of the median time difference between
           consecutive observations in the time series.

    Examples
    --------
    ```{python}
    import pytimetk as tk
    import pandas as pd

    dates = pd.date_range(start = '2020-01-01', end = '2020-01-10', freq = 'D')

    tk.get_frequency_summary(dates)
    ```

    ```{python}
    # pandas inferred frequency fails
    dates = pd.to_datetime(["2021-01-01", "2021-02-01"])

    # Returns None
    dates.inferred_freq == None

    # Returns '1MS'
    tk.get_frequency_summary(dates)

    ```
    ```{python}
    # Polars Series example
    import polars as pl
    from datetime import datetime, timezone

    idx = pl.Series("date", pl.date_range(start=datetime(2020, 1, 1, tzinfo=timezone.utc), end=datetime(2020, 1, 10, tzinfo=timezone.utc), interval="1d", eager=True))

    tk.get_frequency_summary(idx, engine="polars")
    ```
    """
    pass


@pf.register_series_method
def get_frequency(
    idx: Union[pd.Series, pd.DatetimeIndex],
    force_regular: bool = False,
    numeric: bool = False,
) -> str:
    """
    Get the frequency of a pandas Series or DatetimeIndex.

    The function `get_frequency` first attempts to get a pandas inferred
    frequency. If the inferred frequency is None, it will attempt calculate the
    frequency manually. If the frequency cannot be determined, the function will
    raise a ValueError.

    Parameters
    ----------
    idx : pd.Series or pd.DatetimeIndex
        The `idx` parameter can be either a `pd.Series` or a `pd.DatetimeIndex`.
        It represents the index or the time series data for which we want to
        determine the frequency.
    force_regular : bool, optional
        The `force_regular` parameter is a boolean flag that determines whether
        to force the frequency to be regular. If set to `True`, the function
        will convert irregular frequencies to their regular counterparts. For
        example, if the inferred frequency is 'B' (business days), it will be
        converted to 'D' (calendar days). The default value is `False`.
    numeric : bool, optional
        The `numeric` parameter is a boolean flag that indicates whether a
        numeric value for the median timestamps per pandas frequency or the
        pandas string frequency alias.

    Returns
    -------
    str
        The frequency of the given pandas series or datetime index.

    """
    pass


def timeseries_unit_frequency_table(
    wide_format: bool = False, engine: str = "pandas"
) -> pd.DataFrame:
    """
    The function `timeseries_unit_frequency_table` returns a pandas DataFrame
    with units of time and their corresponding frequencies in seconds.

    Parameters
    ----------
    wide_format : bool, optional
        The wide_format parameter determines the format of the output table. If
        wide_format is set to True, the table will be transposed.
    engine : str, optional
        The `engine` parameter is used to specify the engine to use for
        generating the timeseries unit frequency table. It can be either "pandas"
        or "polars".

            - The default value is "pandas".

            - When "polars", the function will internally use the `polars` library
            for generating a timeseries unit frequency table.

    Returns
    -------
    pd.DataFrame
        a pandas DataFrame that contains two columns: "unit" and "freq". The
        "unit" column contains the units of time (seconds, minutes, hours, etc.),
        and the "freq" column contains the corresponding frequencies in seconds
        for each unit.


    Examples
    --------
    ```{python}
    import pytimetk as tk

    tk.timeseries_unit_frequency_table()
    ```

    ```{python}
    # Polars engine example
    import pytimetk as tk

    tk.timeseries_unit_frequency_table(engine='polars')
    ```

    """
    pass


def _timeseries_unit_frequency_table_pandas(wide_format: bool = False) -> pd.DataFrame:
    pass


def _timeseries_unit_frequency_table_polars(wide_format: bool = False) -> pd.DataFrame:
    pass


def time_scale_template(
    wide_format: bool = False, engine: str = "pandas"
) -> pd.DataFrame:
    """
    The function `time_scale_template` returns a table with time scale
    information in either wide or long format.

    Parameters
    -------
    wide_format : bool, optional
        The wide_format parameter determines the format of the output table. If
        wide_format is set to True, the table will be transposed.
    engine : str, optional
        The `engine` parameter is used to specify the engine to use for
        generating a date summary. It can be either "pandas" or "polars".

        - The default value is "pandas".

        - When "polars", the function will internally use the `polars` library
          for generating the time scale information.

    Examples
    --------
    ```{python}
    import pytimetk as tk

    tk.time_scale_template()
    ```

    ```{python}
    # Polars engine example
    import pytimetk as tk

    tk.time_scale_template(engine='polars')
    ```

    """
    pass


def _time_scale_template_pandas(wide_format: bool = False):
    pass


def _time_scale_template_polars(wide_format: bool = False):
    pass


@pf.register_series_method
def get_seasonal_frequency(
    idx: Union[pd.Series, pd.DatetimeIndex],
    force_regular: bool = False,
    numeric: bool = False,
    engine: str = "pandas",
):
    """
    The `get_seasonal_frequency` function returns the seasonal period of a given
    time series or datetime index.

    Parameters
    ----------
    idx : Union[pd.Series, pd.DatetimeIndex]
        The `idx` parameter can be either a pandas Series or a pandas
        DatetimeIndex. It represents the time index for which you want to
        calculate the seasonal frequency.
    force_regular : bool, optional
        force_regular is a boolean parameter that determines whether to force
        the frequency to be regular. If set to True, the function will try to
        find a regular frequency even if the data is irregular. If set to False,
        the function will return the actual frequency of the data.
    numeric : bool, optional
        The `numeric` parameter is a boolean flag that determines whether the
        output should be in numeric format or a string Pandas Frequency Alias.
        If `numeric` is set to `True`, the output will be a numeric representation
        of the seasonal period. If `numeric` is set to `False` (default), the
        output will
    engine : str, optional
        The `engine` parameter is used to specify the engine to use for
        generating a date summary. It can be either "pandas" or "polars".

        - The default value is "pandas".

        - When "polars", the function will internally use the `polars` library
          for generating the time scale information.

    Returns
    -------
        The function `get_seasonal_frequency` returns the seasonal period based
        on the input index. If the index is a `pd.DatetimeIndex`, it is converted
        to a `pd.Series` with the name "idx". The function then calculates the
        summary frequency of the index using the `get_frequency_summary` function.
        It determines the scale and unit of the frequency and adjusts the unit if
        the scale is

    Examples
    --------
    ```{python}
    import pytimetk as tk
    import pandas as pd

    dates = pd.date_range(start='2021-01-01', end='2024-01-01', freq='MS')

    tk.get_seasonal_frequency(dates)
    ```

    ```{python}
    # Polars Series example
    import polars as pl
    from datetime import datetime, timezone

    idx = pl.Series("date", pl.date_range(start=datetime(2021, 1, 1, tzinfo=timezone.utc), end=datetime(2024, 1, 1, tzinfo=timezone.utc), interval="1mo", eager=True))

    tk.get_seasonal_frequency(idx, engine='polars')
    ```
    """
    def _lookup_seasonal_period(unit):
        pass
    pass


@pf.register_series_method
def get_trend_frequency(
    idx: Union[pd.Series, pd.DatetimeIndex],
    force_regular: bool = False,
    numeric: bool = False,
    engine: str = "pandas",
) -> str:
    """
    The `get_trend_frequency` function returns the trend period of a given time
    series or datetime index.

    Parameters
    ----------
    idx : Union[pd.Series, pd.DatetimeIndex]
        The `idx` parameter can be either a pandas Series or a pandas
        DatetimeIndex. It represents the time index for which you want to
        calculate the trend frequency.
    force_regular : bool, optional
        force_regular is a boolean parameter that determines whether to force the
        frequency to be regular. If set to True, the function will try to find a
        regular frequency even if the data is irregular. If set to False, the
        function will return the actual frequency of the data.
    numeric : bool, optional
        The `numeric` parameter is a boolean flag that determines whether the
        output should be in numeric format or a string Pandas Frequency Alias.
        If `numeric` is set to `True`, the output will be a numeric representation
        of the trend period. If `numeric` is set to `False` (default), the output
        will
    engine : str, optional
        The `engine` parameter is used to specify the engine to use for
        generating a date summary. It can be either "pandas" or "polars".

        - The default value is "pandas".

        - When "polars", the function will internally use the `polars` library
          for generating the time scale information.

    Returns
    -------
        The function `get_trend_frequency` returns the trend period based on the
        input index. If the index is a `pd.DatetimeIndex`, it is converted to a
        `pd.Series` with the name "idx". The function then calculates the summary
        frequency of the index using the `get_frequency_summary` function. It
        determines the scale and unit of the frequency and adjusts the unit if
        the scale is

    Examples
    --------
    ```{python}
    import pytimetk as tk
    import pandas as pd

    dates = pd.date_range(start='2021-01-01', end='2024-01-01', freq='MS')

    tk.get_trend_frequency(dates)
    ```

    ```{python}
    # Polars Series example
    import polars as pl
    from datetime import datetime, timezone

    idx = pl.Series("date", pl.date_range(start=datetime(2021, 1, 1, tzinfo=timezone.utc), end=datetime(2024, 1, 1, tzinfo=timezone.utc), interval="1mo", eager=True))

    tk.get_trend_frequency(idx, engine='polars')
    ```
    """
    def _lookup_trend_period(unit):
        pass
    pass


def _get_median_timestamps(idx, period):
    pass


# UTILITIES ---------------------------------------------------------------


def _get_manual_frequency(idx: Union[pd.Series, pd.DatetimeIndex]) -> str:
    """
    This is an internal function and not meant to be called directly.

    Parameters
    ----------
    idx : Union[pd.Series, pd.DatetimeIndex]
        The `idx` parameter can be either a pandas Series or a pandas DatetimeIndex.

    Returns
    -------
        a string representing the frequency alias.

    """
    pass


def _get_pandas_frequency(
    idx: Union[pd.Series, pd.DatetimeIndex], force_regular: bool = False
) -> str:
    """
    This is an internal function and not meant to be called directly.

    Parameters
    ----------
    idx : pd.Series or pd.DatetimeIndex
        The `idx` parameter can be either a `pd.Series` or a `pd.DatetimeIndex`.
        It represents the index or the time series data for which we want to
        determine the frequency.
    force_regular : bool, optional
        The `force_regular` parameter is a boolean flag that determines whether
        to force the frequency to be regular. If set to `True`, the function will
        convert irregular frequencies to their regular counterparts. For example,
        if the inferred frequency is 'B' (business days), it will be converted
        to 'D' (calendar days). The default value is `False`.

    Returns
    -------
    str
        The frequency of the given pandas series or datetime index.

    """
    pass
