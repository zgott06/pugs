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
        TypeError: If the variable(s) is not of type str, list, or None.
        ValueError: If the file format is not supported (neither .nc nor .csv).
    """
    # Check if the file exists
    if not os.path.isfile(file):
        raise FileNotFoundError(f"The file '{file}' does not exist.")

    # Check if variable(s) is provided and is of correct type
    if variable is not None:
        if isinstance(variable, str):
            variable = [variable]
        elif not isinstance(variable, list):
            raise TypeError("Variable(s) must be a string or a list of strings.")

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
        ValueError: If the variable(s) is not present in the netCDF file.
        ValueError: If the variable(s) is not supported (does not end with "_t" or "_st").
    """
    # Load the netCDF file into a Dataset
    ds = Dataset(file, "r")

    # Retrieve all eligible variables if no specific variable(s) is provided
    if variable is None:
        variable = [var for var in ds["Diagnostics"].variables.keys()
                    if var.endswith("_t") or var.endswith("_st")]

    # Assign time and selected variable(s) to a dictionary
    data = {"time": ds["Grids"]["time"][:]}
    for var in variable:
        # Current capabilities only support variabels ending with "_t" or "_st"
        if not (var.endswith("_t") or var.endswith("_st")):
            raise ValueError(f"""Variable '{var}' is not supported with current capabilities.
                             Only variables ending with '_t' or '_st' are supported.""")

        # Check if variable(s) exists in Dataset
        if var not in ds["Diagnostics"].variables:
            raise ValueError(f"Variable '{var}' not found in the netCDF file.")
         
        # Handle multi-dimensional variables
        if ds["Diagnostics"][var].ndim > 1:
            ds["Diagnostics"][var][:].flatten()

        data[var] = ds["Diagnostics"][var][:]

    ds.close()

    # Return DataFrame with selected variable(s)
    return pd.DataFrame(data)

def _load_csv_file(file: str, variable: str | list = None) -> pd.DataFrame:
    """Load a GX output file in the form of a CSV file and retrieve selected variable(s).
    
    Args:
        file (str): GX output file path (.csv)
        variable (str or list, optional): Variable(s) to retrieve. If None, retrieves all.
            Defaults to None.
    
    Returns:
        pd.DataFrame: DataFrame containing the request variable(s) time-series data.
    
    Raises:
        ValueError: If the variable(s) is not present in the CSV file.
        ValueError: If the variable(s) is not supported (does not end with "_t" or "_st").
    """
    # Load the CSV file into a DataFrame
    df = pd.read_csv(file)
    
    # Retrieve all eligible variables if no specific variable(s) is provided
    if variable is None:
        variable = [var for var in df.columns if var.endswith("_t") or var.endswith("_st")]

    # Assign time and selected variable(s) to a dictionary
    data = {"time": df["time"]}
    for var in variable:
         # Current capabilities only support variabels ending with "_t" or "_st"
        if not (var.endswith("_t") or var.endswith("_st")):
            raise ValueError(f"""Variable '{var}' is not supported with current capabilities.
                             Only variables ending with '_t' or '_st' are supported.""")
        
        # Check if variable(s) exists in DataFrame
        if var not in df.columns:
            raise ValueError(f"Variable '{var}' not found in the CSV file.")

        data[var] = df[var]

     # Return DataFrame with selected variable(s)
    return pd.DataFrame(data)

def export_file(df: pd.DataFrame, file: str, format: str = "csv"):
    pass

def _export_csv_file(df: pd.DataFrame, file: str):
    pass

def _export_nc_file(df: pd.DataFrame, file: str):
    pass