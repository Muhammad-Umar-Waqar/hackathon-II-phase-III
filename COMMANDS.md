# Quick Command Reference

## Start Application

### Backend
```bash
cd backend
.\venv\Scripts\activate
uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload
```

### Frontend
```bash
cd frontend
npm run dev
```

## Run Migrations

### Frontend (Better Auth tables)
```bash
cd frontend
python run-migration.py
```

### Backend (Convert user_id to TEXT)
```bash
cd backend
python run-migration.py
```

## Test URLs

- Frontend: http://localhost:3000
- Backend: http://localhost:8001
- API Docs: http://localhost:8001/docs

## Database Queries

```sql
-- Check Better Auth users
SELECT id, email, name FROM "user";

-- Check tasks
SELECT id, title, user_id, status FROM tasks;

-- Verify user_id type
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'tasks' AND column_name = 'user_id';
```

## Troubleshooting

### Reset Everything
```bash
# Delete all users
DELETE FROM "user";

# Delete all tasks
DELETE FROM tasks;
```

### Check Logs
- Backend: Check terminal where uvicorn is running
- Frontend: Check browser console (F12)

### Restart Services
```bash
# Stop with Ctrl+C, then restart
cd backend && uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload
cd frontend && npm run dev
```
