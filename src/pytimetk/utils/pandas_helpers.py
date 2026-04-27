import pandas as pd
import pandas_flavor as pf
import polars as pl
import re

from pytimetk.utils.pandas_flavor_compat import patch_pandas_flavor

patch_pandas_flavor()

from pytimetk.utils.checks import check_dataframe_or_groupby
from pytimetk.utils.dataframe_ops import resolve_pandas_groupby_frame

from typing import Union, List, Callable


@pf.register_dataframe_method
def glimpse(data: pd.DataFrame, max_width: int = 76, engine: str = "pandas") -> None:
    """
    Takes a pandas DataFrame and prints a summary of its dimensions, column
    names, data types, and the first few values of each column.

    Parameters
    ----------
    data : pd.DataFrame
        The `data` parameter is a pandas DataFrame that contains the data you
        want to glimpse at. It is the main input to the `glimpse` function.
    max_width : int, optional
        The `max_width` parameter is an optional parameter that specifies the
        maximum width of each line when printing the glimpse of the DataFrame.
        If not provided, the default value is set to 76.
    engine : str, optional
        The `engine` parameter is used to specify the engine to use for
        generating a glimpse. It can be either "pandas" or "polars".

        - The default value is "pandas".

        - When "polars", the function will internally use the `polars` library
          for generating the glimpse.

    Examples
    --------
    ```{python}
    import pytimetk as tk
    import pandas as pd

    df = tk.load_dataset('walmart_sales_weekly', parse_dates=['Date'])

    df.glimpse()
    ```

    """
    pass


def _glimpse_pandas(data: pd.DataFrame, max_width: int = 76) -> None:
    pass


def _glimpse_polars(df, max_width=76):
    def make_lalign_formatter(df, cols=None):
        pass
    pass


@pf.register_groupby_method
@pf.register_dataframe_method
def sort_dataframe(
    data: Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy],
    date_column: str,
    keep_grouped_df: bool = True,
) -> Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy]:
    """The function `sort_dataframe` sorts a DataFrame by a specified date column, handling both regular
    DataFrames and grouped DataFrames.

    Parameters
    ----------
    data : Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy]
        The `data` parameter in the `sort_dataframe` function can accept either a pandas DataFrame or a
        grouped DataFrame (DataFrameGroupBy object).
    date_column
        The `date_column` parameter in the `sort_dataframe` method is used to specify the column in the
        DataFrame by which the sorting will be performed. This column contains dates that will be used as
        the basis for sorting the DataFrame or DataFrameGroupBy object.
    keep_grouped_df
        If `True` and `data` is a grouped data frame, a grouped data frame will be returned. If `False`, an ungrouped data frame is returned.

    Returns
    -------
        The `sort_dataframe` function returns a sorted DataFrame based on the specified date column. If the
        input data is a regular DataFrame, it sorts the DataFrame by the specified date column. If the input
        data is a grouped DataFrame (DataFrameGroupBy object), it sorts the DataFrame by the group names and
        the specified date column. The function returns the sorted DataFrame.

    Examples
    --------
    ```{python}
    import pytimetk as tk
    import pandas as pd

    df = tk.load_dataset('walmart_sales_weekly', parse_dates=['Date'])

    df.sort_dataframe('Date')

    df.groupby('id').sort_dataframe('Date').obj

    df.groupby(['id', 'Store', 'Dept']).sort_dataframe('Date').obj
    ```

    """
    pass


@pf.register_dataframe_method
def drop_zero_variance(
    data: pd.DataFrame,
):
    """The function `drop_zero_variance` takes a pandas DataFrame as input and returns a new DataFrame with
    columns that have zero variance removed.

    Parameters
    ----------
    data : pd.DataFrame
        The `data` parameter is a pandas DataFrame or a pandas DataFrameGroupBy object. It represents the
    data that you want to filter out columns with zero variance from.

    Returns
    -------
    DataFrame:
        a filtered DataFrame with columns that have non-zero variance.

    """
    def all_values_same(series):
        pass
    pass


@pf.register_dataframe_method
def transform_columns(
    data: pd.DataFrame,
    columns: Union[str, List[str]],
    transform_func: Callable[[pd.Series], pd.Series],
):
    """The function `transform_columns` applies a user-provided function to specified columns in a pandas DataFrame.

    Parameters
    ----------
    data : pd.DataFrame
        The `data` parameter is a pandas DataFrame or a pandas DataFrameGroupBy object. It represents the
        data on which the transformation will be applied.
    columns : Union[str, List[str]]
        The `columns` parameter can be either a string or a list of strings. These strings represent the
        column names or regular expressions that will be matched against the column names in the DataFrame.
        If a column name matches any of the provided patterns, the transformation function will be applied to that column.
    transform_func : Callable[[pd.Series], pd.Series]
        A function that takes a pandas Series as input and returns a transformed pandas Series. This function
        will be applied to each column that matches the `columns` parameter.

    Returns
    -------
    DataFrame:
        A modified copy of the input DataFrame where the specified columns are transformed using the provided
        function.

    """
    pass


@pf.register_dataframe_method
def flatten_multiindex_column_names(data: pd.DataFrame, sep="_") -> pd.DataFrame:
    """Takes a DataFrame as input and flattens the column
    names if they are in a multi-index format.

    Parameters
    ----------
    data : pd.DataFrame
        The parameter "data" is expected to be a pandas DataFrame object.

    Returns
    -------
    pd.DataFrame
        The input data with flattened multiindex column names.

    Examples
    --------
    ```{python}
    import pandas as pd
    import pytimetk as tk

    date_rng = pd.date_range(start='2023-01-01', end='2023-01-03', freq='D')

    data = {
        'date': date_rng,
        ('values', 'value1'): [1, 4, 7],
        ('values', 'value2'): [2, 5, 8],
        ('metrics', 'metric1'): [3, 6, 9],
        ('metrics', 'metric2'): [3, 6, 9],
    }
    df = pd.DataFrame(data)

    df.flatten_multiindex_column_names()

    ```
    """
    pass


def pd_quantile(**kwargs):
    """Generates configuration for the rolling quantile function in Polars."""
    pass


def update_dict(d1, d2):
    """
    Update values in dictionary `d1` based on matching keys from dictionary `d2`.

    This function will only update the values of existing keys in `d1`.
    New keys present in `d2` but not in `d1` will be ignored.
    """
    pass
