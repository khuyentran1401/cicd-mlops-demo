from pathlib import Path

import dvc.api
import joblib
import pandas as pd
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
    hyperparameters: dict,
    cv: int,
) -> GridSearchCV:
    grid_search = GridSearchCV(
        pipeline, dict(hyperparameters), cv=cv, verbose=3
    )
    grid_search.fit(X_train, y_train)
    return grid_search


def save_model(model, path: str):
    Path(path).parent.mkdir(exist_ok=True)
    joblib.dump(model, path)


def train() -> None:
    params = dvc.api.params_show()
    with Live(save_dvc_exp=True) as live:
        X_train = load_data(f"{params['data']['intermediate']}/X_train.pkl")
        y_train = load_data(f"{params['data']['intermediate']}/y_train.pkl")
        pipeline = create_pipeline()
        grid_search = train_model(
            X_train,
            y_train,
            pipeline,
            params["train"]["hyperparameters"],
            params["train"]["cv"],
        )
        live.log_params({"Best hyperparameters": grid_search.best_params_})
        save_model(grid_search, params["model"])


if __name__ == "__main__":
    train()
