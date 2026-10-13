import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path

def single_plot(df: pd.DataFrame, variable: str, start_time: float = None, title: str = None,
                save: bool = False, output_file: str = None, output_dir: str = None,
                overwrite: bool = False, dpi: int = 300) -> str:
    """Plot a specified variable from a single DataFrame. Optionally, mark the start of
        the steady-state region and save the plot to a file.

    Args:
        df (pd.DataFrame): Single DataFrame containing time-series data.
        variable (str): Variable to plot.
        start_time (float, optional): Start time of the steady-state region. Defaults
            to None.
        title (str, optional): Title of the plot. If None, a default title is used.
        save (bool, optional): Whether to save the plot to a file. Defaults to False.
        output_file (str, optional): Output file name for saving the plot. If None, a
            default name is used.
        output_dir (str, optional): Directory to save the plot. If None, current directory
            will be used.
        overwrite (bool, optional): Whether to overwrite existing files. Defaults to False.
        dpi (int, optional): Dots per inch for saved figure. Defaults to 300.
    
    Returns:
        str: Path to the saved plot file, or an empty string if the plot is not saved.

    Raises:
        TypeError: If the df is not a pandas DataFrame.
        TypeError: If the variable, title, output_file, or output_dir is not of type str.
        TypeError: If the start_time is not of type float.
        TypeError: If save or overwrite is not of type bool.
        TypeError: If the dpi is not of type int.
        ValueError: If variable is not present in the DataFrame.
        ValueError: If the start_time is not within the range of the DataFrame.
        ValueError: If the dpi is not positive.
        FileExistsError: If the output file exists and overwrite is False.
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

    # Check if start_time is provided and is of correct type
    if start_time is not None:
        if not isinstance(start_time, float):
            raise TypeError("Input start_time must be of type float.")
        if start_time < df["time"].min() or start_time > df["time"].max():
            raise ValueError("Input start_time is not within the range of the DataFrame.")

    # Check if optional strings are provided and are of correct type
    for name, value in {"title": title, "output_file": output_file, "output_dir": output_dir}.items():
        if value is not None and not isinstance(value, str):
            raise TypeError(f"Input {name} {value} must be a string.")

    # Check if save and overwrite are of type bool
    if not isinstance(save, bool):
        raise TypeError("Input save must be of type bool.")
    if not isinstance(overwrite, bool):
        raise TypeError("Input overwrite must be of type bool.")

    # Check if dpi is a positive integer
    if not isinstance(dpi, int) or isinstance(dpi, bool):
        raise TypeError("Input dpi must be of type int.")
    if dpi <= 0:
        raise ValueError("Input dpi must be positive.")

    # Prepare output file
    output = ""
    if save:
        if output_file is None:
            output_file = f"{variable}_plot.png"
        output = Path(output_file).expanduser()
        if not output.suffix:
            output = output.with_suffix(".png")
        if output_dir is not None:
            output = Path(output_dir).expanduser() / output
        if output.exists() and not overwrite:
            raise FileExistsError(f"The file '{output}' already exists. " \
                                  "Set overwrite=True to overwrite.")
        output.parent.mkdir(parents=True, exist_ok=True)

    # Preprocess DataFrame to extract time-series data
    t = df["time"].to_numpy()
    x = df[variable].to_numpy()

    # Plot variable and optionally mark the steady-state region
    fig, ax = plt.subplots(figsize=(8, 4))
    try:
        ax.plot(t, x)
        if start_time is not None:
            ax.axvline(start_time, color='red', linestyle='--', label="Steady-State")
            ax.legend()

        if title is None:
            title = f"{variable} vs Time"
        ax.set_title(title)
        ax.set_xlabel("Time")
        ax.set_ylabel(variable)
        fig.tight_layout()

        # Save plot if requested and display the figure
        if save:
            fig.savefig(output, dpi=dpi, bbox_inches="tight")
        plt.show()
    finally:
        plt.close(fig)

    return str(output)

def multi_plot(dfs: list[pd.DataFrame], variables: str | list[str], start_times: list[float] = None,
               title: str = None, save: bool = False, output_file: str = None,
               output_dir: str = None, overwrite: bool = False, dpi: int = 300) -> str:
    """Plot specified variables from a list of DataFrames in a single figure. Optionally,
        mark the start of the steady-state region and save the plot to a file. A maximum of
        9 plots is supported, with one plot per DataFrame in list order.

    Args:
        dfs (list[pd.DataFrame]): List of 1 to 9 DataFrames containing time-series data.
        variables (str or list[str]): Variable to plot for all DataFrames, or a list of
            variables to plot, one for each DataFrame.
        start_times (list[float], optional): List of start times for the steady-state region,
            one for each DataFrame. Use None for plots without a start time. Defaults to None.
        title (str, optional): Title of the figure. If None, a default title is used.
        save (bool, optional): Whether to save the plot to a file. Defaults to False.
        output_file (str, optional): Output file name for saving the plot. If None, a
            default name is used.
        output_dir (str, optional): Directory to save the plot. If None, current directory
            will be used.
        overwrite (bool, optional): Whether to overwrite existing files. Defaults to False.
        dpi (int, optional): Dots per inch for saved figure. Defaults to 300.
    
    Returns:
        str: Path to the saved plot file, or an empty string if the plot is not saved.

    Raises:
        TypeError: If dfs is not a list of pandas DataFrames.
        TypeError: If variables is not a string or a list of strings.
        TypeError: If start_times is not a list or a provided start time is not of type float.
        TypeError: If title, output_file, or output_dir is not of type str.
        TypeError: If save or overwrite is not of type bool.
        TypeError: If the dpi is not of type int.
        ValueError: If the number of DataFrames is not between 1 and 9.
        ValueError: If variables or start_times does not have one entry for each DataFrame.
        ValueError: If a variable is not present in its DataFrame.
        ValueError: If a start time is not within the range of its DataFrame.
        ValueError: If the dpi is not positive.
        FileExistsError: If the output file exists and overwrite is False.
    """
    # Check if dfs is a list of pandas DataFrames
    if not isinstance(dfs, list):
        raise TypeError("Input dfs must be a list of pandas DataFrames. Consider preprocessing data " \
                        "with the load_file function.")
    for df in dfs:
        if not isinstance(df, pd.DataFrame):
            raise TypeError("Input dfs must be a list of pandas DataFrames. Consider preprocessing data " \
                            "with the load_file function.")

    # Check if the number of DataFrames is supported
    if not 1 <= len(dfs) <= 9:
        raise ValueError("Input dfs must contain between 1 and 9 DataFrames.")

    # Check if variables is a string or a list of strings
    if isinstance(variables, str):
        variables = [variables] * len(dfs)
    elif not isinstance(variables, list) or not all(isinstance(var, str) for var in variables):
        raise TypeError("Input variables must be a string or a list of strings.")
    if len(variables) != len(dfs):
        raise ValueError("Input variables must have one entry for each DataFrame.")

    # Check if each variable is present in its DataFrame
    for df, var in zip(dfs, variables):
        if var not in df.columns:
            raise ValueError(f"Input variable {var} is not present in the DataFrame.")

    # Check if start_times is provided and is of correct type
    if start_times is not None:
        if not isinstance(start_times, list):
            raise TypeError("Input start_times must be a list of floats or None.")
        if len(start_times) != len(dfs):
            raise ValueError("Input start_times must have one entry for each DataFrame.")
        for df, time in zip(dfs, start_times):
            if time is not None:
                if not isinstance(time, float):
                    raise TypeError("Input start_times entries must be of type float or None.")
                if time < df["time"].min() or time > df["time"].max():
                    raise ValueError("Input start_times is not within the range of the DataFrame.")
    else:
        start_times = [None] * len(dfs)

    # Check if optional strings are provided and are of correct type
    for name, value in {"title": title, "output_file": output_file, "output_dir": output_dir}.items():
        if value is not None and not isinstance(value, str):
            raise TypeError(f"Input {name} {value} must be a string.")

    # Check if save and overwrite are of type bool
    if not isinstance(save, bool):
        raise TypeError("Input save must be of type bool.")
    if not isinstance(overwrite, bool):
        raise TypeError("Input overwrite must be of type bool.")

    # Check if dpi is a positive integer
    if not isinstance(dpi, int) or isinstance(dpi, bool):
        raise TypeError("Input dpi must be of type int.")
    if dpi <= 0:
        raise ValueError("Input dpi must be positive.")

    # Prepare output file
    output = ""
    if save:
        if output_file is None:
            output_file = "multi_plot.png"
        output = Path(output_file).expanduser()
        if not output.suffix:
            output = output.with_suffix(".png")
        if output_dir is not None:
            output = Path(output_dir).expanduser() / output
        if output.exists() and not overwrite:
            raise FileExistsError(f"The file '{output}' already exists. Set overwrite=True to overwrite.")
        output.parent.mkdir(parents=True, exist_ok=True)

    # Choose layout based on the number of plots
    if len(dfs) == 1:
        rows, cols = 1, 1
    elif len(dfs) <= 4:
        rows, cols = 2, 2
    elif len(dfs) <= 6:
        rows, cols = 3, 2
    else:
        rows, cols = 3, 3

    # Plot variables and optionally mark the steady-state regions
    fig, axes = plt.subplots(rows, cols, figsize=(6 * cols, 3 * rows), squeeze=False)
    try:
        legend_added = False
        for ax, df, var, time in zip(axes.flatten(), dfs, variables, start_times):
            # Preprocess DataFrame to extract time-series data
            t = df["time"].to_numpy()
            x = df[var].to_numpy()

            ax.plot(t, x)
            if time is not None:
                ax.axvline(time, color='red', linestyle='--', label="Steady-State")
                # Show the legend only in the first plot with a steady-state marker
                if not legend_added:
                    ax.legend()
                    legend_added = True

            ax.set_xlabel("Time")
            ax.set_ylabel(var)

        # Hide unused plots and set the figure title
        for ax in axes.flatten()[len(dfs):]:
            ax.set_visible(False)
        if title is None:
            title = "Time-Series Data vs Time"
        fig.suptitle(title)

        fig.tight_layout()

        # Save plot if requested and display the figure
        if save:
            fig.savefig(output, dpi=dpi, bbox_inches="tight")
        plt.show()
    finally:
        plt.close(fig)

    return str(output)
