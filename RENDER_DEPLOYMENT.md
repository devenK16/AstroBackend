# 🚀 Render.com Deployment - Step by Step

## Why Render?
- ✅ **Free tier** available
- ✅ **Auto-deploy** from GitHub
- ✅ **Easy setup** (5 minutes)
- ✅ **HTTPS included**
- ✅ **No credit card** required

---

## Step 1: Create Render Account

1. Go to: https://render.com
2. Click **"Get Started for Free"**
3. **Sign up with GitHub** (recommended - easiest)
   - Click "Continue with GitHub"
   - Authorize Render
   - Or sign up with email

---

## Step 2: Prepare Your Code

### 2.1 Make Sure Files Are Ready

Your project should have:
- ✅ `api_server.py` (updated for production)
- ✅ `requirements.txt`
- ✅ `Procfile`
- ✅ `modules/` folder with all modules
- ✅ `data/` folder with all JSON files

### 2.2 Verify requirements.txt

Make sure `requirements.txt` has:
```
flask==2.3.3
flask-cors==4.0.0
jyotishganit==0.1.2
python-dateutil
```

### 2.3 Push Latest Code to GitHub

```bash
cd d:\astroTests
git add .
git commit -m "Ready for deployment"
git push
```

---

## Step 3: Deploy on Render

### 3.1 Create New Web Service

1. **Go to Render Dashboard:**
   - After logging in, you'll see the dashboard
   - Click **"New +"** button (top right)
   - Click **"Web Service"**

### 3.2 Connect GitHub Repository

1. **Connect GitHub** (if not connected):
   - Click **"Connect GitHub"**
   - Authorize Render to access your repositories
   - Select repositories (or all)

2. **Select Repository:**
   - Search for: `astrology-api`
   - Click on it

### 3.3 Configure Service

Fill in the form:

**Basic Settings:**
- **Name:** `astrology-api` (or your choice)
- **Region:** Choose closest to you (e.g., "Oregon (US West)")
- **Branch:** `main` (or `master` if that's your branch)
- **Root Directory:** (leave empty)

**Build & Deploy:**
- **Environment:** `Python 3`
- **Build Command:** 
  ```
  pip install -r requirements.txt
  ```
- **Start Command:**
  ```
  python api_server.py
  ```

**Advanced Settings:**
- Click **"Advanced"** to expand
- **Instance Type:** `Free` (or paid if you want)
- **Auto-Deploy:** `Yes` (deploys automatically on git push)

### 3.4 Add Environment Variables (Optional)

Click **"Advanced"** → **"Environment Variables"**

Add if needed:
- `FLASK_ENV` = `production`
- `PORT` = `10000` (Render sets this automatically, but you can specify)

### 3.5 Create Service

1. Click **"Create Web Service"**
2. Wait for deployment (2-5 minutes)
   - You'll see build logs
   - Watch for errors

---

## Step 4: Get Your API URL

After deployment succeeds:

1. **Your API URL will be:**
   ```
   https://astrology-api.onrender.com
   ```
   Or:
   ```
   https://YOUR-SERVICE-NAME.onrender.com
   ```

2. **Test Health Endpoint:**
   ```bash
   curl https://YOUR-SERVICE-NAME.onrender.com/api/health
   ```

   Or open in browser:
   ```
   https://YOUR-SERVICE-NAME.onrender.com/api/health
   ```

---

## Step 5: Test Your Deployed API

### Using Postman:

1. **URL:** `https://YOUR-SERVICE-NAME.onrender.com/api/birth-chart`
2. **Method:** POST
3. **Headers:** `Content-Type: application/json`
4. **Body:**
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

### Using curl:
```bash
curl -X POST https://YOUR-SERVICE-NAME.onrender.com/api/birth-chart \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Deven",
    "date": "2002-02-16",
    "time": "10:20",
    "latitude": 21.1458,
    "longitude": 79.0882,
    "timezone": 5.5
  }'
```

---

## Step 6: Update Frontend (If You Have One)

Change your API URL from:
```javascript
const API_URL = 'http://localhost:5000';
```

To:
```javascript
const API_URL = 'https://YOUR-SERVICE-NAME.onrender.com';
```

---

## Important Notes

### Free Tier Limitations:

1. **Service Sleeps:**
   - After 15 minutes of inactivity
   - First request after sleep takes 30-60 seconds
   - Subsequent requests are fast

2. **Solution:**
   - Use a service like UptimeRobot (free) to ping your API every 10 minutes
   - Or upgrade to paid plan ($7/month) for always-on

### Auto-Deploy:

- Every time you push to GitHub, Render automatically redeploys
- No manual deployment needed!

### View Logs:

1. Go to your service on Render
2. Click **"Logs"** tab
3. See real-time logs

---

## Troubleshooting

### Build Fails

**Error: "Module not found"**
- Check `requirements.txt` has all dependencies
- Check build logs for specific error

**Error: "Command failed"**
- Check `Procfile` or start command is correct
- Verify `api_server.py` exists

### Service Crashes

**Check Logs:**
1. Go to Render dashboard
2. Click your service
3. Click "Logs" tab
4. Look for error messages

**Common Issues:**
- Missing environment variables
- Port not set correctly
- Import errors

### Service Sleeping

**First request slow:**
- This is normal for free tier
- Wait 30-60 seconds for first response
- Use UptimeRobot to keep it awake

---

## Update Your Code

Whenever you make changes:

```bash
# 1. Make changes to your code
# 2. Commit and push
git add .
git commit -m "Update description"
git push

# 3. Render automatically deploys!
# Check Render dashboard for deployment status
```

---

## ✅ Success Checklist

- [ ] Render account created
- [ ] GitHub repository connected
- [ ] Web service created
- [ ] Deployment successful
- [ ] Health endpoint works
- [ ] Birth chart endpoint tested
- [ ] API URL saved

---

## 🎉 You're Live!

Your API is now accessible worldwide at:
```
https://YOUR-SERVICE-NAME.onrender.com
```

Share this URL with your frontend or test it in Postman!

---

## Next Steps

1. **Keep Service Awake (Optional):**
   - Sign up at https://uptimerobot.com (free)
   - Add monitor for your API URL
   - Set interval to 10 minutes

2. **Add Custom Domain (Optional):**
   - Render → Your Service → Settings
   - Add custom domain
   - Update DNS records

3. **Monitor Usage:**
   - Render dashboard shows usage
   - Free tier: 750 hours/month

---

**Your API is deployed! 🚀**
