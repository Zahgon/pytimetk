import pandas as pd
import polars as pl
import numpy as np
import pandas_flavor as pf

from typing import Union

from pytimetk.utils.dataframe_ops import (
    convert_to_engine,
    normalize_engine,
    restore_output_type,
    conversion_to_pandas,
    resolve_pandas_groupby_frame,
)


@pf.register_groupby_method
@pf.register_dataframe_method
def binarize(
    data: Union[
        pd.DataFrame,
        pd.core.groupby.generic.DataFrameGroupBy,
        pl.DataFrame,
        pl.dataframe.group_by.GroupBy,
    ],
    n_bins: int = 4,
    thresh_infreq: float = 0.01,
    name_infreq: str = "-OTHER",
    one_hot: bool = True,
    engine: str = "pandas",
) -> Union[pd.DataFrame, pl.DataFrame]:
    """The `binarize` function prepares data for `correlate`, which is used for analyzing correlationfunnel plots.

    Binarization does the following:

    1. Takes in a pandas DataFrame or DataFrameGroupBy object, converts non-numeric
    columns to categorical,
    2. Replaces boolean columns with integers,
    3. Checks for data type and missing
    values,
    4. fixes low cardinality numeric data,
    5. fixes high skew numeric data, and
    6. finally applies a
    transformation to create a new DataFrame with binarized data.

    Parameters
    ----------
    data : DataFrame or GroupBy (pandas or polars)
        The `data` parameter is the input data that you want to binarize. It can be either a pandas/polars
        DataFrame or a grouped object.
    n_bins : int
        The `n_bins` parameter specifies the number of bins to use when binarizing numeric data. It is used
        in the `create_recipe` function to determine the number of bins for each numeric column.
        `pd.qcut()` is used to bin the numeric data.
    thresh_infreq : float
        The `thresh_infreq` parameter is a float that represents the threshold for infrequent categories.
        Categories that have a frequency below this threshold will be grouped together and labeled with the
        name specified in the `name_infreq` parameter. By default, the threshold is set to 0.01.
    name_infreq : str
        The `name_infreq` parameter is used to specify the name that will be assigned to the category
        representing infrequent values in a column. This is applicable when performing binarization on
        non-numeric columns. By default, the name assigned is "-OTHER".
    one_hot : bool
        The `one_hot` parameter is a boolean flag that determines whether or not to perform one-hot
        encoding on the categorical variables after binarization. If `one_hot` is set to `True`, the
        categorical variables will be one-hot encoded, creating binary columns for each unique category.
    engine : {"pandas", "polars", "auto"}, optional
        Execution engine. ``"pandas"`` (default) performs the computation using pandas.
        ``"polars"`` converts the result to a polars DataFrame on return. ``"auto"``
        infers the engine from the input data.

    Returns
    -------
        The function `binarize` returns the transformed data after applying various data preprocessing
        steps such as converting non-numeric columns to categorical, replacing boolean columns with
        integers, fixing low cardinality numeric data, fixing high skew numeric data, and creating a recipe
        for binarization. The concrete DataFrame type matches the engine used to process the data.

    See Also
    --------
    - `correlate()` : Calculates the correlation between a target variable and all other variables in a pandas DataFrame.

    Examples
    --------

    ``` {python}
    # NON-TIMESERIES EXAMPLE ----

    import pandas as pd
    import numpy as np
    import pytimetk as tk

    # Set a random seed for reproducibility
    np.random.seed(0)

    # Define the number of rows for your DataFrame
    num_rows = 200

    # Create fake data for the columns
    data = {
        'Age': np.random.randint(18, 65, size=num_rows),
        'Gender': np.random.choice(['Male', 'Female'], size=num_rows),
        'Marital_Status': np.random.choice(['Single', 'Married', 'Divorced'], size=num_rows),
        'City': np.random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Miami'], size=num_rows),
        'Years_Playing': np.random.randint(0, 30, size=num_rows),
        'Average_Income': np.random.randint(20000, 100000, size=num_rows),
        'Member_Status': np.random.choice(['Bronze', 'Silver', 'Gold', 'Platinum'], size=num_rows),
        'Number_Children': np.random.randint(0, 5, size=num_rows),
        'Own_House_Flag': np.random.choice([True, False], size=num_rows),
        'Own_Car_Count': np.random.randint(0, 3, size=num_rows),
        'PersonId': range(1, num_rows + 1),  # Add a PersonId column as a row count
        'Client': np.random.choice(['A', 'B'], size=num_rows)  # Add a Client column with random values 'A' or 'B'
    }

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Binarize the data
    df_binarized = df.binarize(n_bins=4, thresh_infreq=0.01, name_infreq="-OTHER", one_hot=True)

    df_binarized.glimpse()
    ```

    ``` {python}
    df_correlated = df_binarized.correlate(target='Member_Status__Platinum')
    df_correlated.head(10)
    ```

    ``` {python}
    # Interactive
    df_correlated.plot_correlation_funnel(
        engine='plotly',
        height=600
    )
    ```

    ``` {python}
    # Static
    df_correlated.plot_correlation_funnel(
        engine ='plotnine',
        height = 900
    )
    ```

    """
    pass


def _binarize_pandas(
    data: Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy],
    *,
    n_bins: int,
    thresh_infreq: float,
    name_infreq: str,
    one_hot: bool,
) -> pd.DataFrame:
    pass


