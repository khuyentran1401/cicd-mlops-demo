import hydra
import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from hydra.utils import to_absolute_path as abs
from omegaconf import DictConfig
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from dvclive import Live
from helper import load_data, save_data


def load_model(path: str):
    return joblib.load(abs(path))


def predict(model: KMeans, pca_df: pd.DataFrame):
    return model.predict(pca_df)


def inverse_scale(df: pd.DataFrame, scaled_path: str):
    scaler = joblib.load(scaled_path)
    return pd.DataFrame(scaler.inverse_transform(df), columns=df.columns)


def insert_clusters_to_df(
    df: pd.DataFrame, clusters: np.ndarray
) -> pd.DataFrame:
    return df.assign(clusters=clusters)


def get_3d_projection(pca_df: pd.DataFrame) -> dict:
    """A 3D Projection Of Data In The Reduced Dimensionality Space"""
    return {"x": pca_df["col1"], "y": pca_df["col2"], "z": pca_df["col3"]}


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


def get_silhouette_score(pca_df: pd.DataFrame, kmeans: KMeans, live):
    score = silhouette_score(pca_df, kmeans.labels_, metric="euclidean")
    live.log_metric("silhouette_score", score)


@hydra.main(version_base=None, config_path="../conf", config_name="config")
def evaluate(config: DictConfig) -> None:
    with Live(save_dvc_exp=True, resume=True) as live:
        pca_df = load_data(config.data.pca)
        scaled_df = load_data(config.data.scaled)
        kmeans = load_model(config.model)
        prediction = predict(kmeans, pca_df)

        inversed_scaled = inverse_scale(scaled_df, config.scaler)
        added_clusters = insert_clusters_to_df(inversed_scaled, prediction)
        projections = get_3d_projection(pca_df)

        plot_clusters(pca_df, prediction, projections, config.image.clusters)
        get_silhouette_score(pca_df, kmeans, live)
        save_data(added_clusters, config.data.final)


if __name__ == "__main__":
    evaluate()
