import numpy as np
import pandas as pd
from scipy import stats 

def steady_state(df: pd.DataFrame, variable: str, method: str = "std", **kwargs) -> float:
    """Input a DataFrame to detect the start of the steady-state region (if any) for a
        specified variable using a specified method.

    Args:
        df (pd.DataFrame): DataFrame containing time-series data.
        variable (str): Variable to analyze for steady-state detection.
        method (str, optional): Method to use for steady-state detection.
            Options are "std", "linreg", "adf", "acf", or "fourier". Defaults to "std".
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
        raise TypeError("Input df must be a pandas DataFrame. Consider preprocessing data " \
                        "with the load_file function.")

    # Check if variable is of type string
    if not isinstance(variable, str):
        raise TypeError(f"Input variable {variable} must be a string.")

    # Check if variable is present in the DataFrame
    if variable not in df.columns:
        raise ValueError(f"Input variable {variable} is not present in the DataFrame.")

    # Define map of methods to corresponding functions
    method_map = {
        "std": _std_method,
        "linreg": _linreg_method,
        "adf": _adf_method,
        "acf": _acf_method,
        "fourier": _fourier_method
    } 

    # Check if the method is supported
    if not isinstance(method, str) or method not in method_map:
        raise KeyError(f"Method {method} is not supported. Please choose from: {list(method_map.keys())}")

    # Call appropriate method
    return method_map[method](df, variable, **kwargs)

def _std_method(df: pd.DataFrame, variable: str) -> float:
    """Detect the start of the steady-state region by finding when the standard deviation
        is maximized on a forward search.

    Args:
        df (pd.DataFrame): DataFrame containing time-series data.
        variable (str): Variable to analyze for steady-state detection.

    Returns:
        float: Steady-state start time if detected, otherwise None.
    """
    # Preprocess DataFrame to extract time-series data
    t = df["time"].to_numpy()
    x = df[variable].to_numpy()
    
    # Check if signal fails to initate
    if np.max(x) < 1e-4: return None

    # Compute standard deviation over time
    stds = np.array([np.std(x[:i+1]) for i in range(len(t))])

    # Find time of maximum standard deviation
    start_time = t[np.argmax(stds)]

    return start_time

def _linreg_method(df: pd.DataFrame, variable: str, slope_tol=0.05) -> float:
    """Detect the start of the steady-state region by finding when the slope of linear
        regression is maximized on a forward search, and if the remaining data fits
        the slope tolerenace criteria.

    Args:
        df (pd.DataFrame): DataFrame containing time-series data.
        variable (str): Variable to analyze for steady-state detection.
        slope_tol (float, optional): Tolerance for the slope criteria. Defaults to 0.05.

    Returns:
        float: Steady-state start time if detected, otherwise None.
    """
    # Preprocess DataFrame to extract time-series data
    t = df["time"].to_numpy()
    x = df[variable].to_numpy()
    
    # Check if signal fails to initate
    if np.max(x) < 1e-4: return None

    # Compute slope over time
    slopes = []
    for i in range(2, len(t)):
        slopes.append(stats.linregress(t[:i], x[:i]).slope)

    # Find time of maximum slope
    slopes = np.array(slopes)
    best_idx = np.argmax(slopes) + 2
    start_time = t[best_idx]

    # Check slope tolerance
    if abs(stats.linregress(t[best_idx:], x[best_idx:]).slope) >= slope_tol:
        return None

    return start_time

def _adf_method(df: pd.DataFrame, variable: str) -> float:
    pass

def _acf_method(df: pd.DataFrame, variable: str) -> float:
    pass

def _fourier_method(df: pd.DataFrame, variable: str) -> float:
    pass