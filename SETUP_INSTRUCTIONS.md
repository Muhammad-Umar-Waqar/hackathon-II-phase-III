# Setup Instructions - Phase II Todo Application

## ✅ Implementation Complete

All hackathon requirements have been implemented:
- ✅ SQLModel ORM (Backend)
- ✅ Better Auth (Frontend)
- ✅ JWT Token Integration
- ✅ Neon PostgreSQL Compatible
- ✅ Next.js + FastAPI Stack
- ✅ Full CRUD Operations
- ✅ User Isolation
- ✅ Responsive Design

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- PostgreSQL database (Neon recommended)

### 1. Clone and Setup Environment

```bash
# Navigate to project
cd hackathon-2-phase-2

# Backend environment
cd backend
cp .env.example .env
# Edit .env with your database credentials and secrets

# Frontend environment
cd ../frontend
cp .env.example .env
# Edit .env with your API URL and secrets
```

### 2. Install Dependencies

**Backend:**
```bash
cd backend
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

### 3. Initialize Database

```bash
# From project root
python init_db.py
```

This creates:
- `users` table (SQLModel)
- `tasks` table (SQLModel)
- Better Auth tables (auto-created on first run)

### 4. Start Services

**Terminal 1 - Backend:**
```bash
cd backend
python -m src.main
# Runs on http://localhost:8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
# Runs on http://localhost:3000
```

### 5. Test the Application

1. Open http://localhost:3000
2. Click "Sign up" to create an account
3. Login with your credentials
4. Create, view, update, and delete tasks
5. Verify user isolation (create another account and check tasks are separate)

## 🔑 Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@host:port/database
JWT_SECRET=your-super-secret-key-must-match-frontend
BETTER_AUTH_SECRET=your-super-secret-key-must-match-frontend
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
PORT=8000
```

### Frontend (.env)
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
BETTER_AUTH_SECRET=your-super-secret-key-must-match-backend
DATABASE_URL=postgresql://user:password@host:port/database
```

**CRITICAL:** `JWT_SECRET` (backend) and `BETTER_AUTH_SECRET` (both) must be identical for token verification to work.

## 📊 API Endpoints

### Authentication (Better Auth)
- POST `/api/auth/sign-up` - Register new user
- POST `/api/auth/sign-in` - Login user
- POST `/api/auth/sign-out` - Logout user
- GET `/api/auth/session` - Get current session

### Tasks (FastAPI)
- GET `/api/v1/tasks` - Get all user's tasks
- POST `/api/v1/tasks` - Create new task
- GET `/api/v1/tasks/{id}` - Get specific task
- PUT `/api/v1/tasks/{id}` - Update task
- DELETE `/api/v1/tasks/{id}` - Delete task

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
pytest --cov=src --cov-report=html
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🐛 Troubleshooting

### "Module not found" errors
```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

### Database connection errors
- Verify DATABASE_URL is correct in both .env files
- Ensure PostgreSQL is running
- Check firewall/network settings for Neon

### Authentication not working
- Verify JWT_SECRET and BETTER_AUTH_SECRET match in both .env files
- Clear browser localStorage and cookies
- Check browser console for errors

### CORS errors
- Verify ALLOWED_ORIGINS in backend .env includes your frontend URL
- Check that frontend is running on expected port

## 📁 Project Structure

```
hackathon-2-phase-2/
├── backend/                    # FastAPI backend
│   ├── src/
│   │   ├── models/            # SQLModel tables
│   │   ├── services/          # Business logic
│   │   ├── api/               # API routers
│   │   ├── middleware/        # Auth middleware
│   │   ├── utils/             # Utilities
│   │   ├── database.py        # SQLModel engine
│   │   └── main.py            # FastAPI app
│   ├── tests/                 # Backend tests
│   ├── requirements.txt       # Python dependencies
│   └── .env.example           # Environment template
├── frontend/                   # Next.js frontend
│   ├── src/
│   │   ├── app/api/auth/      # Better Auth routes
│   │   ├── lib/               # Better Auth config
│   │   ├── pages/             # Next.js pages
│   │   ├── components/        # React components
│   │   └── services/          # API client
│   ├── tests/                 # Frontend tests
│   ├── package.json           # Node dependencies
│   └── .env.example           # Environment template
├── specs/                      # Specifications
├── docs/                       # Documentation
├── history/                    # Prompt history
├── init_db.py                 # Database initialization
├── MIGRATION_GUIDE.md         # Migration details
├── IMPLEMENTATION_STATUS.md   # Status report
└── README.md                  # Project overview
```

## 🎯 Hackathon Compliance Checklist

- [x] SQLModel ORM for database operations
- [x] Better Auth for authentication
- [x] JWT token integration (shared secret)
- [x] Neon PostgreSQL compatible
- [x] Next.js 14+ frontend
- [x] FastAPI backend
- [x] User registration and login
- [x] Task CRUD operations
- [x] User isolation (can't see other users' tasks)
- [x] Responsive design (mobile, tablet, desktop)
- [x] REST API endpoints
- [x] Environment configuration
- [x] Documentation

## 📝 Next Steps

1. Deploy backend to hosting service (Railway, Render, etc.)
2. Deploy frontend to Vercel
3. Configure production environment variables
4. Set up Neon PostgreSQL production database
5. Test production deployment
6. Submit to hackathon

## 🆘 Support

For issues or questions:
1. Check MIGRATION_GUIDE.md for detailed migration steps
2. Review IMPLEMENTATION_STATUS.md for feature status
3. Check browser console and backend logs for errors
4. Verify all environment variables are set correctly
