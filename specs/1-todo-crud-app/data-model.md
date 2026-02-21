# Data Model: Todo CRUD Application

## User Entity

**Description**: Represents a registered user of the system with authentication credentials and identity information.

**Fields**:
- id: Unique identifier for the user (UUID/string)
- email: User's email address (string, required, unique)
- username: User's chosen username (string, required, unique)
- password_hash: Hashed password for authentication (string, required)
- created_at: Timestamp when the user account was created (datetime)
- updated_at: Timestamp when the user account was last updated (datetime)
- is_active: Boolean indicating if the account is active (boolean, default: true)

**Validation Rules**:
- Email must be valid email format
- Username must be 3-30 characters alphanumeric with underscores/hyphens
- Password must meet security requirements (length, complexity)
- Email and username must be unique across all users

**Relationships**:
- One-to-many relationship with Task entity (one user can have many tasks)

## Task Entity

**Description**: Represents a todo item with properties like title, description, status, creation date, and association with a specific user.

**Fields**:
- id: Unique identifier for the task (UUID/string)
- title: Title of the task (string, required, max 200 characters)
- description: Detailed description of the task (string, optional, max 1000 characters)
- status: Current status of the task (string/enumeration, required, values: 'pending', 'in-progress', 'completed')
- user_id: Foreign key linking to the owning user (reference to User.id, required)
- created_at: Timestamp when the task was created (datetime)
- updated_at: Timestamp when the task was last updated (datetime)
- due_date: Optional deadline for the task (datetime, optional)

**Validation Rules**:
- Title must be 1-200 characters
- Description must be 0-1000 characters if provided
- Status must be one of the allowed values
- User_id must reference an existing user
- Due date must be in the future if provided

**State Transitions**:
- 'pending' → 'in-progress': When user starts working on the task
- 'in-progress' → 'completed': When user marks task as done
- 'completed' → 'pending': When user reopens the task (optional functionality)

**Relationships**:
- Many-to-one relationship with User entity (many tasks belong to one user)