@pf.register_groupby_method
@pf.register_dataframe_method
def correlate(
    data: Union[
        pd.DataFrame,
        pd.core.groupby.generic.DataFrameGroupBy,
        pl.DataFrame,
        pl.dataframe.group_by.GroupBy,
    ],
    target: str,
    method: str = "pearson",
    engine: str = "pandas",
) -> Union[pd.DataFrame, pl.DataFrame]:
    """The `correlate` function calculates the correlation between a target variable and all other
    variables in a pandas DataFrame, and returns the results sorted by absolute correlation in
    descending order.

    Parameters
    ----------
    data : DataFrame or GroupBy (pandas or polars)
        The `data` parameter is the input data that you want to calculate correlations for. It can be
        either a pandas/polars DataFrame or a grouped DataFrame obtained from a groupby operation.
    target : str
        The `target` parameter is a string that represents the column name in the DataFrame for which you
        want to calculate the correlation with other columns.
    method : str, default = 'pearson'
        The `method` parameter in the `correlate` function is used to specify the method for calculating
        the correlation coefficient. The available options for the `method` parameter are:

        * pearson : standard correlation coefficient
        * kendall : Kendall Tau correlation coefficient
        * spearman : Spearman rank correlation
    engine : {"pandas", "polars", "auto"}, optional
        Execution engine. ``"pandas"`` (default) performs the computation using pandas.
        ``"polars"`` converts the result to a polars DataFrame on return. ``"auto"``
        infers the engine from the input data.


    Returns
    -------
        The function `correlate` returns a DataFrame with two columns: 'feature' and 'correlation'. The
        'feature' column contains the names of the features in the input data, and the 'correlation' column
        contains the correlation coefficients between each feature and the target variable. The DataFrame is
        sorted in descending order based on the absolute correlation values. The concrete type matches the
        engine used to process the data.

    See Also
    --------
    - `binarize()` : Prepares data for `correlate`, which is used for analyzing correlationfunnel plots.

    Examples
    --------

    ``` {python}
    # NON-TIMESERIES EXAMPLE ----

    import pandas as pd
    import numpy as np
    import pytimetk as tk

    # Set a random seed for reproducibility
    np.random.seed(0)

    # Define the number of rows for your DataFrame
    num_rows = 200

    # Create fake data for the columns
    data = {
        'Age': np.random.randint(18, 65, size=num_rows),
        'Gender': np.random.choice(['Male', 'Female'], size=num_rows),
        'Marital_Status': np.random.choice(['Single', 'Married', 'Divorced'], size=num_rows),
        'City': np.random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Miami'], size=num_rows),
        'Years_Playing': np.random.randint(0, 30, size=num_rows),
        'Average_Income': np.random.randint(20000, 100000, size=num_rows),
        'Member_Status': np.random.choice(['Bronze', 'Silver', 'Gold', 'Platinum'], size=num_rows),
        'Number_Children': np.random.randint(0, 5, size=num_rows),
        'Own_House_Flag': np.random.choice([True, False], size=num_rows),
        'Own_Car_Count': np.random.randint(0, 3, size=num_rows),
        'PersonId': range(1, num_rows + 1),  # Add a PersonId column as a row count
        'Client': np.random.choice(['A', 'B'], size=num_rows)  # Add a Client column with random values 'A' or 'B'
    }

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Binarize the data
    df_binarized = df.binarize(n_bins=4, thresh_infreq=0.01, name_infreq="-OTHER", one_hot=True)

    df_binarized.glimpse()
    ```

    ``` {python}
    df_correlated = df_binarized.correlate(target='Member_Status__Platinum')
    df_correlated
    ```

    ``` {python}
    # Interactive
    df_correlated.plot_correlation_funnel(
        engine='plotly',
        height=400
    )
    ```

    ``` {python}
    # Static
    fig = df_correlated.plot_correlation_funnel(
        engine ='plotnine',
        height = 600
    )
    fig
    ```

    ``` {python}
    # Polars DataFrame using the tk accessor
    import pandas as pd
    import polars as pl


    sample = pd.DataFrame(
        {
            "Outcome": ["Yes", "No", "Yes", "No"],
            "Segment": ["A", "A", "B", "B"],
        }
    )

    pl_df = pl.from_pandas(sample)

    binarized = pl_df.tk.binarize(
        n_bins=2,
        thresh_infreq=0.0,
        name_infreq="-OTHER",
        one_hot=True,
    )

    binarized.tk.correlate(target='Outcome__Yes')
    ```

    """
    pass


def _correlate_pandas(
    data: Union[pd.DataFrame, pd.core.groupby.generic.DataFrameGroupBy],
    *,
    target: str,
    method: str,
) -> pd.DataFrame:
    pass


# UTILITIES ----


def check_data_type(data, classes_not_allowed, fun_name=None):
    pass


def check_missing(data, fun_name=None):
    pass


def fix_low_cardinality_numeric(data, thresh):
    # Converts numeric columns with number of unique values <= thresh to categorical
    pass


def fix_high_skew_numeric_data(data, unique_limit):
    # Converts numeric columns with number of unique quantile values <= limit to categorical
    pass


def create_recipe(data, n_bins, thresh_infreq, name_infreq, one_hot):
    # Recipe creation steps (similar to R code)
    pass


def logical_to_integer(data):
    # Convert logical columns to integer
    pass
