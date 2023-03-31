import numpy as np
import pandas as pd

from src.segment import *


def test_reduce_dimension():
    # Create a test dataset
    data = pd.DataFrame(
        {
            "feat1": [1, 2, 3],
            "feat2": [4, 5, 6],
            "feat3": [7, 8, 9],
            "feat4": [3, 4, 5],
        }
    )

    pca = get_pca_model(data)
    transformed_data = reduce_dimension(data, pca)

    print(transformed_data)

    # Test that the transformed data has the correct shape
    assert (
        transformed_data.shape[1] == pca.n_components_
    ), "Transformed data does not have the correct number of components"

    # Check that the transformed data is centered
    assert np.allclose(
        transformed_data.mean(axis=0), np.zeros(pca.n_components_)
    ), "Transformed data is not centered"

    # Check that the transformed data can be transformed back to the original data with reasonable accuracy
    reconstructed_data = pca.inverse_transform(transformed_data)
    max_error = np.max(np.abs(reconstructed_data - data), axis=0)
    assert (
        max_error.all() < 1e-6
    ), f"Maximum reconstruction error {max_error} is too large"


def test_get_kmeans_model():
    np.random.seed(42)
    data = np.random.rand(100, 3)
    df = pd.DataFrame(data, columns=["col1", "col2", "col3"])

    # create a KMeans model
    model_params = DictConfig(
        {"algorithm": "KMeans", "args": {"n_clusters": 2, "n_init": "auto"}}
    )
    k = 4
    kmeans = get_kmeans_model(df, k, model_params)

    # fit the model to the data
    kmeans.fit(df)

    # check that the model assigns each point to a cluster
    assert set(kmeans.labels_) == {0, 1, 2, 3}

    # check that the model assigns the correct cluster to each point
    assert kmeans.predict([[0, 0], [4, 5]]) == np.array([0, 1])

    # check that the model's inertia is greater after fitting than before
    assert kmeans.inertia_ > 0
