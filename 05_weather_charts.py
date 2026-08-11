import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 150

combined = pd.read_csv("data/weather_merged_combined.csv")
STATIONS = {229252: "NSI Kalyanpur", 5662: "Nehru Nagar"}

fig, axes = plt.subplots(1, 2, figsize=(14,5.5))
for ax, (location_id, name) in zip(axes, STATIONS.items()):
    sub = combined[combined['location_id']==location_id]
    corr = sub[['pm25','pm10','temperature','relativehumidity','wind_speed']].corr()
    corr.columns = ['PM2.5','PM10','Temp','Humidity','Wind Speed']
    corr.index = ['PM2.5','PM10','Temp','Humidity','Wind Speed']
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='RdBu_r', center=0, vmin=-1, vmax=1,
                ax=ax, cbar=ax==axes[-1], square=True, linewidths=0.5)
    ax.set_title(name, fontsize=12)
plt.suptitle('Correlation Between PM2.5/PM10 and Weather Variables', fontsize=13, y=1.02)
plt.tight_layout()
plt.savefig('charts/05_correlation_heatmap.png', bbox_inches='tight')
plt.close()
print("Saved 05_correlation_heatmap.png")

fig, axes = plt.subplots(1, 2, figsize=(13,5))
colors = {229252: '#e07b39', 5662: '#3d7ea6'}

for location_id, name in STATIONS.items():
    sub = combined[combined['location_id']==location_id].dropna(subset=['pm25','wind_speed'])
    axes[0].scatter(sub['wind_speed'], sub['pm25'], s=4, alpha=0.25, color=colors[location_id], label=name)
    r, p = stats.pearsonr(sub['wind_speed'], sub['pm25'])
    axes[0].annotate(f"{name}: r={r:.2f}", xy=(0.98,0.95-0.07*(list(STATIONS).index(location_id))),
                      xycoords='axes fraction', ha='right', fontsize=9, color=colors[location_id])

for location_id, name in STATIONS.items():
    sub = combined[combined['location_id']==location_id].dropna(subset=['pm25','temperature'])
    axes[1].scatter(sub['temperature'], sub['pm25'], s=4, alpha=0.25, color=colors[location_id], label=name)
    r, p = stats.pearsonr(sub['temperature'], sub['pm25'])
    axes[1].annotate(f"{name}: r={r:.2f}", xy=(0.98,0.95-0.07*(list(STATIONS).index(location_id))),
                      xycoords='axes fraction', ha='right', fontsize=9, color=colors[location_id])

axes[0].set_xlabel('Wind Speed (m/s)')
axes[0].set_ylabel('PM2.5 (µg/m³)')
axes[0].set_title('PM2.5 vs. Wind Speed')
axes[0].legend(fontsize=8, loc='upper left')

axes[1].set_xlabel('Temperature (°C)')
axes[1].set_ylabel('PM2.5 (µg/m³)')
axes[1].set_title('PM2.5 vs. Temperature')
axes[1].legend(fontsize=8, loc='upper left')

plt.tight_layout()
plt.savefig('charts/06_scatter_weather.png')
plt.close()
print("Saved 06_scatter_weather.png")

fig, axes = plt.subplots(1, 2, figsize=(13,6), subplot_kw={'projection':'polar'})
DIR_BINS = np.arange(0, 361, 22.5)
DIR_LABELS = ['N','NNE','NE','ENE','E','ESE','SE','SSE','S','SSW','SW','WSW','W','WNW','NW','NNW']

for ax, (location_id, name) in zip(axes, STATIONS.items()):
    sub = combined[combined['location_id']==location_id].dropna(subset=['pm25','wind_direction'])
    sub = sub.copy()
    sub['dir_bin'] = pd.cut(sub['wind_direction'], bins=DIR_BINS, labels=DIR_LABELS[:len(DIR_BINS)-1], include_lowest=True)
    avg_by_dir = sub.groupby('dir_bin', observed=True)['pm25'].mean().reindex(DIR_LABELS)

    angles = np.linspace(0, 2*np.pi, len(DIR_LABELS), endpoint=False)
    values = avg_by_dir.values
    values = np.nan_to_num(values, nan=0)

    ax.bar(angles, values, width=2*np.pi/len(DIR_LABELS)*0.9, color='#c0392b', alpha=0.75)
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_xticks(angles)
    ax.set_xticklabels(DIR_LABELS, fontsize=8)
    ax.set_title(f'{name}\nAvg PM2.5 (µg/m³) by Wind Direction', fontsize=11, pad=20)

plt.tight_layout()
plt.savefig('charts/07_wind_rose.png')
plt.close()
print("Saved 07_wind_rose.png")
