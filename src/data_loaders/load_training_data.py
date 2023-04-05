from src.helper import load_data


@data_loader
def create_training_set(*args, **kwargs):
    X_train = load_data('/home/src/src/data/intermediate/X_train.pkl')

    return X_train

@test
def validate_number_of_rows(X_train):
    assert len(X_train.index) >= 1279, 'Training data does not have enough rows.'


@test
def validate_number_of_columns(X_train):
    assert len(X_train.columns) >= 11, 'Training data does not have enough columns.'