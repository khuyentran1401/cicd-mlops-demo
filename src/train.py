from pathlib import Path
from typing import Tuple

import hydra
import joblib
import pandas as pd
from hydra.utils import to_absolute_path as abs
from omegaconf import DictConfig
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR

from dvclive import Live
from helper import load_data


def create_pipeline() -> Pipeline:
    return Pipeline([("scaler", StandardScaler()), ("svm", SVR())])


def train_model(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    pipeline: Pipeline,
    hyperparameters: DictConfig,
    cv: int,
) -> GridSearchCV:
    grid_search = GridSearchCV(
        pipeline, dict(hyperparameters), cv=cv, verbose=3
    )
    grid_search.fit(X_train, y_train)
    return grid_search


def save_model(model, path: str):
    path = abs(path)
    Path(path).parent.mkdir(exist_ok=True)
    joblib.dump(model, path)


@hydra.main(version_base=None, config_path="../conf", config_name="config")
def train(config: DictConfig) -> None:
    with Live(save_dvc_exp=True) as live:
        X_train = load_data(f"{config.data.intermediate}/X_train.pkl")
        y_train = load_data(f"{config.data.intermediate}/y_train.pkl")
        pipeline = create_pipeline()
        grid_search = train_model(
            X_train,
            y_train,
            pipeline,
            config.train.hyperparameters,
            config.train.cv,
        )
        live.log_params({"Best hyperparameters": grid_search.best_params_})
        save_model(grid_search, config.model)


if __name__ == "__main__":
    train()
