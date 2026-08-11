# Kanpur Air Quality Analysis
### PM2.5 & PM10 Trends at Two CPCB/UPPCB Monitoring Stations (2021–2026)

**Author:** Avnish Singh
**Data source:** OpenAQ API (originating from CPCB/UPPCB continuous ambient air quality monitoring stations)
**Stations analyzed:** NSI Kalyanpur (Station ID 229252), Nehru Nagar (Station ID 5662), Kanpur, Uttar Pradesh

---

## 1. Objective

Kanpur is consistently ranked among India's most polluted cities in CPCB and WHO air quality assessments. This project analyzes real, station-level PM2.5 and PM10 monitoring data from two locations in Kanpur to identify seasonal pollution patterns, quantify how many days fall into unhealthy Air Quality Index (AQI) categories, compare pollution levels between a more industrial zone (Kalyanpur) and a more residential/commercial zone (Nehru Nagar), and examine how pollution varies across the hours of a single day.

## 2. Data Source & Methodology

Data was pulled directly from the OpenAQ v3 API, which aggregates measurements from CPCB and state pollution control board (UPPCB) monitoring stations. Both stations report hourly PM2.5 and PM10 concentrations (µg/m³).

**Data collection process:** Initial exports via OpenAQ's web interface were capped at 2,000 rows per pollutant. A custom Python script (using the `requests` library) was built to query the API directly with pagination, and was extended to pull from all historical sensor IDs associated with each station (station hardware is periodically replaced, and each physical sensor generation is assigned a separate ID in OpenAQ's system).

**Data coverage — important limitation, stated upfront:** Both stations show a genuine data gap from roughly **November 2022 to February 2025** (a ~2.3 year gap), which reflects an actual absence of reported readings during that period — not a limitation of the collection method. The usable data therefore falls into two windows:
- **Window 1: July 2021 – October 2022** (~15 months)
- **Window 2: February 2025 – August 2026** (~18 months, includes the most recent available data)

All seasonal analysis below combines both windows by calendar month (e.g., all "November" days from both windows are pooled together) to build a fuller seasonal picture, since neither window alone spans a complete, unbroken year for both stations.

**Cleaning steps applied:**
- Removed duplicate timestamps
- Removed negative-value readings (sensor errors — physically impossible for concentration data)
- Removed extreme outliers above 1,000 µg/m³ (a small number of readings, almost certainly sensor faults)
- Aggregated sub-hourly readings into daily averages, since CPCB's AQI categories are officially defined on 24-hour average concentrations
- AQI categories assigned using CPCB's standard PM2.5 breakpoints (Good ≤30, Satisfactory ≤60, Moderate ≤90, Poor ≤120, Very Poor ≤250, Severe >250 µg/m³)

**Note on Nehru Nagar PM2.5 in Window 1:** the PM2.5 sensor at Nehru Nagar has no data during Window 1 (Jul 2021–Oct 2022) — only PM10 was reported for that period. This is a genuine sensor availability gap, not an error in processing.

## 3. Findings

### 3.1 Seasonal Pattern

![Monthly seasonal average](charts/02_monthly_seasonal.png)

Both stations show a sharp, consistent seasonal cycle. PM2.5 peaks in **November** (94.8 µg/m³ at Kalyanpur, 84.9 µg/m³ at Nehru Nagar) — more than five times the **monsoon-season low in August** (16.1 µg/m³ at Kalyanpur, 22.6 µg/m³ at Nehru Nagar). This pattern is consistent with the well-documented North Indian winter pollution cycle: temperature inversion traps pollutants closer to the ground, crop-residue burning in neighboring states peaks in October–November, and Diwali-linked firecracker activity typically falls in this window, while monsoon rainfall (July–September) scrubs particulates from the air and improves dispersal.

### 3.2 Daily Time Series

![Daily PM2.5 time series](charts/01_timeseries.png)

The full daily record makes the November spike and the 2022–2025 data gap directly visible. Both monitoring windows independently reproduce the same winter-high, monsoon-low pattern, which strengthens confidence that this is a real recurring seasonal cycle rather than an artifact of one particular year's weather.

### 3.3 AQI Category Breakdown

![AQI category breakdown](charts/03_aqi_breakdown.png)

