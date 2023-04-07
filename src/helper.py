from pathlib import Path

import pandas as pd


def load_data(path: str, csv_delimeter=","):
    """Load data from path"""
    file_path = Path(path)
    if file_path.suffix == ".csv":
        df = pd.read_csv(file_path, csv_delimeter)
    elif file_path.suffix == ".pkl":
        df = pd.read_pickle(file_path)
    else:
        raise ValueError(
            "File format not supported. Please use a CSV or PKL file."
        )

    return df


def save_data(df: pd.DataFrame, path: str, name: str):
    """Save data to path"""
    path = f"{path}/{name}.pkl"
    Path(path).parent.mkdir(exist_ok=True)
    df.to_pickle(path)
