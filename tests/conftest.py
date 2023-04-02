import pandas as pd
import pytest
from deepchecks.tabular import Dataset
from hydra import compose, initialize

from src.evaluate import load_model
from src.helper import load_data


@pytest.fixture
def train_data():
    with initialize(version_base=None, config_path="../conf"):
        config = compose(config_name="config")
        X_train = load_data(f"{config.data.intermediate}/X_train.pkl")
        y_train = load_data(f"{config.data.intermediate}/y_train.pkl")
    df = pd.concat([X_train, y_train], axis=1)
    return Dataset(df, label=config.process.feature)


@pytest.fixture
def test_data():
    with initialize(version_base=None, config_path="../conf"):
        config = compose(config_name="config")
        X_train = load_data(f"{config.data.intermediate}/X_test.pkl")
        y_train = load_data(f"{config.data.intermediate}/y_test.pkl")
    df = pd.concat([X_train, y_train], axis=1)
    return Dataset(df, label=config.process.feature)


@pytest.fixture
def model():
    with initialize(version_base=None, config_path="../conf"):
        config = compose(config_name="config")
        return load_model(config.model)
