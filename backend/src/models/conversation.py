from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid


class Conversation(SQLModel, table=True):
    """SQLModel for Conversation entity"""
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
