import numpy as np
import pandas as pd
import polars as pl
import pandas_flavor as pf
from patsy import bs, cr, cc
from typing import Literal, Optional, Sequence, Union
import warnings

from pytimetk.utils.checks import (
    check_dataframe_or_groupby,
    check_date_column,
    check_value_column,
)
from pytimetk.utils.memory_helpers import reduce_memory_usage
from pytimetk.utils.dataframe_ops import (
    FrameConversion,
    convert_to_engine,
    ensure_row_id_column,
    normalize_engine,
    resolve_pandas_groupby_frame,
    restore_output_type,
)


SplineTypeInput = Literal[
    "bs",
    "basis",
    "b-spline",
    "bspline",
    "natural",
    "ns",
    "cr",
    "cyclic",
    "cc",
]


VALID_SPLINE_TYPES = {
    "bs": "bs",
    "basis": "bs",
    "b-spline": "bs",
    "bspline": "bs",
    "natural": "cr",
    "ns": "cr",
    "cr": "cr",
    "cyclic": "cc",
    "cc": "cc",
}

SPLINE_NAME_MAP = {
    "bs": "bspline",
    "cr": "natural_spline",
    "cc": "cyclic_spline",
}


@pf.register_groupby_method
@pf.register_dataframe_method
def augment_spline(
    data: Union[
        pd.DataFrame,
        pd.core.groupby.generic.DataFrameGroupBy,
        pl.DataFrame,
        pl.dataframe.group_by.GroupBy,
    ],
    date_column: str,
    value_column: str,
    spline_type: SplineTypeInput = "bs",
    df: Optional[int] = 5,
    degree: int = 3,
    knots: Optional[Sequence[float]] = None,
    include_intercept: bool = False,
    lower_bound: Optional[float] = None,
    upper_bound: Optional[float] = None,
    prefix: Optional[str] = None,
    reduce_memory: bool = False,
    engine: Optional[str] = "auto",
) -> Union[pd.DataFrame, pl.DataFrame]:
    """
    Add spline basis expansions for a numeric column.

    Parameters
    ----------
    data : DataFrame or GroupBy (pandas or polars)
        Input tabular data or grouped data.
    date_column : str
        Name of the datetime column used to order observations prior to building
        the spline basis.
    value_column : str
        Name of the numeric column to transform into spline basis features.
    spline_type : str, optional
        Spline family. Supported values are "bs" (B-spline), "natural"/"cr"
        (natural cubic spline) and "cyclic"/"cc" (cyclic spline). Defaults to
        "bs".
    df : int, optional
        Degrees of freedom passed to the spline constructor. Required unless
        `knots` are supplied. Defaults to 5.
    degree : int, optional
        Degree of the polynomial pieces (B-spline only). Defaults to 3.
    knots : Sequence[float], optional
        Internal knot positions to use when constructing the spline basis.
    include_intercept : bool, optional
        Whether to include the intercept column (B-spline only). Defaults to
        False.
    lower_bound : float, optional
        Lower boundary for the spline. When omitted the minimum value of
        `value_column` is used.
    upper_bound : float, optional
        Upper boundary for the spline. When omitted the maximum value of
        `value_column` is used.
    prefix : str, optional
        Custom prefix for the generated column names. When omitted a name is
        derived from `value_column` and `spline_type`.
    reduce_memory : bool, optional
        If True, attempt to downcast numeric columns to reduce memory usage.
    engine : {"auto", "pandas", "polars"}, optional
        Execution engine. When set to "auto" (default) the backend is inferred
        from the input data type. Use "pandas" or "polars" to force a specific
        backend regardless of input type.

    Returns
    -------
    DataFrame
        DataFrame with spline basis columns appended. The result matches the
        input data backend (pandas or polars).

    Examples
    --------

    ```{python}
    # Pandas Example
    import pandas as pd
    import polars as pl
    import pytimetk as tk


    df = tk.load_dataset('m4_daily', parse_dates=['date'])

    df_spline = (
        df
            .query("id == 'D10'")
            .augment_spline(
                date_column='date',
                value_column='value',
                spline_type='bs',
                df=5,
                degree=3,
                prefix='value_bs'
            )
    )

    df_spline.head()
    ```

    ```{python}
    pl_spline = (
        pl.from_pandas(df.query("id == 'D10'"))
        .tk.augment_spline(
            date_column='date',
            value_column='value',
            spline_type='bs',
            df=5,
            degree=3,
            prefix='value_bs'
        )
    )

    pl_spline.head()
    ```

    """
    pass


def _augment_spline_pandas(
    data: Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy],
    date_column: str,
    value_column: str,
    spline_key: str,
    df: Optional[int],
    degree: int,
    knots: Optional[Sequence[float]],
    include_intercept: bool,
    lower_bound: Optional[float],
    upper_bound: Optional[float],
    prefix: Optional[str],
) -> pd.DataFrame:
    pass


def _augment_spline_frame(
    frame: pd.DataFrame,
    date_column: str,
    value_column: str,
    spline_key: str,
    df: Optional[int],
    degree: int,
    knots: Optional[Sequence[float]],
    include_intercept: bool,
    lower_bound: Optional[float],
    upper_bound: Optional[float],
    prefix: Optional[str],
) -> pd.DataFrame:
    pass


def _augment_spline_polars(
    data: Union[pl.DataFrame, pl.dataframe.group_by.GroupBy],
    date_column: str,
    value_column: str,
    spline_key: str,
    df: Optional[int],
    degree: int,
    knots: Optional[Sequence[float]],
    include_intercept: bool,
    lower_bound: Optional[float],
    upper_bound: Optional[float],
    prefix: Optional[str],
    row_id_column: Optional[str],
    group_columns: Optional[Sequence[str]],
) -> pl.DataFrame:
    pass


def _resolve_polars_group_columns(
    groupby: pl.dataframe.group_by.GroupBy,
) -> Sequence[str]:
    pass


def _augment_spline_polars_frame(
    frame: pl.DataFrame,
    date_column: str,
    value_column: str,
    spline_key: str,
    df: Optional[int],
    degree: int,
    knots: Optional[Sequence[float]],
    include_intercept: bool,
    lower_bound: Optional[float],
    upper_bound: Optional[float],
    prefix: Optional[str],
) -> pl.DataFrame:
    pass


def _build_spline_basis_matrix(
    values: Union[Sequence[float], np.ndarray],
    value_column: str,
    spline_key: str,
    df: Optional[int],
    degree: int,
    knots: Optional[Sequence[float]],
    include_intercept: bool,
    lower_bound: Optional[float],
    upper_bound: Optional[float],
) -> np.ndarray:
    pass


def _normalise_spline_type(spline_type: SplineTypeInput) -> str:
    pass


def _default_prefix(value_column: str, spline_key: str, degree: int) -> str:
    pass


def _prepare_knots(knots: Optional[Sequence[float]]) -> Optional[Sequence[float]]:
    pass
