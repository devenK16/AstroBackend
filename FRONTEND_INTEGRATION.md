# 📖 Frontend Integration Guide

## Quick Start - Connecting Your Frontend to the Backend

### 1. Start the Backend Server

```bash
cd d:\astroTests
python api_server.py
```

The server will run on `http://localhost:5000`

---

## 2. API Endpoint Reference

### Health Check
```
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "Jyotishganit Astrology API",
  "version": "1.0.0"
}
```

---

### Get Complete Birth Chart
```
POST /api/birth-chart
```

**Request Body:**
```json
{
  "name": "John Doe",
  "date": "1990-01-15",
  "time": "10:30",
  "latitude": 28.6139,
  "longitude": 77.2090,
  "timezone": 5.5
}
```

**Field Descriptions:**
- `name` (string): Person's name
- `date` (string): Birth date in YYYY-MM-DD format
- `time` (string): Birth time in HH:MM format (24-hour)
- `latitude` (number): Birth location latitude in decimal degrees
- `longitude` (number): Birth location longitude in decimal degrees
- `timezone` (number): UTC offset (e.g., 5.5 for IST, -5 for EST)

**Response:**
```json
{
  "success": true,
  "chart_created": true,
  "input": { ... },
  // All available birth chart data
  // (varies based on library features)
}
```

---

### Get Panchanga Details
```
POST /api/panchanga
```

**Request Body:**
```json
{
  "date": "1990-01-15",
  "time": "10:30",
  "latitude": 28.6139,
  "longitude": 77.2090,
  "timezone": 5.5
}
```

**Response:**
```json
{
  "success": true,
  "tithi": "...",
  "nakshatra": "...",
  "yoga": "...",
  "karana": "...",
  "vaara": "..."
}
```

---

### Get Dasha Periods
```
POST /api/dasha
```

**Request Body:**
```json
{
  "name": "John Doe",
  "date": "1990-01-15",
  "time": "10:30",
  "latitude": 28.6139,
  "longitude": 77.2090,
  "timezone": 5.5
}
```

**Response:**
```json
{
  "success": true,
  "dasha": "...",
  "vimshottari_dasha": "...",
  "mahadasha": "..."
}
```

---

## 3. JavaScript/Frontend Integration Examples

### Using Fetch API (Vanilla JavaScript)

```javascript
async function getBirthChart(formData) {
  try {
    const response = await fetch('http://localhost:5000/api/birth-chart', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name: formData.name,
        date: formData.date,        // "1990-01-15"
        time: formData.time,        // "10:30"
        latitude: parseFloat(formData.latitude),
        longitude: parseFloat(formData.longitude),
        timezone: parseFloat(formData.timezone)
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    
    if (data.success) {
      console.log('Birth Chart Data:', data);
      displayBirthChart(data);
    } else {
      console.error('Error:', data.error);
      showError(data.error);
    }
  } catch (error) {
    console.error('Network error:', error);
    showError('Failed to connect to server');
  }
}

function displayBirthChart(data) {
  // Update your UI with the birth chart data
  document.getElementById('result').innerHTML = `
    <h2>Birth Chart for ${data.input.name}</h2>
    <pre>${JSON.stringify(data, null, 2)}</pre>
  `;
}

function showError(message) {
  document.getElementById('error').textContent = message;
}
```

### Using Axios (React/Vue/Angular)

```javascript
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

export const getBirthChart = async (birthData) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/birth-chart`, {
      name: birthData.name,
      date: birthData.date,
      time: birthData.time,
      latitude: parseFloat(birthData.latitude),
      longitude: parseFloat(birthData.longitude),
      timezone: parseFloat(birthData.timezone)
    });
    
    return response.data;
  } catch (error) {
    console.error('Error fetching birth chart:', error);
    throw error;
  }
};

export const getPanchanga = async (dateData) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/panchanga`, dateData);
    return response.data;
  } catch (error) {
    console.error('Error fetching panchanga:', error);
    throw error;
  }
};

export const getDasha = async (birthData) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/dasha`, birthData);
    return response.data;
  } catch (error) {
    console.error('Error fetching dasha:', error);
    throw error;
  }
};
```

### React Component Example

```jsx
import React, { useState } from 'react';
import { getBirthChart } from './api';

