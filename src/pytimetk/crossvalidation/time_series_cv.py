import pandas as pd
import numpy as np

import plotly.graph_objects as go

from sklearn.model_selection import BaseCrossValidator

from timebasedcv import TimeBasedSplit
from timebasedcv.splitstate import SplitState
from timebasedcv.utils._types import ModeType
from timebasedcv.utils._types import TensorLike
from timebasedcv.utils._types import NullableDatetime
from timebasedcv.utils._types import SeriesLike
from timebasedcv.utils._types import DateTimeLike

from typing import Generator
from typing import Tuple
from typing import TypeVar
from typing import Union
from typing import Optional

from pytimetk.plot.theme import palette_timetk

TL = TypeVar("TL", bound=TensorLike)


class TimeSeriesCV(TimeBasedSplit):
    """
    `TimeSeriesCV` is a subclass of `TimeBasedSplit` with default mode set to 'backward'
    and an optional `split_limit` to return the first `n` slices of time series cross-validation sets.

    Parameters
    ----------
    frequency: str
        The frequency (or time unit) of the time series. Must be one of "days", "seconds", "microseconds",
        "milliseconds", "minutes", "hours", "weeks", "months" or "years". These are the valid values for the
        `unit` argument of `relativedelta` from python `dateutil` library.
    train_size: int
        Defines the minimum number of time units required to be in the train set.
    forecast_horizon: int
        Specifies the number of time units to forecast.
    gap: int
        Sets the number of time units to skip between the end of the train set and the start of the forecast set.
    stride: int
        How many time unit to move forward after each split. If `None` (or set to 0), the stride is equal to the
        `forecast_horizon` quantity.
    window:
        The type of window to use, either "rolling" or "expanding".
    mode: ModeType, optional
        The mode to use for cross-validation. Default is 'backward'.
    split_limit: int, optional
        The maximum number of splits to return. If not provided, all splits are returned.

    Raises:
    ----------
    ValueError:

    - If `frequency` is not one of "days", "seconds", "microseconds", "milliseconds", "minutes", "hours",
    "weeks".
    - If `window` is not one of "rolling" or "expanding".
    - If `mode` is not one of "forward" or "backward"
    - If `train_size`, `forecast_horizon`, `gap` or `stride` are not strictly positive.

    TypeError:

    If `train_size`, `forecast_horizon`, `gap` or `stride` are not of type `int`.

    Examples:
    ---------

    ``` {python}
    import pandas as pd
    import numpy as np
    from pytimetk import TimeSeriesCV

    RNG = np.random.default_rng(seed=42)

    dates = pd.Series(pd.date_range("2023-01-01", "2023-01-31", freq="D"))
    size = len(dates)

    df = (
        pd.concat(
            [
                pd.DataFrame(
                    {
                        "time": pd.date_range(start, end, periods=_size, inclusive="left"),
                        "a": RNG.normal(size=_size - 1),
                        "b": RNG.normal(size=_size - 1),
                    }
                )
                for start, end, _size in zip(dates[:-1], dates[1:], RNG.integers(2, 24, size - 1))
            ]
        )
        .reset_index(drop=True)
        .assign(y=lambda t: t[["a", "b"]].sum(axis=1) + RNG.normal(size=t.shape[0]) / 25)
    )

    # Set index
    df.set_index("time", inplace=True)

    # Create an X dataframeand y series
    X, y = df.loc[:, ["a", "b"]], df["y"]

    # Initialize TimeSeriesCV with desired parameters
    tscv = TimeSeriesCV(
        frequency="days",
        train_size=10,
        forecast_horizon=5,
        gap=0,
        stride=0,
        split_limit=3  # Limiting to 3 splits
    )

    tscv
    ```

    ``` {python}
    # Creates a split generator
    splits = tscv.split(X, y)

    for X_train, X_forecast, y_train, y_forecast in splits:
        print(X_train)
        print(X_forecast)
    ```

    ``` {python}
    # Also, you can use `glimpse()` to print summary information about the splits

    tscv.glimpse(y)
    ```

    ``` {python}
    # You can also plot the splits by calling `plot()` on the `TimeSeriesCV` instance with the `y` Pandas series

    tscv.plot(y)
    ```
    """

    def __init__(
        self,
        frequency: str,
        train_size: int,
        forecast_horizon: int,
        gap: int,
        stride: int = 0,
        window: str = "rolling",
        mode: ModeType = "backward",
        split_limit: int = None,
        **kwargs,
    ):
        # Initialize the parent class
        super().__init__(
            frequency=frequency,
            train_size=train_size,
            forecast_horizon=forecast_horizon,
            gap=gap,
            stride=stride,
            window=window,
            mode=mode,
            **kwargs,
        )

        self.split_limit = split_limit

        # Assign the parameters to the class

    def split(
        self,
        *arrays: TL,
        time_series: SeriesLike[DateTimeLike] = None,
        start_dt: NullableDatetime = None,
        end_dt: NullableDatetime = None,
        return_splitstate: bool = False,
    ) -> Generator[
        Union[Tuple[TL, ...], Tuple[Tuple[TL, ...], SplitState]], None, None
    ]:
        """Returns a generator of split arrays.

        Parameters
        ----------
        *arrays: pd.DataFrame, pd.Series
            The arrays to split. Must have the same length as `time_series`.
        time_series: pd.Series
            The time series used to create boolean masks for splits. If not provided, the method will try
            to use the index of the first array (if it is a DataFrame or Series) as the time series.
        start_dt: pd.Timestamp
            The start of the time period. If provided, it is used in place of `time_series.min()`.
        end_dt: pd.Timestamp
            The end of the time period. If provided, it is used in place of `time_series.max()`.
        return_splitstate: bool
            Whether to return the `SplitState` instance for each split.

        Returns:
        -------
        A generator of tuples of arrays containing the training and forecast data. If `split_limit` is set,
        yields only up to `split_limit` splits.
        """
        pass

    def glimpse(self, *arrays: TL, time_series: SeriesLike[DateTimeLike] = None):
        """Prints summary information about the splits, focusing on the first two arrays.

        Arguments:
            *arrays:
                The arrays to split. Only the first one will be used for summary information.
            time_series:
                The time series used for splitting. If not provided, the index of the first array is used. Default is None.
        """
        pass

    def plot(
        self,
        y: pd.Series,
        time_series: pd.Series = None,
        color_palette: Optional[Union[dict, list, str]] = None,
        bar_height: float = 0.3,
        title: str = "Time Series Cross-Validation Plot",
        x_lab: str = "",
        y_lab: str = "Fold",
        x_axis_date_labels: str = None,
        base_size: float = 11,
        width: Optional[int] = None,
        height: Optional[int] = None,
        engine: str = "plotly",
    ):
        """Plots the cross-validation folds on a single plot with folds on the y-axis and dates on the x-axis using filled Scatter traces.

        Parameters
        ----------
        y : pd.Series
            The target time series as a pandas Series.
        time_series : pd.Series
            The time series used for splitting. If not provided, the index of `y` is used. Default is None.
        color_palette : Optional[Union[dict, list, str]]
            The color palette to use for the train and forecast. If not provided, the default colors are used.
        bar_height : float
            The height of each bar in the plot. Default is 0.3.
        title : str
            The title of the plot. Default is "Time Series Cross-Validation Plot".
        x_lab : str
            The label for the x-axis. Default is "".
        y_lab : str
            The label for the y-axis. Default is "Fold".
        x_axis_date_labels : str
            The format of the date labels on the x-axis. Default is None.
        base_size : float
            The base font size for the plot. Default is 11.
        width : Optional[int]
            The width of the plot in pixels. Default is None.
        height : Optional[int]
            The height of the plot in pixels. Default is None.
        engine : str
            The plotting engine to use. Default is "plotly".
        """
        pass


