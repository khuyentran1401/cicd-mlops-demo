import dvc.api
import joblib
import pandas as pd
from sklearn.svm import SVR

from dvclive import Live
from helper import load_data


def load_model(path: str):
    return joblib.load(path)


def get_mean_accuracy(model: SVR, X_test: pd.DataFrame, y_test: pd.Series):
    return model.score(X_test, y_test)


def evaluate() -> None:
    params = dvc.api.params_show()
    with Live(save_dvc_exp=True, resume=True) as live:
        X_test = load_data(f"{params['data']['intermediate']}/X_test.pkl")
        y_test = load_data(f"{params['data']['intermediate']}/y_test.pkl")
        model = load_model(params["model"])
        score = get_mean_accuracy(model, X_test, y_test)
        live.log_metric("mean_accuracy", score)


if __name__ == "__main__":
    evaluate()
