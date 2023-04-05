columns = ['mode value', 'frequency', '% of values']

column_index = []
rows = []
for col in df_1.columns:
    value_counts = df_1[col].value_counts()
    if len(value_counts.index) == 0:
        continue
    column_value = value_counts.index[0]
    value = value_counts[column_value]
    number_of_rows = df_1[col].count()
    column_index.append(col)
    rows.append([
        column_value,
        f'{round(100 * value / number_of_rows, 2)}%',
        value,
      ])
