from src.helper import load_data


@data_loader
def create_training_set(*args, **kwargs):
    y_train = load_data('/home/src/src/data/intermediate/y_train.pkl')

    return y_train.to_frame()


@test
def validate_number_of_rows(y_train):
    assert len(y_train.index) >= 1279, 'Training labels does not have enough rows.'