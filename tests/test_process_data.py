import pandas as pd
from pandas.testing import assert_frame_equal, assert_series_equal

from src.process_data import get_X_y


def test_get_X_y():
    """Test get_X_y function"""
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": [0, 1, 0]})
    feature = "c"
    X, y = get_X_y(df, feature)
    expected_X = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    expected_y = pd.Series([0, 1, 0])
    assert_frame_equal(X, expected_X)
    assert_series_equal(y, expected_y, check_names=False)
