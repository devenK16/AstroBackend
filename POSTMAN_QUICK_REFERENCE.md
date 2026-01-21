# 🚀 Postman Quick Reference - Deven's Test

## ⚡ Quick Setup (Copy & Paste Ready)

### 1. Server URL
```
http://localhost:5000/api/birth-chart
```

### 2. Request Method
```
POST
```

### 3. Headers
```
Content-Type: application/json
```

### 4. Request Body (Copy this exactly)
```json
{
  "name": "Deven",
  "date": "2002-02-16",
  "time": "10:20",
  "latitude": 21.1458,
  "longitude": 79.0882,
  "timezone": 5.5
}
```

---

## 📝 Step-by-Step (30 seconds)

1. **Start Server:**
   ```bash
   cd d:\astroTests
   python api_server.py
   ```

2. **Open Postman:**
   - Click **New** → **HTTP Request**

3. **Set Method & URL:**
   - Method: **POST**
   - URL: `http://localhost:5000/api/birth-chart`

4. **Add Header:**
   - Go to **Headers** tab
   - Add: `Content-Type` = `application/json`

5. **Add Body:**
   - Go to **Body** tab
   - Select **raw** → **JSON**
   - Paste the JSON above

6. **Send:**
   - Click **Send** button

7. **Check Response:**
   - Status: **200 OK** ✅
   - Should see `"success": true`
   - Should see `compatibility` and `sections`

---

## ✅ Expected Response Structure

```json
{
  "success": true,
  "basic_details": {...},
  "compatibility": {
    "varna": "...",
    "vashya": "...",
    "yoni": "...",
    "gan": "...",
    "nadi": "...",
    "tatva": "...",
    "paya": "...",
    "sign": "...",
    "nakshatra": "..."
  },
  "sections": {
    "career": {...},
    "wealth": {...},
    "health": {...},
    "marriage": {...}
  }
}
```

---

## 🔧 If Something Goes Wrong

**Error: "Could not get any response"**
→ Server not running? Check terminal window

**Error: "400 Bad Request"**
→ Check JSON format, all fields present

**Error: "500 Internal Server Error"**
→ Check server terminal for error messages

---

**That's it! You're ready to test! 🎉**
