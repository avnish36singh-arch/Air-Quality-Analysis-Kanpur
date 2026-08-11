import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 150

daily = pd.read_csv("data/daily_aggregated.csv")
daily['date'] = pd.to_datetime(daily['date'])
monthly = pd.read_csv("data/monthly_averages.csv")
diurnal = pd.read_csv("data/diurnal_pattern.csv")

MONTH_NAMES = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

# CHART 1: Time series with visible gap
fig, ax = plt.subplots(figsize=(13,5))
for loc, color in zip(daily['location_name'].unique(), ['#e07b39','#3d7ea6']):
    sub = daily[daily['location_name']==loc].sort_values('date').copy()
    sub = sub.set_index('date')
    full_range = pd.date_range(sub.index.min(), sub.index.max(), freq='D')
    sub = sub.reindex(full_range)
    ax.plot(sub.index, sub['pm25'], label=loc, color=color, linewidth=1, alpha=0.85)
ax.axhline(60, color='orange', linestyle='--', linewidth=1, label='Satisfactory/Moderate threshold (60)')
ax.axhline(120, color='red', linestyle='--', linewidth=1, label='Poor/Very Poor threshold (120)')
ax.set_title('Kanpur PM2.5 — Daily Average, Two Monitoring Windows (2021-2022 & 2025-2026)', fontsize=13)
ax.set_ylabel('PM2.5 (µg/m³)')
ax.set_xlabel('Date')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax.legend(loc='upper left', fontsize=9)
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig('charts/01_timeseries.png')
plt.close()
print("Saved 01_timeseries.png")

# CHART 2: Monthly seasonal average
fig, ax = plt.subplots(figsize=(12,5))
pivot = monthly.pivot(index='month', columns='location_name', values='pm25')
pivot = pivot.reindex(range(1,13))
pivot.index = MONTH_NAMES
pivot.plot(kind='bar', ax=ax, color=['#e07b39','#3d7ea6'], width=0.75)
ax.axhline(60, color='orange', linestyle='--', linewidth=1)
ax.set_title('Kanpur PM2.5 — Average by Month (all years combined)', fontsize=13)
ax.set_ylabel('PM2.5 (µg/m³)')
ax.set_xlabel('Month')
plt.xticks(rotation=0)
plt.legend(title='')
plt.tight_layout()
plt.savefig('charts/02_monthly_seasonal.png')
plt.close()
print("Saved 02_monthly_seasonal.png")

# CHART 3: AQI category breakdown
CATEGORY_ORDER = ["Good", "Satisfactory", "Moderate", "Poor", "Very Poor", "Severe"]
CATEGORY_COLORS = ['#4CAF50','#8BC34A','#FFC107','#FF9800','#F44336','#7B1FA2']
fig, ax = plt.subplots(figsize=(10,5))
breakdown = {}
for loc in daily['location_name'].unique():
    sub = daily[daily['location_name']==loc].dropna(subset=['pm25_category'])
    pct = (sub['pm25_category'].value_counts(normalize=True)*100).reindex(CATEGORY_ORDER).fillna(0)
    breakdown[loc] = pct
bd_df = pd.DataFrame(breakdown)
bottom = pd.Series([0]*len(bd_df.columns), index=bd_df.columns)
for cat, color in zip(CATEGORY_ORDER, CATEGORY_COLORS):
    vals = bd_df.loc[cat]
    ax.bar(bd_df.columns, vals, bottom=bottom, label=cat, color=color)
    bottom += vals
ax.set_title('Kanpur PM2.5 — Share of Days by AQI Category', fontsize=13)
ax.set_ylabel('% of days')
ax.legend(bbox_to_anchor=(1.02,1), loc='upper left')
plt.tight_layout()
plt.savefig('charts/03_aqi_breakdown.png')
plt.close()
print("Saved 03_aqi_breakdown.png")

# CHART 4: Diurnal pattern
fig, ax = plt.subplots(figsize=(11,5))
for loc, color in zip(diurnal['location_name'].unique(), ['#e07b39','#3d7ea6']):
    sub = diurnal[diurnal['location_name']==loc].sort_values('hour')
    ax.plot(sub['hour'], sub['pm25'], marker='o', markersize=3, label=loc, color=color)
ax.set_title('Kanpur PM2.5 — Average by Hour of Day (Local Time, IST)', fontsize=13)
ax.set_xlabel('Hour (IST, 24-hr)')
ax.set_ylabel('PM2.5 (µg/m³)')
ax.set_xticks(range(0,24,2))
ax.legend()
plt.tight_layout()
plt.savefig('charts/04_diurnal.png')
plt.close()
print("Saved 04_diurnal.png")