from src.helper import load_data


@data_loader
def create_training_set(*args, **kwargs):
    X_train = load_data('/home/src/src/data/intermediate/X_train.pkl')
    y_train = load_data('/home/src/src/data/intermediate/y_train.pkl')

    return [X_train, y_train.to_frame()]