import requests
import json
import time

API_KEY = "Rh24VyLekR832grMXT5eEXTADfJHQR9NhIim2hP4"
headers = {"x-api-key": API_KEY}
BASE_URL = "https://api.fac.gov"

def fetch_metadata():
    print("Fetching general records for MA (2023-2025)...")
    ma_records = []
    offset = 0
    limit = 1000
    while True:
        general_url = f"{BASE_URL}/general?auditee_state=eq.MA&audit_year=in.(2023,2024,2025)&limit={limit}&offset={offset}"
        res = requests.get(general_url, headers=headers)
        if res.status_code == 200:
            batch = res.json()
            if not batch:
                break
            ma_records.extend(batch)
            offset += limit
        else:
            print("Error fetching general:", res.status_code, res.text)
            break
            
    print(f"Found {len(ma_records)} total audits in MA.")
    reports_map = {r['report_id']: r for r in ma_records}

    print("Fetching federal awards to find FQHCs (ALN 93.224 or 93.527)...")
    health_center_reports = set()
    offset = 0
    while True:
        # CFDA 93.224 and 93.527 are the Health Center Program
        url = f"{BASE_URL}/federal_awards?federal_agency_prefix=eq.93&federal_award_extension=in.(224,527)&audit_year=in.(2023,2024,2025)&limit={limit}&offset={offset}"
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            awards = res.json()
            if not awards:
                break
            for a in awards:
                if a['report_id'] in reports_map:
                    health_center_reports.add(a['report_id'])
            offset += limit
        else:
            print("Error fetching awards:", res.status_code, res.text)
            break

    print(f"Found {len(health_center_reports)} FQHC audits in MA.")
    fqhc_records = [reports_map[rid] for rid in health_center_reports]
    with open("fqhc_audits_ma.json", "w") as f:
        json.dump(fqhc_records, f, indent=2)

    print("Saved FQHC metadata to fqhc_audits_ma.json.")

if __name__ == '__main__':
    fetch_metadata()
