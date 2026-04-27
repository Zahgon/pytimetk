import pandas as pd
import polars as pl
import pandas_flavor as pf
import inspect
import warnings

from typing import Callable, List, Optional, Sequence, Tuple, Union

try:  # Optional cudf dependency for GPU acceleration
    import cudf  # type: ignore
except ImportError:  # pragma: no cover - cudf optional
    cudf = None  # type: ignore

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
def augment_expanding(
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
    min_periods: Optional[int] = None,
    engine: Optional[str] = "auto",
    threads: int = 1,
    show_progress: bool = True,
    reduce_memory: bool = False,
    **kwargs,
) -> Union[pd.DataFrame, pl.DataFrame]:
    """
    Apply one or more Series-based expanding functions to one or more columns of a DataFrame.

    Parameters
    ----------
    data : Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy]
        Input data to be processed. Can be a Pandas DataFrame or a GroupBy object.
    date_column : str
        Name of the datetime column. Data is sorted by this column within each group.
    value_column : Union[str, list]
        Column(s) to which the expanding window functions should be applied. Can be
        a single column name or a list.
    window_func : Union[str, list, Tuple[str, Callable]], optional, default 'mean'
        The `window_func` parameter in the `augment_expanding` function specifies
        the function(s) to be applied to the expanding windows of the value column(s).

        1. It can be either:
            - A string representing the name of a standard function (e.g., 'mean', 'sum').

        2. For custom functions:
            - Provide a list of tuples. Each tuple should contain a custom name for
              the function and the function itself.
            - Each custom function should accept a Pandas Series as its input and
              operate on that series. Example: ("range", lambda x: x.max() - x.min())

        (See more Examples below.)

        Note: If your function needs to operate on multiple columns (i.e., it
              requires access to a DataFrame rather than just a Series), consider
              using the `augment_expanding_apply` function in this library.
    min_periods : int, optional, default None
        Minimum observations in the window to have a value. Defaults to the window
        size. If set, a value will be produced even if fewer observations are
        present than the window size.
    engine : {"auto", "pandas", "polars", "cudf"}, optional, default "auto"
        Specifies the backend computation library for augmenting expanding window
        functions. When "auto" the backend is inferred from the input data type.
        Use "pandas" or "polars" to force a specific backend.
    threads : int, optional, default 1
        Number of threads to use for parallel processing. If `threads` is set to
        1, parallel processing will be disabled. Set to -1 to use all available CPU cores.
    show_progress : bool, optional, default True
        If `True`, a progress bar will be displayed during parallel processing.
    reduce_memory : bool, optional
        The `reduce_memory` parameter is used to specify whether to reduce the memory usage of the DataFrame by converting int, float to smaller bytes and str to categorical data. This reduces memory for large data but may impact resolution of float and will change str to categorical. Default is True.
    **kwargs : additional keyword arguments
        Additional arguments passed to the `pandas.Series.expanding` method when
        using the Pandas engine.

    Returns
    -------
    pd.DataFrame
        The `augment_expanding` function returns a DataFrame with new columns for
        each applied function, window size, and value column.

    Notes
    -----

    ## Performance

    ### Polars Engine (3X faster than Pandas)

    In most cases, the `polars` engine will be faster than the `pandas` engine. Speed tests indicate 3X or more.

    ### Parallel Processing (Pandas Engine Only)

    This function uses parallel processing to speed up computation for large
    datasets with many time series groups:

    Parallel processing has overhead and may not be faster on small datasets.

    To use parallel processing, set `threads = -1` to use all available processors.

    Examples
    --------

    ```{python}
    # Example 1 - Pandas Backend for Expanding Window Functions
    # This example demonstrates the use of string-named functions
    # on an expanding window using the Pandas backend for computations.

    import pytimetk as tk
    import pandas as pd
    import numpy as np

    df = tk.load_dataset("m4_daily", parse_dates = ['date'])

    expanded_df = (
        df
            .groupby('id')
            .augment_expanding(
                date_column = 'date',
                value_column = 'value',
                window_func = [
                    'mean',  # Built-in mean function
                    'std',   # Built-in standard deviation function,
                     ('quantile_75', lambda x: pd.Series(x).quantile(0.75)),  # Custom quantile function

                ],
                min_periods = 1,
                engine = 'pandas',  # Utilize pandas for the underlying computations
                threads = 1,  # Disable parallel processing
                show_progress = True,  # Display a progress bar
                )
    )
    display(expanded_df)
    ```


    ```{python}
    # Example 2 - Polars Backend for Expanding Window Functions using Built-Ins
    #             (538X Faster than Pandas)
    #  This example demonstrates the use of string-named functions and configurable
    #  functions using the Polars backend for computations. Configurable functions,
    #  like pl_quantile, allow the use of specific parameters associated with their
    #  corresponding polars.Expr.rolling_<function_name> method.
    #  For instance, pl_quantile corresponds to polars.Expr.rolling_quantile.

    import pytimetk as tk
    import pandas as pd
    import polars as pl
    import numpy as np

    from pytimetk.utils.polars_helpers import pl_quantile
    from pytimetk.utils.pandas_helpers import pd_quantile

    df = tk.load_dataset("m4_daily", parse_dates = ['date'])

    expanded_df = (
        pl.from_pandas(df)
            .group_by('id')
            .tk.augment_expanding(
                date_column = 'date',
                value_column = 'value',
                window_func = [
                    'mean',  # Built-in mean function
                    'std',   # Built-in std function
                    ('quantile_75', pl_quantile(quantile=0.75)),
                ],
                min_periods = 1,
            )
    )
    display(expanded_df)
    ```

    ```{python}
    # Example 3 - Lambda Functions for Expanding Window Functions are faster in Pandas than Polars
    # This example demonstrates the use of lambda functions of the form lambda x: x
    # Identity lambda functions, while convenient, have signficantly slower performance.
    # When using lambda functions the Pandas backend will likely be faster than Polars.

    import pytimetk as tk
    import pandas as pd
    import numpy as np

    df = tk.load_dataset("m4_daily", parse_dates = ['date'])

    expanded_df = (
        df
            .groupby('id')
            .augment_expanding(
                date_column = 'date',
                value_column = 'value',
                window_func = [

                    ('range', lambda x: x.max() - x.min()),  # Identity lambda function: can be slower, especially in Polars
                ],
                min_periods = 1,
                engine = 'pandas',  # Utilize pandas for the underlying computations
            )
    )
    display(expanded_df)
    ```
    """
    pass


