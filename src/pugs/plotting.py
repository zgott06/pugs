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
    """
    pass

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