| Station | Good | Satisfactory | Moderate | Poor | Very Poor | Severe |
|---|---|---|---|---|---|---|
| NSI Kalyanpur | 42.4% | 35.9% | 15.6% | 4.2% | 1.8% | 0.0% |
| Nehru Nagar | 30.7% | 43.6% | 19.2% | 4.4% | 2.1% | 0.0% |

Kalyanpur recorded a higher share of "Good" days (42.4% vs. 30.7%), while Nehru Nagar spent more days in the "Satisfactory" and "Moderate" bands. Both stations logged **Poor or Very Poor** air quality on roughly **6% of monitored days** — meaningful given PM2.5 exposure risk compounds with repeated exposure, even at levels below the "Severe" threshold.

### 3.4 Station Comparison

| Station | Window | Mean PM2.5 (µg/m³) | Mean PM10 (µg/m³) |
|---|---|---|---|
| NSI Kalyanpur | Window 1 (2021–22) | 51.6 | 107.3 |
| NSI Kalyanpur | Window 2 (2025–26) | 36.7 | 88.2 |
| Nehru Nagar | Window 1 (2021–22) | — (no PM2.5 data) | 132.7 |
| Nehru Nagar | Window 2 (2025–26) | 47.0 | 68.9 |

Interestingly, **PM2.5 at Kalyanpur dropped from 51.6 to 36.7 µg/m³** between the two windows — a meaningful improvement worth flagging, though it's not possible from this data alone to say whether that reflects real air quality improvement, a change in the station's surroundings, or a sensor recalibration between hardware generations. This is a genuine open question the data raises rather than answers — worth stating honestly rather than overclaiming a trend.

### 3.5 Diurnal (Hour-of-Day) Pattern

![Diurnal pattern](charts/04_diurnal.png)

PM2.5 shows a clear daily rhythm at both stations: concentrations are lowest in the **mid-afternoon (around 3–4 PM IST)**, when daytime heating deepens the atmospheric mixing layer and disperses pollutants, and rise sharply through the evening to peak around **9–10 PM IST** — consistent with evening traffic volume combined with the atmosphere's boundary layer collapsing after sunset, which traps emissions closer to the ground. A smaller secondary bump appears around the morning rush hour (7–8 AM).

### 3.6 Weather Correlation Analysis

**Coverage note:** temperature, humidity, and wind data are only available for Window 2 (Feb 2025 – Aug 2026) — these sensors were not part of either station's instrumentation during Window 1. All correlation findings below reflect this ~18-month period only.

![Correlation heatmap](charts/05_correlation_heatmap.png)

Pearson correlation coefficients between PM2.5 and each weather variable, computed on hourly data:

| Variable | NSI Kalyanpur (r) | Nehru Nagar (r) |
|---|---|---|
| Temperature | -0.39 | -0.27 |
| Relative Humidity | +0.08 | -0.05 |
| Wind Speed | -0.28 | -0.36 |
| PM10 (cross-check) | +0.81 | +0.93 |

Both **temperature** and **wind speed** show a consistent, moderate negative correlation with PM2.5 at both stations — meaning as either increases, pollution tends to decrease. This quantitatively confirms the seasonal and diurnal mechanisms described above: warmer conditions deepen the atmospheric mixing layer, and stronger wind physically disperses particulates, both diluting concentrations. **Humidity shows a weak, inconsistent relationship** with PM2.5 directly (+0.08 at Kalyanpur, -0.05 at Nehru Nagar) — despite humidity correlating strongly with temperature itself (-0.60, -0.54), it does not appear to be an independent driver of PM2.5 in this data; its apparent effect, if any, is likely a downstream reflection of temperature rather than a separate mechanism.

![Scatter plots](charts/06_scatter_weather.png)

The scatter plots make an additional pattern visible that the correlation coefficient alone doesn't fully capture: the most extreme PM2.5 spikes (values above 400 µg/m³) occur almost exclusively at **very low wind speeds** (under ~1 m/s). This is consistent with calm-wind pollution accumulation events — still air allows particulates to build up locally with no dispersal, rather than any single spike being explainable by one dominant weather variable alone.

### 3.7 Wind Direction Analysis

![Wind rose](charts/07_wind_rose.png)

Average PM2.5 concentration was calculated for each 22.5° wind direction bin, at both stations independently. The result is a genuinely striking, non-obvious finding: **both stations show their highest average PM2.5 when wind blows from the North / North-Northeast** — Kalyanpur averages 97.4 µg/m³ under northerly wind (more than double its overall average), and Nehru Nagar averages 85.9 µg/m³ under the same condition.

