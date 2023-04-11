import dvc.api

from helper import load_data
from sklearn.metrics import accuracy_score
from dvclive import Live
from mlem.api import load


def load_model(path: str):
    """Load model from path"""
    return load(path)


def evaluate() -> None:
    """Evaluate model and log metrics"""
    params = dvc.api.params_show()
    with Live(save_dvc_exp=True, resume=True) as live:
        X_test = load_data(f"{params['data']['intermediate']}/X_test.pkl")
        y_test = load_data(f"{params['data']['intermediate']}/y_test.pkl")
        model = load_model(params["model"])
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"The model's accuracy is {accuracy}")
        live.log_metric("accuracy", accuracy)

if __name__ == "__main__":
    evaluate()
