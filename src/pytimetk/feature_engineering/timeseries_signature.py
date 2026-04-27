# Dependencies
import pandas as pd
import numpy as np
import polars as pl
import pandas_flavor as pf
import warnings
from typing import Union

from pytimetk.utils.datetime_helpers import week_of_month
from pytimetk.utils.checks import (
    check_series_or_datetime,
    check_dataframe_or_groupby,
    check_date_column,
)
from pytimetk.utils.memory_helpers import reduce_memory_usage
from pytimetk.utils.dataframe_ops import (
    FrameConversion,
    convert_to_engine,
    normalize_engine,
    restore_output_type,
)


@pf.register_groupby_method
@pf.register_dataframe_method
def augment_timeseries_signature(
    data: Union[
        pd.DataFrame,
        pd.core.groupby.generic.DataFrameGroupBy,
        pl.DataFrame,
        pl.dataframe.group_by.GroupBy,
    ],
    date_column: str,
    reduce_memory: bool = False,
    engine: str = "pandas",
) -> Union[pd.DataFrame, pl.DataFrame]:
    """
    The function `augment_timeseries_signature` takes a DataFrame and a date
    column as input and returns the original DataFrame with the **29 different
    date and time based features** added as new columns with the feature name
    based on the date_column.

    Parameters
    ----------
    data : DataFrame or GroupBy (pandas or polars)
        Tabular time series data. Grouped inputs are processed per group before
        the signature columns are appended. Accepts both pandas and polars inputs.
    date_column : str
        The `date_column` parameter is a string that represents the name of the
        date column in the `data` DataFrame.
    reduce_memory : bool, optional
        The `reduce_memory` parameter is used to specify whether to reduce the memory usage of the DataFrame by converting int, float to smaller bytes and str to categorical data. This reduces memory for large data but may impact resolution of float and will change str to categorical. Default is False.
    engine : str, optional
        The `engine` parameter is used to specify the engine to use for
        augmenting datetime features. It can be either "pandas" or "polars".

        - The default value is "pandas".

        - When "polars", the function will internally use the `polars` library
          for feature generation. This is generally faster than using "pandas"
          for large datasets.

    Returns
    -------
    DataFrame
        Data with 29 datetime features appended. The return type matches the
        input backend.

    - _index_num: An int64 feature that captures the entire datetime as a numeric value to the second
    - _year: The year of the datetime
    - _year_iso: The iso year of the datetime
    - _yearstart: Logical (0,1) indicating if first day of year (defined by frequency)
    - _yearend: Logical (0,1) indicating if last day of year (defined by frequency)
    - _leapyear: Logical (0,1) indicating if the date belongs to a leap year
    - _half: Half year of the date: Jan-Jun = 1, July-Dec = 2
    - _quarter: Quarter of the date: Jan-Mar = 1, Apr-Jun = 2, Jul-Sep = 3, Oct-Dec = 4
    - _quarteryear: Quarter of the date + relative year
    - _quarterstart: Logical (0,1) indicating if first day of quarter (defined by frequency)
    - _quarterend: Logical (0,1) indicating if last day of quarter (defined by frequency)
    - _month: The month of the datetime
    - _month_lbl: The month label of the datetime
    - _monthstart: Logical (0,1) indicating if first day of month (defined by frequency)
    - _monthend: Logical (0,1) indicating if last day of month (defined by frequency)
    - _yweek: The week ordinal of the year
    - _mweek: The week ordinal of the month
    - _wday: The number of the day of the week with Monday=1, Sunday=6
    - _wday_lbl: The day of the week label
    - _mday: The day of the datetime
    - _qday: The days of the relative quarter
    - _yday: The ordinal day of year
    - _weekend: Logical (0,1) indicating if the day is a weekend
    - _hour: The hour of the datetime
    - _minute: The minutes of the datetime
    - _second: The seconds of the datetime
    - _msecond: The microseconds of the datetime
    - _nsecond: The nanoseconds of the datetime
    - _am_pm: Half of the day, AM = ante meridiem, PM = post meridiem

    Examples
    --------
    ```{python}
    import pandas as pd
    import pytimetk as tk

    df = tk.load_dataset('bike_sales_sample', parse_dates = ['order_date'])
    ```

    ```{python}
    # Adds 29 new time series features as columns to the original DataFrame (pandas engine)
    (
        df
            .augment_timeseries_signature(date_column='order_date', engine ='pandas')
            .glimpse()
    )
    ```

    ```{python}
    # Adds 29 new time series features as columns to the original DataFrame (polars engine)
    (
        df
            .augment_timeseries_signature(date_column='order_date', engine ='polars')
            .glimpse()
    )
    ```

    ```{python}
    # Polars DataFrame using the tk accessor
    import polars as pl


    pl_df = pl.from_pandas(df)

    pl_df.tk.augment_timeseries_signature(date_column='order_date')
    ```
    """
    pass


