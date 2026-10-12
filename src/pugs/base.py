import pandas as pd

from .io import load_file, export_file
from.steady_state import steady_state
from.utils import trim, stats

def process_file(trim_variable: str, input_file: str, output_file: str = None,
                output_format: str = "csv", variable: str | list = None,
                method: str = "std", **kwargs) -> str:
    """Complete workflow method to process a file:
        1) Load a GX output file and retrieve specified variable(s),
        2) Detect the start of the steady-state region (if any) for a specified
            variable using a specified method,
        3) Trim all variables from the start of the steady-state region,
        4) Compute statistics,
        5) Export to a specified file format.

        Args:
            trim_variable (str): Variable to analyze for steady-state detection.
            input_file (str): GX output file path (.nc or .csv)
            output_file (str, optional): Output file path. If None, a default name is used.
            output_format (str, optional): Output file format. Defaults to a CSV file.
            variable (str or list, optional): Variable(s) to retrieve. If None, retrieves all.
                Defaults to None
            method (str, optional): Method to use for steady-state detection.
                Options are "std", "linreg", "adf", "acf", or "fourier". Defaults to "std".
            **kwargs: Addtional keyword arguments for specific methods.

        Returns:
            str: Path to the output file if steady-state start time is detected,
                otherwise None.
    """
    # Load the GX file
    df = load_file(input_file, variable)

    # Compute steady-state start time
    start_time = steady_state(df, trim_variable, method=method, **kwargs)
    if start_time is None: return None

    # Trim DataFrame and compute statistics
    df = trim(df, start_time)
    stats_summary = stats(df)

    # Extract parameters to return
    results = []
    for var in stats_summary:
        results.append({
            "file": input_file,
            "trim_variable": trim_variable,
            "variable": var,
            "method": method,
            **kwargs,
            "start_time": start_time
        })

        for key, value in stats_summary[var].items():
            results[-1][key] = value

    # Prepare output file
    if output_file is None:
        output_file = f"{trim_variable}_{method}"
        if kwargs:
            output_file += "_" + "_".join([f"{key}_{value}" for key, value in kwargs.items()])

    # Export results
    df = pd.DataFrame(results)
    output_file = export_file(df, output_file, format=output_format)

    return output_file