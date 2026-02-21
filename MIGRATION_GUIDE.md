# Better Auth + SQLModel Migration Guide

## ✅ Completed Changes

### Backend (SQLModel Migration)
- ✅ Migrated from SQLAlchemy to SQLModel
- ✅ Updated `database.py` to use SQLModel engine
- ✅ Updated `models/user.py` and `models/task.py` to SQLModel
- ✅ Updated `services/user_service.py` and `services/task_service.py`
- ✅ Updated `requirements.txt` to include `sqlmodel==0.0.14`

### Frontend (Better Auth Integration)
- ✅ Created `lib/auth.ts` - Better Auth server configuration
- ✅ Created `lib/auth-client.ts` - Better Auth client
- ✅ Created `app/api/auth/[...all]/route.ts` - Auth API routes
- ✅ Updated `package.json` with Better Auth dependencies
- ✅ Updated environment templates

## 🔧 Required Manual Updates

### 1. Update Frontend Auth Pages

**File: `frontend/src/pages/login.jsx`**
Replace the import:
```javascript
// OLD
import AuthService from '../services/auth';

// NEW
import { signIn } from '@/lib/auth-client';
```

Replace the handleSubmit function:
```javascript
const handleSubmit = async (e) => {
  e.preventDefault();
  setLoading(true);
  setError('');

  try {
    await signIn.email({
      email: formData.email,
      password: formData.password,
    });
    router.push('/');
  } catch (err) {
    setError(err.message || 'Login failed');
  } finally {
    setLoading(false);
  }
};
```

**File: `frontend/src/pages/register.jsx`**
Replace the import:
```javascript
// OLD
import AuthService from '../services/auth';

// NEW
import { signUp } from '@/lib/auth-client';
```

Replace the handleSubmit function:
```javascript
const handleSubmit = async (e) => {
  e.preventDefault();
  setLoading(true);
  setError('');

  try {
    await signUp.email({
      email: formData.email,
      password: formData.password,
      name: formData.username,
    });
    setSuccess('Registration successful!');
    setTimeout(() => router.push('/login'), 2000);
  } catch (err) {
    setError(err.message || 'Registration failed');
  } finally {
    setLoading(false);
  }
};
```

### 2. Update API Client

**File: `frontend/src/services/api.js`**
Replace the request interceptor:
```javascript
import { authClient } from '@/lib/auth-client';

// Request interceptor
api.interceptors.request.use(
  async (config) => {
    const session = await authClient.getSession();
    if (session?.session?.token) {
      config.headers.Authorization = `Bearer ${session.session.token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);
```

### 3. Update Home Page

**File: `frontend/src/pages/index.jsx`**
Add Better Auth session hook:
```javascript
import { useSession, signOut } from '@/lib/auth-client';

const HomePage = () => {
  const { data: session, isPending } = useSession();

  if (isPending) {
    return <div>Loading...</div>;
  }

  if (!session) {
    router.push('/login');
    return null;
  }

  const handleLogout = async () => {
    await signOut();
    router.push('/login');
  };

  // Rest of component...
};
```

### 4. Backend JWT Verification

The backend already verifies JWT tokens. Ensure the `JWT_SECRET` in backend matches `BETTER_AUTH_SECRET` in frontend.

**File: `backend/.env`**
```env
JWT_SECRET=your-super-secret-key
BETTER_AUTH_SECRET=your-super-secret-key  # Must match
```

**File: `frontend/.env`**
```env
BETTER_AUTH_SECRET=your-super-secret-key  # Must match backend
DATABASE_URL=postgresql://user:pass@host:port/db
```

## 📦 Installation Steps

### Backend
```bash
cd backend
pip install -r requirements.txt
python -c "from src.database import init_db; init_db()"
python -m src.main
```

### Frontend
```bash
cd frontend
npm install
# Better Auth will auto-create tables on first run
npm run dev
```

## 🔑 Key Changes Summary

| Component | Before | After |
|-----------|--------|-------|
| Backend ORM | SQLAlchemy + Pydantic | SQLModel |
| Frontend Auth | Custom JWT | Better Auth |
| Token Sharing | Manual | Shared JWT_SECRET |
| Database | Direct SQLAlchemy | SQLModel + Better Auth tables |

## ✅ Verification Checklist

- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] Can register new user
- [ ] Can login with credentials
- [ ] JWT token is sent to backend
- [ ] Backend verifies token correctly
- [ ] Can create/view/update/delete tasks
- [ ] User isolation works (can't see other users' tasks)
- [ ] Logout works correctly

## 🎯 Hackathon Compliance

✅ **SQLModel** - Backend now uses SQLModel as required
✅ **Better Auth** - Frontend uses Better Auth for authentication
✅ **JWT Integration** - Shared secret enables backend verification
✅ **Neon PostgreSQL** - Compatible with connection string
✅ **Next.js + FastAPI** - Stack unchanged
