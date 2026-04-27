import pandas as pd
import polars as pl
import pandas_flavor as pf
from typing import Union, Optional, Sequence, List

from pytimetk.core.frequency import get_frequency
from pytimetk.utils.checks import check_dataframe_or_groupby, check_date_column

from pytimetk.utils.parallel_helpers import conditional_tqdm, get_threads

from pytimetk.utils.memory_helpers import reduce_memory_usage
from pytimetk.utils.dataframe_ops import (
    convert_to_engine,
    normalize_engine,
    restore_output_type,
    conversion_to_pandas,
    resolve_pandas_groupby_frame,
    resolve_polars_group_columns,
)
from pytimetk.utils.selection import ColumnSelector, resolve_column_selection
from pytimetk.utils.datetime_helpers import parse_human_duration, normalize_frequency_alias
from pytimetk.utils.ray_helpers import run_ray_tasks


def _resolve_selector_frame(
    data: Union[
        pd.DataFrame,
        pd.core.groupby.generic.DataFrameGroupBy,
        pl.DataFrame,
        pl.dataframe.group_by.GroupBy,
    ],
) -> pd.DataFrame:
    pass


def _normalize_frequency_spec(
    freq: Optional[Union[str, pd.DateOffset]]
) -> Optional[pd.DateOffset]:
    pass


def _frequency_to_str(freq: Optional[pd.DateOffset]) -> Optional[str]:
    pass



try:  # Optional cudf dependency
    import cudf  # type: ignore
except ImportError:  # pragma: no cover - cudf optional
    cudf = None  # type: ignore


