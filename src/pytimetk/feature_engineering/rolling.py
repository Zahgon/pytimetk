import pandas as pd
import polars as pl
import pandas_flavor as pf
import inspect
import warnings

from typing import Callable, List, Optional, Sequence, Tuple, Union

try:  # Optional cudf dependency for GPU acceleration
    import cudf  # type: ignore
    from cudf.core.groupby.groupby import DataFrameGroupBy as CudfDataFrameGroupBy
except ImportError:  # pragma: no cover - cudf optional
    cudf = None  # type: ignore
    CudfDataFrameGroupBy = None  # type: ignore

from functools import partial

from pytimetk._polars_compat import ensure_polars_rolling_kwargs
from pytimetk.utils.checks import (
    check_dataframe_or_groupby,
    check_date_column,
    check_value_column,
)
from pytimetk.utils.parallel_helpers import conditional_tqdm, get_threads
from pytimetk.utils.ray_helpers import run_ray_tasks
from pytimetk.utils.polars_helpers import update_dict
from pytimetk.utils.memory_helpers import reduce_memory_usage
from pytimetk.utils.pandas_helpers import sort_dataframe
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


@pf.register_groupby_method
@pf.register_dataframe_method
def augment_rolling(
    data: Union[
        pd.DataFrame,
        pd.core.groupby.generic.DataFrameGroupBy,
        pl.DataFrame,
        pl.dataframe.group_by.GroupBy,
        "cudf.DataFrame",
        "cudf.core.groupby.groupby.DataFrameGroupBy",
    ],
    date_column: str,
    value_column: Union[str, List[str]],
    window_func: Union[
        str, List[Union[str, Tuple[str, Callable]]], Tuple[str, Callable]
    ] = "mean",
    window: Union[int, Tuple[int, int], List[int]] = 2,
    min_periods: Optional[int] = None,
    engine: Optional[str] = "auto",
    center: bool = False,
    threads: int = 1,
    show_progress: bool = True,
    reduce_memory: bool = False,
    **kwargs,
) -> Union[pd.DataFrame, pl.DataFrame]:
    """
    Apply one or more Series-based rolling functions and window sizes to one or more columns of a DataFrame.

    Parameters
    ----------
    data : Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy]
        Input data to be processed. Can be a Pandas DataFrame or a GroupBy
        object.
    date_column : str
        Name of the datetime column. Data is sorted by this column within each
        group.
    value_column : Union[str, list]
        Column(s) to which the rolling window functions should be applied. Can
        be a single column name or a list.
    window_func : Union[str, list, Tuple[str, Callable]], optional, default 'mean'
        The `window_func` parameter in the `augment_rolling` function specifies
        the function(s) to be applied to the rolling windows of the value
        column(s).

        1. It can be either:
            - A string representing the name of a standard function (e.g.,
              'mean', 'sum').

        2. For custom functions:
            - Provide a list of tuples. Each tuple should contain a custom name
              for the function and the function itself.
            - Each custom function should accept a Pandas Series as its input
              and operate on that series.
              Example: ("range", lambda x: x.max() - x.min())

        (See more Examples below.)

        Note: If your function needs to operate on multiple columns (i.e., it
              requires access to a DataFrame rather than just a Series),
              consider using the `augment_rolling_apply` function in this library.
    window : Union[int, tuple, list], optional, default 2
        Specifies the size of the rolling windows.
        - An integer applies the same window size to all columns in `value_column`.
        - A tuple generates windows from the first to the second value (inclusive).
        - A list of integers designates multiple window sizes for each respective
          column.
    min_periods : int, optional, default None
        Minimum observations in the window to have a value. Defaults to the
        window size. If set, a value will be produced even if fewer observations
        are present than the window size.
    center : bool, optional, default False
        If `True`, the rolling window will be centered on the current value. For
        even-sized windows, the window will be left-biased. Otherwise, it uses a trailing window.
    threads : int, optional, default 1
        Number of threads to use for parallel processing. If `threads` is set to
        1, parallel processing will be disabled. Set to -1 to use all available CPU cores.
    show_progress : bool, optional, default True
        If `True`, a progress bar will be displayed during parallel processing.
    reduce_memory : bool, optional
        The `reduce_memory` parameter is used to specify whether to reduce the memory usage of the DataFrame by converting int, float to smaller bytes and str to categorical data. This reduces memory for large data but may impact resolution of float and will change str to categorical. Default is False.
    engine : {"auto", "pandas", "polars", "cudf"}, optional, default "auto"
        Specifies the backend computation library for augmenting rolling window
        functions. When "auto" the backend is inferred from the input data type.
        Use "pandas" or "polars" to force a specific backend.

    Returns
    -------
    pd.DataFrame
        The `augment_rolling` function returns a DataFrame with new columns for
        each applied function, window size, and value column.

    Notes
    -----
    ## Performance

    This function uses parallel processing to speed up computation for large
    datasets with many time series groups:

    Parallel processing has overhead and may not be faster on small datasets.

    To use parallel processing, set `threads = -1` to use all available processors.

    Examples
    --------
    ```{python}
    import pytimetk as tk
    import pandas as pd
    import numpy as np

    df = tk.load_dataset("m4_daily", parse_dates = ['date'])
    ```

    ```{python}
    # Example 1 - Using a single window size and a single function name, pandas engine
    # This example demonstrates the use of both string-named functions and lambda
    # functions on a rolling window. We specify a list of window sizes: [2,7].
    # As a result, the output will have computations for both window sizes 2 and 7.
    # Note - It's preferred to use built-in or configurable functions instead of
    # lambda functions for performance reasons.

    rolled_df = (
        df
            .groupby('id')
            .augment_rolling(
                date_column = 'date',
                value_column = 'value',
                window = [2,7],  # Specifying multiple window sizes
                window_func = [
                    'mean',  # Built-in mean function
                    ('std', lambda x: x.std())  # Lambda function to compute standard deviation
                ],
                threads = 1,  # Disabling parallel processing
                engine = 'pandas'  # Using pandas engine
            )
    )
    display(rolled_df)
    ```

    ```{python}
    # Example 2 - Multiple groups, pandas engine
    # Example showcasing the use of string function names and lambda functions
    # applied on rolling windows. The `window` tuple (1,3) will generate window
    # sizes of 1, 2, and 3.
    # Note - It's preferred to use built-in or configurable functions instead of
    # lambda functions for performance reasons.

    rolled_df = (
        df
            .groupby('id')
            .augment_rolling(
                date_column = 'date',
                value_column = 'value',
                window = (1,3),  # Specifying a range of window sizes
                window_func = [
                    'mean',  # Using built-in mean function
                    ('std', lambda x: x.std())  # Lambda function for standard deviation
                ],
                threads = 1,  # Disabling parallel processing
                engine = 'pandas'  # Using pandas engine
            )
    )
    display(rolled_df)
    ```

    ```{python}
    # Example 3 - Multiple groups, polars engine

    import polars as pl


    rolled_df = (
        pl.from_pandas(df)
            .group_by('id')
            .tk.augment_rolling(
                date_column = 'date',
                value_column = 'value',
                window = (1,3),  # Specifying a range of window sizes
                window_func = [
                    'mean',  # Using built-in mean function
                    'std',  # Using built-in standard deviation function
                ],
            )
    )
    display(rolled_df)
    ```
    """
    pass


