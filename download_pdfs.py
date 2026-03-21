import requests
import json
import os
import time

API_KEY = "YDgWzfe3BWh5nemujfGo9BIuiim7QiFAbdHvbC5G"
headers = {"x-api-key": API_KEY}
BASE_URL = "https://api.fac.gov"

if not os.path.exists("pdfs"):
    os.makedirs("pdfs")

with open("ma_fqhc_metadata.json", "r") as f:
    records = json.load(f)

print(f"Starting download for {len(records)} reports...")

# Only test downloading 3 initially to make sure the script and URLs are correct before spamming
for r in records[:5]:
    report_id = r['report_id']
    pdf_path = f"pdfs/{report_id}.pdf"
    if os.path.exists(pdf_path):
        continue
        
    res = requests.get(f"{BASE_URL}/rpc/request_file_access?report_id={report_id}", headers=headers)
    if res.status_code == 200:
        data = res.json()
        download_url = None
        if isinstance(data, dict) and "url" in data:
            download_url = data["url"]
        elif isinstance(data, str):
            if data.startswith("http"):
                download_url = data
            elif data.endswith(".pdf"):
                download_url = f"{BASE_URL}/{data}"
        elif isinstance(data, list) and len(data) > 0:
            if isinstance(data[0], dict) and "url" in data[0]:
                download_url = data[0]["url"]
            elif isinstance(data[0], str):
                download_url = data[0]

        # The FAC API might also return a direct redirect for file access
        if download_url:
            print(f"Downloading {report_id} from {download_url[:30]}...")
            pdf_res = requests.get(download_url)
            with open(pdf_path, "wb") as pdf_file:
                pdf_file.write(pdf_res.content)
            time.sleep(1)
        else:
            print(f"Could not find URL for {report_id}. Schema was: {str(data)[:200]}")
    else:
        print(f"Error accessing {report_id}: {res.status_code} {res.text}")

print("Test chunk downloads finished.")
