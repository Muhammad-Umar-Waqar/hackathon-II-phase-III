# Data Model: AI Chat Agent & Conversation System

**Feature**: 1-ai-chat-agent
**Date**: 2026-02-22
**Status**: Complete

## Entity Definitions

### Conversation

**Purpose**: Represents a chat session between a user and the AI agent.

**Attributes**:
- `id` (UUID, Primary Key): Unique identifier for the conversation
- `user_id` (String, Foreign Key, Indexed): References the user who owns this conversation (from Phase-II auth)
- `created_at` (DateTime, Indexed): Timestamp when conversation was created
- `updated_at` (DateTime): Timestamp when conversation was last updated

**Relationships**:
- One-to-Many with Message: A conversation contains multiple messages
- Many-to-One with User: A conversation belongs to one user

**Validation Rules**:
- `user_id` MUST be a valid user ID from the authentication system
- `created_at` MUST be set on creation and immutable
- `updated_at` MUST be updated whenever a new message is added

**State Transitions**: None (conversations are always active; deletion/archival deferred to future)

**Indexes**:
- Primary index on `id`
- Index on `user_id` for fast lookup of user's conversations
- Index on `created_at` for chronological sorting

**SQLModel Definition**:
```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(index=True)  # References Better Auth user
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ConversationCreate(SQLModel):
    """Schema for creating a new conversation"""
    # user_id will be extracted from JWT, not provided by client
    pass

class ConversationResponse(SQLModel):
    """Schema for conversation response"""
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
```

---

### Message

**Purpose**: Represents a single message within a conversation (from user, assistant, or system).

**Attributes**:
- `id` (UUID, Primary Key): Unique identifier for the message
- `conversation_id` (UUID, Foreign Key, Indexed): References the conversation this message belongs to
- `user_id` (String, Indexed): User who owns the conversation (denormalized for security checks)
- `role` (String, Enum): Message role - one of: "user", "assistant", "system"
- `content` (Text): Message content (user input or agent response)
- `tool_calls` (JSON, Optional): Structured tool call suggestions from agent (if role=assistant)
- `created_at` (DateTime, Indexed): Timestamp when message was created

**Relationships**:
- Many-to-One with Conversation: A message belongs to one conversation
- Many-to-One with User: A message belongs to one user (via conversation)

**Validation Rules**:
- `conversation_id` MUST reference an existing conversation
- `user_id` MUST match the conversation's user_id
- `role` MUST be one of: "user", "assistant", "system"
- `content` MUST NOT be empty
- `tool_calls` MUST be valid JSON if present (validated against MCP schema)
- `created_at` MUST be set on creation and immutable

**Role Definitions**:
- **user**: Message from the end user
- **assistant**: Response from the AI agent
- **system**: System-generated messages (e.g., "Conversation started")

**Tool Calls Structure** (JSON):
```json
[
  {
    "tool": "add_task",
    "parameters": {
      "title": "Buy groceries",
      "description": "Milk, eggs, bread"
    },
    "requires_confirmation": false
  }
]
```

**Indexes**:
- Primary index on `id`
- Composite index on `(conversation_id, created_at)` for fast chronological retrieval
- Index on `user_id` for security checks

**SQLModel Definition**:
```python
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import JSON
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid

class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    conversation_id: str = Field(index=True)
    user_id: str = Field(index=True)  # Denormalized for security
    role: str = Field(index=True)  # "user", "assistant", "system"
    content: str = Field(max_length=10000)
    tool_calls: Optional[List[Dict[str, Any]]] = Field(default=None, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)

class MessageCreate(SQLModel):
    """Schema for creating a new message"""
    conversation_id: Optional[str] = None  # Optional for first message
    content: str

class MessageResponse(SQLModel):
    """Schema for message response"""
    id: str
    conversation_id: str
    user_id: str
    role: str
    content: str
    tool_calls: Optional[List[Dict[str, Any]]]
    created_at: datetime
```

---

## Entity Relationships

```
User (Phase-II)
  │
  └─── has many ───> Conversation
                        │
                        └─── has many ───> Message
```

