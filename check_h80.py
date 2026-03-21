import requests
import pandas as pd

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

def fetch_and_check(year):
    url = f"https://www.hrsa.gov/sites/default/files/hrsa/foia/h80-{year}.xlsx"
    alt_url = f"https://bphc.hrsa.gov/sites/default/files/bphc/datareporting/research/h80-{year}.xlsx"
    print(f"Fetching {year}...")
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        res = requests.get(alt_url, headers=headers)
    
    if res.status_code == 200:
        filename = f"h80-{year}.xlsx"
        with open(filename, "wb") as f:
            f.write(res.content)
        # Try to read all sheets
        xl = pd.ExcelFile(filename)
        print(f"Found {year} sheets:", xl.sheet_names)
        
        for sheet in xl.sheet_names:
            df = xl.parse(sheet, nrows=5)
            financials = [c for c in df.columns if any(x in str(c).lower() for x in ['asset', 'liabilit', 'revenue', 'cost', 'cash'])]
            if financials:
                print(f"  {sheet} Financial columns:", financials[:10])
    else:
        print(f"Failed {year}:", res.status_code)

fetch_and_check(2023)
fetch_and_check(2024)
