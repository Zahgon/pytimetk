import inspect
import numpy as np
import pandas as pd
import polars as pl

from dataclasses import dataclass
from typing import Any, Literal, Optional, Sequence, Tuple, Union

try:  # Optional dependency; imported lazily when available
    import cudf  # type: ignore
    from cudf.core.groupby.groupby import DataFrameGroupBy as CudfDataFrameGroupBy
except ImportError:  # pragma: no cover - GPU support optional
    cudf = None  # type: ignore
    CudfDataFrameGroupBy = None  # type: ignore

from pytimetk.utils.polars_helpers import collect_lazyframe


def resolve_pandas_groupby_frame(
    groupby: pd.core.groupby.generic.DataFrameGroupBy,
) -> pd.DataFrame:
    """
    Retrieve the underlying pandas DataFrame backing a GroupBy object.

    The pandas-accelerated cudf proxy does not guarantee the public ``obj``
    attribute, so we look through a handful of internal hooks and gracefully
    degrade when only cudf frames are available by converting back to pandas.
    """
    pass


def _patch_groupby_obj_access() -> None:
    """
    Ensure pandas-style GroupBy objects expose an ``obj`` attribute even when
    accelerated backends (e.g., cudf.pandas) replace the implementation.
    """
    def _getter(self):
        pass
    def _setter(self, value):
        pass
    pass


_patch_groupby_obj_access()


PandasLike = Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy]
PolarsLike = Union[pl.DataFrame, pl.dataframe.group_by.GroupBy]
CudfLike = Union["cudf.DataFrame", "cudf.core.groupby.groupby.DataFrameGroupBy"]
AnyFrame = Union[PandasLike, PolarsLike, CudfLike, "pl.LazyFrame"]

FrameKind = Literal[
    "pandas_df",
    "pandas_groupby",
    "polars_df",
    "polars_groupby",
    "polars_lazy",
    "cudf_df",
    "cudf_groupby",
]

ROW_ID_BASE = "__pytimetk_row_id__"


@dataclass
class FrameConversion:
    data: Union[PandasLike, PolarsLike, Any]
    original_kind: FrameKind
    row_id_column: Optional[str] = None
    pandas_index: Optional[pd.Index] = None
    group_columns: Optional[Sequence[str]] = None
    pandas_cache: Optional[pd.DataFrame] = None


def identify_frame_kind(data: AnyFrame) -> FrameKind:
    pass


def normalize_engine(
    engine: Optional[str],
    data: AnyFrame,
) -> Literal["pandas", "polars", "cudf"]:
    """
    Normalise the engine parameter. Defaults to the backend implied by the input data.
    """
    pass


def convert_to_engine(
    data: AnyFrame,
    engine: Literal["pandas", "polars", "cudf"],
) -> FrameConversion:
    """
    Ensure the data matches the target engine. Returns conversion metadata that
    can be used to restore the result to the original input type.
    """
    pass


def restore_output_type(
    result: Union[pd.DataFrame, pl.DataFrame, Any],
    conversion: FrameConversion,
) -> Union[pd.DataFrame, pl.DataFrame, Any]:
    """
    Convert the result back to the type implied by the original input.
    """
    pass


def conversion_to_pandas(
    conversion: FrameConversion,
) -> Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy]:
    """
    Convenience helper that converts the stored frame within a conversion object
    to its pandas representation. When the conversion originates from a pandas
    -> polars transformation a temporary row identifier may exist; this helper
    strips that column before returning the pandas frame.
    """
    pass


def ensure_row_id_column(
    frame: pl.DataFrame,
    existing_column: Optional[str] = None,
) -> Tuple[pl.DataFrame, str, bool]:
    """
    Ensure a row identifier column exists on the provided polars frame.
    Returns the frame (possibly modified), the column name, and a flag indicating
    whether the column was generated within this function.
    """
    pass


def _make_temp_column(columns: Sequence[str], base: str = ROW_ID_BASE) -> str:
    pass


def _extract_polars_group_columns(
    groupby: pl.dataframe.group_by.GroupBy,
) -> Sequence[str]:
    pass


def _extract_pandas_group_columns(
    groupby: pd.core.groupby.generic.DataFrameGroupBy,
) -> Sequence[str]:
    pass


def pandas_groupby_apply(
    groupby: pd.core.groupby.generic.DataFrameGroupBy,
    func,
    *args,
    include_groups: Optional[bool] = None,
    **kwargs,
):
    """Call pandas GroupBy.apply while bridging pandas 2/3 include_groups semantics."""
    pass


def pandas_groupby_default_includes_groups(
    groupby: pd.core.groupby.generic.DataFrameGroupBy,
) -> bool:
    """Return whether the current pandas GroupBy.apply default includes group columns."""
    pass


def _normalize_polars_temporal_columns(frame: pl.DataFrame) -> pl.DataFrame:
    """Cast datetime columns to nanosecond precision for pandas parity."""
    pass


def _extract_cudf_group_columns(
    groupby: "cudf.core.groupby.groupby.DataFrameGroupBy",
) -> Sequence[str]:
    pass


def resolve_polars_group_columns(
    data: Union[pl.DataFrame, pl.dataframe.group_by.GroupBy],
    group_columns: Optional[Sequence[str]] = None,
) -> Sequence[str]:
    """
    Resolve the list of polars group columns from either stored metadata or the
    groupby object itself.
    """
    pass


def _engine_for_kind(kind: FrameKind) -> Literal["pandas", "polars", "cudf"]:
    pass