function BirthChartForm() {
  const [formData, setFormData] = useState({
    name: '',
    date: '',
    time: '',
    latitude: '',
    longitude: '',
    timezone: '5.5'
  });
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const data = await getBirthChart(formData);
      setChartData(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="name"
          placeholder="Name"
          value={formData.name}
          onChange={handleChange}
          required
        />
        <input
          type="date"
          name="date"
          value={formData.date}
          onChange={handleChange}
          required
        />
        <input
          type="time"
          name="time"
          value={formData.time}
          onChange={handleChange}
          required
        />
        <input
          type="number"
          step="any"
          name="latitude"
          placeholder="Latitude"
          value={formData.latitude}
          onChange={handleChange}
          required
        />
        <input
          type="number"
          step="any"
          name="longitude"
          placeholder="Longitude"
          value={formData.longitude}
          onChange={handleChange}
          required
        />
        <input
          type="number"
          step="any"
          name="timezone"
          placeholder="Timezone (UTC offset)"
          value={formData.timezone}
          onChange={handleChange}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Calculating...' : 'Get Birth Chart'}
        </button>
      </form>

      {error && <div className="error">{error}</div>}
      
      {chartData && (
        <div className="chart-result">
          <h2>Birth Chart for {chartData.input.name}</h2>
          <pre>{JSON.stringify(chartData, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default BirthChartForm;
```

---

## 4. Getting Location Coordinates

### Option 1: User Input
Let users manually enter latitude/longitude

### Option 2: Geocoding API
Convert city names to coordinates:

```javascript
async function getCoordinates(cityName) {
  // Using OpenStreetMap Nominatim (free, no API key needed)
  const response = await fetch(
    `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(cityName)}&format=json&limit=1`
  );
  const data = await response.json();
  
  if (data.length > 0) {
    return {
      latitude: parseFloat(data[0].lat),
      longitude: parseFloat(data[0].lon)
    };
  }
  throw new Error('Location not found');
}
```

### Option 3: Google Places API
More accurate but requires API key

---

## 5. Date/Time Format Conversion

### Converting from HTML Date/Time Inputs

```javascript
function formatDateTime(dateInput, timeInput) {
  // dateInput: "1990-01-15" (from <input type="date">)
  // timeInput: "10:30" (from <input type="time">)
  
  return {
    date: dateInput,  // Already in correct format
    time: timeInput   // Already in correct format
  };
}
```

### Converting from JavaScript Date Object

```javascript
function formatDateTimeFromDate(dateObj) {
  const year = dateObj.getFullYear();
  const month = String(dateObj.getMonth() + 1).padStart(2, '0');
  const day = String(dateObj.getDate()).padStart(2, '0');
  const hours = String(dateObj.getHours()).padStart(2, '0');
  const minutes = String(dateObj.getMinutes()).padStart(2, '0');
  
  return {
    date: `${year}-${month}-${day}`,
    time: `${hours}:${minutes}`
  };
}
```

---

## 6. Error Handling

```javascript
async function getBirthChartWithErrorHandling(formData) {
  try {
    const response = await fetch('http://localhost:5000/api/birth-chart', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData)
    });

    const data = await response.json();

    if (!response.ok) {
      // Server returned an error
      throw new Error(data.error || 'Server error');
    }

    if (!data.success) {
      // API returned success: false
      throw new Error(data.error || 'Calculation failed');
    }

    return data;

  } catch (error) {
    if (error.message.includes('fetch')) {
      // Network error
      throw new Error('Cannot connect to server. Make sure the API is running.');
    }
    throw error;
  }
}
```

---

## 7. CORS Issues

If you encounter CORS errors:

1. **Make sure the API server is running** with CORS enabled (it already is in `api_server.py`)

2. **Check your frontend URL** - If your frontend is on a different port, that's fine

3. **For production**, update the CORS settings in `api_server.py`:
```python
CORS(app, origins=['https://yourdomain.com'])
```

---

## 8. Production Deployment

### For Production Use:

1. **Change debug mode** in `api_server.py`:
```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

2. **Use a production server** like Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 api_server:app
```

3. **Update frontend API URL**:
```javascript
const API_BASE_URL = 'https://your-api-domain.com/api';
```

---

## 9. Testing Checklist

- [ ] API server starts without errors
- [ ] Health check endpoint responds
- [ ] Birth chart endpoint accepts valid data
- [ ] Error messages are clear for invalid data
- [ ] Frontend can connect to API
- [ ] CORS is working (no browser errors)
- [ ] Loading states work in frontend
- [ ] Error states display properly
- [ ] Results display correctly

---

## 10. Common Issues & Solutions

### Issue: "Failed to fetch"
**Solution:** Make sure API server is running on port 5000

### Issue: "CORS policy error"
**Solution:** Verify `flask-cors` is installed and imported

### Issue: "Invalid date/time format"
**Solution:** Use YYYY-MM-DD for date and HH:MM for time

### Issue: "Missing required field"
**Solution:** Check all required fields are included in request

### Issue: "Connection refused"
**Solution:** Check firewall settings, ensure port 5000 is open

---

**You're all set! 🚀** Your frontend can now get complete astrological calculations from the backend.
