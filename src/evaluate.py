import hydra
import joblib
import pandas as pd
from hydra.utils import to_absolute_path as abs
from omegaconf import DictConfig
from sklearn.svm import SVR

from dvclive import Live
from helper import load_data


def load_model(path: str):
    return joblib.load(abs(path))


def get_mean_accuracy(model: SVR, X_test: pd.DataFrame, y_test: pd.Series):
    return model.score(X_test, y_test)


@hydra.main(version_base=None, config_path="../conf", config_name="config")
def evaluate(config: DictConfig) -> None:
    with Live(save_dvc_exp=True, resume=True) as live:
        X_test = load_data(f"{config.data.intermediate}/X_test.pkl")
        y_test = load_data(f"{config.data.intermediate}/y_test.pkl")
        model = load_model(config.model)
        score = get_mean_accuracy(model, X_test, y_test)
        live.log_metric("mean_accuracy", score)


if __name__ == "__main__":
    evaluate()
