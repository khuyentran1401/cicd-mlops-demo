from pathlib import Path

import dvc.api
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from dvclive import Live
from helper import load_data
from mlem.api import save

def create_pipeline() -> Pipeline:
    return Pipeline([("scaler", StandardScaler()), ("svm", SVC())])


def train_model(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    pipeline: Pipeline,
    hyperparameters: dict,
    grid_params: dict,
) -> GridSearchCV:
    """Train model using GridSearchCV"""
    grid_search = GridSearchCV(
        pipeline, dict(hyperparameters), **grid_params
    )
    grid_search.fit(X_train, y_train)
    return grid_search


def save_model(model, path: str, X_train: pd.DataFrame):
    """Save model to path"""
    Path(path).parent.mkdir(exist_ok=True)
    save(model, path, sample_data=X_train)


def train() -> None:
    """Train model and save it"""
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
            params["train"]["grid_search"],
        )
        live.log_params({"Best hyperparameters": grid_search.best_params_})
        save_model(grid_search.best_estimator_, params["model"], X_train)


if __name__ == "__main__":
    train()
