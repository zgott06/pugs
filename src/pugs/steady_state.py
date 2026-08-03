import numpy as np
import pandas as pd
from scipy import stats 

def steady_state(df: pd.DataFrame, variable: str, method: str = "threshold", **kwargs) -> float:
    """Input a DataFrame to detect start of steady-state region (if any) for a specified variable using a specified method.

    Args:
        df (pd.DataFrame): DataFrame containing time-series data.
        variable (str): Variable to analyze for steady-state detection.
        method (str, optional): Method to use for steady-state detection.
            Options are "threshold", "adf", "acf", or "fourier". Defaults to "threshold".
        **kwargs: Additional keyword arguments for specific methods.
    
    Returns:
        float: Steady-state start time if detected, otherwise None.
    
    Raises:
        TypeError: If the df is not a pandas DataFrame.
        TypeError: If the variable is not of type str.
        ValueError: If the variable is not present in the DataFrame.
        KeyError: If the method is not one of the supported options.
    """
    # Check if df is a pandas DataFrame
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input df must be a pandas DataFrame. Consider pre-processing data with the load_file function.")

    # Check if variable is a string
    if not isinstance(variable, str):
        raise TypeError(f"Variable {variable} must be a string.")

    # Check if variable is present in the DataFrame
    if variable not in df.columns:
        raise ValueError(f"Variable {variable} is not present in the DataFrame.")

    # Define map of methods to corresponding functions
    method_map = {
        "threshold": _threshold,
        "adf": _adf,
        "acf": _acf,
        "fourier": _fourier
    } 

    # Check if the method is supported
    if not isinstance(method, str) or method not in method_map:
        raise KeyError(f"Method {method} is not supported. Please choose from: {list(method_map.keys())}")

    # Call appropriate method
    return method_map[method](df, variable, **kwargs)

def _threshold(df: pd.DataFrame, variable: str, threshold: float = 0.05) -> float:
    pass

def _adf(df: pd.DataFrame, variable: str) -> float:
    pass

def _acf(df: pd.DataFrame, variable: str) -> float:
    pass

def _fourier(df: pd.DataFrame, variable: str) -> float:
    pass