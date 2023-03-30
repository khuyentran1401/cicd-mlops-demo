from pathlib import Path

import pandas as pd


def save_data(df: pd.DataFrame, path: str):
    Path(path).parent.mkdir(exist_ok=True)
    df.to_pickle(path)
