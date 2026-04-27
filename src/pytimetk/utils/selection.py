import re
from typing import Callable, Iterable, List, Sequence, Union

import pandas as pd

try:  # Optional dependency
    import polars as pl
except ImportError:  # pragma: no cover - optional import
    pl = None  # type: ignore

from pytimetk.utils.dataframe_ops import resolve_pandas_groupby_frame

ColumnSelector = Union[
    str,
    Sequence[str],
    re.Pattern,
    Callable[[pd.Index], Iterable[str]],
    None,
]


def contains(
    pattern: str, *, case: bool = True, regex: bool = False
) -> Callable[[pd.Index], List[str]]:
    """
    Build a selector that returns columns containing ``pattern``.

    Parameters
    ----------
    pattern : str
        Substring or regular expression to match.
    case : bool, optional
        Perform case-sensitive matching. Defaults to True.
    regex : bool, optional
        Treat ``pattern`` as a regular expression. Defaults to False.

    Examples
    --------
    ```{python}
    import pandas as pd
    from pytimetk.utils.selection import contains

    columns = pd.Index(["value", "VALUE_DELTA", "category"])
    contains("value", case=False)(columns)
    ```
    """
    def _selector(columns: pd.Index) -> List[str]:
        pass
    pass


def starts_with(prefix: str, *, case: bool = True) -> Callable[[pd.Index], List[str]]:
    """
    Build a selector that returns columns starting with ``prefix``.

    Examples
    --------
    ```{python}
    import pandas as pd
    from pytimetk.utils.selection import starts_with

    columns = pd.Index(["value", "val_growth", "category"])
    starts_with("val")(columns)
    ```
    """
    def _selector(columns: pd.Index) -> List[str]:
        pass
    pass


def ends_with(suffix: str, *, case: bool = True) -> Callable[[pd.Index], List[str]]:
    """
    Build a selector that returns columns ending with ``suffix``.

    Examples
    --------
    ```{python}
    import pandas as pd
    from pytimetk.utils.selection import ends_with

    columns = pd.Index(["value", "total_value", "category"])
    ends_with("value")(columns)
    ```
    """
    def _selector(columns: pd.Index) -> List[str]:
        pass
    pass


def matches(pattern: str, *, flags: int = 0) -> Callable[[pd.Index], List[str]]:
    """
    Build a selector that returns columns matching the supplied regular expression.

    Examples
    --------
    ```{python}
    import pandas as pd
    from pytimetk.utils.selection import matches

    columns = pd.Index(["lag_1", "lag_2", "value"])
    matches(r"^lag_\\d$")(columns)
    ```
    """
    def _selector(columns: pd.Index) -> List[str]:
        pass
    pass


def resolve_column_selection(
    data: Union[
        pd.DataFrame,
        pd.core.groupby.generic.DataFrameGroupBy,
        "pl.DataFrame",
        "pl.dataframe.group_by.GroupBy",
    ],
    selectors: ColumnSelector,
    *,
    allow_none: bool = True,
    require_match: bool = True,
    unique: bool = True,
) -> List[str]:
    """
    Resolve flexible column selectors into a concrete list of column names.

    Parameters
    ----------
    data : DataFrame or GroupBy
        Data source used to validate column existence.
    selectors : various
        - ``str``: treated as a literal column name.
        - ``Sequence[str]``: a collection of literal column names.
        - ``re.Pattern``: matches columns via ``pattern.search``.
        - ``Callable``: receives the column ``Index`` and must return an
          iterable of column names.
        - ``None``: permitted when ``allow_none`` is True (default), yielding ``[]``.
    allow_none : bool, optional
        Allow ``None`` selectors without raising an error. Defaults to True.
    require_match : bool, optional
        Raise ``ValueError`` when a selector does not match any columns. Defaults to True.
    unique : bool, optional
        Return deduplicated column names while preserving order. Defaults to True.

    Returns
    -------
    list[str]
        Ordered list of columns satisfying the selector(s).
    Examples
    --------
    ```{python}
    import pandas as pd
    import pytimetk as tk
    from pytimetk.utils.selection import contains

    df = pd.DataFrame({"grp": [1, 1], "value": [10, 20], "category": ["a", "b"]})
    tk.resolve_column_selection(df, ["value", contains("cat")])
    ```
    ```{python}
    import polars as pl
    import pytimetk as tk

    pl_df = pl.DataFrame({"grp": [1, 1], "value": [10, 20], "extra": [0.1, 0.2]})
    tk.resolve_column_selection(pl_df, ["value"])
    ```
    """
    def _resolve_single(selector) -> List[str]:
        pass
    pass
