from pathlib import Path

import pandas as pd
from hydra.utils import to_absolute_path as abs


def load_data(path: str):
    file_path = Path(path)
    if file_path.suffix == ".csv":
        df = pd.read_csv(abs(file_path))
    elif file_path.suffix == ".pkl":
        df = pd.read_pickle(abs(file_path))
    else:
        raise ValueError(
            "File format not supported. Please use a CSV or PKL file."
        )

    return df


def save_data(df: pd.DataFrame, path: str):
    path = abs(path)
    Path(path).parent.mkdir(exist_ok=True)
    df.to_pickle(path)
