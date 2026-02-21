@echo off
echo ========================================
echo BETTER AUTH - FINAL FIX TEST
echo ========================================
echo.
echo This will test the registration fix.
echo Make sure both servers are running:
echo   Backend: uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload
echo   Frontend: npm run dev
echo.
pause

echo.
echo Testing registration...
curl -X POST http://localhost:3000/api/auth/sign-up/email ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"test@example.com\",\"password\":\"Password123!\",\"name\":\"Test User\"}"

echo.
echo.
echo ========================================
echo If you see user data above, it worked!
echo If you see an error, check the Frontend terminal for details.
echo ========================================
pause
