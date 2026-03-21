import pandas as pd

def inspect_sheet(filename, sheet_name):
    print(f"\n--- {sheet_name} ---")
    df = pd.read_excel(filename, sheet_name=sheet_name, header=None, nrows=10)
    for index, row in df.iterrows():
        print(row.values[:8])  # print first 8 columns

inspect_sheet("h80-2023.xlsx", "HealthCenterInfo")
inspect_sheet("h80-2023.xlsx", "Table8A")
inspect_sheet("h80-2023.xlsx", "Table9E")
