import pandas as pd
import polars as pl
import pandas_flavor as pf

from functools import partial

from pytimetk.utils.parallel_helpers import conditional_tqdm, get_threads
from pytimetk.utils.ray_helpers import run_ray_tasks

from pytimetk.utils.checks import (
    check_dataframe_or_groupby,
    check_date_column,
    check_value_column,
    check_installed,
)

from typing import Optional, Union

from pytimetk.utils.dataframe_ops import (
    convert_to_engine,
    normalize_engine,
    restore_output_type,
    conversion_to_pandas,
    resolve_pandas_groupby_frame,
)

try:
    from tsfeatures import (
        acf_features,
        arch_stat,
        crossing_points,
        entropy,
        flat_spots,
        heterogeneity,
        holt_parameters,
        lumpiness,
        nonlinearity,
        pacf_features,
        stl_features,
        stability,
        hw_parameters,
        unitroot_kpss,
        unitroot_pp,
        series_length,
        hurst,
    )
    from tsfeatures.tsfeatures import _get_feats
except ImportError:
    pass

dict_freqs = {"H": 24, "D": 1, "M": 12, "Q": 4, "W": 1, "Y": 1}


@pf.register_groupby_method
@pf.register_dataframe_method
def ts_features(
    data: Union[
        pd.DataFrame,
        pd.core.groupby.generic.DataFrameGroupBy,
        pl.DataFrame,
        pl.dataframe.group_by.GroupBy,
    ],
    date_column: str,
    value_column: str,
    features: Optional[list] = None,
    freq: Optional[str] = None,
    scale: bool = True,
    threads: Optional[int] = 1,
    show_progress: bool = True,
    engine: str = "pandas",
) -> Union[pd.DataFrame, pl.DataFrame]:
    """
    Extracts aggregated time series features from a DataFrame or DataFrameGroupBy object using the `tsfeatures` package.

    Note: Requires the `tsfeatures` package to be installed.

    Parameters
    ----------
    data : DataFrame or GroupBy (pandas or polars)
        The `data` parameter is the input data that can be either a pandas/polars
        DataFrame or a grouped DataFrame. It contains the time series data that
        you want to extract features from.
    date_column : str
        The `date_column` parameter is the name of the column in the input data
        that contains the dates or timestamps of the time series data.
    value_column : str
        The `value_column` parameter is the name of the column in the DataFrame
        that contains the time series values.
    features : list
        The `features` parameter is a list of functions that represent the time
        series features to be extracted. Each function should take a time series
        as input and return a scalar value as output.

        When `None`, uses the default list of features:
        - acf_features
        - arch_stat
        - crossing_points
        - entropy
        - flat_spots
        - heterogeneity
        - holt_parameters
        - lumpiness
        - nonlinearity
        - pacf_features
        - stl_features
        - stability
        - hw_parameters
        - unitroot_kpss
        - unitroot_pp
        - series_length
        - hurst

    freq : str
        The `freq` parameter specifies the frequency of the time series data.
        It is used to calculate features that are dependent on the frequency,
        such as seasonal features.

        - The frequency can be specified as a string, such as 'D' for daily, 'W'
          for weekly, 'M' for monthly.

        - The frequency can be a numeric value representing the number of
          observations per year, such as 365 for daily, 52 for weekly, 12 for
          monthly.
    scale : bool, optional
        The `scale` parameter in the `ts_features` function determines whether
        or not to scale the extracted features.
        - If `scale` is set to `True`, the features will be scaled using z-score
          normalization.
        - If `scale` is set to `False`, the features will not be scaled.
    threads : Optional[int]
        The `threads` parameter is an optional parameter that specifies the
        number of threads to use for parallel processing.
        - If is `None`, tthe function will use all available threads on the system.
        - If is -1, the function will use all available threads on the system.
    show_progress : bool
        The `show_progress` parameter is a boolean parameter that determines
        whether or not to show a progress bar when extracting features.
    engine : {"pandas", "polars", "auto"}, optional
        Execution engine. ``"pandas"`` (default) performs the computation using pandas.
        ``"polars"`` converts the result to a polars DataFrame on return. ``"auto"``
        infers the engine from the input data.

    Returns
    -------
    DataFrame
        A DataFrame containing the extracted time series features. If grouped data is provided,
        the DataFrame will contain the grouping columns as well. The concrete type matches the
        engine used to process the data.

    Notes
    -----
    ## Performance

    This function uses Ray-based parallel processing to speed up computation for large
    datasets with many time series groups:

    Parallel processing has overhead and may not be faster on small datasets.

    To use parallel processing, set `threads = -1` (or any value other than ``1``) to
    use Ray workers across the available processors.

    Examples
    --------
    ```{python}
    import pandas as pd
    import pytimetk as tk

    # tsfeatures comes with these features:
    from tsfeatures import (
        acf_features, arch_stat, crossing_points,
        entropy, flat_spots, heterogeneity,
        holt_parameters, lumpiness, nonlinearity,
        pacf_features, stl_features, stability,
        hw_parameters, unitroot_kpss, unitroot_pp,
        series_length, hurst
    )

    df = tk.load_dataset('m4_daily', parse_dates = ['date'])

    # Example 1 - Grouped DataFrame
    # Feature Extraction
    feature_df = (
        df
            .groupby('id')
            .ts_features(
                date_column   = 'date',
                value_column  = 'value',
                features      = [acf_features, hurst],
                freq          = 7,
                threads       = 1,
                show_progress = True
            )
    )
    feature_df
    ```

    ```{python}
    # Polars DataFrame using the tk accessor
    import pandas as pd
    import polars as pl

    from tsfeatures import acf_features, hurst

    sample = pd.DataFrame(
        {
            "date": pd.date_range(start="2020-01-01", periods=10, freq="D"),
            "value": range(10),
        }
    )

    pl_df = pl.from_pandas(sample)

    pl_df.tk.ts_features(
        date_column='date',
        value_column='value',
        features=[acf_features, hurst],
        show_progress=False,
    )
    ```
    """
    pass


def _ts_features_pandas(
    data: Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy],
    *,
    date_column: str,
    value_column: str,
    features: Optional[list],
    freq: Optional[str],
    scale: bool,
    threads: Optional[int],
    show_progress: bool,
) -> pd.DataFrame:
    pass


def _tsfeatures_ray_worker(name, group, freq, scale, features_to_use):
    pass
