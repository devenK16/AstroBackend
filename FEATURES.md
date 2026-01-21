# 📚 Jyotishganit Library Features Documentation

## Overview

The `jyotishganit` library is a comprehensive Python library for Vedic Astrology calculations with NASA JPL ephemeris precision. This document details ALL features discovered through comprehensive exploration.

---

## 🎯 Core Functions

### 1. `calculate_birth_chart()`

**Purpose:** Calculate complete Vedic birth chart with all components

**Signature:**
```python
calculate_birth_chart(
    birth_date: datetime,
    latitude: float,
    longitude: float,
    timezone_offset: float = 0.0,
    location_name: Optional[str] = None,
    name: Optional[str] = None
) -> VedicBirthChart
```

**Parameters:**
- `birth_date` (datetime): Birth date and time
- `latitude` (float): Birth location latitude in decimal degrees
- `longitude` (float): Birth location longitude in decimal degrees
- `timezone_offset` (float): UTC offset (e.g., 5.5 for IST, -5 for EST)
- `location_name` (str, optional): Name of birth location
- `name` (str, optional): Person's name

**Returns:** `VedicBirthChart` object

**Example:**
```python
from jyotishganit import calculate_birth_chart
from datetime import datetime

chart = calculate_birth_chart(
    birth_date=datetime(1990, 1, 15, 10, 30),
    latitude=28.6139,
    longitude=77.2090,
    timezone_offset=5.5,
    name="John Doe"
)
```

---

### 2. `get_birth_chart_json()`

**Purpose:** Get complete birth chart data as JSON string

**Signature:**
```python
get_birth_chart_json(
    birth_date: datetime,
    latitude: float,
    longitude: float,
    timezone_offset: float = 0.0,
    location_name: Optional[str] = None,
    name: Optional[str] = None
) -> str
```

**Parameters:** Same as `calculate_birth_chart()`

**Returns:** JSON string with complete birth chart data

**Example:**
```python
from jyotishganit import get_birth_chart_json
import json

json_string = get_birth_chart_json(
    birth_date=datetime(1990, 1, 15, 10, 30),
    latitude=28.6139,
    longitude=77.2090,
    timezone_offset=5.5,
    name="John Doe"
)

data = json.loads(json_string)
```

---

### 3. `Person` Class

**Purpose:** Represents a person with birth details

**Constructor:**
```python
Person(
    birth_datetime: datetime,
    latitude: float,
    longitude: float,
    timezone: Optional[str] = None,
    name: Optional[str] = None
)
```

**Note:** The `Person` class is used internally by the library. For most use cases, use `calculate_birth_chart()` or `get_birth_chart_json()` instead.

---

## 📊 VedicBirthChart Object

The `VedicBirthChart` object returned by `calculate_birth_chart()` contains the following attributes:

### Main Attributes

1. **person** - Person object with birth details
2. **d1_chart** - D1 (Rasi) birth chart
3. **divisional_charts** - All divisional charts (D1-D60)
4. **ayanamsa** - Ayanamsa calculation
5. **ashtakavarga** - Ashtakavarga calculations
6. **dashas** - Vimshottari Dasha periods

---

## 🏠 D1 Chart (Rasi Chart)

The D1 chart represents the main birth chart (Rasi chart).

**Attributes:**
- Planetary positions
- House placements
- Ascendant (Lagna)
- Aspects
- Sign placements

---

## 🔢 Divisional Charts (Vargas)

The library supports ALL 16 main divisional charts:

| Chart | Name | Purpose |
|-------|------|---------|
| D1 | Rasi | Main birth chart |
| D2 | Hora | Wealth |
| D3 | Drekkana | Siblings |
| D4 | Chaturthamsa | Property |
| D7 | Saptamsa | Children |
| D9 | Navamsa | Spouse/Dharma |
| D10 | Dasamsa | Career |
| D12 | Dwadasamsa | Parents |
| D16 | Shodasamsa | Vehicles |
| D20 | Vimsamsa | Spiritual progress |
| D24 | Chaturvimsamsa | Education |
| D27 | Nakshatramsa | Strengths/Weaknesses |
| D30 | Trimsamsa | Evils/Misfortunes |
| D40 | Khavedamsa | Auspicious/Inauspicious effects |
| D45 | Akshavedamsa | Character |
| D60 | Shashtiamsa | Past life/Karma |

**Access:** Via `chart.divisional_charts.d9`, `chart.divisional_charts.d10`, etc.

---

## 📅 Panchanga Elements

Panchanga (five limbs) calculations include:

1. **Tithi** - Lunar day (1-30)
2. **Nakshatra** - Lunar mansion (27 nakshatras)
3. **Yoga** - Combination of Sun and Moon (27 yogas)
4. **Karana** - Half of Tithi (11 karanas)
5. **Vaara** - Weekday (7 days)

**Note:** These are included in the JSON output from `get_birth_chart_json()`

---

## 💪 Ashtakavarga

Ashtakavarga is a system of planetary strength calculation.

**Features:**
- Individual planet ashtakavarga
- Sarvashtakavarga (combined)
- Bindus (points) for each house
- Strength analysis

**Access:** Via `chart.ashtakavarga`

---

## ⏰ Dashas (Vimshottari Dasha System)

The library calculates Vimshottari Dasha periods:

**Levels:**
- **Mahadasha** - Major period (planetary period)
- **Antardasha** - Sub-period within Mahadasha
- **Pratyantardasha** - Sub-sub-period

**Features:**
- Start and end dates for each period
- Current running dasha
- Complete dasha sequence for 120 years

**Access:** Via `chart.dashas`

