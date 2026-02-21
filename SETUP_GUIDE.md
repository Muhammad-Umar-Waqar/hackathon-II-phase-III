# Setup and Run Guide

## Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Activate virtual environment:
```bash
# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Run the backend server:
```bash
# CORRECT command (note --port flag):
uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload

# NOT: uvicorn src.main:app --host 0.0.0.0 8001 (missing --port)
```

Backend will run on: http://localhost:8001

## Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies (first time only):
```bash
npm install
```

3. Run the frontend:
```bash
npm run dev
```

Frontend will run on: http://localhost:3000

## Testing the Application

1. Open browser to http://localhost:3000
2. Click "Create a new account"
3. Register with:
   - Email: test@example.com
   - Username: testuser
   - Password: Password123!
4. After registration, you'll be redirected to login
5. Login with the credentials you just created
6. You should see the Todo dashboard

## API Endpoints

- Register: POST http://localhost:8001/api/v1/auth/register
- Login: POST http://localhost:8001/api/v1/auth/login
- Get Tasks: GET http://localhost:8001/api/v1/tasks
- Create Task: POST http://localhost:8001/api/v1/tasks

## Troubleshooting

### Backend won't start
- Make sure venv is activated
- Check if port 8001 is already in use
- Verify .env file exists in backend directory

### Frontend can't connect to backend
- Verify backend is running on port 8001
- Check .env.local in frontend has: NEXT_PUBLIC_API_BASE_URL=http://localhost:8001
- Clear browser cache and restart frontend

### Registration fails with 404
- Verify backend is running with correct --port flag
- Check browser console for the exact URL being called
- Should be: http://localhost:8001/api/v1/auth/register (not /api/v1/api/v1/...)