Two honest, competing explanations for this, neither of which can be fully separated with this dataset alone:
1. **A real upwind source or source region** to the north of both stations, driving elevated PM2.5 whenever wind carries air from that direction across the city.
2. **A seasonal confound** — northerly/northwesterly winds in North India are more common during winter months (the same season already shown to have the highest PM2.5), so this finding may partly restate the seasonal pattern already established in Section 3.1, rather than revealing an independent spatial source.

Distinguishing between these would require either wind-direction data cross-tabulated by season specifically, or knowledge of what industrial or dense-traffic zones lie north of these two monitoring locations — a natural next step for extending this project.

## 4. Interpretation

The findings point to three distinct, actionable pollution drivers in Kanpur: a **seasonal driver** (temperature inversion, agricultural burning, and reduced monsoon dispersal, concentrated Oct–Jan), a **daily driver** (traffic and nighttime boundary-layer collapse, concentrated evening hours), and a **meteorological driver quantitatively confirmed by this analysis** — wind speed and temperature both measurably suppress PM2.5, while calm-wind conditions are disproportionately linked to the most extreme pollution spikes. The wind-direction finding adds a potential fourth, spatial dimension worth further investigation: pollution consistently arrives from the north at both monitoring sites, which — if confirmed as a real source rather than a seasonal artifact — would point toward a specific upwind area for future monitoring or source investigation.

Practically, this means outdoor exposure risk in Kanpur is not constant — it is meaningfully higher on winter evenings, on calm-wind days, and (potentially) when wind blows from the north, than on monsoon afternoons with steady wind. This has direct relevance for public health advisories, school outdoor-activity timing, and traffic/source policy discussions of the kind NMCG- and CPCB-adjacent bodies engage in.

## 5. Limitations

- **Data gap (Nov 2022 – Feb 2025):** no readings exist for either station in this window; findings combine two separate periods by calendar month rather than analyzing one continuous year.
- **Nehru Nagar PM2.5, Window 1:** entirely missing; only PM10 is available for that station in that period.
- **Two-station sample:** Kanpur has more CPCB/UPPCB monitoring locations than the two analyzed here; findings reflect these two sites specifically; and may not generalize to areas of the city without a nearby monitor.
- **AQI classification uses PM2.5 only:** India's official composite AQI takes the worst sub-index across all measured pollutants (PM2.5, PM10, NO2, SO2, CO, O3); this analysis classifies using PM2.5 alone, since it is the pollutant most consistently linked to health outcomes and was available across both stations, but the true composite AQI on some days may be worse than the PM2.5-only figure suggests.
- **Outlier removal:** readings above 1,000 µg/m³ were excluded as likely sensor faults; a small number of genuine extreme pollution events, if any occurred, could theoretically have been filtered out along with sensor errors.

## 6. Summary

Using real CPCB/UPPCB monitoring data pulled via the OpenAQ API, this analysis confirms a strong, recurring seasonal PM2.5 cycle in Kanpur (November peak roughly 5x the August low), identifies a clear evening pollution spike tied to traffic and atmospheric conditions, and finds both monitored stations spend roughly 6% of days in "Poor" or worse AQI territory. Weather correlation analysis quantitatively confirms that wind speed and temperature both measurably suppress PM2.5 (r = -0.28 to -0.39), while the most extreme pollution spikes cluster under calm-wind conditions. Wind-direction analysis reveals a consistent, independently-replicated pattern at both stations: PM2.5 is highest when wind blows from the north, a finding that opens a genuine follow-up question about upwind source location versus seasonal confounding. The analysis also surfaces an open question around a possible year-over-year improvement in PM2.5 at one station that would need further data to confirm.

## 7. Suggested Next Steps

- Cross-tabulate wind direction by season to separate the northerly-wind finding from the seasonal pattern.
- Identify what lies north of both monitoring stations (industrial zones, major roads) to test the upwind-source hypothesis directly.
- Extend to a third or fourth Kanpur CPCB/UPPCB station to test whether these patterns hold city-wide.
- Investigate the cause of the Kalyanpur PM2.5 decline between the two windows (hardware recalibration vs. genuine improvement).

---
*Data and analysis: Python (pandas, matplotlib). Full cleaned datasets and analysis scripts available alongside this report.*
