# Quick Deployment Guide

## ✅ Prerequisites Complete
- ✅ Code pushed to GitHub: https://github.com/Muhammad-Umar-Waqar/hackathon-II-phase-II
- ✅ Frontend build successful
- ✅ Backend tested locally
- ✅ Deployment configs ready

---

## 🚀 Step 1: Deploy Frontend to Vercel (5 minutes)

### 1.1 Sign Up / Sign In
- Go to: https://vercel.com
- Click "Sign Up" or "Log In"
- Choose "Continue with GitHub"
- Authorize Vercel to access your repositories

### 1.2 Import Project
- Click "Add New..." → "Project"
- Find and select: `Muhammad-Umar-Waqar/hackathon-II-phase-II`
- Click "Import"

### 1.3 Configure Project
**Root Directory:** `frontend`
**Framework Preset:** Next.js (auto-detected)
**Build Command:** `npm run build` (auto-filled)
**Output Directory:** `.next` (auto-filled)

### 1.4 Add Environment Variables
Click "Environment Variables" and add these:

```
NEXT_PUBLIC_API_BASE_URL=https://todo-backend.onrender.com/api/v1
BETTER_AUTH_SECRET=your-super-secret-jwt-key-change-in-production
DATABASE_URL=postgresql://neondb_owner:npg_rM9kaQEf8UuT@ep-wispy-lake-a1ygpmrm-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
NODE_ENV=production
```

**Note:** You'll update `NEXT_PUBLIC_API_BASE_URL` after deploying the backend.

### 1.5 Deploy
- Click "Deploy"
- Wait 2-3 minutes for build to complete
- Copy your Vercel URL (e.g., `https://your-app.vercel.app`)

---

## 🔧 Step 2: Deploy Backend to Render (5 minutes)

### 2.1 Sign Up / Sign In
- Go to: https://render.com
- Click "Get Started" or "Sign In"
- Choose "GitHub" authentication
- **No credit card required** ✅

### 2.2 Create Web Service
- Click "New +" → "Web Service"
- Click "Connect account" if needed
- Find and select: `Muhammad-Umar-Waqar/hackathon-II-phase-II`
- Click "Connect"

### 2.3 Configure Service
**Name:** `todo-backend` (or any name you prefer)
**Region:** Singapore (closest to you)
**Branch:** `main`
**Root Directory:** `backend`
**Runtime:** Python 3
**Build Command:** `pip install -r requirements.txt`
**Start Command:** `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
**Instance Type:** Free

### 2.4 Add Environment Variables
Click "Advanced" → "Add Environment Variable" and add these:

```
DATABASE_URL=postgresql://neondb_owner:npg_rM9kaQEf8UuT@ep-wispy-lake-a1ygpmrm-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
JWT_SECRET=your-super-secret-jwt-key-change-in-production
BETTER_AUTH_SECRET=your-super-secret-jwt-key-change-in-production
ALLOWED_ORIGINS=https://your-app.vercel.app
ENVIRONMENT=production
PORT=10000
```

**Note:** Replace `https://your-app.vercel.app` with your actual Vercel URL from Step 1.

### 2.5 Deploy
- Click "Create Web Service"
- Wait 5-10 minutes for first deployment
- Copy your Render URL (e.g., `https://todo-backend.onrender.com`)

---

## 🔄 Step 3: Update Frontend Environment Variable

### 3.1 Update Vercel
- Go back to Vercel dashboard
- Click on your project
- Go to "Settings" → "Environment Variables"
- Find `NEXT_PUBLIC_API_BASE_URL`
- Click "Edit" and update to: `https://todo-backend.onrender.com/api/v1`
- Click "Save"

### 3.2 Redeploy Frontend
- Go to "Deployments" tab
- Click "..." on latest deployment
- Click "Redeploy"
- Wait 2-3 minutes

---

## ✅ Step 4: Test Your Deployment

### 4.1 Test Backend
Visit: `https://todo-backend.onrender.com/docs`
- You should see the Swagger API documentation

### 4.2 Test Frontend
Visit: `https://your-app.vercel.app`
- You should see the login page
- Try registering a new user
- Try logging in
- Try creating a todo task

---

## 📝 Step 5: Submit to Hackathon

Go to: https://forms.gle/KMKEKaFUD6ZX4UtY8

Submit:
1. **GitHub Repo:** https://github.com/Muhammad-Umar-Waqar/hackathon-II-phase-II
2. **Frontend URL:** https://your-app.vercel.app
3. **Backend URL:** https://todo-backend.onrender.com/docs
4. **Demo Video:** (Record 90-second demo)
5. **WhatsApp Number:** Your number

---

## 🎥 Creating Demo Video (Optional but Recommended)

### Quick Demo Script (90 seconds):
1. **Intro (10s):** "Hi, this is my Phase II Todo App for the hackathon"
2. **Registration (15s):** Show user registration
3. **Login (10s):** Show login process
4. **Create Task (15s):** Create a new todo task
5. **Update Task (15s):** Edit a task
6. **Complete Task (10s):** Mark task as complete
7. **Delete Task (10s):** Delete a task
8. **Outro (5s):** "Built with Next.js, FastAPI, and Neon PostgreSQL"

### Tools for Recording:
- **Windows:** Xbox Game Bar (Win + G)
- **Online:** Loom.com (free)
- **NotebookLM:** https://notebooklm.google.com (AI-generated)

---

## ⚠️ Important Notes

### Free Tier Limitations:
- **Render:** Spins down after 15 min inactivity (30-60s cold start on first request)
- **Vercel:** Unlimited for personal projects
- **Neon:** 0.5 GB storage limit

### If Something Goes Wrong:
1. Check Render logs: Dashboard → Logs
2. Check Vercel logs: Deployments → View Function Logs
3. Verify environment variables are set correctly
4. Ensure CORS is configured with correct Vercel URL

---

## 🎉 You're Done!

Your Phase II Todo App is now live and ready for submission!

**Estimated Total Time:** 15-20 minutes
**Cost:** $0 (completely free)
