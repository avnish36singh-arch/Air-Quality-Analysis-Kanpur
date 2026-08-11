import pandas as pd
import numpy as np

STATIONS = {229252: "NSI Kalyanpur", 5662: "Nehru Nagar"}
WEATHER_VARS = ['temperature', 'relativehumidity', 'wind_speed', 'wind_direction']

def load_var(location_id, param):
    df = pd.read_csv(f"kanpur_{location_id}_{param}_merged.csv")
    df['datetime_from'] = pd.to_datetime(df['datetime_from'])
    df = df[['datetime_from', 'value']].rename(columns={'value': param})
    df = df.drop_duplicates(subset='datetime_from', keep='first')
    return df

all_merged = []

for location_id, name in STATIONS.items():
    print(f"\n=== {name} ({location_id}) ===")

    pm25 = pd.read_csv(f"kanpur_{location_id}_pm25_merged.csv")
    pm25['datetime_from'] = pd.to_datetime(pm25['datetime_from'])
    pm25 = pm25[['datetime_from','value']].rename(columns={'value':'pm25'}).drop_duplicates('datetime_from')
    pm25 = pm25[(pm25['pm25'] >= 0) & (pm25['pm25'] <= 1000)]

    pm10 = pd.read_csv(f"kanpur_{location_id}_pm10_merged.csv")
    pm10['datetime_from'] = pd.to_datetime(pm10['datetime_from'])
    pm10 = pm10[['datetime_from','value']].rename(columns={'value':'pm10'}).drop_duplicates('datetime_from')
    pm10 = pm10[(pm10['pm10'] >= 0) & (pm10['pm10'] <= 1000)]

    merged = pd.merge(pm25, pm10, on='datetime_from', how='outer')

    for wv in WEATHER_VARS:
        wdf = load_var(location_id, wv)
        merged = pd.merge(merged, wdf, on='datetime_from', how='inner')

    merged['location_id'] = location_id
    merged['location_name'] = name
    merged = merged.sort_values('datetime_from')

    print(f"  Hourly rows with weather + at least one pollutant: {len(merged)}")
    print(f"  Date range: {merged['datetime_from'].min()} to {merged['datetime_from'].max()}")

    merged.to_csv(f"data/weather_merged_{location_id}.csv", index=False)
    all_merged.append(merged)

combined = pd.concat(all_merged, ignore_index=True)
combined.to_csv("data/weather_merged_combined.csv", index=False)
print(f"\nTotal combined rows: {len(combined)}")

print("\n=== Correlation matrix (Pearson) ===")
for location_id, name in STATIONS.items():
    sub = combined[combined['location_id']==location_id]
    corr = sub[['pm25','pm10','temperature','relativehumidity','wind_speed']].corr()
    print(f"\n{name}:")
    print(corr.round(2))
