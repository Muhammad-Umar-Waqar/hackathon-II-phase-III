from sqlmodel import SQLModel, Field, Column
from sqlalchemy import JSON
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid


class Message(SQLModel, table=True):
    """SQLModel for Message entity"""
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