def _augment_expanding_cudf_dataframe(
    frame: "cudf.DataFrame",
    *,
    date_column: str,
    value_columns: List[str],
    window_funcs: List[str],
    min_periods: Optional[int],
    group_columns: Optional[Sequence[str]],
    row_id_column: Optional[str],
) -> "cudf.DataFrame":
    pass


def _expanding_window_ray_worker(
    group_df: pd.DataFrame,
    value_columns: List[str],
    window_funcs: List[Union[str, Tuple[str, Callable]]],
    min_periods: Optional[int],
    kwargs: dict,
) -> pd.DataFrame:
    pass


def _augment_expanding_pandas(
    data: Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy],
    date_column: str,
    value_columns: List[str],
    window_funcs: List[Union[str, Tuple[str, Callable]]],
    min_periods: Optional[int] = None,
    threads: int = 1,
    show_progress: bool = True,
    **kwargs,
) -> pd.DataFrame:
    """
    Augments the given dataframe with expanding calculations using the Pandas library.
    """
    pass


def _process_expanding_window(
    group_df: pd.DataFrame,
    value_columns: List[str],
    window_funcs: List[Union[str, Tuple[str, Callable]]],
    min_periods: Optional[int],
    **kwargs,
):
    pass


def _augment_expanding_polars(
    data: Union[pl.DataFrame, pl.dataframe.group_by.GroupBy],
    date_column: str,
    value_columns: List[str],
    window_funcs: List[Union[str, Tuple[str, Callable]]],
    min_periods: Optional[int],
    group_columns: Optional[Sequence[str]],
    row_id_column: Optional[str],
) -> pl.DataFrame:
    pass
