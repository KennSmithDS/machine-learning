def classify(row):
    row_class = 0
    if row['close'] > row['open'] and row['close'] == row['high']:
        row_class = 3
    elif row['close'] > row['open'] and row['close'] < row['high']:
        row_class = 2
    elif row['close'] < row['open'] and row['close'] > row['low']:
        row_class = 1
    else:
        pass
    return row_class