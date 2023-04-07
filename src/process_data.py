import warnings
from typing import Tuple

import dvc.api
import pandas as pd
from sklearn.model_selection import train_test_split

from helper import load_data, save_data

# Ignore all future warnings
warnings.simplefilter(action="ignore", category=FutureWarning)


def get_X_y(
    data: pd.DataFrame, feature: str
) -> Tuple[pd.DataFrame, pd.Series]:
    """Split data into X and y"""
    X = data.drop(columns=feature)
    y = data[feature]
    return X, y


def split_train_test(X: pd.DataFrame, y: pd.Series, test_size: float) -> dict:
    """Split data into train and test sets"""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )
    return {
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
    }


def process_data():
    params = dvc.api.params_show()
    df = load_data(params["data"]["raw"], csv_delimeter=";")
    X, y = get_X_y(df, params["process"]["feature"])
    splitted_datasets = split_train_test(X, y, params["process"]["test_size"])
    for name, data in splitted_datasets.items():
        save_data(data, params["data"]["intermediate"], name)


if __name__ == "__main__":
    process_data()
