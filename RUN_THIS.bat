@echo off
echo ========================================
echo BETTER AUTH SETUP - FINAL TEST
echo ========================================
echo.
echo This script will:
echo 1. Kill any running servers
echo 2. Start backend on port 8001
echo 3. Start frontend on port 3000
echo 4. Test registration
echo.
echo Press Ctrl+C to cancel, or
pause

echo.
echo Killing existing processes...
taskkill /F /IM node.exe 2>nul
taskkill /F /IM python.exe 2>nul

echo.
echo Starting backend...
cd backend
start "Backend" cmd /k "venv\Scripts\activate && uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload"

echo Waiting for backend to start...
timeout /t 5 /nobreak

echo.
echo Starting frontend...
cd ..\frontend
start "Frontend" cmd /k "npm run dev"

echo Waiting for frontend to start...
timeout /t 15 /nobreak

echo.
echo Testing registration...
curl -X POST http://localhost:3000/api/auth/sign-up/email -H "Content-Type: application/json" -d "{\"email\":\"test@example.com\",\"password\":\"Password123!\",\"name\":\"Test User\"}"

echo.
echo.
echo ========================================
echo Check the Backend and Frontend windows for any errors
echo Then try registering at: http://localhost:3000/register
echo ========================================
pause
