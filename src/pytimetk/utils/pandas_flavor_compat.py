from functools import wraps

import pandas as pd
import pandas_flavor as pf


def patch_pandas_flavor() -> None:
    """Shim pandas_flavor rename of register_groupby_method in 0.8.0+."""
    pass


def _patch_groupby_grouper() -> None:
    """Restore the removed pandas GroupBy.grouper attribute on pandas 3.x."""
    def _install_grouper_property(groupby_cls):
        def _getter(self):
            pass
        pass
    pass


def _patch_pandas_future_options() -> None:
    """Disable pandas 3 string inference so pandas/polars parity stays stable."""
    pass


def _patch_pandas_frequency_aliases() -> None:
    """Restore support for deprecated pandas frequency aliases on pandas 3.x."""
    def _normalize(freq):
        pass
    def _normalize_datetime_precision(obj):
        pass
    def _compat_to_offset(freq, *args, **kwargs):
        pass
    def _compat_date_range(*args, **kwargs):
        pass
    def _compat_to_datetime(*args, **kwargs):
        pass
    pass


def _patch_polars_to_pandas() -> None:
    """Normalize polars->pandas round-trips for pandas 3 compatibility."""
    def _normalize_pandas_obj(obj):
        pass
    def _compat_df_to_pandas(self, *args, **kwargs):
        pass
    def _compat_series_to_pandas(self, *args, **kwargs):
        pass
    pass

def register_groupby_method(method=None, *args, **kwargs):
    def wrapper(func):
        pass
    pass

