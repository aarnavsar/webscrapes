import requests 
from datetime import date, timedelta
import time



BASE_URL = "https://api.anera.markets"

params = {"timestamp": "2025-06-01"}

response = requests.get(f"{BASE_URL}/api/v1/public/revenue/model", params = params)


response.raise_for_status()

data = response.json()

print(data["timestamp"], "->", len(data["items"]), "models")

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

series = count_models_by_day(date(2026, 1, 1), date(2026, 6, 18))

with_data = [d for d, c in series if c > 0]
print("first date with data:", with_data[0] if with_data else "none found")
        
