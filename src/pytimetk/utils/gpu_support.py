"""
Helpers for detecting optional GPU backends.

The functions in this module are intentionally lightweight so they can be
imported without incurring heavy GPU initialisation costs. They are used by
higher-level APIs to determine whether cudf or the Polars GPU engine is
available before attempting to leverage those runtimes. All checks are
best-effort and fall back to ``False`` when optional dependencies are missing
or misconfigured to guarantee backwards compatibility for CPU-only users.
"""

from __future__ import annotations

import importlib
import importlib.util
from typing import Optional

import polars as pl

_CUDA_AVAILABLE_CACHE: Optional[bool] = None
_CUDF_AVAILABLE_CACHE: Optional[bool] = None


def is_cuda_available() -> bool:
    """
    Return True when the CUDA runtime appears usable.

    This performs a best-effort import of ``numba.cuda`` which is bundled with
    RAPIDS. Failure to import the module or to query the driver is interpreted
    as CUDA being unavailable.
    """
    pass


def is_cudf_available() -> bool:
    """
    Return True if cudf is importable.

    We avoid importing cudf repeatedly by caching the result. Any exception
    raised during import is treated as cudf being unavailable to prevent crashes
    in CPU-only deployments.
    """
    pass


def cudf_version() -> Optional[str]:
    """
    Return the cudf version if available, otherwise ``None``.
    """
    pass


def is_polars_gpu_available() -> bool:
    """
    Check whether the Polars GPU engine API is present.

    This does not validate that an NVIDIA device is present; it merely asserts
    that the runtime was installed with GPU support (``polars[gpu]``).
    """
    pass


__all__ = [
    "cudf_version",
    "is_cuda_available",
    "is_cudf_available",
    "is_polars_gpu_available",
]