class TimeSeriesCVSplitter(BaseCrossValidator):
    """The `TimeSeriesCVSplitter` is a scikit-learn compatible cross-validator using `TimeSeriesCV`.

    This cross-validator generates splits based on time values, making it suitable for time series data.

    Parameters:
    -----------
    frequency: str
        The frequency (or time unit) of the time series. Must be one of "days", "seconds", "microseconds",
        "milliseconds", "minutes", "hours", "weeks", "months" or "years". These are the valid values for the
        `unit` argument of `relativedelta` from python `dateutil` library.
    train_size: int
        Minimum number of time units in the training set.
    forecast_horizon: int
        Number of time units to forecast in each split.
    time_series: pd.Series
        A pandas Series or Index representing the time values.
    gap: int
        Number of time units to skip between training and testing sets.
    stride: int
        Number of time units to move forward after each split.
    window: str
        Type of window, either "rolling" or "expanding".
    mode: str
        Order of split generation, "forward" or "backward".
    start_dt: pd.Timestamp
        Start date for the time period.
    end_dt: pd.Timestamp
        End date for the time period.
    split_limit: int
        Maximum number of splits to generate. If None, all possible splits will be generated.

    Raises:
    -------
    ValueError:
        If the input arrays are incompatible in length with the time series.

    Returns:
    --------
    A generator of tuples of arrays containing the training and forecast data.

    See Also:
    --------
    TimeSeriesCV

    Examples
    --------
    ``` {python}
    import pandas as pd
    import numpy as np

    from pytimetk import TimeSeriesCVSplitter

    start_dt = pd.Timestamp(2023, 1, 1)
    end_dt = pd.Timestamp(2023, 1, 31)

    time_series = pd.Series(pd.date_range(start_dt, end_dt, freq="D"))
    size = len(time_series)

    df = pd.DataFrame(data=np.random.randn(size, 2), columns=["a", "b"])

    X, y = df[["a", "b"]], df[["a", "b"]].sum(axis=1)

    cv = TimeSeriesCVSplitter(
        time_series=time_series,
        frequency="days",
        train_size=14,
        forecast_horizon=7,
        gap=0,
        stride=1,
        window="rolling",
    )

    cv
    ```

    ``` {python}
    # Insepct the cross-validation splits
    cv.splitter.plot(y, time_series = time_series)
    ```

    ``` {python}
    # Using the TimeSeriesCVSplitter in a scikit-learn CV model

    from sklearn.linear_model import Ridge
    from sklearn.model_selection import RandomizedSearchCV

    # Fit and get best estimator
    param_grid = {
        "alpha": np.linspace(0.1, 2, 10),
        "fit_intercept": [True, False],
        "positive": [True, False],
    }

    random_search_cv = RandomizedSearchCV(
        estimator=Ridge(),
        param_distributions=param_grid,
        cv=cv,
        n_jobs=-1,
    ).fit(X, y)

    random_search_cv.best_estimator_
    ```
    """

    def __init__(
        self,
        *,
        frequency: str,
        train_size: int,
        forecast_horizon: int,
        time_series: Union[pd.Series, pd.Index],
        gap: int = 0,
        stride: Union[int, None] = None,
        window: str = "rolling",
        mode: str = "backward",
        start_dt: pd.Timestamp = None,
        end_dt: pd.Timestamp = None,
        split_limit: int = None,
    ):
        self.splitter = TimeSeriesCV(
            frequency=frequency,
            train_size=train_size,
            forecast_horizon=forecast_horizon,
            gap=gap,
            stride=stride,
            window=window,
            mode=mode,
            split_limit=split_limit,
        )
        self.time_series_ = time_series
        self.start_dt_ = start_dt
        self.end_dt_ = end_dt
        self.n_splits = self._compute_n_splits()
        self.size_ = len(time_series)

    def split(
        self,
        X: Union[np.ndarray, None] = None,
        y: Union[np.ndarray, None] = None,
        groups: Union[np.ndarray, None] = None,
    ) -> Generator[Tuple[np.ndarray, np.ndarray], None, None]:
        """Generates train and test indices for cross-validation.

        Parameters:
        -----------
        X:
            Optional input features (ignored, for compatibility with scikit-learn).
        y:
            Optional target variable (ignored, for compatibility with scikit-learn).
        groups:
            Optional group labels (ignored, for compatibility with scikit-learn).

        Yields:
        -------
        Tuple[np.ndarray, np.ndarray]:
            Tuples of train and test indices.
        """
        pass

    def get_n_splits(
        self,
        X: Union[np.ndarray, None] = None,
        y: Union[np.ndarray, None] = None,
        groups: Union[np.ndarray, None] = None,
    ) -> int:
        """Returns the number of splits."""
        pass

    def _compute_n_splits(self) -> int:
        """Computes the number of splits based on the time period."""
        pass

    @staticmethod
    def _validate_split_args(
        size: int,
        X: Union[np.ndarray, None] = None,
        y: Union[np.ndarray, None] = None,
        groups: Union[np.ndarray, None] = None,
    ) -> None:
        """Validates that input arrays match the expected size."""
        pass
