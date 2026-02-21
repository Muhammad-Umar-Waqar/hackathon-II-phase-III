# PAGES ROUTER SETUP - READY TO TEST

## ✅ What I Just Did

1. ✅ Verified Pages Router file exists at `pages/api/auth/[...all].ts`
2. ✅ Removed App Router auth directory (`src/app/api/auth`)
3. ✅ Cleaned Next.js cache (`.next` and `node_modules/.cache`)

## 🚀 RESTART FRONTEND NOW

### In your frontend terminal:

```bash
# If frontend is running, press Ctrl+C to stop it

cd frontend
npm run dev
```

**Wait for:** `✓ Ready in X ms`

## 🧪 TEST REGISTRATION

### Test 1: Curl Command (Quick Test)

Open a new terminal:

```bash
curl -X POST http://localhost:3000/api/auth/sign-up/email \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"test@example.com\",\"password\":\"Password123!\",\"name\":\"Test User\"}"
```

**Expected Success Response:**
```json
{
  "user": {
    "id": "some-uuid-here",
    "email": "test@example.com",
    "name": "Test User",
    "emailVerified": false,
    "createdAt": "2026-02-21T...",
    "updatedAt": "2026-02-21T..."
  },
  "session": {
    "token": "...",
    "expiresAt": "..."
  }
}
```

**If you see this ✅ - IT'S WORKING!**

**If you see 405 or 404 ❌ - Share the exact error**

### Test 2: Browser Registration

1. Open **NEW incognito window**: http://localhost:3000/register
2. Fill in:
   - Email: `yourname@example.com`
   - Name: `Your Name`
   - Password: `Password123!`
3. Click "Create Account"

**Expected:**
- ✅ Success message appears
- ✅ Redirects to login after 2 seconds
- ✅ No errors in console (F12)

### Test 3: Verify Database

Connect to Neon and run:

```sql
SELECT id, email, name, created_at
FROM "user"
ORDER BY created_at DESC
LIMIT 5;
```

Should show your registered users.

## 📋 Complete Flow Test

Once registration works:

1. **Login** at http://localhost:3000/login
2. **Create Task** - Add "Buy groceries"
3. **Update Status** - Change to "In Progress"
4. **Complete Task** - Change to "Completed"
5. **Delete Task** - Remove it
6. **Logout** - Click logout button
7. **Login Again** - Verify tasks persist

## 🎯 Success Indicators

✅ Curl returns user data (not 405)
✅ Browser registration succeeds
✅ User appears in database
✅ Can login with credentials
✅ Can create tasks
✅ Tasks are saved with user_id
✅ Can logout and login again

## 🐛 If Still Not Working

Share:
1. **Curl command output** (copy entire response)
2. **Frontend terminal output** (last 20 lines)
3. **Browser console errors** (F12 → Console)

## 📁 Current Setup

- **Auth Route:** `pages/api/auth/[...all].ts` (Pages Router)
- **Auth Config:** `lib/auth.ts`
- **Auth Client:** `lib/auth-client.ts`
- **Database:** All Better Auth tables exist
- **Backend:** Updated to use TEXT user_ids

## Why This Should Work Now

Pages Router is more stable and has better support for Better Auth. The route handler is simpler and doesn't have the export issues that App Router has.

---

**Just restart frontend and test the curl command. It should work immediately.**
