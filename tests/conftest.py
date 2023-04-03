import dvc.api
import pandas as pd
import pytest
from deepchecks.tabular import Dataset

from src.evaluate import load_model
from src.helper import load_data


@pytest.fixture
def train_data():
    params = dvc.api.params_show()
    X_train = load_data(f"{params['data']['intermediate']}/X_train.pkl")
    y_train = load_data(f"{params['data']['intermediate']}/y_train.pkl")
    df = pd.concat([X_train, y_train], axis=1)
    return Dataset(df, label=params["process"]["feature"], cat_features=[])


@pytest.fixture
def test_data():
    params = dvc.api.params_show()
    X_test = load_data(f"{params['data']['intermediate']}/X_test.pkl")
    y_test = load_data(f"{params['data']['intermediate']}/y_test.pkl")
    df = pd.concat([X_test, y_test], axis=1)
    return Dataset(df, label=params["process"]["feature"], cat_features=[])


@pytest.fixture
def model():
    params = dvc.api.params_show()
    return load_model(params["model"])
