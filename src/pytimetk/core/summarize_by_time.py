import pandas as pd
import pandas_flavor as pf
import polars as pl

from typing import Union, Callable, Tuple, List, Sequence
import re
import warnings
from itertools import cycle

from pytimetk.utils.pandas_helpers import flatten_multiindex_column_names

from pytimetk.utils.checks import (
    check_dataframe_or_groupby,
    check_date_column,
    check_value_column,
)

from pytimetk.utils.dataframe_ops import (
    FrameConversion,
    convert_to_engine,
    normalize_engine,
    restore_output_type,
    resolve_pandas_groupby_frame,
)
from pytimetk.utils.selection import ColumnSelector, resolve_column_selection
from pytimetk.utils.datetime_helpers import normalize_frequency_alias

try:  # Optional cudf dependency
    import cudf  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    cudf = None  # type: ignore

# FUNCTIONS -------------------------------------------------------------------


@pf.register_groupby_method
@pf.register_dataframe_method
def summarize_by_time(
    data: Union[
        pd.DataFrame,
        pd.core.groupby.generic.DataFrameGroupBy,
        pl.DataFrame,
        pl.dataframe.group_by.GroupBy,
    ],
    date_column: Union[str, ColumnSelector],
    value_column: Union[str, ColumnSelector, Sequence[Union[str, ColumnSelector]]],
    freq: str = "D",
    agg_func: Union[str, list, Tuple[str, Callable]] = "sum",
    wide_format: bool = False,
    fillna: int = 0,
    engine: str = "pandas",
):
    """
    Summarize a DataFrame or GroupBy object by time.

    The `summarize_by_time` function aggregates data by a specified time period
    and one or more numeric columns, allowing for grouping and customization of
    the time-based aggregation.

    Parameters
    ----------
    data : pd.DataFrame or pd.core.groupby.generic.DataFrameGroupBy
        A pandas DataFrame or a pandas GroupBy object. This is the data that you
        want to summarize by time.
    date_column : str or ColumnSelector
        The column containing the timestamps to aggregate by (selector-friendly).
    value_column : str, ColumnSelector, or list
        The `value_column` parameter is the name of one or more columns in the
        DataFrame that you want to aggregate by. It can be either a string
        representing a single column name, or a list of strings representing
        multiple column names.
    freq : str, optional
        The `freq` parameter specifies the frequency at which the data should be
        aggregated. It accepts a string representing a pandas frequency offset,
        such as "D" for daily or "MS" for month start. The default value is "D",
        which means the data will be aggregated on a daily basis. Some common
        frequency aliases include:

        - S: secondly frequency
        - min: minute frequency
        - H: hourly frequency
        - D: daily frequency
        - W: weekly frequency
        - M: month end frequency
        - MS: month start frequency
        - Q: quarter end frequency
        - QS: quarter start frequency
        - Y: year end frequency
        - YS: year start frequency

    agg_func : list, optional
        The `agg_func` parameter is used to specify one or more aggregating
        functions to apply to the value column(s) during the summarization
        process. It can be a single function or a list of functions. The default
        value is `"sum"`, which represents the sum function. Some common
        aggregating functions include:

        - "sum": Sum of values
        - "mean": Mean of values
        - "median": Median of values
        - "min": Minimum of values
        - "max": Maximum of values
        - "std": Standard deviation of values
        - "var": Variance of values
        - "first": First value in group
        - "last": Last value in group
        - "count": Count of values
        - "nunique": Number of unique values
        - "corr": Correlation between values

        Pandas Engine Only:
        Custom `lambda` aggregating functions can be used too. Here are several
        common examples:

        - ("q25", lambda x: x.quantile(0.25)): 25th percentile of values
        - ("q75", lambda x: x.quantile(0.75)): 75th percentile of values
        - ("iqr", lambda x: x.quantile(0.75) - x.quantile(0.25)): Interquartile range of values
        - ("range", lambda x: x.max() - x.min()): Range of values

    wide_format : bool, optional
        A boolean parameter that determines whether the output should be in
        "wide" or "long" format. If set to `True`, the output will be in wide
        format, where each group is represented by a separate column. If set to
        False, the output will be in long format, where each group is represented
        by a separate row. The default value is `False`.
    fillna : int, optional
        The `fillna` parameter is used to specify the value to fill missing data
        with. By default, it is set to 0. If you want to keep missing values as
        NaN, you can use `np.nan` as the value for `fillna`.
    engine : str, optional
        The `engine` parameter is used to specify the engine to use for
        summarizing the data. It can be "pandas", "polars", or "cudf".

        - The default value is "pandas".

        - When "polars", the function will internally use the `polars` library
          for summarizing the data. This can be faster than using "pandas" for
          large datasets.

    Returns
    -------
    pd.DataFrame
        A Pandas DataFrame that is summarized by time.

    Examples
    --------
    ```{python}
    import pytimetk as tk
    import pandas as pd

    df = tk.load_dataset('bike_sales_sample', parse_dates = ['order_date'])

    df
    ```

    ```{python}
    # Example 1 - Summarize by time with a DataFrame object, pandas engine
    (
        df
            .summarize_by_time(
                date_column  = 'order_date',
                value_column = 'total_price',
                freq         = "MS",
                agg_func     = ['mean', 'sum'],
                engine       = 'pandas'
            )
    )
    ```

    ```{python}
    # Example 2 - Summarize by time with a GroupBy object (Wide Format), polars engine
    (
        df
            .groupby(['category_1', 'frame_material'])
            .summarize_by_time(
                date_column  = 'order_date',
                value_column = ['total_price', 'quantity'],
                freq         = 'MS',
                agg_func     = 'sum',
                wide_format  = True,
                engine       = 'polars'
            )
    )
    ```

    ```{python}
    # Example 2b - Summarize by time on a polars DataFrame using the tk accessor
    import polars as pl


    pl_df = pl.from_pandas(df)

    (
        pl_df
            .tk.summarize_by_time(
                date_column='order_date',
                value_column='total_price',
                freq='MS',
                agg_func='sum',
            )
    )
    ```

    ```{python}
    # Example 3 - Summarize by time with a GroupBy object (Wide Format)
    (
        df
            .groupby('category_1')
            .summarize_by_time(
                date_column  = 'order_date',
                value_column = 'total_price',
                freq         = 'MS',
                agg_func     = 'sum',
                wide_format  = True,
                engine       = 'pandas'
            )
    )
    ```

    ```{python}
    # Example 4 - Summarize by time with a GroupBy object and multiple value columns and summaries (Wide Format)
    # Note - This example only works with the pandas engine
    (
        df
            .groupby('category_1')
            .summarize_by_time(
                date_column  = 'order_date',
                value_column = ['total_price', 'quantity'],
                freq         = 'MS',
                agg_func     = [
                    'sum',
                    'mean',
                    ('q25', lambda x: x.quantile(0.25)),
                    ('q75', lambda x: x.quantile(0.75))
                ],
                wide_format  = False,
                engine       = 'pandas'
            )
    )
    ```
    """
    def _resolve_single(selector, label):
        pass
    def _resolve_multi(selector, label):
        pass
    pass


