import warnings
from typing import Tuple

import hydra
import pandas as pd
from omegaconf import DictConfig
from sklearn.model_selection import train_test_split

from helper import load_data, save_data

# Ignore all future warnings
warnings.simplefilter(action="ignore", category=FutureWarning)


def get_X_y(
    data: pd.DataFrame, feature: str
) -> Tuple[pd.DataFrame, pd.Series]:
    X = data.drop(columns=feature)
    y = data[feature]
    return X, y


def split_train_test(X: pd.DataFrame, y: pd.Series, test_size: float) -> dict:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )
    return {
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
    }


@hydra.main(version_base=None, config_path="../conf", config_name="config")
def process_data(config: DictConfig):
    df = load_data(config.data.raw, csv_delimeter=";")
    X, y = get_X_y(df, config.process.feature)
    splitted_datasets = split_train_test(X, y, config.process.test_size)
    for name, data in splitted_datasets.items():
        save_data(data, config.data.intermediate, name)


if __name__ == "__main__":
    process_data()
