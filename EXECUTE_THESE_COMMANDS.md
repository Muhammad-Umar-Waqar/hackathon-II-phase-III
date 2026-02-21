# COMPLETE SETUP - STEP BY STEP COMMANDS

## Current Status
✅ All code changes complete
✅ Database migrations done
✅ Better Auth configured
⏳ Needs server restart and testing

## EXECUTE THESE COMMANDS IN ORDER

### Terminal 1: Stop and Restart Backend

```bash
# If backend is running, press Ctrl+C to stop it

cd D:/GIAIC/hackathon-2-phase-2/hackathon-2-phase-2/backend
.\venv\Scripts\activate
uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload
```

**Wait for this output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8001
INFO:     Application startup complete.
```

### Terminal 2: Stop, Clean, and Restart Frontend

```bash
# If frontend is running, press Ctrl+C to stop it

cd D:/GIAIC/hackathon-2-phase-2/hackathon-2-phase-2/frontend

# Clean cache (IMPORTANT)
rm -rf .next
rm -rf node_modules/.cache

# Start frontend
npm run dev
```

**Wait for this output:**
```
✓ Ready in X ms
- Local: http://localhost:3000
```

### Terminal 3: Test the Auth Endpoint

```bash
curl -X POST http://localhost:3000/api/auth/sign-up/email \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"curltest@example.com\",\"password\":\"Password123!\",\"name\":\"Curl Test\"}"
```

**Expected Output (Success):**
```json
{
  "user": {
    "id": "some-uuid",
    "email": "curltest@example.com",
    "name": "Curl Test",
    ...
  },
  "session": {...}
}
```

**NOT Expected (Failure):**
```json
{"error": "Method Not Allowed"}
```
or
```
404 Not Found
```

## Browser Test

1. **Open NEW incognito window** (Ctrl+Shift+N in Chrome)
2. Go to: http://localhost:3000/register
3. Open DevTools (F12) → Network tab
4. Fill in form:
   - Email: `yourname@example.com`
   - Name: `Your Name`
   - Password: `Password123!`
5. Click "Create Account"
6. Watch Network tab for the request

**Success Indicators:**
- Request URL: `http://localhost:3000/api/auth/sign-up/email`
- Status: `200 OK`
- Response contains user data
- Success message appears
- Redirects to login after 2 seconds

**Failure Indicators:**
- Status: `405 Method Not Allowed`
- Status: `404 Not Found`
- Error in console

## If curl Test Succeeds but Browser Fails

The issue is in the frontend registration code. Share:
1. Browser console error (F12 → Console)
2. Network request details (F12 → Network → click the failed request)

## If curl Test Fails (405 or 404)

The route handler isn't working. Try Pages Router instead:

```bash
cd frontend

# Remove App Router auth
rm -rf src/app/api/auth

# Create Pages Router auth
mkdir -p pages/api/auth

# Create the file
cat > pages/api/auth/[...all].ts << 'EOF'
import { auth } from "../../../lib/auth";
import type { NextApiRequest, NextApiResponse } from "next";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  return auth.handler(req, res);
}
EOF

# Clean and restart
rm -rf .next
npm run dev
```

Then test curl command again.

## Verify Database

After successful registration:

```sql
-- Connect to Neon database and run:
SELECT id, email, name, created_at
FROM "user"
ORDER BY created_at DESC
LIMIT 5;
```

Should show your registered users.

## Complete Flow Test

Once registration works:

1. **Login:** http://localhost:3000/login
2. **Create Task:** Add a task on dashboard
3. **Update Task:** Change status to "In Progress"
4. **Delete Task:** Remove the task
5. **Logout:** Click logout button
6. **Login Again:** Verify tasks persist

## What to Share If Still Failing

1. **curl command output** (copy entire response)
2. **Browser console errors** (F12 → Console, copy all red errors)
3. **Network request details** (F12 → Network → click failed request → copy Headers and Response)
4. **Frontend terminal output** (copy last 20 lines)
5. **Backend terminal output** (copy last 20 lines)

## Files That Should Exist

Verify these files exist:

```bash
cd frontend

# Check these files
ls -la src/app/api/auth/[...all]/route.ts
ls -la lib/auth.ts
ls -la lib/auth-client.ts
ls -la .env.local

# Check content
cat src/app/api/auth/[...all]/route.ts
```

Should show:
```typescript
import { auth } from "../../../lib/auth";

export const GET = auth.handler;
export const POST = auth.handler;
```

## Summary

I've completed all code changes. The application should work after:
1. Restarting both servers
2. Clearing frontend cache
3. Testing registration

I cannot restart your servers or test in your browser, so I need you to:
1. Run the commands above
2. Test registration
3. Share results (success or specific error messages)

Then I can help with any remaining issues.
