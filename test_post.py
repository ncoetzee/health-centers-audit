import requests

API_KEY = "YDgWzfe3BWh5nemujfGo9BIuiim7QiFAbdHvbC5G"
headers = {"x-api-key": API_KEY}
BASE_URL = "https://api.fac.gov"

# Try POSTing multiple formats
report_id = "2023-06-GSAFAC-0000001450"
print("Testing POST JSON...")
res1 = requests.post(f"{BASE_URL}/rpc/request_file_access", headers=headers, json={"report_id": report_id})
print(res1.status_code, res1.text[:200])

print("\nTesting POST Form...")
res2 = requests.post(f"{BASE_URL}/rpc/request_file_access", headers=headers, data={"report_id": report_id})
print(res2.status_code, res2.text[:200])
