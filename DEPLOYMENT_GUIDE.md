# 🚀 Deployment Guide - GitHub + Free Hosting

## 📋 Table of Contents
1. [GitHub Deployment](#1-github-deployment)
2. [Free Hosting Options](#2-free-hosting-options)
3. [Render Deployment (Recommended)](#3-render-deployment-recommended)
4. [Railway Deployment](#4-railway-deployment)
5. [Fly.io Deployment](#5-flyio-deployment)

---

## 1. GitHub Deployment

### Step 1: Create GitHub Account (if you don't have one)
1. Go to https://github.com
2. Click "Sign up"
3. Create your account

### Step 2: Install Git (if not installed)
1. Download Git: https://git-scm.com/downloads
2. Install it (default settings are fine)
3. Verify installation:
   ```bash
   git --version
   ```

### Step 3: Initialize Git Repository

1. **Open Terminal/Command Prompt** in your project folder:
   ```bash
   cd d:\astroTests
   ```

2. **Initialize Git:**
   ```bash
   git init
   ```

3. **Create .gitignore file** (to exclude unnecessary files):
   ```bash
   # Create .gitignore
   ```
   
   Create a file named `.gitignore` with this content:
   ```
   # Python
   __pycache__/
   *.py[cod]
   *$py.class
   *.so
   .Python
   venv/
   env/
   ENV/
   
   # IDE
   .vscode/
   .idea/
   *.swp
   *.swo
   
   # OS
   .DS_Store
   Thumbs.db
   
   # Project specific
   *.log
   .env
   ```

4. **Add all files:**
   ```bash
   git add .
   ```

5. **Create first commit:**
   ```bash
   git commit -m "Initial commit: Astrology API with analysis modules"
   ```

### Step 4: Create GitHub Repository

1. **Go to GitHub:**
   - Visit https://github.com
   - Click the **"+"** icon (top right) → **"New repository"**

2. **Repository Settings:**
   - **Repository name:** `astrology-api` (or your choice)
   - **Description:** "Vedic Astrology API with compatibility and analysis"
   - **Visibility:** Public (for free hosting) or Private
   - **DO NOT** check "Initialize with README" (we already have files)
   - Click **"Create repository"**

### Step 5: Connect Local Repository to GitHub

1. **Copy the repository URL** from GitHub (it will show after creation)

2. **Add remote and push:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/astrology-api.git
   git branch -M main
   git push -u origin main
   ```

3. **Enter your GitHub credentials** when prompted

### Step 6: Verify on GitHub
- Go to your repository on GitHub
- You should see all your files there!

---

## 2. Free Hosting Options

### Comparison Table

| Platform | Free Tier | Pros | Cons |
|----------|-----------|------|------|
| **Render** | ✅ Yes | Easy setup, auto-deploy from GitHub | Sleeps after 15 min inactivity |
| **Railway** | ✅ Yes ($5 credit/month) | Fast, modern, good docs | Limited free tier |
| **Fly.io** | ✅ Yes | Global edge deployment | More complex setup |
| **PythonAnywhere** | ✅ Yes | Python-focused | Limited features |
| **Replit** | ✅ Yes | Browser-based IDE | Less control |

### Recommendation: **Render** (Easiest & Most Reliable)

---

## 3. Render Deployment (Recommended)

### Why Render?
- ✅ Free tier available
- ✅ Auto-deploy from GitHub
- ✅ Easy setup
- ✅ HTTPS included
- ✅ Good documentation

### Step 1: Create Render Account

1. Go to https://render.com
2. Click **"Get Started for Free"**
3. Sign up with GitHub (recommended) or email

### Step 2: Prepare Your Project

1. **Create `render.yaml` file** in your project root:
   ```yaml
   services:
     - type: web
       name: astrology-api
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: python api_server.py
       envVars:
         - key: PYTHON_VERSION
           value: 3.10.0
   ```

2. **Create `Procfile`** (alternative method):
   ```
   web: python api_server.py
   ```

3. **Update `api_server.py`** to use environment port:
   ```python
   # At the bottom of api_server.py, change:
   if __name__ == '__main__':
       port = int(os.environ.get('PORT', 5000))
       app.run(debug=False, host='0.0.0.0', port=port)
   ```

4. **Update requirements.txt** (make sure it has all dependencies):
   ```
   flask==2.3.3
   flask-cors==4.0.0
   jyotishganit==0.1.2
   ```

### Step 3: Deploy on Render

1. **Go to Render Dashboard:**
   - Click **"New +"** → **"Web Service"**

2. **Connect GitHub:**
   - Click **"Connect GitHub"**
   - Authorize Render
   - Select your repository: `astrology-api`

3. **Configure Service:**
   - **Name:** `astrology-api`
   - **Region:** Choose closest to you
   - **Branch:** `main`
   - **Root Directory:** (leave empty)
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python api_server.py`
   - **Instance Type:** Free

4. **Environment Variables:**
   - Click **"Advanced"**
   - Add environment variable:
     - Key: `PORT`
     - Value: `10000` (Render uses this port)

5. **Click "Create Web Service"**

6. **Wait for deployment** (2-5 minutes)

7. **Get your URL:**
   - Your API will be at: `https://astrology-api.onrender.com`
   - Or: `https://YOUR-SERVICE-NAME.onrender.com`

### Step 4: Update API Server for Production

Update `api_server.py`:

```python
import os

# At the bottom, replace with:
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
```

### Step 5: Test Your Deployed API

```bash
curl https://YOUR-SERVICE-NAME.onrender.com/api/health
```

Or test in Postman:
- URL: `https://YOUR-SERVICE-NAME.onrender.com/api/birth-chart`
- Method: POST
- Body: (same as before)

---

## 4. Railway Deployment

### Step 1: Create Railway Account
1. Go to https://railway.app
2. Click **"Start a New Project"**
3. Sign up with GitHub

### Step 2: Deploy
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your repository
4. Railway auto-detects Python
5. Add environment variable:
   - `PORT` = `5000` (Railway sets this automatically)

### Step 3: Get URL
- Railway provides a URL like: `https://astrology-api-production.up.railway.app`

---

## 5. Fly.io Deployment

### Step 1: Install Fly CLI
```bash
# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex
```

### Step 2: Create fly.toml
Create `fly.toml` in project root:
```toml
app = "astrology-api"
primary_region = "iad"

[build]

[env]
  PORT = "8080"

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0
  processes = ["app"]

[[vm]]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 256
```

### Step 3: Deploy
```bash
fly launch
fly deploy
```

---

## 📝 Important Notes

### For All Platforms:

1. **Update CORS** (if needed):
   ```python
   # In api_server.py
   CORS(app, resources={r"/api/*": {"origins": "*"}})
   ```

2. **Environment Variables:**
   - Never commit `.env` files
   - Use platform's environment variable settings

3. **Free Tier Limitations:**
   - Services may sleep after inactivity
   - First request after sleep may be slow
   - Limited resources

4. **Keep GitHub Updated:**
   ```bash
   git add .
   git commit -m "Update for deployment"
   git push
   ```
   (Auto-deploys on Render/Railway)

---

## 🎯 Quick Start Checklist

- [ ] Git installed
- [ ] GitHub account created
- [ ] Repository created on GitHub
- [ ] Code pushed to GitHub
- [ ] `requirements.txt` updated
- [ ] `api_server.py` updated for production
- [ ] Chosen hosting platform
- [ ] Deployed and tested

---

## 🆘 Troubleshooting

### Issue: "Module not found"
- Check `requirements.txt` has all dependencies
- Rebuild service

### Issue: "Port already in use"
- Use environment variable `PORT`
- Platform sets this automatically

### Issue: "Service sleeping"
- Free tier limitation
- First request after sleep takes longer
- Consider paid tier for always-on

---

**Ready to deploy! Start with GitHub, then choose Render for easiest deployment! 🚀**
