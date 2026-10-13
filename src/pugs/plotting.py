import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path

def single_plot(df: pd.DataFrame, variable: str, start_time: float = None, title: str = None, save: bool = False, output_file: str = None, output_dir: str = None, overwrite: bool = False, dpi: int = 300) -> str:
    """Plot a specified variable from a single DataFrame. Optionally, mark the start of the steady-state region and save the plot to a file.

    Args:
        df (pd.DataFrame): Single DataFrame containing time-series data.
        variable (str): Variable to plot.
        start_time (float, optional): Start time of the steady-state region. Defaults to None.
        title (str, optional): Title of the plot. If None, a default title is used.
        save (bool, optional): Whether to save the plot to a file. Defaults to False.
        output_file (str, optional): Output file name for saving the plot. If None, a default name is used.
        output_dir (str, optional): Directory to save the plot. If None, current directory will be used.
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
            raise FileExistsError(f"The file '{output}' already exists. Set overwrite=True to overwrite.")
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

def multi_plot(dfs: list[pd.DataFrame], variables: list[str], start_time: list[float] = None, title: str = None, save: bool = False, output_file: str = None, output_dir: str = None, overwrite: bool = False, dpi: int = 300) -> str:
    """Plot a specified variable from a list of DataFrames. Optionally, mark the start of the steady-state region and save the plot to a file.

    Args:
        dfs (list[pd.DataFrame]): List of DataFrames containing time-series data.
        variables (list[str]): List of variables to plot.
        start_time (list[float], optional): List of start times for the steady-state region. Defaults to None.
        title (str, optional): Title of the plot. If None, a default title is used.
        save (bool, optional): Whether to save the plot to a file. Defaults to False.
        output_file (str, optional): Output file name for saving the plot. If None, a default name is used.
        output_dir (str, optional): Directory to save the plot. If None, current directory will be used.
        overwrite (bool, optional): Whether to overwrite existing files. Defaults to False.
        dpi (int, optional): Dots per inch for saved figure. Defaults to 300.
    
    Returns:
        str: Path to the saved plot file, or an empty string if the plot is not saved.
    """
    pass
