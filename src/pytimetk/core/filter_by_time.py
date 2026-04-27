# Imports
import pandas as pd
import polars as pl
import pandas_flavor as pf
from typing import Union

from pytimetk.utils.checks import (
    check_dataframe_or_groupby,
    check_date_column,
)
from pytimetk.utils.datetime_helpers import parse_end_date
from pytimetk.utils.dataframe_ops import (
    convert_to_engine,
    normalize_engine,
    restore_output_type,
    resolve_pandas_groupby_frame,
)

try:  # Optional cudf dependency
    import cudf  # type: ignore
except ImportError:  # pragma: no cover - cudf optional
    cudf = None  # type: ignore


# Function ----
@pf.register_groupby_method
@pf.register_dataframe_method
def filter_by_time(
    data: Union[
        pd.DataFrame,
        pd.core.groupby.generic.DataFrameGroupBy,
        pl.DataFrame,
        pl.dataframe.group_by.GroupBy,
    ],
    date_column: str,
    start_date: str = "start",
    end_date: str = "end",
    engine: str = "pandas",
) -> Union[pd.DataFrame, pl.DataFrame]:
    """
    Filters a DataFrame or GroupBy object based on a specified date range.

    This function filters data in a pandas DataFrame or a pandas GroupBy object
    by a given date range. It supports various date formats and can handle both
    DataFrame and GroupBy objects.

    Parameters
    ----------
    data : DataFrame or GroupBy (pandas or polars)
        The data to be filtered. Supports both pandas and polars DataFrames / GroupBy
        objects. Grouped inputs are processed per group before the final result is returned.
    date_column : str
        The name of the column in `data` that contains date information.
        This column is used for filtering the data based on the date range.
    start_date : str
        The start date of the filtering range. The format of the date can be
        YYYY, YYYY-MM, YYYY-MM-DD, YYYY-MM-DD HH, YYYY-MM-DD HH:SS, or YYYY-MM-DD HH:MM:SS.
        Default: 'start', which will filter from the earliest date in the data.
    end_date : str
        The end date of the filtering range. It supports the same formats as
        `start_date`.
        Default: 'end', which will filter until the latest date in the data.
    engine : str, default = 'pandas'
        Computation engine. Use ``'pandas'``, ``'polars'``, or ``'cudf'``. The special value ``'auto'``
        infers the engine from the input data.

    Returns
    -------
    DataFrame
        Data containing rows within the specified date range. The concrete type matches the
        engine used.

    Raises
    ------
    ValueError
        If the provided date strings do not match any of the supported formats.

    Notes
    -----
    - The function uses pd.to_datetime to convert the start date
      (e.g. start_date = "2014" becomes "2014-01-01").
    - The function internally uses the `parse_end_date` function to convert the
      end dates (e.g. end_date = "2014" becomes "2014-12-31").


    Examples
    --------
    ```{python}
    import pytimetk as tk
    import pandas as pd
    import datetime

    m4_daily_df = tk.datasets.load_dataset('m4_daily', parse_dates = ['date'])

    ```

    ```{python}
    # Example 1 - Filter by date

    df_filtered = tk.filter_by_time(
        data        = m4_daily_df,
        date_column = 'date',
        start_date  = '2014-07-03',
        end_date    = '2014-07-10'
    )

    df_filtered

    ```

    ```{python}
    # Example 2 - Filter by month.
    # Note: This will filter by the first day of the month.

    df_filtered = tk.filter_by_time(
        data        = m4_daily_df,
        date_column = 'date',
        start_date  = '2014-07',
        end_date    = '2014-09'
    )

    df_filtered

    ```

    ```{python}
    # Example 3 - Filter by year.
    # Note: This will filter by the first day of the year.

    df_filtered = tk.filter_by_time(
        data        = m4_daily_df,
        date_column = 'date',
        start_date  = '2014',
        end_date    = '2014'
    )

    df_filtered

    ```

    ```{python}
    # Example 4 - Filter by day/hour/minute/second
    # Here we'll use an hourly dataset, however this will also work for minute/second data

    # Load data and format date column appropriately
    m4_hourly_df = tk.datasets.load_dataset('m4_hourly', parse_dates = ['date'])

    df_filtered = tk.filter_by_time(
        data        = m4_hourly_df,
        date_column = "date",
        start_date  = '2015-07-01 12:00:00',
        end_date    = '2015-07-01 20:00:00'
    )

    df_filtered
    ```

    ```{python}
    # Example 5 - Combine year/month/day/hour/minute/second filters
    df_filtered = tk.filter_by_time(
        data        = m4_hourly_df,
        date_column = "date",
        start_date  = '2015-07-01',
        end_date    = '2015-07-29'
    )

    df_filtered

    ```

    ```{python}
    # Example 7 - Filter using the polars engine and tk accessor
    import polars as pl


    pl_df = pl.from_pandas(m4_daily_df)

    df_filtered = (
        pl_df
            .tk.filter_by_time(
                date_column = 'date',
                start_date  = '2014-07-03',
                end_date    = '2014-07-10'
            )
    )

    df_filtered

    ```

    ```{python}
    # Example 6 - Filter a GroupBy object

    df_filtered = (
        m4_hourly_df
            .groupby('id')
            .filter_by_time(
                date_column = "date",
                start_date  = '2015-07-01 12:00:00',
                end_date    = '2015-07-01 20:00:00'
            )
    )

    df_filtered
    ```

    """
    pass


# Monkey Patch the Method to Pandas Grouby Objects
def _filter_by_time_pandas(
    data: Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy],
    date_column: str,
    start_date: str,
    end_date: str,
):
    pass


def _filter_by_time_polars(
    data: Union[pl.DataFrame, pl.dataframe.group_by.GroupBy],
    date_column: str,
    start_date: str,
    end_date: str,
) -> pl.DataFrame:
    pass


def _filter_by_time_cudf(
    data: Union["cudf.DataFrame", "cudf.core.groupby.groupby.DataFrameGroupBy"],
    date_column: str,
    start_date: str,
    end_date: str,
) -> "cudf.DataFrame":
    pass


# Utilities ----
