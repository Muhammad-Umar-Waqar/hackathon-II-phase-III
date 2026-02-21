# Deployment Guide

## Frontend - Vercel (Free, No Card Required)

### Steps:
1. Go to [vercel.com](https://vercel.com)
2. Sign in with GitHub
3. Click "New Project"
4. Import your repository: `Muhammad-Umar-Waqar/hackathon-II-completed`
5. Configure:
   - **Framework Preset:** Next.js
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `.next`

6. Add Environment Variables:
   ```
   NEXT_PUBLIC_API_BASE_URL=https://your-backend.onrender.com/api/v1
   BETTER_AUTH_SECRET=your-super-secret-jwt-key-change-in-production
   DATABASE_URL=your-neon-database-url
   NODE_ENV=production
   ```

7. Click "Deploy"

---

## Backend - Render (Free, No Card Required)

### Steps:
1. Go to [render.com](https://render.com)
2. Sign in with GitHub
3. Click "New +" → "Web Service"
4. Connect your repository: `Muhammad-Umar-Waqar/hackathon-II-completed`
5. Configure:
   - **Name:** `todo-backend`
   - **Region:** Singapore (closest to you)
   - **Branch:** `main`
   - **Root Directory:** `backend`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn src.main:app --host 0.0.0.0 --port $PORT`

6. Add Environment Variables:
   ```
   DATABASE_URL=your-neon-database-url
   JWT_SECRET=your-super-secret-jwt-key-change-in-production
   BETTER_AUTH_SECRET=your-super-secret-jwt-key-change-in-production
   ALLOWED_ORIGINS=https://your-frontend.vercel.app,http://localhost:3000
   ENVIRONMENT=production
   PORT=10000
   ```

7. Click "Create Web Service"

### Important Notes:
- ⚠️ Free tier spins down after 15 minutes of inactivity
- First request after sleep takes 30-60 seconds (cold start)
- 750 hours/month free (enough for hackathon)
- No credit card required

---

## Database - Neon (Already Configured)

Your Neon database is already set up. Just use the connection string in both deployments.

---

## Post-Deployment Steps

### 1. Update Frontend Environment
After backend deploys, update Vercel environment variable:
```
NEXT_PUBLIC_API_BASE_URL=https://todo-backend.onrender.com/api/v1
```

### 2. Update Backend CORS
After frontend deploys, update Render environment variable:
```
ALLOWED_ORIGINS=https://your-app.vercel.app
```

### 3. Initialize Database
Run this once after deployment:
```bash
# SSH into Render or run locally pointing to production DB
python init_db.py
```

---

## Testing Deployment

### Backend Health Check:
```bash
curl https://todo-backend.onrender.com/docs
```

### Frontend:
Visit: `https://your-app.vercel.app`

---

## Troubleshooting

### Backend Issues:
- Check Render logs: Dashboard → Logs
- Verify environment variables are set
- Ensure DATABASE_URL is correct

### Frontend Issues:
- Check Vercel deployment logs
- Verify API_BASE_URL points to Render backend
- Check browser console for CORS errors

### CORS Errors:
Update backend `ALLOWED_ORIGINS` to include your Vercel URL

---

## Free Tier Limits

| Platform | Limit | What Happens After |
|----------|-------|-------------------|
| Vercel | Unlimited for personal | Continues working |
| Render | 750 hours/month | Service pauses (can restart) |
| Neon | 0.5 GB storage | Need to upgrade or create new project |

---

## Submission Links

After deployment, submit these URLs:
1. **GitHub:** https://github.com/Muhammad-Umar-Waqar/hackathon-II-completed
2. **Frontend:** https://your-app.vercel.app
3. **Backend API:** https://todo-backend.onrender.com/docs
