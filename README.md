# Postprocessing Utilities for Gyrokinetic Simulations (PUGS)

PUGS is Python-based toolkit for analyzing time-series data of turbulent plasma simulations. The library provides methods for steady-state detection, statistical summaries, and plotting, with support for single runs or batch processing.

## Installation

PUGS requires Python 3.10 or newer. The distribution is named `pugs_plasma`, while the Python import is `pugs`.

Install from PyPI:

```bash
python -m pip install pugs_plasma
```

To install the latest development version directly from GitHub:

```bash
python -m pip install "git+https://github.com/zgott06/pugs.git"
```

For local development, run the following from the repository root:

```bash
python -m pip install --editable .
```

Installation includes NumPy, pandas, SciPy, Matplotlib, and netCDF4.

## Usage

### Load simulation data

`load_file` reads GX netCDF output files ending in `.nc`. It retrieves time from the `Grids` group and variables from the `Diagnostics` group. Supported variable names end in `_t` or `_st`.

Replace `gx.out.nc` in these examples with the path to your simulation output.

```python
import pugs

variable = "HeatFlux_st"
df = pugs.load_file("gx.out.nc", variable=variable)
```

You can also provide a list of variable names. Omitting `variable` loads all supported variables in the file. Analysis and plotting functions accept pandas DataFrames with a `time` column and the requested variable columns.

### Detect steady state and compute statistics

```python
start_time = pugs.steady_state(
    df, variable, method="linreg", slope_tol=0.1
)

if start_time is None:
    print("No steady-state region found.")
else:
    trimmed_df = pugs.trim(df, start_time)
    summary = pugs.stats(trimmed_df, variable=variable)
    print(summary[variable])
```

The implemented methods are `std` (the default) and `linreg`:

- `std` selects the time of maximum standard deviation during a forward search.
- `linreg` selects a candidate start time using a forward regression search, then checks the normalized slope of the remaining data against `slope_tol`.

Both methods return `None` when the signal fails the initialization check. The `linreg` method also returns `None` when the remaining data does not meet its criteria. Methods `adf`, `acf`, and `fourier` raise `NotImplementedError`.

`stats` returns a dictionary containing mean, median, standard deviation, variance, and other statistical summaries for each selected variable.

### Plot and save a single run

```python
pugs.single_plot(
    df,
    variable,
    start_time=None if start_time is None else start_time,
    title="Heat Flux vs Time",
    save=True,
    output_file="heat_flux.png",
    output_dir="plots",
)
```

The plot is displayed and saved in the `plots` folder. A steady-state marker is added when `start_time` is provided. Existing files are protected unless `overwrite=True`.

### Plot multiple runs in one figure

```python
files = ["run_1/gx.out.nc", "run_2/gx.out.nc", "run_3/gx.out.nc"]
dfs = [pugs.load_file(file, variable=variable) for file in files]

pugs.multi_plot(
    dfs,
    variables=variable,
    title="Heat Flux Across Runs",
    save=True,
    output_file="heat_flux_comparison.png",
    output_dir="plots",
)
```

`multi_plot` supports up to nine DataFrames in one figure. Pass one variable name for all runs, or a list with one variable name per DataFrame. Optional `start_times` should contain one float or `None` per DataFrame. The layouts are 1x1, 2x2, 3x2, and 3x3, with unused panels hidden.

### Process and export a run

`process_file` loads a run, detects steady state, trims the data, computes statistics, and exports the results:

```python
output = pugs.process_file(
    trim_variable=variable,
    input_file="gx.out.nc",
    variable=variable,
    method="linreg",
    slope_tol=0.1,
    output_file="heat_flux_summary.csv",
)

if output is None:
    print("No steady-state region found; no summary exported.")
else:
    print(f"Saved summary to {output}")
```

To process multiple runs, call `process_file` in a loop with a separate output file for each run.

Supported export formats are `csv`, `json`, and `html`. Use `output_format` with `process_file`, or export a DataFrame directly:

```python
pugs.export_file(df, "heat_flux_data.csv", format="csv")
```

## License

PUGS is distributed under the [MIT License](LICENSE).
