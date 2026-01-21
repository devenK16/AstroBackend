# ⚡ Quick Deployment Guide - 10 Minutes

## 🎯 Goal
Deploy your Astrology API to GitHub and host it for free on Render.com

---

## Part 1: GitHub (5 minutes)

### Step 1: Install Git
- Download: https://git-scm.com/downloads
- Install with defaults

### Step 2: Initialize Git
```bash
cd d:\astroTests
git init
git add .
git commit -m "Initial commit"
```

### Step 3: Create GitHub Repo
1. Go to: https://github.com/new
2. Name: `astrology-api`
3. Click "Create repository"

### Step 4: Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/astrology-api.git
git branch -M main
git push -u origin main
```
(Use Personal Access Token as password - see GITHUB_DEPLOYMENT.md)

---

## Part 2: Render.com (5 minutes)

### Step 1: Sign Up
- Go to: https://render.com
- Click "Get Started for Free"
- Sign up with GitHub

### Step 2: Deploy
1. Click "New +" → "Web Service"
2. Connect GitHub → Select `astrology-api`
3. Configure:
   - **Name:** `astrology-api`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python api_server.py`
   - **Instance Type:** `Free`
4. Click "Create Web Service"

### Step 3: Wait & Test
- Wait 2-5 minutes for deployment
- Get your URL: `https://astrology-api.onrender.com`
- Test: `https://astrology-api.onrender.com/api/health`

---

## ✅ Done!

Your API is live at: `https://YOUR-SERVICE-NAME.onrender.com`

**For detailed steps, see:**
- `GITHUB_DEPLOYMENT.md` - Complete GitHub guide
- `RENDER_DEPLOYMENT.md` - Complete Render guide
- `DEPLOYMENT_GUIDE.md` - All hosting options

---

## 🎉 Test Your API

**Postman:**
- URL: `https://YOUR-SERVICE-NAME.onrender.com/api/birth-chart`
- Method: POST
- Body: Same as before

**Success!** 🚀