@pf.register_groupby_method
@pf.register_dataframe_method
def future_frame(
    data: Union[
        pd.DataFrame,
        pd.core.groupby.generic.DataFrameGroupBy,
        pl.DataFrame,
        pl.dataframe.group_by.GroupBy,
    ],
    date_column: Union[str, ColumnSelector],
    length_out: int,
    freq: Optional[str] = None,
    force_regular: bool = False,
    bind_data: bool = True,
    threads: int = 1,
    show_progress: bool = True,
    reduce_memory: bool = False,
    engine: str = "pandas",
) -> Union[pd.DataFrame, pl.DataFrame]:
    """
    Extend a DataFrame or GroupBy object with future dates.

    The `future_frame` function extends a given DataFrame or GroupBy object with
    future dates based on a specified length, optionally binding the original data.


    Parameters
    ----------
    data : DataFrame or GroupBy (pandas or polars)
        The `data` parameter is the input DataFrame or grouped object that you want to
        extend with future dates.
    date_column : str or ColumnSelector
        Column containing the timestamps that anchor the extension.
    freq : str, optional
        Frequency for generated dates. When ``None`` the cadence is inferred
        from the observed series (respecting ``force_regular``). Accepts pandas
        aliases (e.g., ``"MS"``, ``"H"``) or human-friendly durations like
        ``"2 weeks"``.
    length_out : int
        The `length_out` parameter specifies the number of future dates to be
        added to the DataFrame.
    force_regular : bool, optional
        The `force_regular` parameter is a boolean flag that determines whether
        the frequency of the future dates should be forced to be regular. If
        `force_regular` is set to `True`, the frequency of the future dates will
        be forced to be regular. If `force_regular` is set to `False`, the
        frequency of the future dates will be inferred from the input data (e.g.
        business calendars might be used). The default value is `False`.
    bind_data : bool, optional
        The `bind_data` parameter is a boolean flag that determines whether the
        extended data should be concatenated with the original data or returned
        separately. If `bind_data` is set to `True`, the extended data will be
        concatenated with the original data using `pd.concat`. If `bind_data` is
        set to `False`, the extended data will be returned separately. The
        default value is `True`.
    threads : int
        The `threads` parameter specifies the number of threads to use for
        parallel processing. If `threads` is set to `None`, it will use all
        available processors. If `threads` is set to `-1`, it will use all
        available processors as well.
    show_progress : bool, optional
        A boolean parameter that determines whether to display progress using tqdm.
        If set to True, progress will be displayed. If set to False, progress
        will not be displayed.
    reduce_memory : bool, optional
        The `reduce_memory` parameter is used to specify whether to reduce the memory usage of the DataFrame by converting int, float to smaller bytes and str to categorical data. This reduces memory for large data but may impact resolution of float and will change str to categorical. Default is True.
    engine : {"pandas", "polars", "cudf", "auto"}, optional
        The `engine` parameter specifies the engine to use for computation.
        ``"pandas"`` (default) performs the computation using pandas. ``"polars"``
        converts the result to a polars DataFrame on return. ``"auto"`` infers the
        engine from the input data.

    Returns
    -------
    DataFrame
        An extended DataFrame with future dates. The concrete type matches the engine
        used to process the data.

    Notes
    -----

    ## Performance

    This function uses a number of techniques to speed up computation for large
    datasets with many time series groups:

    - We vectorize where possible and use parallel processing to speed up.
    - The `threads` parameter controls the number of Ray workers used for
      parallel processing (Ray initializes automatically when `threads != 1`).

        - Set threads = -1 to use all available processors.
        - Set threads = 1 to disable parallel processing.


    See Also
    --------
    make_future_timeseries: Generate future dates for a time series.

    Examples
    --------
    ```{python}
    import pandas as pd
    import pytimetk as tk

    df = tk.load_dataset('m4_hourly', parse_dates = ['date'])
    df

    # Example 1 - Extend the data for a single time series group by 12 hours
    extended_df = (
        df
            .query('id == "H10"')
            .future_frame(
                date_column = 'date',
                length_out  = 12
            )
    )
    extended_df
    ```

    ```{python}
    # Example 2 - Extend the data for each group by 12 hours
    extended_df = (
        df
            .groupby('id', sort = False) # Use sort = False to preserve the original order of the data
            .future_frame(
                date_column = 'date',
                length_out  = 12,
                threads     = 1 # Use 2 threads for parallel processing
            )
    )
    extended_df
    ```

    ```{python}
    # Example 3 - Same as above, but just return the extended data with bind_data=False
    extended_df = (
        df
            .groupby('id', sort = False)
            .future_frame(
                date_column = 'date',
                length_out  = 12,
                bind_data   = False # Returns just future data
            )
    )
    extended_df
    ```

    ```{python}
    # Example 4 - Working with irregular dates: Business Days (Stocks Data)

    import pytimetk as tk
    import pandas as pd

    # Stock data
    df = tk.load_dataset('stocks_daily', parse_dates = ['date'])
    df

    # Allow irregular future dates (i.e. business days)
    extended_df = (
        df
            .groupby('symbol', sort = False)
            .future_frame(
                date_column = 'date',
                length_out  = 12,
                force_regular = False, # Allow irregular future dates (i.e. business days)),
                bind_data   = True,
                threads     = 1
            )
    )
    extended_df
    ```

    ```{python}
    # Force regular: Include Weekends
    extended_df = (
        df
            .groupby('symbol', sort = False)
            .future_frame(
                date_column = 'date',
                length_out  = 12,
                force_regular = True, # Force regular future dates (i.e. include weekends)),
                bind_data   = True
            )
    )
    extended_df
    ```

    ```{python}
    # Polars DataFrame using the tk accessor
    import pandas as pd
    import polars as pl


    sample = pd.DataFrame(
        {
            "date": pd.date_range("2022-01-03", periods=4, freq="D"),
            "value": [1, 2, 3, 4],
        }
    )

    pl_df = pl.from_pandas(sample)

    pl_df.tk.future_frame(
        date_column='date',
        length_out=2,
    )
    ```
    """
    pass


def _future_frame_pandas(
    data: Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy],
    date_column: str,
    length_out: int,
    freq: Optional[Union[str, pd.DateOffset]] = None,
    force_regular: bool = False,
    bind_data: bool = True,
    threads: int = 1,
    show_progress: bool = True,
    reduce_memory: bool = False,
) -> pd.DataFrame:
    pass


# --------------------------------------------------------------------------- #
# Polars helper                                                               #
# --------------------------------------------------------------------------- #


def _future_frame_polars(
    data: Union[pl.DataFrame, pl.dataframe.group_by.GroupBy],
    date_column: str,
    length_out: int,
    freq: Optional[Union[str, pd.DateOffset]],
    force_regular: bool,
    bind_data: bool,
    threads: int,
    show_progress: bool,
    row_id_column: Optional[str],
    group_columns: Optional[Sequence[str]],
) -> pl.DataFrame:
    def _cast_series(series: pl.Series) -> pl.Series:
        pass
    pass


# UTILITIES ------------------------------------------------------------------


def _process_future_frame_subset(
    subset, date_column, group_names, length_out, freq
):
    pass


def _process_future_frame_rows(
    row, date_column, group_names, length_out, freq
):
    pass


def _generate_future_index(
    anchor_value, freq: Optional[pd.DateOffset], length_out: int
) -> pd.DatetimeIndex:
    pass
