import requests 
from datetime import date, timedelta
import pandas as pd
import time
import os


BASE_URL = "https://api.anera.markets"

params = {"timestamp": "2026-06-01"}

response = requests.get(f"{BASE_URL}/api/v1/public/revenue/model", params = params)


response.raise_for_status()

data = response.json()

#print(data["timestamp"], "->", len(data["items"]), "models")

def count_models_by_day(start, end) :
    """For each day from start to end, record how many models have revenue data.
    Returns a list of (date_string, count) tuples."""
    results = []
    current = start
    while current <= end:
        day = current.isoformat()
        params = {"timestamp": day}
        response = requests.get(f"{BASE_URL}/api/v1/public/revenue/model", params = params)

        if response.status_code == 200:
            count = len(response.json()["items"])
        else:
            count = 0
        results.append((day,count))
        print(f"{day} -> {count}")
        current+=timedelta(days=1)
        time.sleep(0.05)
    return results


# series = count_models_by_day(date(2025, 6, 1), date(2026, 1, 1))

# with_data = [d for d, c in series if c > 0]
# print("first date with data:", with_data[0] if with_data else "none found")
        
# checks = requests.get(f"{BASE_URL}/api/v1/public/revenue/model").json()

# print(len(checks["items"]))

def build_revs_panel(start, end):
    """For a time frame build a daily company and api revenus panel/dataframe"""
    results = []
    current = start
    while current <= end:
        day = current.isoformat()
        params = {"timestamp": day}
        response = requests.get(f"{BASE_URL}/api/v1/public/revenue/model", params=params)

        if response.status_code == 200:
            for item in response.json().get("items", []):
                results.append({"date":day, "model":item["resource_id"], "revenue":item["revenue_usd"] })
                

        current += timedelta(days=1)
        print(f"{day} -> {len(results)} rows so far")
        time.sleep(0.1)
    return pd.DataFrame(results)


panel = build_revs_panel(date(2026,1,1), date(2026,6,19))
panel.to_parquet("data/model_revenue.parquet",index=False)
print(panel.head())
print(panel.shape)








