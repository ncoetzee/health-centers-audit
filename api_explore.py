import requests
import json

API_KEY = "Rh24VyLekR832grMXT5eEXTADfJHQR9NhIim2hP4"
headers = {"x-api-key": API_KEY}

def probe(url):
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        data = res.json()
        if isinstance(data, list) and len(data) > 0:
            print(f"[{url}] Fields:")
            print("  ", list(data[0].keys()))
        else:
            print(f"[{url}] Data:", str(data)[:500])
    else:
        print(f"[{url}] Error:", res.status_code, res.text)

probe("https://api.fac.gov/general?limit=1")
probe("https://api.fac.gov/federal_awards?limit=1")

with open("swagger.json", "r") as f:
    schema = json.load(f)
    print("\nRPC params:")
    # Print the rpc definition
    rpc = schema.get('paths', {}).get('/rpc/request_file_access', {})
    print(json.dumps(rpc, indent=2)[:500])
