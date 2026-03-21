import pandas as pd

def find_columns():
    # Table 8A
    df8 = pd.read_excel("h80-2023.xlsx", sheet_name="Table8A", header=None, nrows=2)
    t8_cols = df8.iloc[0].values
    t8_desc = df8.iloc[1].values
    for c, d in zip(t8_cols, t8_desc):
        if 'total' in str(d).lower() and 'cost' in str(d).lower():
            print(f"Table8A Possible Total Cost: {c} -> {d}")
            if '17' in str(c) or '35' in str(c):
                print(f"  *** High confidence: {c}")

    # Table 9D
    df9d = pd.read_excel("h80-2023.xlsx", sheet_name="Table9D", header=None, nrows=2)
    t9d_cols = df9d.iloc[0].values
    t9d_desc = df9d.iloc[1].values
    for c, d in zip(t9d_cols, t9d_desc):
        if 'total' in str(d).lower() and 'revenue' in str(d).lower():
            print(f"Table9D Possible Revenue: {c} -> {d}")

    # Table 9E
    df9e = pd.read_excel("h80-2023.xlsx", sheet_name="Table9E", header=None, nrows=2)
    t9e_cols = df9e.iloc[0].values
    t9e_desc = df9e.iloc[1].values
    for c, d in zip(t9e_cols, t9e_desc):
        if 'total' in str(d).lower() and 'revenue' in str(d).lower():
            print(f"Table9E Possible Revenue: {c} -> {d}")

find_columns()
