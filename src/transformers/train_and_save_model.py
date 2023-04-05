from pathlib import Path
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
import dvc.api
import joblib
import pandas as pd


def create_pipeline() -> Pipeline:
    return Pipeline([("scaler", StandardScaler()), ("svm", SVC())])


def train_model(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    pipeline: Pipeline,
    hyperparameters: dict,
    grid_params: dict,
) -> GridSearchCV:
    grid_search = GridSearchCV(
        pipeline, dict(hyperparameters), **grid_params
    )
    grid_search.fit(X_train, y_train)
    return grid_search


def save_model(model, path: str):
    Path(path).parent.mkdir(exist_ok=True)
    joblib.dump(model, path)


@transformer
def transform(data, **kwargs):
    params = dvc.api.params_show()
    X_train, y_train = data

    pipeline = create_pipeline()
    grid_search = train_model(
        X_train,
        y_train,
        pipeline,
        params["train"]["hyperparameters"],
        params["train"]["grid_search"],
    )

    save_model(grid_search, params["model"])

    return grid_search.best_params_