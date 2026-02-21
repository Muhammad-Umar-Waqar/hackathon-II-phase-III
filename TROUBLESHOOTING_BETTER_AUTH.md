# Better Auth Troubleshooting Steps

## Current Status
- Better Auth version: 0.6.2
- Next.js version: 14.2.35
- Error: 405 Method Not Allowed

## Steps to Fix

### 1. Stop Frontend Completely
```bash
# Press Ctrl+C in frontend terminal
# Make sure it's fully stopped
```

### 2. Clear Next.js Cache
```bash
cd frontend
rm -rf .next
rm -rf node_modules/.cache
```

### 3. Verify Route File
```bash
cat src/app/api/auth/[...all]/route.ts
```

Should show:
```typescript
import { auth } from "@/lib/auth";

export const GET = auth.handler;
export const POST = auth.handler;
```

### 4. Restart Frontend
```bash
npm run dev
```

### 5. Test Registration

Open http://localhost:3000/register in a **new incognito window**

Fill in:
- Email: test@example.com
- Name: Test User
- Password: Password123!

Click "Create Account"

## Check These If Still Failing

### A. Verify Database Connection
```bash
cd frontend
node -e "const { Pool } = require('pg'); const pool = new Pool({ connectionString: process.env.DATABASE_URL }); pool.query('SELECT NOW()', (err, res) => { console.log(err ? err : res.rows); pool.end(); });"
```

### B. Check Better Auth Tables
Connect to Neon and run:
```sql
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'public'
AND table_name IN ('user', 'session', 'account', 'verification');
```

Should return all 4 tables.

### C. Test Better Auth Endpoint Directly
```bash
curl -X POST http://localhost:3000/api/auth/sign-up/email \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Password123!","name":"Test User"}'
```

Should return user data, not 405.

### D. Check Frontend Logs
Look for errors in the terminal where `npm run dev` is running.

### E. Check Browser Console
Open DevTools (F12) → Console tab
Look for any JavaScript errors

## Alternative: Use Pages Router Instead

If App Router continues to have issues, we can switch to Pages Router:

```bash
cd frontend
mkdir -p pages/api/auth
```

Create `pages/api/auth/[...all].ts`:
```typescript
import { auth } from "@/lib/auth";
import type { NextApiRequest, NextApiResponse } from "next";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  return auth.handler(req, res);
}
```

Then restart frontend.

## If Nothing Works

We can fall back to the original FastAPI authentication (not Better Auth) which was working before. Let me know if you want to do that.
