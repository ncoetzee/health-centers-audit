import pandas as pd

filename = "h80-2023.xlsx"
df_info = pd.read_excel(filename, sheet_name="HealthCenterInfo")
df_info['BHCMISID'] = df_info['BHCMISID'].astype(str).str.strip()
df_info['HealthCenterState'] = df_info['HealthCenterState'].astype(str).str.strip()
df_ma = df_info[df_info['HealthCenterState'] == 'MA']

df_8a = pd.read_excel(filename, sheet_name="Table8A")
df_8a['BHCMISID'] = df_8a['BHCMISID'].astype(str).str.strip()

print("MA IDs:", df_ma['BHCMISID'].head(5).values)
print("Table8A IDs:", df_8a['BHCMISID'].head(10).values)

merged = df_ma.merge(df_8a, on='BHCMISID', how='inner')
print("Merged len:", len(merged))
