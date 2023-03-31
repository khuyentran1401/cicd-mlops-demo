from pathlib import Path
from typing import Tuple

import hydra
import joblib
import matplotlib.pyplot as plt
import pandas as pd
from hydra.utils import to_absolute_path as abs
from omegaconf import DictConfig
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from yellowbrick.cluster import KElbowVisualizer

from helper import load_data, save_data


def get_pca_model(data: pd.DataFrame) -> PCA:
    pca = PCA(n_components=3)
    pca.fit(data)
    return pca


def reduce_dimension(df: pd.DataFrame, pca: PCA) -> pd.DataFrame:
    return pd.DataFrame(pca.transform(df), columns=["col1", "col2", "col3"])


def compare_k_clusters(
    pca_df: pd.DataFrame, elbow_metric: str
) -> pd.DataFrame:
    fig = plt.figure(figsize=(10, 8))
    fig.add_subplot(111)

    elbow = KElbowVisualizer(KMeans(n_init="auto"), metric=elbow_metric)
    elbow.fit(pca_df)

    return elbow


def save_elbow_image(elbow: KElbowVisualizer, image_path: str):
    path = abs(image_path)
    Path(path).parent.mkdir(exist_ok=True)
    elbow.fig.savefig(image_path)


def get_kmeans_model(
    pca_df: pd.DataFrame, elbow: KElbowVisualizer, model_params: dict
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    model_args = dict(model_params.args)
    model_args["n_clusters"] = elbow.elbow_value_

    model = KMeans(**model_args)

    # Fit
    return model.fit(pca_df)


def save_model(model, path: str):
    path = abs(path)
    Path(path).parent.mkdir(exist_ok=True)
    joblib.dump(model, path)


@hydra.main(version_base=None, config_path="../conf", config_name="config")
def segment(config: DictConfig) -> None:
    data = load_data(config.data.scaled)
    pca = get_pca_model(data)
    pca_df = reduce_dimension(data, pca)

    elbow = compare_k_clusters(pca_df, config.elbow_metric)

    save_elbow_image(elbow, config.image.elbow)
    kmeans = get_kmeans_model(pca_df, elbow, config.segment)
    save_data(pca_df, config.data.pca)
    save_model(kmeans, config.model)


if __name__ == "__main__":
    segment()
