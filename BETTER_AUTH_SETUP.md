# Better Auth Setup Guide

## What Changed

Your application now uses **Better Auth** for authentication as required by the hackathon.

### Before (Wrong):
- FastAPI handled registration/login
- FastAPI created JWT tokens
- Custom authentication implementation

### After (Correct):
- Better Auth (Next.js) handles registration/login
- Better Auth creates JWT tokens
- FastAPI only verifies tokens from Better Auth

## Setup Steps

### 1. Database Migration (COMPLETED ✓)

The Better Auth tables have been created in your Neon database:
- `user` - User accounts
- `session` - User sessions
- `account` - Password storage
- `verification` - Email verification tokens

### 2. Install Dependencies

```bash
cd frontend
npm install
```

Dependencies already installed:
- `better-auth@^0.6.0`
- `pg` (PostgreSQL client)

### 3. Environment Variables

**Frontend (.env.local):**
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8001
BETTER_AUTH_SECRET=your-super-secret-jwt-key-change-in-production
DATABASE_URL=postgresql://...
NODE_ENV=development
```

**Backend (.env):**
```env
DATABASE_URL=postgresql://...
JWT_SECRET=your-super-secret-jwt-key-change-in-production
BETTER_AUTH_SECRET=your-super-secret-jwt-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=http://localhost:3000
PORT=8001
HOST=0.0.0.0
ENVIRONMENT=development
```

**IMPORTANT:** Both frontend and backend must use the **same** `BETTER_AUTH_SECRET` for JWT verification.

### 4. Start the Application

**Terminal 1 - Backend:**
```bash
cd backend
.\venv\Scripts\activate
uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## How It Works

### Registration Flow

1. User fills registration form at `/register`
2. Frontend calls Better Auth: `signUp.email()`
3. Better Auth:
   - Creates user in `user` table
   - Hashes password and stores in `account` table
   - Creates session in `session` table
   - Returns JWT token
4. User redirected to login

### Login Flow

1. User fills login form at `/login`
2. Frontend calls Better Auth: `signIn.email()`
3. Better Auth:
   - Verifies email/password
   - Creates new session
   - Returns JWT token
4. Frontend stores user info in localStorage
5. User redirected to dashboard

### API Request Flow

1. Frontend makes API request to FastAPI
2. Includes JWT token in `Authorization: Bearer <token>` header
3. FastAPI middleware:
   - Extracts token from header
   - Verifies token signature using `BETTER_AUTH_SECRET`
   - Decodes user ID from token
4. FastAPI returns user-specific data

## Testing Better Auth

### Test 1: Registration

1. Go to http://localhost:3000/register
2. Fill in:
   - Email: `test@example.com`
   - Name: `Test User`
   - Password: `Password123!`
3. Click "Create Account"
4. Should see success message and redirect to login

### Test 2: Login

1. Go to http://localhost:3000/login
2. Enter credentials from registration
3. Click "Sign in"
4. Should redirect to dashboard

### Test 3: Verify Database

Check that Better Auth created the user:

```sql
SELECT id, email, name, created_at FROM "user";
SELECT id, user_id, provider_id FROM "account";
SELECT id, user_id, expires_at FROM "session";
```

### Test 4: API Authentication

1. Login to get JWT token
2. Open browser DevTools → Application → Local Storage
3. Should see `user_id` and `username`
4. Make API request to create task
5. Backend should verify token and allow request

## Troubleshooting

### Issue: "Failed to fetch" on registration

**Solution:**
- Check frontend is running on port 3000
- Check Better Auth API route exists: `/pages/api/auth/[...all].ts`
- Restart frontend: `npm run dev`

### Issue: "Invalid token" when accessing tasks

**Solution:**
- Verify `BETTER_AUTH_SECRET` is the same in both .env files
- Logout and login again to get new token
- Check backend logs for JWT verification errors

### Issue: "User already exists"

**Solution:**
- Email is already registered
- Use different email or delete from database:
  ```sql
  DELETE FROM "user" WHERE email = 'test@example.com';
  ```

### Issue: Backend still using old auth

**Solution:**
- Backend needs to be updated to verify Better Auth tokens
- See next section for backend updates

## Backend Updates Needed

The backend currently has custom auth endpoints that need to be disabled or removed. The backend should only:

1. Verify JWT tokens from Better Auth
2. Extract user ID from token
3. Filter data by user ID

**Current backend auth endpoints (to be disabled):**
- POST `/api/v1/auth/register` ❌
- POST `/api/v1/auth/login` ❌
- GET `/api/v1/auth/me` ❌

**Backend should only have:**
- JWT verification middleware ✓
- Task endpoints with user filtering ✓

## Success Criteria

- [ ] Can register new user via Better Auth
- [ ] Can login with registered credentials
- [ ] JWT token is created by Better Auth
- [ ] Backend verifies Better Auth tokens
- [ ] Can create/view/update/delete tasks
- [ ] Tasks are filtered by authenticated user
- [ ] Logout works correctly

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Next.js Frontend                         │
│                                                              │
│  ┌──────────────┐         ┌─────────────────────────────┐  │
│  │ Register/    │         │   Better Auth               │  │
│  │ Login Pages  │────────▶│   /api/auth/[...all]        │  │
│  └──────────────┘         │   - Creates users           │  │
│                           │   - Issues JWT tokens        │  │
│                           │   - Manages sessions         │  │
│                           └─────────────┬───────────────┘  │
│                                         │                   │
│  ┌──────────────┐                      │ JWT Token         │
│  │ Task Pages   │──────────────────────┘                   │
│  │ (Dashboard)  │                                           │
│  └──────┬───────┘                                           │
└─────────┼───────────────────────────────────────────────────┘
          │
          │ API Requests with JWT
          │ Authorization: Bearer <token>
          ▼
┌─────────────────────────────────────────────────────────────┐
│                     FastAPI Backend                          │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  JWT Verification Middleware                        │   │
│  │  - Verifies token signature                         │   │
│  │  - Extracts user_id from token                      │   │
│  └─────────────────┬───────────────────────────────────┘   │
│                    │                                         │
│                    ▼                                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Task Endpoints                                     │   │
│  │  - GET /api/v1/tasks (filtered by user_id)         │   │
│  │  - POST /api/v1/tasks (user_id from token)         │   │
│  │  - PUT /api/v1/tasks/{id} (verify ownership)       │   │
│  │  - DELETE /api/v1/tasks/{id} (verify ownership)    │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│              Neon PostgreSQL Database                        │
│                                                              │
│  Better Auth Tables:        Application Tables:             │
│  - user                     - tasks                          │
│  - session                                                   │
│  - account                                                   │
│  - verification                                              │
└─────────────────────────────────────────────────────────────┘
```

## Next Steps

1. Test registration and login with Better Auth
2. Update backend to disable old auth endpoints
3. Verify JWT token verification works
4. Test complete end-to-end flow
5. Deploy to production

## Important Notes

- Better Auth manages the `user`, `session`, `account`, and `verification` tables
- Do NOT manually modify these tables
- The `tasks` table references `user.id` via foreign key
- JWT tokens expire after 7 days (configurable in `lib/auth.ts`)
- Sessions are automatically refreshed by Better Auth
