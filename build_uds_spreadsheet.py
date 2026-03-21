import pandas as pd

def clean_id(x):
    s = str(x).replace('.0', '').strip()
    if s and s != 'nan' and s != '---':
        return s.zfill(6)
    return s

def build_spreadsheet(year):
    filename = f"h80-{year}.xlsx"
    print(f"Processing {filename}...")
    
    df_info = pd.read_excel(filename, sheet_name="HealthCenterInfo", dtype=str)
    df_info['BHCMISID'] = df_info['BHCMISID'].apply(clean_id)
    df_info['HealthCenterState'] = df_info['HealthCenterState'].astype(str).str.strip()
    df_ma = df_info[df_info['HealthCenterState'] == 'MA'].copy()
    print(f"Found {len(df_ma)} MA health centers in {year}.")
    
    df_8a = pd.read_excel(filename, sheet_name="Table8A", dtype=str)
    df_8a['BHCMISID'] = df_8a['BHCMISID'].apply(clean_id)
    cost_col = [c for c in df_8a.columns if str(c).upper() == 'T8A_L17_CC'][0]
    df_8a = df_8a[['BHCMISID', cost_col]]
    
    df_9e = pd.read_excel(filename, sheet_name="Table9E", dtype=str)
    df_9e['BHCMISID'] = df_9e['BHCMISID'].apply(clean_id)
    rev_col = [c for c in df_9e.columns if str(c).upper() == 'T9E_L11_CA'][0]
    df_9e = df_9e[['BHCMISID', rev_col]]
    
    merged = df_ma.merge(df_8a, on='BHCMISID', how='inner')
    merged = merged.merge(df_9e, on='BHCMISID', how='inner')
    
    merged[cost_col] = pd.to_numeric(merged[cost_col], errors='coerce')
    merged[rev_col] = pd.to_numeric(merged[rev_col], errors='coerce')
    
    merged = merged.rename(columns={
        'HealthCenterName': 'Health Center Name',
        'HealthCenterCity': 'City',
        cost_col: 'Total Cost',
        rev_col: 'Total Revenue'
    })
    
    merged['Operating Margin (%)'] = ((merged['Total Revenue'] - merged['Total Cost']) / merged['Total Revenue'] * 100).round(2)
    merged['Cost to Revenue Ratio (%)'] = (merged['Total Cost'] / merged['Total Revenue'] * 100).round(2)
    
    final_cols = ['Health Center Name', 'City', 'Total Revenue', 'Total Cost', 'Operating Margin (%)', 'Cost to Revenue Ratio (%)']
    final_df = merged[final_cols].sort_values(by='Operating Margin (%)', ascending=False)
    
    out_name = f"MA_FQHC_Financials_{year}.csv"
    final_df.to_csv(out_name, index=False)
    print(f"Saved {len(final_df)} records to {out_name}.")
    return final_df

if __name__ == '__main__':
    df2023 = build_spreadsheet(2023)
