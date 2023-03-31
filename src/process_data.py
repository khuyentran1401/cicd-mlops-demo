from pathlib import Path

import hydra
import joblib
import pandas as pd
from hydra.utils import to_absolute_path as abs
from omegaconf import DictConfig
from sklearn.preprocessing import StandardScaler

from helper import load_data, save_data


def drop_na(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna().reset_index(drop=True)


def get_age(df: pd.DataFrame) -> pd.DataFrame:
    return df.assign(age=2021 - df["Year_Birth"])


def get_total_children(df: pd.DataFrame) -> pd.DataFrame:
    return df.assign(total_children=df["Kidhome"] + df["Teenhome"])


def get_total_purchases(df: pd.DataFrame) -> pd.DataFrame:
    purchases_columns = df.filter(like="Purchases", axis=1).columns
    return df.assign(total_purchases=df[purchases_columns].sum(axis=1))


def get_enrollment_years(df: pd.DataFrame) -> pd.DataFrame:
    df["Dt_Customer"] = pd.to_datetime(df["Dt_Customer"], format="%d-%m-%Y")
    return df.assign(enrollment_years=2022 - df["Dt_Customer"].dt.year)


def get_family_size(df: pd.DataFrame, size_map: DictConfig) -> pd.DataFrame:
    return df.assign(
        family_size=df["Marital_Status"].map(size_map) + df["total_children"]
    )


def drop_features(df: pd.DataFrame, keep_columns: list):
    df = df[keep_columns]
    return df


def drop_outliers(df: pd.DataFrame, column_threshold: DictConfig):
    for col, threshold in column_threshold.items():
        df = df[df[col] < threshold]
    return df.reset_index(drop=True)


def drop_columns_and_rows(
    df: pd.DataFrame,
    keep_columns: DictConfig,
    remove_outliers_threshold: DictConfig,
) -> pd.DataFrame:
    df = df.pipe(drop_features, keep_columns=keep_columns).pipe(
        drop_outliers, column_threshold=remove_outliers_threshold
    )

    return df


def get_scaler(df: pd.DataFrame):
    scaler = StandardScaler()
    scaler.fit(df)

    return scaler


def save_scaler(scaler: StandardScaler, path: str):
    path = abs(path)
    Path(path).parent.mkdir(exist_ok=True)
    joblib.dump(scaler, path)


def scale_features(df: pd.DataFrame, scaler: StandardScaler):
    return pd.DataFrame(scaler.transform(df), columns=df.columns)


@hydra.main(version_base=None, config_path="../conf", config_name="config")
def process_data(config: DictConfig):
    df = load_data(config.data.raw)
    df = drop_na(df)
    df = get_age(df)
    df = get_total_children(df)
    df = get_total_purchases(df)
    df = get_enrollment_years(df)
    df = get_family_size(df, config.process.encode.family_size)
    df = drop_columns_and_rows(
        df,
        config.process.keep_columns,
        config.process.remove_outliers_threshold,
    )
    scaler = get_scaler(df)
    df = scale_features(df, scaler)
    save_data(df, config.data.scaled)
    save_scaler(scaler, config.scaler)


if __name__ == "__main__":
    process_data()
