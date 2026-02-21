from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    """SQLModel for User entity (Legacy - Better Auth is now used)"""
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)
    password_hash: str
    password_reset_token: Optional[str] = None
    password_reset_expires: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)

    # Note: Relationship removed - tasks now reference Better Auth user table

class UserCreate(SQLModel):
    """Schema for creating a new User"""
    email: str
    username: str
    password: str

class UserUpdate(SQLModel):
    """Schema for updating a User"""
    email: Optional[str] = None
    username: Optional[str] = None

class UserResponse(SQLModel):
    """Schema for User response (excludes sensitive data)"""
    id: int
    email: str
    username: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
