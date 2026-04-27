import pandas as pd
import polars as pl
from datetime import datetime
import pandas_flavor as pf

from typing import List, Sequence, Union

import holidays


def _coerce_to_timestamp(
    value: Union[str, datetime, pd.Timestamp, pd.DatetimeIndex],
    pick: str,
) -> pd.Timestamp:
    pass


def _build_holiday_filter(
    dates: pd.DatetimeIndex,
    remove_holidays: bool,
    country: Union[str, None],
) -> Sequence[pd.Timestamp]:
    pass


def _make_sequence(
    start_date: Union[str, datetime, pd.DatetimeIndex],
    end_date: Union[str, datetime, pd.DatetimeIndex],
    allowed_weekdays: List[int],
    label: str,
    remove_holidays: bool,
    country: Union[str, None],
    engine: str,
) -> Union[pd.Series, pl.Series]:
    pass


@pf.register_series_method
def make_weekday_sequence(
    start_date: Union[str, datetime, pd.DatetimeIndex],
    end_date: Union[str, datetime, pd.DatetimeIndex],
    sunday_to_thursday: bool = False,
    remove_holidays: bool = False,
    country: str = None,
    engine: str = "pandas",
) -> Union[pd.Series, pl.Series]:
    """
    Generate a sequence of weekday dates within a specified date range,
    optionally excluding weekends and holidays.

    Parameters
    ----------
    start_date : str or datetime or pd.DatetimeIndex
        The start date of the date range.
    end_date : str or datetime or pd.DatetimeIndex
        The end date of the date range.
    sunday_to_thursday : bool, optional
        If True, generates a sequence with Sunday to Thursday weekdays (excluding
        Friday and Saturday). If False (default), generates a sequence with
        Monday to Friday weekdays.
    remove_holidays : bool, optional
        If True, excludes holidays (based on the specified country) from the
        generated sequence.
        If False (default), includes holidays in the sequence.
    country (str, optional):
        The name of the country for which to generate holiday-specific sequences.
        Defaults to None, which uses the United States as the default country.
    engine : str, optional
        The `engine` parameter is used to specify the engine to use for
        generating a weekday series. It can be either "pandas" or "polars".

        - The default value is "pandas".

        - When "polars", the function will internally use the `polars` library
          for generating a weekday series. This can be faster than using
          "pandas" for large datasets.

    Returns
    -------
    Series
        A Series containing the generated weekday dates. The concrete type
        matches the requested engine.

    Examples
    --------
    ```{python}
    import pandas as pd
    import pytimetk as tk

    # United States has Monday to Friday as weekdays (excluding Saturday and
    # Sunday and holidays)
    tk.make_weekday_sequence("2023-01-01", "2023-01-15",
                              sunday_to_thursday = False,
                              remove_holidays    = True,
                              country            = 'UnitedStates',
                              engine             = 'pandas')
    ```

    ```{python}
    # Israel has Sunday to Thursday as weekdays (excluding Friday and Saturday
    # and Israel holidays)
    tk.make_weekday_sequence("2023-01-01", "2023-01-15",
                              sunday_to_thursday = True,
                              remove_holidays    = True,
                              country            = 'Israel',
                              engine             = 'pandas')
    ```

    ```{python}
    # Israel has Sunday to Thursday as weekdays (excluding Friday and Saturday
    # and Israel holidays)
    tk.make_weekday_sequence("2023-01-01", "2023-01-15",
                              sunday_to_thursday = True,
                              remove_holidays    = True,
                              country            = 'Israel',
                              engine             = 'polars')
    ```
    """
    pass


@pf.register_series_method
def make_weekend_sequence(
    start_date: Union[str, datetime, pd.DatetimeIndex],
    end_date: Union[str, datetime, pd.DatetimeIndex],
    friday_saturday: bool = False,
    remove_holidays: bool = False,
    country: str = None,
    engine: str = "pandas",
) -> Union[pd.Series, pl.Series]:
    """
    Generate a sequence of weekend dates within a specified date range,
    optionally excluding holidays.

    Parameters
    ----------
    start_date : str or datetime or pd.DatetimeIndex
        The start date of the date range.
    end_date : str or datetime or pd.DatetimeIndex
        The end date of the date range.
    friday_saturday (bool, optional):
        If True, generates a sequence with Friday and Saturday as weekends. If
        False (default), generates a sequence with Saturday and Sunday as
        weekends.
    remove_holidays : bool, optional
        If True, excludes holidays (based on the specified country) from the
        generated sequence.
        If False (default), includes holidays in the sequence.
    country (str, optional):
        The name of the country for which to generate holiday-specific sequences.
        Defaults to None, which uses the United States as the default country.
    engine : str, optional
        The `engine` parameter is used to specify the engine to use for
        generating a weekend series. It can be either "pandas" or "polars".

        - The default value is "pandas".

        - When "polars", the function will internally use the `polars` library
          for generating a weekend series. This can be faster than using
          "pandas" for large datasets.

    Returns
    -------
    Series
        A Series containing the generated weekend dates. The concrete type
        matches the requested engine.

    Examples
    --------
    ```{python}
    import pandas as pd
    import pytimetk as tk

    # United States has Saturday and Sunday as weekends
    tk.make_weekend_sequence("2023-01-01", "2023-01-31",
                             friday_saturday = False,
                             remove_holidays = True,
                             country         = 'UnitedStates',
                             engine          = 'pandas')
    ```

    ```{python}
    # Saudi Arabia has Friday and Saturday as weekends
    tk.make_weekend_sequence("2023-01-01", "2023-01-31",
                             friday_saturday = True,
                             remove_holidays = True,
                             country         = 'SaudiArabia',
                             engine          = 'pandas')
    ```

    ```{python}
    # Saudi Arabia has Friday and Saturday as weekends (polars engine)
    tk.make_weekend_sequence("2023-01-01", "2023-01-31",
                             friday_saturday = True,
                             remove_holidays = True,
                             country         = 'SaudiArabia',
                             engine          = 'polars')
    ```
    """
    pass
