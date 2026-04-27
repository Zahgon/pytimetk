import os
import warnings
from typing import Optional

import polars as pl

from pytimetk.utils.gpu_support import is_polars_gpu_available
from pytimetk.utils.string_helpers import parse_freq_str

_GPU_WARNED = False


def pandas_to_polars_frequency(pandas_freq_str, default=(1, "d")):
    pass


def pandas_to_polars_aggregation_mapping(column_name):
    pass


def pl_quantile(**kwargs):
    """Generates configuration for the rolling quantile function in Polars."""
    pass


def update_dict(d1, d2):
    """
    Update values in dictionary `d1` based on matching keys from dictionary `d2`.

    This function will only update the values of existing keys in `d1`.
    New keys present in `d2` but not in `d1` will be ignored.
    """
    pass


def collect_lazyframe(
    lazy_frame: pl.LazyFrame,
    *,
    force_gpu: Optional[bool] = None,
) -> pl.DataFrame:
    """Collect a Polars ``LazyFrame`` while optionally attempting GPU execution.

    Parameters
    ----------
    lazy_frame : pl.LazyFrame
        The Polars lazy plan to collect.
    force_gpu : Optional[bool], optional
        When ``True`` the function attempts GPU execution even if the environment
        variable ``PYTIMETK_POLARS_GPU`` disables it. When ``False`` the GPU path
        is skipped. ``None`` (default) respects the environment variable and
        defaults to attempting the GPU when available.
    """
    pass