---

## 🌟 Planetary Calculations

The library calculates positions for:

**Grahas (Planets):**
- Sun (Surya)
- Moon (Chandra)
- Mars (Mangal)
- Mercury (Budha)
- Jupiter (Guru)
- Venus (Shukra)
- Saturn (Shani)
- Rahu (North Node)
- Ketu (South Node)

**For each planet:**
- Longitude
- Sign (Rashi)
- Nakshatra
- Nakshatra Pada
- House placement
- Retrograde status
- Combustion status
- Aspects

---

## 🏛️ House System

**Features:**
- 12 houses (Bhavas)
- House cusps
- House lords
- Planets in houses
- House strengths

---

## 🎯 Ayanamsa

The library uses **Lahiri Ayanamsa** (most commonly used in Vedic Astrology).

**Precision:** Based on NASA JPL DE421 ephemeris data

---

## 📤 JSON Output Format

The `get_birth_chart_json()` function returns a comprehensive JSON object with:

```json
{
  "person": {
    "name": "...",
    "birth_datetime": "...",
    "latitude": ...,
    "longitude": ...,
    "timezone_offset": ...
  },
  "d1_chart": {
    "planets": [...],
    "houses": [...],
    "ascendant": {...}
  },
  "divisional_charts": {
    "d1": {...},
    "d9": {...},
    ...
  },
  "panchanga": {
    "tithi": "...",
    "nakshatra": "...",
    "yoga": "...",
    "karana": "...",
    "vaara": "..."
  },
  "dashas": {
    "current_mahadasha": {...},
    "current_antardasha": {...},
    "all_dashas": [...]
  },
  "ashtakavarga": {...}
}
```

---

## ⚙️ Technical Details

### Ephemeris Data

The library automatically downloads required ephemeris files on first use:
- **de421.bsp** - NASA JPL planetary ephemeris (~17MB)
- **hip_main.dat** - Hipparcos star catalog (~53MB)

These files are cached locally for future use.

### Accuracy

- **Planetary positions:** Accurate to arc-seconds
- **Time precision:** Accurate to minutes
- **Ayanamsa:** Lahiri (standard for Vedic Astrology)

### Performance

- **First calculation:** ~5-10 seconds (downloads ephemeris data)
- **Subsequent calculations:** <1 second

---

## 🚀 Usage Examples

### Example 1: Basic Birth Chart

```python
from jyotishganit import calculate_birth_chart
from datetime import datetime

chart = calculate_birth_chart(
    birth_date=datetime(1990, 1, 15, 10, 30),
    latitude=28.6139,
    longitude=77.2090,
    timezone_offset=5.5,
    name="Test Person"
)

print(f"Chart created for: {chart.person.name}")
print(f"Ascendant: {chart.d1_chart.ascendant}")
```

### Example 2: Get JSON Data

```python
from jyotishganit import get_birth_chart_json
import json

json_string = get_birth_chart_json(
    birth_date=datetime(1990, 1, 15, 10, 30),
    latitude=28.6139,
    longitude=77.2090,
    timezone_offset=5.5
)

data = json.loads(json_string)
print(json.dumps(data, indent=2))
```

### Example 3: Access Specific Data

```python
chart = calculate_birth_chart(...)

# Access D9 (Navamsa) chart
navamsa = chart.divisional_charts.d9

# Access Dashas
dashas = chart.dashas

# Access Ashtakavarga
ashtakavarga = chart.ashtakavarga
```

---

## 📝 Important Notes

1. **Timezone:** Must be numeric offset from UTC (e.g., 5.5 for IST, not "Asia/Kolkata")
2. **Coordinates:** Use decimal degrees (e.g., 28.6139, not 28°36'50")
3. **Date Format:** Use Python `datetime` objects
4. **First Run:** Will download ~70MB of ephemeris data

---

## 🔧 Common Use Cases

### For Astrology Websites/Apps

```python
# Get complete data as JSON for frontend
json_data = get_birth_chart_json(
    birth_date=user_datetime,
    latitude=user_lat,
    longitude=user_lon,
    timezone_offset=user_tz,
    name=user_name
)

# Send to frontend
return jsonify(json.loads(json_data))
```

### For Detailed Analysis

```python
# Get chart object for detailed analysis
chart = calculate_birth_chart(...)

# Access specific components
d1 = chart.d1_chart
d9 = chart.divisional_charts.d9
dashas = chart.dashas
ashtakavarga = chart.ashtakavarga
```

---

## 🎓 Learning Resources

The library follows traditional Vedic Astrology principles:
- **Parashara Hora Shastra** - Classical text
- **Brihat Jataka** - Classical text
- **BPHS** - Brihat Parashara Hora Shastra

---

## ✅ Feature Checklist

- [x] Birth chart calculation (D1)
- [x] All 16 divisional charts (D1-D60)
- [x] Panchanga calculations
- [x] Vimshottari Dasha system
- [x] Ashtakavarga
- [x] Planetary positions
- [x] House system
- [x] Aspects
- [x] JSON output
- [x] NASA JPL ephemeris precision

---

## 🆘 Troubleshooting

### Issue: "Ephemeris data download failed"
**Solution:** Check internet connection, library will auto-download on first use

### Issue: "Invalid timezone"
**Solution:** Use numeric offset (5.5) not timezone string ("Asia/Kolkata")

### Issue: "Slow first calculation"
**Solution:** Normal - downloading ephemeris data (~70MB), subsequent calls are fast

---

**Last Updated:** Based on jyotishganit v0.1.2

**For More Information:** Check the library's PyPI page or GitHub repository
