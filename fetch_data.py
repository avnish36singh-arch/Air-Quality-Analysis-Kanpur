import requests
import pandas as pd
import time
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")
HEADERS = {"X-API-Key": API_KEY}
BASE_URL = "https://api.openaq.org/v3"

STATIONS = {
    229252: {
        "name": "NSI Kalyanpur, Kanpur",
        "temperature": [12236696],
        "relativehumidity": [12236694],
        "wind_speed": [14341073],
        "wind_direction": [14341072],
    },
    5662: {
        "name": "Nehru Nagar, Kanpur",
        "temperature": [12235516],
        "relativehumidity": [12235514],
        "wind_speed": [14341850],
        "wind_direction": [14341849],
    }
}

def safe_get(url, params=None, retries=6):
    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(url, headers=HEADERS, params=params, timeout=40)
            return resp
        except (requests.exceptions.ConnectionError,
                requests.exceptions.SSLError,
                requests.exceptions.Timeout,
                requests.exceptions.ReadTimeout) as e:
            wait = attempt * 3
            print(f"    Network error (attempt {attempt}/{retries}): {type(e).__name__}")
            print(f"    Retrying in {wait}s...")
            time.sleep(wait)
    print(f"    GIVING UP on {url} after {retries} retries, skipping this sensor.")
    return None

def get_all_measurements(sensor_id):
    all_data = []
    page = 1
    limit = 1000
    while True:
        url = f"{BASE_URL}/sensors/{sensor_id}/hours"
        params = {"limit": limit, "page": page}
        resp = safe_get(url, params=params)
        if resp is None:
            break
        if resp.status_code != 200:
            print(f"    Stopped at page {page}, status {resp.status_code}: {resp.text[:200]}")
            break
        results = resp.json().get("results", [])
        if not results:
            break
        all_data.extend(results)
        print(f"    sensor {sensor_id}: page {page}, {len(results)} rows (total: {len(all_data)})")
        if len(results) < limit:
            break
        page += 1
        time.sleep(1)
    return all_data

def main():
    for location_id, info in STATIONS.items():
        location_name = info["name"]
        print(f"\n=== {location_name} ({location_id}) ===")
        for param, sensor_ids in info.items():
            if param == "name":
                continue
            print(f"  Pulling {param} from sensors {sensor_ids}...")
            all_rows = []
            for sensor_id in sensor_ids:
                data = get_all_measurements(sensor_id)
                for d in data:
                    all_rows.append({
                        "location_id": location_id,
                        "location_name": location_name,
                        "parameter": param,
                        "sensor_id": sensor_id,
                        "value": d["value"],
                        "datetime_from": d["period"]["datetimeFrom"]["utc"],
                        "datetime_to": d["period"]["datetimeTo"]["utc"],
                    })
            if not all_rows:
                print(f"  No data at all for {param}")
                continue
            df = pd.DataFrame(all_rows)
            df["datetime_from"] = pd.to_datetime(df["datetime_from"])
            df = df.sort_values("datetime_from")
            df = df.drop_duplicates(subset="datetime_from", keep="first")
            filename = f"kanpur_{location_id}_{param}_merged.csv"
            df.to_csv(filename, index=False)
            print(f"  Saved {len(df)} rows to {filename} (range: {df['datetime_from'].min()} to {df['datetime_from'].max()})")

if __name__ == "__main__":
    main()