import pandas as pd

from .steady_state import steady_state

def trim(df: pd.DataFrame, start_time: float) -> pd.DataFrame:
    """Input a DataFrame and trim all variables from the start of the steady-state region.

    Args:
        df (pd.DataFrame): DataFrame containing time-series data.
        start_time (float): Start time to trim the DataFrame.

    Returns:
        pd.DataFrame: Trimmed DataFrame starting from the specified start time
    
    Raises:
        TypeError: If the df is not a pandas DataFrame.
        TypeError: If the start_time is not of type float.
        ValueError: If the start_time is not present in the DataFrame.
    """
    # Check if df is a pandas DataFrame
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input df must be a pandas DataFrame. Consider preprocessing data " \
                         "with the load_file function.")

    # Check if start_time is of type float
    if not isinstance(start_time, float):
        raise TypeError("Input start_time must be of type float.")

    # Check if start_time is present in the DataFrame
    if start_time not in df["time"].values:
        raise ValueError("Input start_time is not present in the DataFrame.")

    return df[df["time"] >= start_time]

def stats(df: pd.DataFrame, variable: str | list = None) -> dict:
    """Compute statistics for specified variable(s) in a DataFrame.

    Args:
        df (pd.DataFrame): DataFrame containing time-series data.
        variable (str or list, optional): Variable(s) to compute statistics for. If None, computes all.
            Defaults to None.
    
    Returns:
        dict: Dictionary containing statistics for the specified variable(s).

    Raises:
        TypeError: If the df is not a pandas DataFrame.
        TypeError: If the variable(s) is not of type str, list, or None.
        ValueError: If the variable(s) is not present in the DataFrame.
    """
    # Check if df is a pandas DataFrame
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input df must be a pandas DataFrame. Consider preprocessing data " \
                         "with the load_file function.")
    
    # Check if variable(s) is provided and is of correct type
    if variable is not None:
        if isinstance(variable, str):
            variable = [variable]
        elif not isinstance(variable, list):
            raise TypeError("Variable(s) must be a string or a list of strings.")

        # Retrieve all eligible variables if no specific variable(s) is provided
        variable = [var for var in df.columns if var is not "time"]

    # Check if variable(s) is present in the DataFrame
    for var in variable:
        if var not in df.columns:
            raise ValueError(f"Input variable {var} is not present in the DataFrame.")

    dict_stats = {}
    for var in variable:
        mean = df[var].mean()
        median = df[var].median()
        std = df[var].std()
        var = df[var].var()
        sem = df[var].sem()
        cv = std / mean
        mad = (df[var] - mean).abs().mean()
        min = df[var].min()
        max = df[var].max()
        ptp = max - min
        size = len(df[var])
        q1 = df[var].quantile(0.25)
        q3 = df[var].quantile(0.75)
        iqr = q3 - q1

        dict_stats[var] = {
            "mean": mean,
            "median": median,
            "std": std,
            "var": var,
            "sem": sem,
            "cv": cv,
            "mad": mad,
            "min": min,
            "max": max,
            "ptp": ptp,
            "size": size,
            "q1": q1,
            "q3": q3,
            "iqr": iqr,
        }

    return dict_stats