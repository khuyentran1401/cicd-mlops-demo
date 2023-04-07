import numpy as np

from src.train import create_pipeline


def test_pipeline():
    """Test the pipeline's behavior"""
    # Define the pipeline
    pipeline = create_pipeline()

    # Create some test data
    X_train = np.array([[1, 2], [3, 4], [5, 6]])
    y_train = np.array([1, 2, 3])
    X_test = np.array([[7, 8], [9, 10]])

    # Fit the pipeline on the training data
    pipeline.fit(X_train, y_train)

    # Test the pipeline's behavior on the test data
    y_pred = pipeline.predict(X_test)

    # Check that the pipeline's output is of the correct shape
    assert y_pred.shape == (2,)

    # Check that the pipeline's output is not all zeros
    assert np.any(y_pred)

    # Check that the pipeline's output is within a reasonable range
    assert np.all(y_pred >= 0) and np.all(y_pred <= 3)
