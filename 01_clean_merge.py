import pandas as pd
import numpy as np

STATIONS = {
    229252: "NSI Kalyanpur",
    5662: "Nehru Nagar"
}

def load_pollutant(location_id, param):
    df = pd.read_csv(f"kanpur_{location_id}_{param}_merged.csv")
    df['datetime_from'] = pd.to_datetime(df['datetime_from'])
    df = df[['datetime_from', 'value']].rename(columns={'value': param})
    df = df.drop_duplicates(subset='datetime_from', keep='first')
    before = len(df)
    df = df[df[param] >= 0]
    after = len(df)
    print(f"  {param}: dropped {before-after} negative/invalid readings")
    before = len(df)
    df = df[df[param] <= 1000]
    after = len(df)
    print(f"  {param}: dropped {before-after} extreme outlier readings (>1000 ug/m3)")
    return df

def tag_window(dt):
    if pd.Timestamp('2021-07-01', tz='UTC') <= dt <= pd.Timestamp('2022-10-31', tz='UTC'):
        return 'Window 1 (Jul 2021 - Oct 2022)'
    elif dt >= pd.Timestamp('2025-02-01', tz='UTC'):
        return 'Window 2 (Feb 2025 - present)'
    else:
        return 'Other/Gap period'

for location_id, name in STATIONS.items():
    print(f"\n=== {name} ({location_id}) ===")
    pm25 = load_pollutant(location_id, 'pm25')
    pm10 = load_pollutant(location_id, 'pm10')

    merged = pd.merge(pm25, pm10, on='datetime_from', how='outer')
    merged = merged.sort_values('datetime_from')
    merged['window'] = merged['datetime_from'].apply(tag_window)
    merged['location_id'] = location_id
    merged['location_name'] = name

    print(f"  Merged rows: {len(merged)}")
    merged.to_csv(f"data/cleaned_{location_id}.csv", index=False)
    print(f"  Saved data/cleaned_{location_id}.csv")