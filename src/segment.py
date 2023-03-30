from pathlib import Path
from typing import Tuple

import hydra
import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from hydra.utils import to_absolute_path as abs
from omegaconf import DictConfig, OmegaConf
from sklearn.cluster import (DBSCAN, OPTICS, AffinityPropagation,
                             AgglomerativeClustering, Birch, KMeans, MeanShift,
                             SpectralClustering)
from sklearn.decomposition import PCA
from yellowbrick.cluster import KElbowVisualizer

from helper import load_data, save_data


def get_pca_model(data: pd.DataFrame) -> PCA:
    pca = PCA(n_components=3)
    pca.fit(data)
    return pca


def reduce_dimension(df: pd.DataFrame, pca: PCA) -> pd.DataFrame:
    return pd.DataFrame(pca.transform(df), columns=["col1", "col2", "col3"])


def get_3d_projection(pca_df: pd.DataFrame) -> dict:
    """A 3D Projection Of Data In The Reduced Dimensionality Space"""
    return {"x": pca_df["col1"], "y": pca_df["col2"], "z": pca_df["col3"]}


def get_best_k_cluster(
    pca_df: pd.DataFrame, image_path: str, elbow_metric: str
) -> pd.DataFrame:
    fig = plt.figure(figsize=(10, 8))
    fig.add_subplot(111)

    elbow = KElbowVisualizer(KMeans(n_init="auto"), metric=elbow_metric)
    elbow.fit(pca_df)

    path = abs(image_path)
    Path(path).parent.mkdir(exist_ok=True)
    elbow.fig.savefig(image_path)

    return elbow.elbow_value_


def predict(
    pca_df: pd.DataFrame, k: int, model: dict
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    model_args = dict(model.args)
    model_args["n_clusters"] = k

    model = KMeans(**model_args)

    # Predict
    return model.fit_predict(pca_df)


def inverse_scale(df: pd.DataFrame, scaled_path: str):
    scaler = joblib.load(scaled_path)
    return pd.DataFrame(scaler.inverse_transform(df), columns=df.columns)


def insert_clusters_to_df(
    df: pd.DataFrame, clusters: np.ndarray
) -> pd.DataFrame:
    return df.assign(clusters=clusters)


def plot_clusters(
    pca_df: pd.DataFrame, preds: np.ndarray, projections: dict, image_path: str
) -> None:
    pca_df["clusters"] = preds

    plt.figure(figsize=(10, 8))
    ax = plt.subplot(111, projection="3d")
    ax.set_title("the plot of the clusters")
    ax.scatter(
        projections["x"],
        projections["y"],
        projections["z"],
        s=40,
        c=pca_df["clusters"],
        marker="o",
        cmap="Accent",
    )
    path = abs(image_path)
    plt.savefig(path)


def save_model(model, path: str):
    path = abs(path)
    Path(path).parent.mkdir(exist_ok=True)
    joblib.dump(model, path)


@hydra.main(version_base=None, config_path="../conf", config_name="config")
def segment(config: DictConfig) -> None:
    data = load_data(config.data.intermediate)
    pca = get_pca_model(data)
    pca_df = reduce_dimension(data, pca)

    projections = get_3d_projection(pca_df)

    k_best = get_best_k_cluster(
        pca_df, config.image.elbow, config.elbow_metric
    )
    prediction = predict(pca_df, k_best, config.segment)

    inversed_scaled = inverse_scale(data, config.scaler)
    added_clusters = insert_clusters_to_df(inversed_scaled, prediction)
    save_data(added_clusters, config.data.final)
    save_model(pca, config.model)
    plot_clusters(pca_df, prediction, projections, config.image.clusters)


if __name__ == "__main__":
    segment()
