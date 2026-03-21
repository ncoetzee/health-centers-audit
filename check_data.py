import json

with open("ma_fqhc_metadata.json", "r") as f:
    records = json.load(f)

if records:
    print("General Fields in metadata:")
    for k, v in records[0].items():
        print(f"  {k}: {v}")
