import os
import pandas as pd
from netCDF4 import Dataset

def load_file(file: str, variable: str | list = None) -> pd.DataFrame:
    """Load a GX output file and retrieve selected variable(s).

    Args:
        file (str): GX output file path (.nc or .csv)
        variable (str or list, optional): Variable(s) to retrieve. If None, retrieves all.
            Defaults to None.

    Returns:
        pd.DataFrame: DataFrame containing the requested variable(s) time-series data.
    
    Raises:
        FileNotFoundError: If the file does not exist.
        TypeError: If the file format is not supported (neither .nc nor .csv).
    """
    # Check if the file exists
    if not os.path.isfile(file):
        raise FileNotFoundError(f"The file '{file}' does not exist.")

    # Determine file format and call appropriate loading function
    if file.endswith(".nc"):
        return _load_nc_file(file, variable=variable)
    elif file.endswith(".csv"):
        return _load_csv_file(file, variable=variable)
    else:
        raise TypeError("Unsupported file format. Please provide a .nc or .csv file.")

def _load_nc_file(file: str, variable: str | list = None) -> pd.DataFrame:
    """Load a GX output file in the form of a netCDF file and retrieve selected variable(s).
    
    Args:
        file (str): GX output file path (.nc)
        variable (str or list, optional): Variable(s) to retrieve. If None, retrieves all.
            Defaults to None.
    
    Returns:
        pd.DataFrame: DataFrame containing the request variable(s) time-series data.

    Raises:
        
    """
    pass

def _load_csv_file(file: str, variable: str | list = None) -> pd.DataFrame:
    """Load a GX output file in the form of a CSV file and retrieve selected variable(s).
    
    Args:
        file (str): GX output file path (.csv)
        variable (str or list, optional): Variable(s) to retrieve. If None, retrieves all.
            Defaults to None.
    
    Returns:
        pd.DataFrame: DataFrame containing the request variable(s) time-series data.
    
    Raises:
        TypeError: If the variable(s) is not of type str or list.
        ValueError: If the variable(s) is not present in the CSV file.
    """
    # Load the file into a DataFrame
    df = pd.read_csv(file)
    
    # Check if variable(s) is provided and is of correct type
    if variable is not None:
        if isinstance(variable, str):
            variable = [variable]
        elif not isinstance(variable, list):
            raise TypeError("Variable(s) must be a string or a list of strings.")

        data = {"time": df["time"]}
        for var in variable:
            # Check if variable(s) exist in DataFrame
            if var not in df.columns:
                raise ValueError(f"Variable '{var}' not found in the CSV file.")

            data[var] = df[var]

        # Return DataFrame with selected variable(s)
        return pd.DataFrame(data)

    # Return entire DataFrame
    else: return df

def export_file(df: pd.DataFrame, file: str, format: str = "csv"):
    pass

def _export_csv_file(df: pd.DataFrame, file: str):
    pass

def _export_nc_file(df: pd.DataFrame, file: str):
    pass