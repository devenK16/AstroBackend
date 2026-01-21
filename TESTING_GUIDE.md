# 🔮 Jyotishganit Library - Step-by-Step Testing Guide

This guide will walk you through testing EVERYTHING the jyotishganit library has to offer.

---

## 📋 Prerequisites

Before you start, make sure you have:
- Python 3.7 or higher installed
- pip (Python package manager)
- A terminal/command prompt

---

## 🚀 STEP 1: Set Up Python Environment

### Option A: Using Virtual Environment (Recommended)

```bash
# Navigate to the project directory
cd d:\astroTests

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### Option B: Use System Python (Not Recommended)

Skip the virtual environment and use your system Python directly.

---

## 📦 STEP 2: Install Dependencies

```bash
# Make sure you're in d:\astroTests directory
pip install -r requirements.txt
```

**What this installs:**
- `jyotishganit` - The main astrology library
- `flask` - Web framework for the API
- `flask-cors` - Enable cross-origin requests
- `python-dateutil` - Date parsing utilities

**Expected output:** You should see successful installation messages for all packages.

---

## 🔍 STEP 3: Explore ALL Library Features

Run the comprehensive exploration script:

```bash
python explore_jyotishganit.py
```

### What This Script Tests:

1. **Basic Birth Chart Creation**
   - Creates a birth chart with sample data
   - Shows all available attributes

2. **Planetary Positions**
   - Tests methods to get planet positions
   - Tries to access individual planets (Sun, Moon, Mars, etc.)

3. **Divisional Charts (D1-D60)**
   - Tests all divisional chart calculations
   - Includes D1 (Rasi), D9 (Navamsa), D10 (Dasamsa), etc.

4. **Panchanga Calculations**
   - Tithi (Lunar day)
   - Nakshatra (Lunar mansion)
   - Yoga
   - Karana
   - Vaara (Weekday)

5. **Shadbala (Planetary Strength)**
   - Tests planetary strength calculations

6. **Vimshottari Dasha System**
   - Tests Mahadasha, Antardasha periods

7. **JSON Output**
   - Tests JSON/dictionary export capabilities

8. **Complete Method Listing**
   - Lists EVERY method and attribute available
   - Attempts to call each one
   - Shows what each returns

### Expected Output:

You'll see detailed sections for each feature with:
- ✓ Success indicators for found methods
- Actual output from each calculation
- Error messages if a feature isn't available
- Complete list of all methods at the end

### 📝 What to Look For:

- **Green checkmarks (✓)** = Feature found and working
- **Red X (✗)** = Feature not available or error
- **Method names** = These are what you can call in your code
- **Result types** = Shows what data format is returned

---

## 🧪 STEP 4: Test with Your Own Birth Data

Edit `explore_jyotishganit.py` and modify these lines (around line 20):

```python
name = "Your Name"
date_of_birth = datetime(1990, 1, 15, 10, 30)  # Year, Month, Day, Hour, Minute
latitude = 28.6139   # Your birth location latitude
longitude = 77.2090  # Your birth location longitude
timezone = 5.5       # Your timezone offset from UTC
```

**How to find your coordinates:**
1. Go to [Google Maps](https://www.google.com/maps)
2. Right-click your birth location
3. Click the coordinates to copy them

**Timezone examples:**
- IST (India): 5.5
- EST (US East): -5
- PST (US West): -8
- GMT (UK): 0

Then run again:
```bash
python explore_jyotishganit.py
```

---

## 🌐 STEP 5: Start the API Server

```bash
python api_server.py
```

**Expected output:**
```
============================================================
  JYOTISHGANIT ASTROLOGY API SERVER
============================================================

Server starting on http://localhost:5000

Available endpoints:
  GET  /api/health       - Health check
  POST /api/birth-chart  - Get complete birth chart
  POST /api/panchanga    - Get Panchanga details
  POST /api/dasha        - Get Dasha periods

