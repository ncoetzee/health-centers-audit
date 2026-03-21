import requests
import json
import sys

API_KEY = "Rh24VyLekR832grMXT5eEXTADfJHQR9NhIim2hP4"
headers = {"x-api-key": API_KEY}
BASE_URL = "https://api.fac.gov"

print("Fetching FQHC federal awards (CFDA 93.224, 93.527)...")
fqhc_report_ids = set()

offset = 0
while True:
    url = f"{BASE_URL}/federal_awards?federal_agency_prefix=eq.93&federal_award_extension=in.(224,527)&audit_year=in.(2023,2024,2025)&limit=5000&offset={offset}"
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        print("Error:", res.status_code, res.text)
        break
    data = res.json()
    if not data:
        break
    for d in data:
        fqhc_report_ids.add(d['report_id'])
    offset += 5000

print(f"Total FQHC report IDs nationwide: {len(fqhc_report_ids)}")

print("Fetching MA general records (2023-2025)...")
ma_fqhc_records = []
offset = 0
while True:
    url2 = f"{BASE_URL}/general?auditee_state=eq.MA&audit_year=in.(2023,2024,2025)&limit=5000&offset={offset}"
    res2 = requests.get(url2, headers=headers)
    if res2.status_code != 200:
        break
    data2 = res2.json()
    if not data2:
        break
    for g in data2:
        if g['report_id'] in fqhc_report_ids:
            ma_fqhc_records.append(g)
    offset += 5000

print(f"Found {len(ma_fqhc_records)} MA FQHC records.")
with open("ma_fqhc_metadata.json", "w") as f:
    json.dump(ma_fqhc_records, f, indent=2)

if ma_fqhc_records:
    # Test rpc endpoint for the first record
    test_id = ma_fqhc_records[0]['report_id']
    print(f"\nTesting PDF download link for report_id: {test_id}")
    rpc_res = requests.get(f"{BASE_URL}/rpc/request_file_access?report_id={test_id}", headers=headers)
    print("RPC status:", rpc_res.status_code)
    try:
        print(rpc_res.json())
    except:
        print(rpc_res.text[:500])