def _augment_rolling_cudf_dataframe(
    frame: "cudf.DataFrame",
    *,
    date_column: str,
    value_columns: List[str],
    window_funcs: List[str],
    windows: List[int],
    min_periods: Optional[int],
    min_periods_override: Optional[int],
    center: bool,
    group_columns: Optional[Sequence[str]],
    row_id_column: Optional[str],
) -> "cudf.DataFrame":
    pass


def _augment_rolling_pandas(
    data: Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy],
    date_column: str,
    value_columns: List[str],
    window_funcs: List[Union[str, Tuple[str, Callable]]],
    windows: List[int],
    min_periods: Optional[int] = None,
    center: bool = False,
    threads: int = 1,
    show_progress: bool = True,
    **kwargs,
) -> pd.DataFrame:
    # Create a fresh copy of the data, leaving the original untouched
    pass


def _process_single_roll(
    group_df: pd.DataFrame,
    value_columns: List[str],
    window_funcs: List[Union[str, Tuple[str, Callable]]],
    windows: List[int],
    min_periods: Optional[int],
    center: bool,
    **kwargs,
) -> pd.DataFrame:
    pass


def _rolling_window_ray_worker(
    group_df: pd.DataFrame,
    value_columns: List[str],
    window_funcs: List[Union[str, Tuple[str, Callable]]],
    windows: List[int],
    min_periods: Optional[int],
    center: bool,
    kwargs: dict,
) -> pd.DataFrame:
    pass


def _augment_rolling_polars(
    data: Union[pl.DataFrame, pl.dataframe.group_by.GroupBy],
    date_column: str,
    value_columns: List[str],
    window_funcs: List[Union[str, Tuple[str, Callable]]],
    windows: List[int],
    min_periods: Optional[int],
    center: bool,
    group_columns: Optional[Sequence[str]],
    row_id_column: Optional[str],
) -> pl.DataFrame:
    pass
