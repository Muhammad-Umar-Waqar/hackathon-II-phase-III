# Quickstart Guide: Todo CRUD Application

## Prerequisites

- Node.js 18+ installed
- Python 3.11+ installed
- PostgreSQL (or access to Neon Serverless PostgreSQL)
- Git

## Setup Instructions

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Backend Setup
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Configure your database connection and auth settings in .env
# Required environment variables:
# - DATABASE_URL: PostgreSQL connection string
# - JWT_SECRET: Secret key for JWT token generation
# - ACCESS_TOKEN_EXPIRE_MINUTES: Token expiration time (default: 30)
# - ALLOWED_ORIGINS: Comma-separated list of allowed CORS origins

# Initialize database (if needed)
python -c "from src.database import init_db; init_db()"

# Run the backend server
python -m src.main
```

The backend will start on `http://localhost:8000`

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env

# Configure your API endpoint in .env
# NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1

# Start the development server
npm run dev
```

The frontend will start on `http://localhost:3000`

## Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql://username:password@host:port/database
JWT_SECRET=your-super-secret-jwt-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
PORT=8000
```

### Frontend (.env)
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
```

## Running Tests

### Backend Tests
```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test files
pytest tests/unit/test_task_service.py
pytest tests/integration/test_api_endpoints.py
```

### Frontend Tests
```bash
cd frontend

# Run all tests
npm test

# Run tests in watch mode
npm test -- --watch

# Run with coverage
npm test -- --coverage
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get JWT token
- `GET /api/v1/auth/me` - Get current user information

### Tasks
- `GET /api/v1/tasks/` - Get all user's tasks (with pagination)
- `POST /api/v1/tasks/` - Create a new task
- `GET /api/v1/tasks/{id}` - Get specific task
- `PUT /api/v1/tasks/{id}` - Update specific task
- `DELETE /api/v1/tasks/{id}` - Delete specific task

### Rate Limits
- Registration: 5 requests/minute
- Login: 10 requests/minute
- Task creation/updates: 30 requests/minute
- Task retrieval: 60 requests/minute

## Key Features

1. **Authentication**: JWT-based authentication with secure password hashing
2. **Task Management**: Full CRUD operations on user tasks
3. **User Isolation**: Strict enforcement that users can only access their own tasks
4. **Responsive UI**: Mobile-first design that works on all screen sizes
5. **Data Persistence**: Reliable storage with PostgreSQL
6. **Security**: Input validation, SQL injection prevention, rate limiting
7. **Performance**: Connection pooling, database indexes, query optimization
8. **Logging**: Comprehensive logging for debugging and monitoring
9. **Error Handling**: User-friendly error messages and comprehensive error tracking

## Development Commands

### Backend
```bash
# Run development server
python -m src.main

# Run tests
pytest

# Run tests with coverage
pytest --cov=src

# Format code
black src tests

# Lint code
flake8 src tests

# Type checking
mypy src
```

### Frontend
```bash
# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run tests
npm test

# Format code
npm run format

# Lint code
npm run lint
```

## API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Troubleshooting

### Database Connection Issues
- Verify DATABASE_URL is correct
- Ensure PostgreSQL is running
- Check firewall settings

### CORS Errors
- Verify ALLOWED_ORIGINS includes your frontend URL
- Check that frontend is using correct API_BASE_URL

### Authentication Issues
- Ensure JWT_SECRET is set and consistent
- Check token expiration settings
- Verify user credentials are correct

### Performance Issues
- Check database connection pool settings
- Review logs for slow queries
- Monitor rate limit headers

## Security Notes

- Never commit `.env` files to version control
- Use strong JWT_SECRET in production
- Configure ALLOWED_ORIGINS to specific domains in production
- Enable HTTPS in production
- Regularly update dependencies for security patches
- Review logs for suspicious activity

## Production Deployment

Before deploying to production:
1. Set strong JWT_SECRET
2. Configure specific ALLOWED_ORIGINS
3. Use production database
4. Enable HTTPS
5. Set appropriate rate limits
6. Configure logging and monitoring
7. Run security audits
8. Set up automated backups