import pandas as pd
import polars as pl
import pandas_flavor as pf
import warnings

from typing import Optional, Union, List, Sequence, Any, Tuple

import numpy as np

try:  # Optional dependency for GPU acceleration
    import cudf  # type: ignore
except ImportError:  # pragma: no cover - cudf optional
    cudf = None  # type: ignore

from pytimetk.utils.checks import (
    check_dataframe_or_groupby,
    check_date_column,
    check_value_column,
)
from pytimetk.utils.dataframe_ops import (
    FrameConversion,
    convert_to_engine,
    normalize_engine,
    resolve_pandas_groupby_frame,
    restore_output_type,
    conversion_to_pandas,
)
from pytimetk.utils.memory_helpers import reduce_memory_usage


@pf.register_groupby_method
@pf.register_dataframe_method
def augment_ewm(
    data: Union[
        pd.DataFrame,
        pd.core.groupby.generic.DataFrameGroupBy,
        pl.DataFrame,
        pl.dataframe.group_by.GroupBy,
        "cudf.DataFrame",
        "cudf.core.groupby.groupby.DataFrameGroupBy",
    ],
    date_column: str,
    value_column: Union[str, list],
    window_func: Union[str, list] = "mean",
    alpha: float = None,
    reduce_memory: bool = False,
    engine: Optional[str] = "auto",
    **kwargs,
) -> Union[pd.DataFrame, pl.DataFrame, "cudf.DataFrame"]:
    """
    Add Exponential Weighted Moving (EWM) window functions to a DataFrame or
    GroupBy object.

    The `augment_ewm` function applies Exponential Weighted Moving (EWM) window
    functions to specified value columns of a DataFrame and adds the results as
    new columns.

    Parameters
    ----------
    data : DataFrame or GroupBy (pandas or polars)
        The input data to augment. Grouped inputs are processed per group before
        the EWM columns are appended.
    date_column : str
        The name of the column containing date information in the input
        DataFrame or GroupBy object.
    value_column : Union[str, list]
        The `value_column` parameter is used to specify the column(s) on which
        the Exponential Weighted Moving (EWM) calculations will be performed. It
        can be either a string or a list of strings, representing the name(s) of
        the column(s) in the input DataFrame or GroupBy
    window_func : Union[str, list], optional
        The `window_func` parameter is used to specify the Exponential Weighted
        Moving (EWM) window function(s) to apply. It can be a string or a list
        of strings. The possible values are:

        - 'mean': Calculate the exponentially weighted mean.
        - 'median': Calculate the exponentially weighted median.
        - 'std': Calculate the exponentially weighted standard deviation.
        - 'var': Calculate the exponentially weighted variance.

    alpha : float or sequence of floats, optional
        The `alpha` parameter represents the smoothing factor for the Exponential
        Weighted Moving (EWM) window function. It controls the rate at which the
        weights decrease exponentially as the data points move further away from
        the current point. Pass a single value to compute one EWM or a sequence
        of values to generate multiple EWM columns in a single call. This option
        is mutually exclusive with specifying decay parameters such as `com`,
        `span`, or `halflife` through ``**kwargs``.
    engine : {"auto", "pandas", "polars", "cudf"}, optional
        Execution engine. ``"auto"`` (default) infers the backend from the input
        data while allowing explicit overrides. Polars and cudf inputs currently
        execute through a pandas fallback.
    reduce_memory : bool, optional
        Attempt to reduce memory usage before/after computation when operating
        on pandas data. If a polars input is supplied a warning is emitted and
        no conversion occurs.
    **kwargs:
        Additional arguments that are directly passed to the pandas EWM method.
        For more details, refer to the "Notes" section below.

    Returns
    -------
    DataFrame
        The function `augment_ewm` returns a DataFrame augmented with the
        results of the Exponential Weighted Moving (EWM) calculations.

    Notes
    ------
    Any additional arguments provided through **kwargs are directly passed
    to the pandas EWM method. These arguments can include parameters like
    'com', 'span', 'halflife', 'ignore_na', 'adjust' and more.

    For a comprehensive list and detailed description of these parameters:

    - Refer to the official pandas documentation:
        https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html

    - Or, within an interactive Python environment, use:
        `?pandas.DataFrame.ewm` to display the method's docstring.

    Examples
    --------
    ```{python}
    import pandas as pd
    import polars as pl
    import pytimetk as tk


    df = tk.load_dataset("m4_daily", parse_dates = ['date'])

    # Pandas example (engine inferred)
    ewm_df = (
        df
            .groupby('id')
            .augment_ewm(
                date_column = 'date',
                value_column = 'value',
                window_func = [
                    'mean',
                    'std',
                ],
                alpha = 0.1,
            )
    )

    # Polars example using the tk accessor
    ewm_pl = (
        pl.from_pandas(df)
        .group_by('id')
        .tk.augment_ewm(
            date_column='date',
            value_column='value',
            window_func='mean',
            alpha=0.1,
        )
    )
    ```
    """
    pass


def _ensure_list_like(values: Union[Any, Sequence[Any]]) -> List[Any]:
    pass


def _prepare_decay_configs(
    alpha: Optional[Union[float, Sequence[float]]],
    kwargs: dict,
) -> List[Tuple[str, Any, dict]]:
    pass


def _augment_ewm_pandas(
    data: Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy],
    date_column: str,
    value_column: Union[str, List[str]],
    window_func: Union[str, List[str]],
    alpha: Optional[Union[float, Sequence[float]]],
    reduce_memory: bool,
    **kwargs,
) -> pd.DataFrame:
    pass
def _augment_ewm_polars(
    data: Union[pl.DataFrame, pl.dataframe.group_by.GroupBy],
    *,
    date_column: str,
    value_column: Union[str, List[str]],
    window_func: Union[str, List[str]],
    alpha: Optional[Union[float, Sequence[float]]],
    group_columns: Optional[Sequence[str]],
    row_id_column: Optional[str],
    **kwargs,
) -> pl.DataFrame:
    def _maybe_over(expr: pl.Expr) -> pl.Expr:
        pass
    pass


def _apply_ewm_function(ewm_obj, func: Union[str, callable]) -> pd.Series:
    pass


def _augment_ewm_cudf_dataframe(
    frame: "cudf.DataFrame",
    *,
    date_column: str,
    value_columns: List[str],
    window_funcs: List[str],
    alpha: Optional[Union[float, Sequence[float]]],
    group_columns: Optional[Sequence[str]],
    row_id_column: Optional[str],
    **kwargs,
) -> "cudf.DataFrame":
    pass
