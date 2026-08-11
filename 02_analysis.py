import pandas as pd
import numpy as np

STATIONS = {229252: "NSI Kalyanpur", 5662: "Nehru Nagar"}

def pm25_category(v):
    if v <= 30: return "Good"
    elif v <= 60: return "Satisfactory"
    elif v <= 90: return "Moderate"
    elif v <= 120: return "Poor"
    elif v <= 250: return "Very Poor"
    else: return "Severe"

def pm10_category(v):
    if v <= 50: return "Good"
    elif v <= 100: return "Satisfactory"
    elif v <= 250: return "Moderate"
    elif v <= 350: return "Poor"
    elif v <= 430: return "Very Poor"
    else: return "Severe"

CATEGORY_ORDER = ["Good", "Satisfactory", "Moderate", "Poor", "Very Poor", "Severe"]

all_daily = []

for location_id, name in STATIONS.items():
    df = pd.read_csv(f"data/cleaned_{location_id}.csv")
    df['datetime_from'] = pd.to_datetime(df['datetime_from'])
    df = df[df['window'] != 'Other/Gap period'].copy()

    df['date'] = df['datetime_from'].dt.date
    daily = df.groupby(['date','window']).agg(pm25=('pm25','mean'), pm10=('pm10','mean')).reset_index()
    daily['date'] = pd.to_datetime(daily['date'])
    daily['location_id'] = location_id
    daily['location_name'] = name
    daily['pm25_category'] = daily['pm25'].apply(lambda v: pm25_category(v) if pd.notna(v) else np.nan)
    daily['pm10_category'] = daily['pm10'].apply(lambda v: pm10_category(v) if pd.notna(v) else np.nan)
    all_daily.append(daily)

daily_all = pd.concat(all_daily, ignore_index=True)
daily_all.to_csv("data/daily_aggregated.csv", index=False)
print(f"Total daily records: {len(daily_all)}")
print(daily_all.groupby('location_name').size())

daily_all['month'] = daily_all['date'].dt.month
monthly = daily_all.groupby(['location_name','month'])[['pm25','pm10']].mean().round(1)
print("\n=== Monthly averages ===")
print(monthly)
monthly.to_csv("data/monthly_averages.csv")

print("\n=== PM2.5 AQI category breakdown (% of days) ===")
for loc in daily_all['location_name'].unique():
    sub = daily_all[daily_all['location_name']==loc].dropna(subset=['pm25_category'])
    pct = (sub['pm25_category'].value_counts(normalize=True)*100).reindex(CATEGORY_ORDER).fillna(0).round(1)
    print(f"\n{loc} (n={len(sub)} days):")
    print(pct)

diurnal_all = []
for location_id, name in STATIONS.items():
    df = pd.read_csv(f"data/cleaned_{location_id}.csv")
    df['datetime_from'] = pd.to_datetime(df['datetime_from'])
    df = df[df['window'] != 'Other/Gap period'].copy()
    df['hour'] = (df['datetime_from'] + pd.Timedelta(hours=5, minutes=30)).dt.hour
    hourly = df.groupby('hour')[['pm25','pm10']].mean().reset_index()
    hourly['location_name'] = name
    diurnal_all.append(hourly)
diurnal_df = pd.concat(diurnal_all, ignore_index=True)
diurnal_df.to_csv("data/diurnal_pattern.csv", index=False)
print("\nSaved data/diurnal_pattern.csv")