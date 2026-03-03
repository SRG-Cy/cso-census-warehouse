import requests
import json
import os

BASE_URL = "https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset"

def fetch_dataset(code):
    url = f"{BASE_URL}/{code}/JSON-stat/2.0/en"
    print(f"Fetching {code}...")
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    data = fetch_dataset("FY001")
    with open("data/fy001_population.json", "w") as f:
        json.dump(data, f, indent=2)
    print("✅ Saved to data/fy001_population.json")