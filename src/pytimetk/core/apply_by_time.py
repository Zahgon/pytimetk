import pandas as pd
import polars as pl
import pandas_flavor as pf
import warnings

from typing import Callable, Dict, List, Optional, Sequence, Union

from pytimetk.utils.checks import check_dataframe_or_groupby, check_date_column
from pytimetk.utils.pandas_helpers import flatten_multiindex_column_names
from pytimetk.utils.memory_helpers import reduce_memory_usage
from pytimetk.utils.dataframe_ops import (
    convert_to_engine,
    normalize_engine,
    restore_output_type,
    FrameConversion,
    resolve_pandas_groupby_frame,
    resolve_polars_group_columns,
    conversion_to_pandas,
)
from pytimetk.utils.selection import ColumnSelector, resolve_column_selection
from pytimetk.utils.datetime_helpers import normalize_frequency_alias


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


@pf.register_groupby_method
@pf.register_dataframe_method
def apply_by_time(
    data: Union[
        pd.DataFrame,
        pd.core.groupby.generic.DataFrameGroupBy,
        pl.DataFrame,
        pl.dataframe.group_by.GroupBy,
    ],
    date_column: Union[str, ColumnSelector],
    freq: str = "D",
    wide_format: bool = False,
    fillna: int = 0,
    reduce_memory: bool = False,
    engine: str = "pandas",
    **named_funcs,
) -> Union[pd.DataFrame, pl.DataFrame]:
    """
    Apply for time series.

    Parameters
    ----------
    data : DataFrame or GroupBy (pandas or polars)
        Tabular data on which the operation is performed. Supports both pandas
        and polars DataFrames / GroupBy objects.
    date_column : str or ColumnSelector
        The column containing timestamps used for resampling.
    freq : str, optional
        The `freq` parameter specifies the frequency at which the data should be
        resampled. It accepts a string representing a time frequency, such as "D"
        for daily, "W" for weekly, "M" for monthly, etc. The default value is "D",
        which means the data will be resampled on a daily basis. Some common
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

    wide_format : bool, optional
        The `wide_format` parameter is a boolean flag that determines whether the
        output should be in wide format or not. If `wide_format` is set to `True`,
        the output will have a multi-index column structure, where the first level
        represents the original columns and the second level represents the group
        names.
    fillna : int, optional
        The `fillna` parameter is used to specify the value that will be used to
        fill missing values in the resulting DataFrame. By default, it is set to 0.
    reduce_memory : bool, optional
        The `reduce_memory` parameter is used to specify whether to reduce the memory usage of the DataFrame by converting int, float to smaller bytes and str to categorical data. This reduces memory for large data but may impact resolution of float and will change str to categorical. Default is True.
    engine : {"pandas", "polars", "cudf", "auto"}, optional
        Execution engine. ``"pandas"`` (default) performs the computation using pandas.
        When "polars" the data is converted to pandas for evaluation and converted
        back to polars on return. ``"cudf"`` inputs currently reuse the pandas
        implementation. ``"auto"`` infers the engine from the input data.
    **named_funcs
        The `**named_funcs` parameter is used to specify one or more custom
        aggregation functions to apply to the data. It accepts named functions
        in the format:

        ``` python
            name = lambda df: df['column1'].corr(df['column2']])
        ```

        Where `name` is the name of the function and `df` is the DataFrame that will
        be passed to the function. The function must return a single value.



    Returns
    -------
    DataFrame
        The resulting data after applying the functions. The concrete type matches
        the engine used to process the data.

    Examples
    --------
    ```{python}
    import pytimetk as tk
    import pandas as pd

    df = tk.load_dataset('bike_sales_sample', parse_dates = ['order_date'])

    df.glimpse()
    ```

    ```{python}
    # Apply by time with a DataFrame object
    # Allows access to multiple columns at once
    (
        df[['order_date', 'price', 'quantity']]
            .apply_by_time(

                # Named apply functions
                price_quantity_sum = lambda df: (df['price'] * df['quantity']).sum(),
                price_quantity_mean = lambda df: (df['price'] * df['quantity']).mean(),

                # Parameters
                date_column  = 'order_date',
                freq         = "MS",

            )
    )
    ```

    ```{python}
    # Apply by time with a GroupBy object
    (
        df[['category_1', 'order_date', 'price', 'quantity']]
            .groupby('category_1')
            .apply_by_time(

                # Named functions
                price_quantity_sum = lambda df: (df['price'] * df['quantity']).sum(),
                price_quantity_mean = lambda df: (df['price'] * df['quantity']).mean(),

                # Parameters
                date_column  = 'order_date',
                freq         = "MS",

            )
    )
    ```

    ```{python}
    # Return complex objects
    (
        df[['order_date', 'price', 'quantity']]
            .apply_by_time(

                # Named apply functions
                complex_object = lambda df: [df],

                # Parameters
                date_column  = 'order_date',
                freq         = "MS",

            )
    )
    ```

    ```{python}
    # Polars DataFrame using the tk accessor
    import polars as pl


    pl_df = pl.from_pandas(df[['order_date', 'price', 'quantity']])

    (
        pl_df
            .tk.apply_by_time(
                date_column='order_date',
                freq='MS',
                total = lambda frame: (frame['price'] * frame['quantity']).sum(),
            )
    )
    ```
    """
    pass


def _apply_by_time_pandas(
    prepared: Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy],
    *,
    date_column: str,
    freq: str,
    wide_format: bool,
    fillna: int,
    reduce_memory: bool,
    named_funcs: Dict[str, callable],
) -> pd.DataFrame:
    def custom_agg(group):
        pass
    pass


def _apply_by_time_polars(
    prepared: Union[pl.DataFrame, pl.dataframe.group_by.GroupBy],
    *,
    date_column: str,
    freq: str,
    wide_format: bool,
    fillna: int,
    reduce_memory: bool,
    named_funcs: Dict[str, Callable],
    row_id_column: Optional[str],
    group_columns: Optional[Sequence[str]],
) -> pl.DataFrame:
    pass
