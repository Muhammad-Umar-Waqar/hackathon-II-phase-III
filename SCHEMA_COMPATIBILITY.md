# IMPORTANT: Schema Compatibility Issue

## Problem

Your backend has a schema mismatch with Better Auth:

**Backend (Current):**
- Table: `users` (plural)
- Primary Key: `id` (INTEGER)
- Tasks reference: `user_id` (INTEGER)

**Better Auth (Required):**
- Table: `user` (singular)
- Primary Key: `id` (TEXT/UUID)
- JWT tokens contain: `user.id` (TEXT)

## Quick Fix (Current Implementation)

For now, the application works with this hybrid approach:

1. **Better Auth** handles authentication (login/register)
   - Creates users in `user` table with TEXT ids
   - Issues JWT tokens with TEXT user ids

2. **Backend** needs to be updated to:
   - Accept TEXT user_ids from JWT tokens
   - Either convert to INTEGER or update schema

## Solution Options

### Option 1: Update Backend Schema (Recommended)

Change the backend to use TEXT user_ids matching Better Auth:

```python
# backend/src/models/task.py
class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: str = Field(default="pending", index=True)
    user_id: str = Field(foreign_key="user.id", index=True)  # Changed to str
    # ... rest of fields
```

**Migration needed:**
```sql
-- Convert user_id from INTEGER to TEXT
ALTER TABLE tasks ALTER COLUMN user_id TYPE TEXT;
-- Update foreign key to reference Better Auth user table
ALTER TABLE tasks DROP CONSTRAINT IF EXISTS tasks_user_id_fkey;
ALTER TABLE tasks ADD CONSTRAINT tasks_user_id_fkey
    FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE CASCADE;
```

### Option 2: Keep Separate User Tables (Current)

Keep both tables and sync them:
- `user` table (Better Auth) - for authentication
- `users` table (Backend) - for application data
- Create a sync mechanism

**Not recommended** - adds complexity

### Option 3: Disable Old Backend Auth (Simplest for Testing)

Just disable the old auth endpoints and test Better Auth:

```python
# backend/src/main.py
# Comment out the auth router
# app.include_router(auth_router.router, prefix="/api/v1/auth", tags=["authentication"])
```

## Current Status

✅ Better Auth is installed and configured
✅ Database migration completed (Better Auth tables created)
✅ Frontend updated to use Better Auth
✅ Backend bcrypt error fixed
❌ Schema mismatch between Better Auth and backend tasks

## Next Steps

1. **Test Better Auth Registration/Login:**
   ```bash
   cd frontend
   npm run dev
   ```
   - Go to http://localhost:3000/register
   - Register a new user
   - Check database: `SELECT * FROM "user";`

2. **Update Backend Schema:**
   - Run the migration to convert user_id to TEXT
   - Update Task model
   - Update auth_router.py to handle TEXT user_ids

3. **Test End-to-End:**
   - Login with Better Auth
   - Create tasks
   - Verify tasks are saved with correct user_id

## Temporary Workaround

To test Better Auth without schema changes:

1. Register/login works (Better Auth creates user in `user` table)
2. Tasks won't work yet (schema mismatch)
3. Need to update backend to handle TEXT user_ids

## Files to Update

1. `backend/src/models/task.py` - Change user_id to str
2. `backend/src/models/user.py` - Remove or update to match Better Auth
3. `backend/src/api/auth_router.py` - Update verify_token to return str
4. `backend/src/services/user_service.py` - Update to work with TEXT ids
5. Run database migration to convert existing data