Press Ctrl+C to stop the server
============================================================
```

**Keep this terminal window open!** The server needs to run for the next steps.

---

## 🧪 STEP 6: Test API Endpoints

Open a **NEW terminal window** (keep the server running in the first one).

### Test 1: Health Check

```bash
curl http://localhost:5000/api/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "service": "Jyotishganit Astrology API",
  "version": "1.0.0"
}
```

### Test 2: Get Birth Chart

```bash
curl -X POST http://localhost:5000/api/birth-chart ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"Test Person\",\"date\":\"1990-01-15\",\"time\":\"10:30\",\"latitude\":28.6139,\"longitude\":77.2090,\"timezone\":5.5}"
```

**Note:** On Mac/Linux, replace `^` with `\` for line continuation.

**Expected response:** A large JSON object with all birth chart data.

### Test 3: Get Panchanga

```bash
curl -X POST http://localhost:5000/api/panchanga ^
  -H "Content-Type: application/json" ^
  -d "{\"date\":\"1990-01-15\",\"time\":\"10:30\",\"latitude\":28.6139,\"longitude\":77.2090,\"timezone\":5.5}"
```

### Test 4: Get Dasha Periods

```bash
curl -X POST http://localhost:5000/api/dasha ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"Test Person\",\"date\":\"1990-01-15\",\"time\":\"10:30\",\"latitude\":28.6139,\"longitude\":77.2090,\"timezone\":5.5}"
```

---

## 🎨 STEP 7: Test with Your Frontend

### Update Your Frontend Code

Your frontend should make POST requests to `http://localhost:5000/api/birth-chart` with this JSON format:

```javascript
const birthData = {
  name: "John Doe",
  date: "1990-01-15",      // YYYY-MM-DD format
  time: "10:30",           // HH:MM format (24-hour)
  latitude: 28.6139,       // Decimal degrees
  longitude: 77.2090,      // Decimal degrees
  timezone: 5.5            // UTC offset
};

fetch('http://localhost:5000/api/birth-chart', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(birthData)
})
.then(response => response.json())
.then(data => {
  console.log('Birth Chart Data:', data);
  // Use the data in your frontend
})
.catch(error => {
  console.error('Error:', error);
});
```

---

## 📊 STEP 8: Use Postman (Optional but Recommended)

If you have Postman installed:

1. **Create a new POST request**
2. **URL:** `http://localhost:5000/api/birth-chart`
3. **Headers:** 
   - Key: `Content-Type`
   - Value: `application/json`
4. **Body (raw JSON):**
```json
{
  "name": "Test Person",
  "date": "1990-01-15",
  "time": "10:30",
  "latitude": 28.6139,
  "longitude": 77.2090,
  "timezone": 5.5
}
```
5. **Click Send**

You'll get a nicely formatted JSON response!

---

## 🐛 Troubleshooting

### Error: "Module not found: jyotishganit"
**Solution:** Run `pip install jyotishganit`

### Error: "Port 5000 already in use"
**Solution:** Change the port in `api_server.py` (last line):
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Changed to 5001
```

### Error: "CORS error" in browser
**Solution:** Make sure `flask-cors` is installed and the server is running

### Error: "Invalid date/time format"
**Solution:** Use exactly this format:
- Date: `YYYY-MM-DD` (e.g., "1990-01-15")
- Time: `HH:MM` (e.g., "10:30")

---

## 📚 What to Check in the Output

After running the exploration script, look for:

1. **Available Methods** - These are functions you can call
2. **Return Types** - What kind of data each method gives you
3. **Error Messages** - Features that might not be implemented
4. **JSON Structure** - How to parse the data in your frontend

---

## ✅ Success Checklist

- [ ] Virtual environment created and activated
- [ ] All dependencies installed successfully
- [ ] Exploration script runs without errors
- [ ] Can see list of all available methods
- [ ] API server starts successfully
- [ ] Health check endpoint works
- [ ] Birth chart endpoint returns data
- [ ] Can test with your own birth data
- [ ] Frontend can connect to the API

---

## 🎯 Next Steps

1. **Review the output** from `explore_jyotishganit.py`
2. **Check FEATURES.md** for detailed documentation of what was found
3. **Integrate with your frontend** using the API endpoints
4. **Customize the API** to return only the data you need
5. **Add error handling** in your frontend for invalid inputs

---

## 💡 Tips

- **Keep the exploration output** - It's your reference for available features
- **Test with multiple birth charts** - Verify accuracy
- **Check the server logs** - They show all requests and errors
- **Use the browser console** - To debug frontend integration
- **Start simple** - Get basic birth chart working first, then add more features

---

## 🆘 Need Help?

If you encounter issues:
1. Check the error messages carefully
2. Verify your Python version: `python --version`
3. Verify pip installation: `pip --version`
4. Check if the library installed: `pip show jyotishganit`
5. Look at the server logs for API errors

---

**Happy Testing! 🚀✨**
