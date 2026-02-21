# Todo CRUD Application

A full-stack web application for managing personal todo tasks with user authentication and responsive design.

## Features

- **User Authentication**: Secure registration and login with JWT tokens
- **Task Management**: Create, read, update, and delete personal tasks
- **User Isolation**: Users can only access their own tasks
- **Responsive Design**: Works on mobile, tablet, and desktop devices
- **Modern Tech Stack**: Next.js frontend with FastAPI backend

## Tech Stack

- **Frontend**: Next.js, React, Tailwind CSS
- **Backend**: FastAPI, Python
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: JWT-based with custom implementation
- **Styling**: Tailwind CSS with responsive utilities

## Prerequisites

- Node.js 18+
- Python 3.11+
- PostgreSQL (or access to Neon Serverless PostgreSQL)

## Setup Instructions

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Configure your database connection and auth settings in .env
python -m src.main  # Run the backend server
```

### 3. Frontend Setup
```bash
cd frontend
npm install
cp .env.example .env
# Configure your API endpoint in .env
npm run dev  # Start the development server
```

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://username:password@host:port/database
JWT_SECRET=your-super-secret-jwt-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend (.env)
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
```

## API Endpoints

- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get JWT token
- `GET /api/v1/tasks` - Get all user's tasks
- `POST /api/v1/tasks` - Create a new task
- `GET /api/v1/tasks/{id}` - Get specific task
- `PUT /api/v1/tasks/{id}` - Update specific task
- `DELETE /api/v1/tasks/{id}` - Delete specific task

## Running Tests

### Backend Tests
```bash
cd backend
pytest  # Run all backend tests
```

### Frontend Tests
```bash
cd frontend
npm test  # Run all frontend tests
```

## Development Commands

### Backend
```bash
# Run development server
python -m src.main

# Run tests
pytest

# Format code
black .

# Lint code
flake8
```

### Frontend
```bash
# Run development server
npm run dev

# Build for production
npm run build

# Run tests
npm test

# Format code
npm run format

# Lint code
npm run lint
```

## Architecture

The application follows a modular architecture:

```
backend/
├── src/
│   ├── models/          # Data models
│   ├── services/        # Business logic
│   ├── api/            # API routes
│   ├── middleware/     # Authentication and other middleware
│   └── main.py         # Application entry point
└── tests/              # Test files

frontend/
├── src/
│   ├── components/     # Reusable UI components
│   ├── pages/         # Page components
│   ├── services/      # API clients and utility services
│   └── contexts/      # React context providers
├── public/            # Static assets
└── tests/             # Frontend tests
```

## Security Features

- JWT-based authentication with secure token handling
- User isolation - users can only access their own tasks
- Input validation and sanitization
- Secure password hashing
- Protection against common web vulnerabilities

## Responsive Design Features

- Mobile-first approach with progressive enhancement
- Media queries for different screen sizes
- Touch-friendly controls and adequate spacing
- Accessibility features including ARIA attributes
- Support for reduced motion and high contrast modes