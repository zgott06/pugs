import os
import pandas as pd
from netCDF4 import Dataset

def load_file(file: str, variable: str | list = None) -> pd.DataFrame:
    """Load a GX output file and retrieve specified variable(s).

    Args:
        file (str): GX output file path (netCDF file ending in ".nc")
        variable (str or list, optional): Variable(s) to retrieve. If None, retrieves all.
            Defaults to None.

    Returns:
        pd.DataFrame: DataFrame containing the requested variable(s) time-series data.
    
    Raises:
        FileNotFoundError: If the file does not exist.
        TypeError: If the variable(s) is not of type str, list, or None.
        ValueError: If the file format is not a netCDF file ending in ".nc".
        ValueError: If the variable(s) is not present in the netCDF file.
        ValueError: If the variable(s) is not supported (does not end with "_t" or "_st").
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

    # Check if the file is a netCDF file
    if not file.endswith(".nc"):
        raise TypeError("Unsupported file format. Please provide a netCDF file ending in '.nc'.")

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
            raise ValueError(f"""Variable '{var}' is not supported with current capabilities. " \
                "Only variables ending with '_t' or '_st' are supported.""")

        # Check if variable(s) exists in Dataset
        if var not in ds["Diagnostics"].variables:
            raise ValueError(f"Variable '{var}' not found in the netCDF file.")
         
        # Handle multi-dimensional variables
        var_data = ds["Diagnostics"][var][:]
        if var_data.ndim > 1:
            var_data = var_data.flatten()

        data[var] = var_data

    ds.close()

    # Return DataFrame with selected variable(s)
    return pd.DataFrame(data)

def export_file(df: pd.DataFrame, file: str, format: str = "csv") -> str:
    """Load a DataFrame and export to a specified file format.

    Args:
        df (pd.DataFrame): DataFrame to export.
        file (str): Output file path.
        format (str, optional): Output file format.
            Options are "csv", "excel", "json", or "html". Defaults to "csv".
    
    Returns:
        str: Path to exported file.

    Raises:
        TypeError: If the df is not a pandas DataFrame.
        TypeError: If the file is not of type string.
        KeyError: If the format is not one of the supported options.
    """
    # Check if df is a pandas DataFrame
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input df must be a pandas DataFrame. Consider preprocessing data " \
                        "with the load_file function.")

    # Check if file is of type string
    if not isinstance(file, str):
        raise TypeError(f"Input file {file} must be a string.")

    # Define map of file formats to corresponding functions
    format_map = {
        "csv": lambda: df.to_csv(file, index=False),
        "excel": lambda: df.to_excel(file, index=False),
        "json": lambda: df.to_json(file, orient="records"),
        "html": lambda: df.to_html(file, index=False)
    }
    format_keys = ["csv", "excel", "json", "html"]

    # Check if the file format is supported
    if not isinstance(format, str) or format not in format_keys:
        raise KeyError(f"File format {format} is not supported. Please choose from: {format_keys}")

    # Prepare file extension
    if not file.endswith(f".{format}"):
        if format == "excel":
            file += ".xlsx"
        else:
            file += f".{format}"

    # Call appropriate export method
    format_map[format]()

    return file