**Cardinality**:
- User : Conversation = 1 : N (one user has many conversations)
- Conversation : Message = 1 : N (one conversation has many messages)

**Referential Integrity**:
- Messages MUST reference a valid conversation
- Conversations MUST reference a valid user
- Deleting a conversation SHOULD cascade delete all messages (future implementation)

---

## Database Migration

**Migration Script** (Alembic):

```python
"""Add conversation and message tables

Revision ID: 001_add_chat_tables
Revises: <previous_migration>
Create Date: 2026-02-22
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSON

def upgrade():
    # Create conversations table
    op.create_table(
        'conversations',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_conversations_user_id', 'conversations', ['user_id'])
    op.create_index('ix_conversations_created_at', 'conversations', ['created_at'])

    # Create messages table
    op.create_table(
        'messages',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('conversation_id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('tool_calls', JSON, nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'])
    )
    op.create_index('ix_messages_conversation_id_created_at', 'messages', ['conversation_id', 'created_at'])
    op.create_index('ix_messages_user_id', 'messages', ['user_id'])
    op.create_index('ix_messages_role', 'messages', ['role'])

def downgrade():
    op.drop_table('messages')
    op.drop_table('conversations')
```

---

## Data Access Patterns

### 1. Create New Conversation
```python
# User sends first message
conversation = Conversation(user_id=user_id)
db.add(conversation)
db.commit()
```

### 2. Add Message to Conversation
```python
# User or agent adds message
message = Message(
    conversation_id=conversation_id,
    user_id=user_id,
    role="user",  # or "assistant"
    content=message_content
)
db.add(message)
db.commit()
```

### 3. Load Conversation History
```python
# Rebuild context for agent
messages = db.query(Message)\
    .filter(Message.conversation_id == conversation_id)\
    .order_by(Message.created_at.asc())\
    .limit(100)\
    .all()
```

### 4. Get User's Conversations
```python
# List all conversations for a user
conversations = db.query(Conversation)\
    .filter(Conversation.user_id == user_id)\
    .order_by(Conversation.updated_at.desc())\
    .all()
```

### 5. Verify Conversation Ownership
```python
# Security check before loading conversation
conversation = db.query(Conversation)\
    .filter(Conversation.id == conversation_id)\
    .filter(Conversation.user_id == user_id)\
    .first()

if not conversation:
    raise HTTPException(status_code=404, detail="Conversation not found")
```

---

## Performance Considerations

### Query Optimization
- **Conversation lookup**: Index on `user_id` enables fast filtering
- **Message retrieval**: Composite index on `(conversation_id, created_at)` enables fast chronological ordering
- **Security checks**: Index on `user_id` in messages table for fast ownership validation

### Scalability
- **Conversation history limit**: 100 messages per conversation (MVP) to prevent large queries
- **Pagination**: Deferred to future (not needed for MVP with 100 message limit)
- **Archival**: Old conversations can be archived to separate table (future optimization)

### Storage Estimates
- Average message size: ~200 bytes (text content)
- 100 messages per conversation: ~20 KB
- 1000 conversations per user: ~20 MB per user
- 10,000 users: ~200 GB total (manageable for Neon PostgreSQL)

---

## Security Considerations

### User Isolation
- All queries MUST filter by `user_id` to prevent cross-user data access
- Conversation ownership validated before loading messages
- JWT token provides authenticated `user_id`

### Data Validation
- Message content sanitized before storage (prevent XSS)
- Tool calls validated against MCP schemas
- Role field restricted to enum values

### Audit Trail
- All messages persisted with timestamps
- Tool calls logged for debugging and compliance
- User actions traceable via conversation history

---

## Future Enhancements

1. **Conversation Metadata**: Add title, tags, archived status
2. **Message Reactions**: Allow users to rate agent responses
3. **Conversation Sharing**: Enable sharing conversations with other users
4. **Message Editing**: Allow users to edit their messages
5. **Conversation Search**: Full-text search across message content
6. **Pagination**: Load conversation history in chunks for large conversations
