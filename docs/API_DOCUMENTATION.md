# API Documentation - Todo CRUD Application

## Base URL
All API endpoints are prefixed with `/api/v1`

## Authentication
Most endpoints require authentication using JWT tokens. Include the token in the Authorization header:
```
Authorization: Bearer <token>
```

## Endpoints

### Authentication

#### POST /api/v1/auth/register
Register a new user

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "username",
  "password": "secure_password"
}
```

**Response:**
```json
{
  "id": "user_id",
  "email": "user@example.com",
  "username": "username",
  "created_at": "2023-01-01T00:00:00Z"
}
```

#### POST /api/v1/auth/login
Login and get JWT token

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "secure_password"
}
```

**Response:**
```json
{
  "access_token": "jwt_token_here",
  "token_type": "bearer",
  "user": {
    "id": "user_id",
    "email": "user@example.com",
    "username": "username"
  }
}
```

### Tasks

#### GET /api/v1/tasks
Get all tasks for the authenticated user

**Response:**
```json
[
  {
    "id": "task_id",
    "title": "Task title",
    "description": "Task description",
    "status": "pending|in-progress|completed",
    "user_id": "user_id",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z",
    "due_date": "2023-01-10T00:00:00Z"
  }
]
```

#### POST /api/v1/tasks
Create a new task

**Request Body:**
```json
{
  "title": "Task title",
  "description": "Task description",
  "status": "pending",
  "due_date": "2023-01-10T00:00:00Z"
}
```

**Response:**
```json
{
  "id": "task_id",
  "title": "Task title",
  "description": "Task description",
  "status": "pending",
  "user_id": "user_id",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z",
  "due_date": "2023-01-10T00:00:00Z"
}
```

#### GET /api/v1/tasks/{id}
Get a specific task

**Response:**
```json
{
  "id": "task_id",
  "title": "Task title",
  "description": "Task description",
  "status": "pending",
  "user_id": "user_id",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z",
  "due_date": "2023-01-10T00:00:00Z"
}
```

#### PUT /api/v1/tasks/{id}
Update a specific task

**Request Body:**
```json
{
  "title": "Updated task title",
  "description": "Updated task description",
  "status": "in-progress",
  "due_date": "2023-01-15T00:00:00Z"
}
```

**Response:**
```json
{
  "id": "task_id",
  "title": "Updated task title",
  "description": "Updated task description",
  "status": "in-progress",
  "user_id": "user_id",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-02T00:00:00Z",
  "due_date": "2023-01-15T00:00:00Z"
}
```

#### DELETE /api/v1/tasks/{id}
Delete a specific task

**Response:**
Status: 204 No Content

## Error Responses
All error responses follow this format:
```json
{
  "detail": "Error message describing the issue"
}
```

## Common Status Codes
- 200: Success
- 201: Created
- 204: No Content
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 422: Validation Error
- 500: Internal Server Error