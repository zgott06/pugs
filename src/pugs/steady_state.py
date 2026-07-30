import pandas as pd

def steady_state(df: pd.DataFrame, variable: str, method: str = "threshold", **kwargs) -> float:
    pass

def _threshold(df: pd.DataFrame, variable: str, threshold: float = 0.05) -> float:
    pass

def _acf(df: pd.DataFrame, variable: str) -> float:
    pass

def _fourier(df: pd.DataFrame, variable: str) -> float:
    pass

def _adf(df: pd.DataFrame, variable: str) -> float:
    pass

