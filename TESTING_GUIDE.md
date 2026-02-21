# Complete Testing Guide

## Prerequisites
- Backend running on http://localhost:8001
- Frontend running on http://localhost:3000
- Database connection configured in backend/.env

## Step 1: Start Backend

```bash
cd backend
.\venv\Scripts\activate
uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## Step 2: Test Backend API (Optional but Recommended)

Open a new terminal:
```bash
cd backend
python test_api.py
```

**Expected output:**
```
=== Testing Registration ===
Status Code: 201
Response: {
  "id": 1,
  "email": "test@example.com",
  "username": "testuser"
}

=== Testing Login ===
Status Code: 200
Response: {
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user_id": 1,
  "username": "testuser"
}

✅ All tests passed!
```

## Step 3: Start Frontend

Open a new terminal:
```bash
cd frontend
npm run dev
```

**Expected output:**
```
- ready started server on 0.0.0.0:3000, url: http://localhost:3000
- event compiled client and server successfully
```

## Step 4: End-to-End Testing

### Test 1: User Registration
1. Open browser: http://localhost:3000
2. You should be redirected to http://localhost:3000/login
3. Click "create a new account"
4. Fill in the form:
   - Email: `yourname@example.com`
   - Username: `yourname`
   - Password: `Password123!` (min 8 characters)
5. Click "Create Account"
6. **Expected:** Success message appears, redirects to login after 2 seconds

**If you see 404 error:**
- Check backend is running on port 8001
- Check browser console for the exact URL
- Should be: `http://localhost:8001/api/v1/auth/register`
- NOT: `http://localhost:8001/api/v1/api/v1/auth/register`

### Test 2: User Login
1. On login page, enter:
   - Email: `yourname@example.com`
   - Password: `Password123!`
2. Click "Sign in"
3. **Expected:** Redirects to home page with Todo dashboard

### Test 3: Create Task
1. On home page, fill in "Create New Task" form:
   - Title: `Buy groceries`
   - Description: `Milk, eggs, bread`
   - Status: `Pending`
   - Due Date: (select tomorrow's date)
2. Click "Create Task"
3. **Expected:** Task appears in "Pending Tasks" section

### Test 4: View Tasks
1. Check the stats at the top:
   - Pending: should show 1
   - In Progress: should show 0
   - Completed: should show 0
2. **Expected:** Your task appears with all details

### Test 5: Update Task Status
1. Find your task in the Pending section
2. Click the status dropdown
3. Change to "In Progress"
4. **Expected:** Task moves to "In Progress" section, stats update

### Test 6: Complete Task
1. Find your task in "In Progress" section
2. Change status to "Completed"
3. **Expected:** Task moves to "Completed Tasks" section

### Test 7: Edit Task
1. Find any task
2. Click "Edit" button
3. Change the title or description
4. Click "Save"
5. **Expected:** Task updates with new information

### Test 8: Delete Task
1. Find any task
2. Click "Delete" button
3. Confirm deletion
4. **Expected:** Task disappears from list, stats update

### Test 9: Logout and Login Again
1. Click "Logout" button in header
2. **Expected:** Redirects to login page
3. Login again with same credentials
4. **Expected:** All your tasks are still there

## Common Issues and Solutions

### Issue: "POST http://localhost:8001/api/v1/api/v1/auth/register 404"
**Solution:**
- Stop frontend (Ctrl+C)
- Delete `frontend/.next` folder
- Restart frontend: `npm run dev`
- Clear browser cache (Ctrl+Shift+Delete)

### Issue: Backend shows "Address already in use"
**Solution:**
- Port 8001 is already taken
- Find and kill the process: `netstat -ano | findstr :8001`
- Or use a different port: `uvicorn src.main:app --host 0.0.0.0 --port 8002 --reload`
- Update frontend/.env.local: `NEXT_PUBLIC_API_BASE_URL=http://localhost:8002`

### Issue: "Could not validate credentials" when accessing tasks
**Solution:**
- Token expired or invalid
- Logout and login again
- Check browser localStorage has `access_token`

### Issue: Tasks not loading
**Solution:**
- Open browser DevTools (F12) → Network tab
- Check the API calls
- Look for errors in Console tab
- Verify backend logs for errors

### Issue: CORS errors
**Solution:**
- Check backend/.env has: `ALLOWED_ORIGINS=http://localhost:3000`
- Restart backend after changing .env

## Verification Checklist

- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] Can register new user
- [ ] Can login with registered user
- [ ] Can create new task
- [ ] Can view all tasks
- [ ] Can update task status
- [ ] Can edit task details
- [ ] Can delete task
- [ ] Stats update correctly
- [ ] Can logout and login again
- [ ] Tasks persist after logout/login

## Success Criteria

All checkboxes above should be checked. If any fail, review the error messages and check the troubleshooting section.
