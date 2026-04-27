import pandas as pd
import polars as pl
import numpy as np
import pandas_flavor as pf
import warnings
from typing import Tuple
from typing import Union, List

from pytimetk.utils.checks import (
    check_dataframe_or_groupby,
    check_date_column,
)

from pytimetk.core.ts_summary import ts_summary
from pytimetk.utils.memory_helpers import reduce_memory_usage
from pytimetk.utils.pandas_helpers import sort_dataframe
from pytimetk.utils.dataframe_ops import (
    FrameConversion,
    convert_to_engine,
    normalize_engine,
    resolve_pandas_groupby_frame,
    restore_output_type,
)


@pf.register_groupby_method
@pf.register_dataframe_method
def augment_fourier(
    data: Union[
        pd.DataFrame,
        pd.core.groupby.generic.DataFrameGroupBy,
        pl.DataFrame,
        pl.dataframe.group_by.GroupBy,
    ],
    date_column: str,
    periods: Union[int, Tuple[int, int], List[int]] = 1,
    max_order: int = 1,
    reduce_memory: bool = True,
    engine: str = "auto",
) -> Union[pd.DataFrame, pl.DataFrame]:
    """
    Adds Fourier transforms to a Pandas DataFrame or DataFrameGroupBy object.

    The `augment_fourier` function takes a Pandas DataFrame or GroupBy object, a date column, a value column or list of value columns, the number of periods for the Fourier series, and the maximum Fourier order, and adds Fourier-transformed columns to the DataFrame.

    Parameters
    ----------
    data : pd.DataFrame or pd.core.groupby.generic.DataFrameGroupBy
        The `data` parameter is the input DataFrame or DataFrameGroupBy object that you want to add Fourier-transformed columns to.
    date_column : str
        The `date_column` parameter is a string that specifies the name of the column in the DataFrame that contains the dates. This column will be used to compute the Fourier transforms.
    periods : int or list, optional
        The `periods` parameter specifies how many timesteps between each peak in the fourier series. Default is 1.
    max_order : int, optional
        The `max_order` parameter specifies the maximum Fourier order to calculate. Default is 1.
    reduce_memory : bool, optional
        The `reduce_memory` parameter is used to specify whether to reduce the memory usage of the DataFrame by converting int, float to smaller bytes and str to categorical data. This reduces memory for large data but may impact resolution of float and will change str to categorical. Default is False.
    engine : str, optional
        The `engine` parameter is used to specify the engine to use for
        augmenting lags. It can be either "pandas" or "polars".

        - The default value is "pandas".

        - When "polars", the function will internally use the `polars` library.
        This can be faster than using "pandas" for large datasets.

    Returns
    -------
    pd.DataFrame
        A Pandas DataFrame with Fourier-transformed columns added to it.

    Examples
    --------
    ```{python}
    import pandas as pd
    import pytimetk as tk

    df = tk.load_dataset('m4_daily', parse_dates=['date'])

    # Example 1 - Add Fourier transforms for a single column
    fourier_df = (
        df
            .query("id == 'D10'")
            .augment_fourier(
                date_column='date',
                periods=[1, 7],
                max_order=1
            )
    )
    fourier_df.head()

    fourier_df.plot_timeseries("date", "date_sin_1_7", x_axis_date_labels = "%B %d, %Y",)
    ```

    ``` {python}
    # Example 2 - Add Fourier transforms for grouped data
    fourier_df = (
        df
            .groupby("id")
            .augment_fourier(
                date_column='date',
                periods=[1, 7],
                max_order=1,
                engine= "pandas"
            )
    )
    fourier_df
    ```

    ``` {python}
    # Example 3 - Add Fourier transforms for grouped data
    fourier_df = (
        df
            .groupby("id")
            .augment_fourier(
                date_column='date',
                periods=[1, 7],
                max_order=1,
                engine= "polars"
            )
    )
    fourier_df
    ```

    ``` {python}
    # Example 4 - Polars DataFrame using the tk accessor
    import polars as pl

    pl_fourier = (
        pl.from_pandas(df)
          .group_by("id")
          .tk.augment_fourier(
              date_column='date',
              periods=[1, 7],
              max_order=1,
          )
    )
    ```

    """
    pass


def calc_fourier(x, period, type: str, K=1):
    pass


def date_to_seq_scale_factor(
    data: pd.DataFrame, date_var: str, engine: str = "pandas"
) -> pd.DataFrame:
    pass


def _augment_fourier_pandas(
    prepared_data: Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy],
    date_column: str,
    periods: List[int],
    max_order: int,
) -> pd.DataFrame:
    pass


def _compute_fourier_columns_for_group(
    frame: pd.DataFrame,
    date_column: str,
    periods: List[int],
    max_order: int,
) -> pd.DataFrame:
    pass


def _compute_fourier_columns(
    frame: pd.DataFrame,
    date_column: str,
    periods: List[int],
    max_order: int,
) -> pd.DataFrame:
    pass
