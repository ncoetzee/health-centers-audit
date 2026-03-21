import requests
from bs4 import BeautifulSoup
import re

url = "https://data.hrsa.gov/data/download"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

links = []
for a in soup.find_all('a', href=True):
    href = a['href']
    text = a.text.lower()
    if 'uds' in text or 'uniform data' in text or 'health center' in text.lower():
        links.append((a.text.strip(), href))
    elif 'zip' in href.lower() or 'csv' in href.lower() or 'xlsx' in href.lower():
        if 'uds' in href.lower() or 'health_center' in href.lower() or 'hcsd' in href.lower():
            links.append((a.text.strip(), href))

print("Found interesting links:")
for name, link in list(set(links)):
    print(f"{name}: {link}")
