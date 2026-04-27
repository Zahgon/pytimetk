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
from pytimetk.utils.selection import ColumnSelector


@pf.register_groupby_method
@pf.register_dataframe_method
def augment_lags(
    data: Union[
        pd.DataFrame,
        pd.core.groupby.generic.DataFrameGroupBy,
        pl.DataFrame,
        pl.dataframe.group_by.GroupBy,
        "cudf.DataFrame",
        "cudf.core.groupby.groupby.DataFrameGroupBy",
    ],
    date_column: Union[str, ColumnSelector],
    value_column: Union[str, ColumnSelector, Sequence[Union[str, ColumnSelector]]],
    lags: Union[int, Tuple[int, int], List[int], Sequence[Union[int, str]], str] = 1,
    reduce_memory: bool = False,
    engine: Optional[str] = "auto",
) -> Union[pd.DataFrame, pl.DataFrame, "cudf.DataFrame"]:
    """
    Adds lags to a Pandas DataFrame or DataFrameGroupBy object.

    The `augment_lags` function takes a Pandas DataFrame or GroupBy object, a
    date column, a value column or list of value columns, and a lag or list of
    lags, and adds lagged versions of the value columns to the DataFrame.

    Parameters
    ----------
    data : DataFrame or GroupBy (pandas or polars)
        The input tabular data or grouped data to augment with lagged columns.
    date_column : str or ColumnSelector
        The column containing timestamps used to order the data before shifting.
        Accepts tidy selectors (e.g., ``contains("date")``) for convenience.
    value_column : str, ColumnSelector, or list
        The `value_column` parameter is the column(s) in the DataFrame that you
        want to add lagged values for. It can be either a single column name,
        a tidy selector, or a list mixing both.
    lags : int, tuple, list, or str, optional
        The `lags` parameter is an integer, tuple, or list that specifies the
        number of lagged values to add to the DataFrame.

        - If it is an integer, the function will add that number of lagged
          values for each column specified in the `value_column` parameter.

        - If it is a tuple, it will generate lags from the first to the second
          value (inclusive).

        - If it is a list, it will generate lags based on the values in the list.
        - If it is a string (e.g. ``"3 days"``), the duration is converted
          into the number of observations implied by ``date_column``.
    engine : {"auto", "pandas", "polars", "cudf"}, optional
        Execution engine. When "auto" (default) the backend is inferred from the
        input data type. Use "pandas", "polars", or "cudf" to force a specific backend.

    Returns
    -------
    DataFrame
        A DataFrame with lagged columns appended. The returned object matches the
        backend of the input (pandas or polars).

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
    # Example 1 - Add 7 lagged values for a single DataFrame object (pandas)
    lagged_df_single = (
        df
            .query('id == "D10"')
            .augment_lags(
                date_column='date',
                value_column='value',
                lags=(1, 7)
            )
    )
    lagged_df_single
    ```
    ```{python}
    # Example 2 - Add lagged values using the polars accessor
    lagged_pl = (
        pl.from_pandas(df)
        .group_by('id')
        .tk.augment_lags(
            date_column='date',
            value_column='value',
            lags=(1, 3)
        )
    )
    lagged_pl
    ```

    ```{python}
    # Example 3 add 2 lagged values, 2 and 4, for a single DataFrame object (pandas)
    lagged_df_single_two = (
        df
            .query('id == "D10"')
            .augment_lags(
                date_column='date',
                value_column='value',
                lags=[2, 4]
            )
    )
    lagged_df_single_two
    ```
    """
    pass


def _augment_lags_pandas(
    data: Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy],
    date_column: str,
    value_column: Union[str, List[str]],
    lags: List[int],
) -> pd.DataFrame:
    pass


def _augment_lags_polars(
    data: Union[pl.DataFrame, pl.dataframe.group_by.GroupBy],
    date_column: str,
    value_column: Union[str, List[str]],
    lags: List[int],
    group_columns: Optional[Sequence[str]],
    row_id_column: Optional[str],
) -> pl.DataFrame:
    pass


def _augment_lags_cudf(
    data: Union["cudf.DataFrame", "cudf.core.groupby.groupby.DataFrameGroupBy"],
    date_column: str,
    value_column: Union[str, List[str]],
    lags: List[int],
    group_columns: Optional[Sequence[str]],
    row_id_column: Optional[str],
):
    pass
