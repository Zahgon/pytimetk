"""Compatibility utilities for bridging Polars API differences."""

from __future__ import annotations

import inspect
from functools import lru_cache
from typing import Any, Dict

import polars as pl


@lru_cache(maxsize=None)
def _polars_supports_min_samples() -> bool:
    """Return True if the current Polars version accepts `min_samples`."""
    pass


def ensure_polars_rolling_kwargs(kwargs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Translate rolling keyword arguments to match the runtime Polars version.

    Polars < 1.3 expects `min_periods` whereas newer versions use `min_samples`.
    This helper rewrites whichever key is missing so callers can always supply
    `min_samples` in their source code.
    """
    pass
