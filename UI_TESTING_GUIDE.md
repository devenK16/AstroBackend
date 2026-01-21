# 🧪 UI Testing Guide for Deven's Dashboard

## 1. Start the Backend Server
The dashboard needs the Python API to be running to fetch calculations.

1. Open a terminal/command prompt.
2. Navigate to your folder:
   ```bash
   cd d:\astroTests
   ```
3. Activate the virtual environment (if not active):
   ```bash
   .\venv\Scripts\activate
   ```
4. Start the server:
   ```bash
   python api_server.py
   ```
   *You should see "Server starting on http://localhost:5000"*

## 2. Open the Dashboard
Since the HTML file is just a static file, you can open it directly in your browser.

1. Navigate to `d:\astroTests` in your File Explorer.
2. Double-click `astrology_dashboard.html`.
3. The page should open with a dark, premium theme.

## 3. Verify Deven's Data
1. Check the inputs. They should be pre-filled with:
   - **Name**: Deven
   - **Date**: 16/02/2002
   - **Time**: 10:20
   - **Lat/Lon**: 21.1458 / 79.0882 (Nagpur)
   - **Timezone**: 5.5

## 4. Generate & Explore
1. Click the **"Generate Chart"** button.
2. **Status**: You should see "Calculating..." then the results appear below.
3. **Check Results**:
   - **Panchanga**: Look for Tithi, Yoga, etc.
   - **Planetary Positions**: Check if the table is populated.
   - **Divisional Charts**: Click tabs (D1, D9) to see raw data for those charts.
   - **Raw Data**: Use the "Raw Data" section at the bottom to see exactly what the library returned!

## Troubleshooting
- **"Error: Failed to fetch"**: Ensure the black terminal window running `api_server.py` is still open and running.
- **Nothing happens**: Open Browser Developer Tools (F12) -> Console to see errors.
