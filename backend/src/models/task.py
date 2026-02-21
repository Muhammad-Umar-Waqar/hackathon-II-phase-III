from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

class Task(SQLModel, table=True):
    """SQLModel for Task entity"""
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: str = Field(default="pending", index=True)  # pending, in-progress, completed
    user_id: str = Field(index=True)  # Changed to str to match Better Auth
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    due_date: Optional[datetime] = Field(default=None, index=True)

class TaskCreate(SQLModel):
    """Schema for creating a new Task"""
    title: str
    description: Optional[str] = None
    status: str = "pending"
    due_date: Optional[datetime] = None

class TaskUpdate(SQLModel):
    """Schema for updating a Task"""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[datetime] = None

class TaskResponse(SQLModel):
    """Schema for Task response"""
    id: int
    title: str
    description: Optional[str]
    status: str
    user_id: str  # Changed to str
    created_at: datetime
    updated_at: datetime
    due_date: Optional[datetime]
