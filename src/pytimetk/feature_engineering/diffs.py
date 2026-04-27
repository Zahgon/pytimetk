import pandas as pd
import polars as pl
import pandas_flavor as pf
import warnings

from typing import List, Optional, Sequence, Tuple, Union

try:  # Optional dependency for GPU acceleration
    import cudf  # type: ignore
    from cudf.core.groupby.groupby import DataFrameGroupBy as CudfDataFrameGroupBy
except ImportError:  # pragma: no cover - cudf optional
    cudf = None  # type: ignore
    CudfDataFrameGroupBy = None  # type: ignore

from pytimetk.utils.checks import (
    check_dataframe_or_groupby,
)
from pytimetk.utils.dataframe_ops import (
    FrameConversion,
    convert_to_engine,
    ensure_row_id_column,
    normalize_engine,
    resolve_pandas_groupby_frame,
    resolve_polars_group_columns,
    restore_output_type,
)
from pytimetk.utils.memory_helpers import reduce_memory_usage
from pytimetk.utils.pandas_helpers import sort_dataframe
from pytimetk.feature_engineering._shift_utils import resolve_shift_values, resolve_shift_columns


@pf.register_groupby_method
@pf.register_dataframe_method
def augment_diffs(
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
    periods: Union[int, Tuple[int, int], List[int], Sequence[Union[int, str]], str] = 1,
    normalize: bool = False,
    reduce_memory: bool = False,
    engine: Optional[str] = "auto",
) -> Union[pd.DataFrame, pl.DataFrame, "cudf.DataFrame"]:
    """
    Adds differences and percentage difference (percentage change) to a Pandas DataFrame or DataFrameGroupBy object.

    The `augment_diffs` function takes a Pandas DataFrame or GroupBy object, a
    date column, a value column or list of value columns, and a period or list of
    periods, and adds differenced versions of the value columns to the DataFrame.

    Parameters
    ----------
    data : DataFrame or GroupBy (pandas or polars)
        The input data to augment with differenced columns.
    date_column : str
        The `date_column` parameter is a string that specifies the name of the
        column in the DataFrame that contains the dates. This column will be
        used to sort the data before adding the differenced values.
    value_column : str or list
        The `value_column` parameter is the column(s) in the DataFrame that you
        want to add differences values for. It can be either a single column name
        (string) or a list of column names.
    periods : int, tuple, list, or str, optional
        The `periods` parameter is an integer, tuple, or list that specifies the
        periods to shift values when differencing.

        - If it is an integer, the function will add that number of differences
          values for each column specified in the `value_column` parameter.

        - If it is a tuple, it will generate differences from the first to the second
          value (inclusive).

        - If it is a list, it will generate differences based on the values in the list.
        - If it is a string (e.g. ``"7 days"``), the duration is converted into
          the equivalent number of observations derived from ``date_column``.
    normalize : bool, optional
        The `normalize` parameter is used to specify whether to normalize the
        differenced values as a percentage difference. Default is False.
    reduce_memory : bool, optional
        The `reduce_memory` parameter is used to specify whether to reduce the memory usage of the DataFrame by converting int, float to smaller bytes and str to categorical data. This reduces memory for large data but may impact resolution of float and will change str to categorical. Default is True.
    engine : {"auto", "pandas", "polars", "cudf"}, optional
        Execution engine. When "auto" (default) the backend is inferred from the
        input data type. Use "pandas", "polars", or "cudf" to force a specific backend.

    Returns
    -------
    DataFrame
        DataFrame with differenced columns added. The return type matches the
        input backend.

    Examples
    --------
    ```{python}
    import pandas as pd
    import polars as pl
    import pytimetk as tk


    df = tk.load_dataset('m4_daily', parse_dates=['date'])
    df
    ```

    ```{python}
    # Example 1 - Add 7 differenced values for a single DataFrame object (pandas)
    diffed_df_single = (
        df
            .query('id == "D10"')
            .augment_diffs(
                date_column='date',
                value_column='value',
                periods=(1, 7)
            )
    )
    diffed_df_single.glimpse()
    ```
    ```{python}
    # Example 2 - Add differenced values via the polars accessor
    diffed_df = (
        pl.from_pandas(df)
        .group_by('id')
        .tk.augment_diffs(
            date_column='date',
            value_column='value',
            periods=2,
        )
    )
    diffed_df
    ```

    ```{python}
    # Example 3 add 2 differenced values, 2 and 4, for a single DataFrame object (pandas)
    diffed_df_single_two = (
        df
            .query('id == "D10"')
            .augment_diffs(
                date_column='date',
                value_column='value',
                periods=[2, 4]
            )
    )
    diffed_df_single_two
    ```
    """
    pass


def _augment_diffs_pandas(
    data: Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy],
    value_column: Union[str, List[str]],
    periods: List[int],
    normalize: bool,
) -> pd.DataFrame:
    pass


def _augment_diffs_polars(
    data: Union[pl.DataFrame, pl.dataframe.group_by.GroupBy],
    date_column: str,
    value_column: Union[str, List[str]],
    periods: List[int],
    normalize: bool,
    group_columns: Optional[Sequence[str]],
    row_id_column: Optional[str],
) -> pl.DataFrame:
    pass


def _augment_diffs_cudf(
    data: Union["cudf.DataFrame", "cudf.core.groupby.groupby.DataFrameGroupBy"],
    date_column: str,
    value_column: Union[str, List[str]],
    periods: List[int],
    normalize: bool,
    group_columns: Optional[Sequence[str]],
    row_id_column: Optional[str],
):
    pass
