import numpy as np
import pandas as pd
import pandas_flavor as pf
from pytimetk.utils.dataframe_ops import resolve_pandas_groupby_frame

from typing import Union


@pf.register_groupby_method
@pf.register_dataframe_method
def reduce_memory_usage(
    data: Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy],
    *,
    convert_string_to_categorical: bool = True,
    inplace: bool = False,
):
    """
    Iterate through all columns of a Pandas DataFrame and modify the dtypes to reduce memory usage.

    Parameters:
    -----------
    data: pd.DataFrame
        Input dataframe to reduce memory usage.
    convert_string_to_categorical: bool, default True
        Convert string/object columns to categoricals when safe. Set to False to keep string dtype.
    inplace: bool, default False
        When True, mutate the supplied DataFrame (or backing GroupBy frame) in place instead of creating a copy.

    Returns:
    --------
    pd.DataFrame
      Dataframe with reduced memory usage.

    """
    pass


def _reduce_memory(
    data: pd.DataFrame,
    *,
    convert_string_to_categorical: bool = True,
    inplace: bool = False,
    # categorical_threshold: int = 100
):
    pass


def _convert_boolean_to_int8(data, col):
    """
    Convert a boolean column to int8 to save memory.
    """
    pass