@pf.register_series_method
def get_timeseries_signature(
    idx: Union[pd.Series, pd.DatetimeIndex],
    reduce_memory: bool = False,
    engine: str = "auto",
) -> pd.DataFrame:
    """
    Convert a timestamp to a set of 29 time series features.

    The function `get_timeseries_signature` engineers **29 different date and
    time based features** from a single datetime index `idx`:

    Parameters
    ----------
    idx : pd.DataFrame
        The `idx` parameter is a pandas Series of DatetimeIndex.
    reduce_memory : bool, optional
        The `reduce_memory` parameter is used to specify whether to reduce the memory usage of the DataFrame by converting int, float to smaller bytes and str to categorical data. This reduces memory for large data but may impact resolution of float and will change str to categorical. Default is False.
    engine : str, optional
        The `engine` parameter is used to specify the engine to use for
        augmenting datetime features. It can be either "pandas" or "polars".

        - The default value is "pandas".

        - When "polars", the function will internally use the `polars` library
          for feature generation. This is generally faster than using "pandas"
          for large datasets.

    Returns
    -------
    pd.DataFrame
        A Pandas DataFrame with 29 datetime features added to it.

    - _index_num: An int64 feature that captures the entire datetime as a numeric value to the second
    - _year: The year of the datetime
    - _year_iso: The iso year of the datetime
    - _yearstart: Logical (0,1) indicating if first day of year (defined by frequency)
    - _yearend: Logical (0,1) indicating if last day of year (defined by frequency)
    - _leapyear: Logical (0,1) indicating if the date belongs to a leap year
    - _half: Half year of the date: Jan-Jun = 1, July-Dec = 2
    - _quarter: Quarter of the date: Jan-Mar = 1, Apr-Jun = 2, Jul-Sep = 3, Oct-Dec = 4
    - _quarteryear: Quarter of the date + relative year
    - _quarterstart: Logical (0,1) indicating if first day of quarter (defined by frequency)
    - _quarterend: Logical (0,1) indicating if last day of quarter (defined by frequency)
    - _month: The month of the datetime
    - _month_lbl: The month label of the datetime
    - _monthstart: Logical (0,1) indicating if first day of month (defined by frequency)
    - _monthend: Logical (0,1) indicating if last day of month (defined by frequency)
    - _yweek: The week ordinal of the year
    - _mweek: The week ordinal of the month
    - _wday: The number of the day of the week with Monday=1, Sunday=6
    - _wday_lbl: The day of the week label
    - _mday: The day of the datetime
    - _qday: The days of the relative quarter
    - _yday: The ordinal day of year
    - _weekend: Logical (0,1) indicating if the day is a weekend
    - _hour: The hour of the datetime
    - _minute: The minutes of the datetime
    - _second: The seconds of the datetime
    - _msecond: The microseconds of the datetime
    - _nsecond: The nanoseconds of the datetime
    - _am_pm: Half of the day, AM = ante meridiem, PM = post meridiem

    Examples
    --------
    ```{python}
    import pandas as pd
    import pytimetk as tk

    dates = pd.date_range(start = '2019-01', end = '2019-03', freq = 'D')
    ```

    ```{python}
    # Makes 29 new time series features from the dates
    tk.get_timeseries_signature(dates, engine='pandas').glimpse()
    ```

    ```{python}
    tk.get_timeseries_signature(dates, engine='polars').glimpse()
    ```
    ```{python}
    pd.Series(dates, name = "date").get_timeseries_signature(engine='pandas').glimpse()
    ```

    ```{python}
    pd.Series(dates, name = "date").get_timeseries_signature(engine='polars').glimpse()
    ```
    """
    pass


# Monkey patch the method to Pandas Series objects
pd.Series.get_timeseries_signature = get_timeseries_signature


# UTILITIES
# ---------


def _pandas_timeseries_signature(data: pd.DataFrame, date_column: str) -> pd.DataFrame:
    pass
