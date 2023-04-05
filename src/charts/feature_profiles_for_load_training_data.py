from mage_ai.data_cleaner.column_types.column_type_detector import infer_column_types
import statistics


columns_and_types = infer_column_types(df_1).items()
columns = [t[0] for t in columns_and_types]
stats = ['Type', 'Missing values', 'Unique values', 'Min', 'Max', 'Mean', 'Median', 'Mode']
rows = [[] for _ in stats]

for col, col_type in columns_and_types:
    series = df_1[col]
    min_value = None
    max_value = None
    mean = None
    median = None

    not_null = series[series.notnull()]

    if col_type.value in ['number', 'number_with_decimals']:
        count = len(not_null.index)
        if count >= 1:
            mean = round(not_null.sum() / count, 2)
            median = sorted(not_null)[int(count / 2)]
        min_value = round(series.min(), 2)
        max_value = round(series.max(), 2)
    else:
        min_value = not_null.astype(str).min()
        max_value = not_null.astype(str).max()

    _, mode = sorted(
      [(v, k) for k, v in not_null.value_counts().items()],
      reverse=True,
    )[0]

    for idx, value in enumerate([
        col_type.value,
        len(series[series.isna()].index),
        len(series.unique()),
        min_value,
        max_value,
        mean,
        median,
        mode,
    ]):
      rows[idx].append(value)