def _summarize_by_time_pandas(
    data: Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy],
    date_column: str,
    value_column: Union[str, list],
    freq: str = "D",
    agg_func: Union[str, list, Tuple[str, Callable]] = "sum",
    wide_format: bool = False,
    fillna: int = 0,
) -> pd.DataFrame:
    pass
 

def _summarize_by_time_cudf(
    prepared: Union["cudf.DataFrame", "cudf.core.groupby.groupby.DataFrameGroupBy"],
    date_column: str,
    value_column: Union[str, List[str]],
    freq: str,
    agg_funcs: List[str],
    fillna: int,
    conversion: FrameConversion,
) -> "cudf.DataFrame":
    def _flatten_columns(frame: "cudf.DataFrame") -> "cudf.DataFrame":
        pass
    pass


def _summarize_by_time_polars(
    prepared: Union[pl.DataFrame, pl.dataframe.group_by.GroupBy],
    date_column: str,
    value_column: Union[str, List[str]],
    freq: str,
    agg_func: Union[str, List[str]],
    wide_format: bool,
    fillna: int,
    conversion: FrameConversion,
) -> pl.DataFrame:
    pass


def _agg_contains_custom(agg_spec: Union[str, List, Tuple]) -> bool:
    pass


def _agg_collect_strings(agg_spec: Union[str, List]) -> List[str]:
    pass
def _resolve_selector_frame(
    data: Union[
        pd.DataFrame,
        pd.core.groupby.generic.DataFrameGroupBy,
        pl.DataFrame,
        pl.dataframe.group_by.GroupBy,
        "cudf.DataFrame",
    ],
) -> pd.DataFrame:
    pass
