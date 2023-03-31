import numpy as np
import pandas as pd
from omegaconf import DictConfig
from pandas.testing import assert_frame_equal, assert_series_equal

from src.process_data import (drop_features, drop_na, drop_outliers, get_age,
                              get_enrollment_years, get_family_size,
                              get_scaler, get_total_children,
                              get_total_purchases, scale_features)


def test_drop_na():
    df = pd.DataFrame({"a": [1, 2, 3], "b": [np.nan, 2, 1]})
    expected = pd.DataFrame({"a": [2, 3], "b": [2, 1]})
    df_without_na = drop_na(df)
    assert_frame_equal(df_without_na, expected, check_dtype=False)


def test_get_age():
    df = pd.DataFrame({"Year_Birth": [1990, 1995, 1997, 1988, 1982]})
    df_with_age = get_age(df)
    assert_series_equal(
        df_with_age["age"], pd.Series([31, 26, 24, 33, 39]), check_names=False
    )


def test_get_total_children():
    df = pd.DataFrame(
        {"Kidhome": [1, 0, 0, 2, 1], "Teenhome": [1, 1, 2, 0, 1]}
    )
    df_with_total_children = get_total_children(df)
    assert_series_equal(
        df_with_total_children["total_children"],
        pd.Series([2, 1, 2, 2, 2]),
        check_names=False,
    )


def test_get_total_purchases():
    df = pd.DataFrame(
        {"Num Web Purchases": [1, 2, 3], "Num Store Purchases": [4, 5, 6]}
    )
    df_with_total_purchases = get_total_purchases(df)
    assert_series_equal(
        df_with_total_purchases["total_purchases"],
        pd.Series([5, 7, 9]),
        check_names=False,
    )


def test_get_enrollment_years():
    df = pd.DataFrame(
        {
            "Dt_Customer": [
                "05-10-2020",
                "15-02-2021",
                "10-03-2021",
                "20-11-2018",
                "12-09-2017",
            ]
        }
    )
    df_with_enrollment_years = get_enrollment_years(df)
    assert_series_equal(
        df_with_enrollment_years["enrollment_years"],
        pd.Series([2, 1, 1, 4, 5]),
        check_names=False,
    )


def test_get_family_size():
    df = pd.DataFrame(
        {
            "Marital_Status": [
                "Married",
                "Single",
                "Divorced",
                "Widow",
                "Together",
            ],
            "total_children": [1, 2, 1, 3, 2],
        }
    )
    size_map = DictConfig(
        {
            "Single": 1,
            "Married": 2,
            "Together": 2,
            "Divorced": 1,
            "Widow": 1,
        }
    )
    df_with_family_size = get_family_size(df, size_map)
    assert_series_equal(
        df_with_family_size["family_size"],
        pd.Series([3, 3, 2, 4, 4]),
        check_names=False,
    )


def test_drop_features():
    df = pd.DataFrame({"a": [1, 2], "b": [2, 3], "c": [3, 4]})
    keep_columns = ["a", "b"]
    df_without_outliers = drop_features(df, keep_columns)
    assert set(df_without_outliers.columns) == set(keep_columns)


def test_drop_outliers():
    df = pd.DataFrame({"Income": [1000, 35_000, 150_000]})
    column_threshold = DictConfig({"Income": 100_000})
    df_without_outliers = drop_outliers(df, column_threshold)
    assert_series_equal(
        df_without_outliers["Income"],
        pd.Series([1000, 35_000]),
        check_names=False,
    )


def test_scale_features():
    df = pd.DataFrame({"a": [100, 20, 50], "b": [1, 3, 5]})
    scaler = get_scaler(df)
    df_scaled = scale_features(df, scaler)
    assert df_scaled.shape == df.shape
    # Test that the mean and standard deviation of the scaled dataframe are close to 0 and 1, respectively
    for col in df.columns:
        assert np.isclose(df_scaled[col].mean(), 0, atol=0.01)
        assert np.isclose(df_scaled[col].std(), 1, atol=0.3)
