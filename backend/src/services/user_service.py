from sqlmodel import Session, select
from ..models.user import User, UserCreate
from ..utils.security import SecurityValidator
from passlib.context import CryptContext
from fastapi import HTTPException, status

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    """Service class for user-related operations"""

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash a plain text password (bcrypt has 72 byte limit)"""
        # Truncate password to 72 characters to avoid bcrypt error
        truncated_password = password[:72]
        return pwd_context.hash(truncated_password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a plain text password against its hash"""
        # Truncate password to 72 characters to match hashing
        truncated_password = plain_password[:72]
        return pwd_context.verify(truncated_password, hashed_password)

    @classmethod
    def create_user(cls, db: Session, user: UserCreate) -> User:
        """Create a new user in the database with security validation"""
        # Validate email
        is_valid, error_msg = SecurityValidator.validate_email(user.email)
        if not is_valid:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_msg)

        # Validate username
        is_valid, error_msg = SecurityValidator.validate_username(user.username)
        if not is_valid:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_msg)

        # Validate password
        is_valid, error_msg = SecurityValidator.validate_password(user.password)
        if not is_valid:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_msg)

        # Hash the password
        hashed_password = cls.get_password_hash(user.password)

        # Create user instance
        db_user = User(
            email=user.email.lower().strip(),
            username=user.username.strip(),
            password_hash=hashed_password
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @classmethod
    def get_user_by_email(cls, db: Session, email: str) -> User:
        """Retrieve a user by email"""
        statement = select(User).where(User.email == email.lower().strip())
        return db.exec(statement).first()

    @classmethod
    def get_user_by_username(cls, db: Session, username: str) -> User:
        """Retrieve a user by username"""
        statement = select(User).where(User.username == username.strip())
        return db.exec(statement).first()

    @classmethod
    def get_user_by_id(cls, db: Session, user_id: str) -> User:
        """Retrieve a user by ID (Better Auth uses string IDs)"""
        # For Better Auth compatibility, we query the Better Auth user table
        # This is a simplified version - in production you'd query the actual Better Auth table
        return None  # Disabled for Better Auth - user verification happens via JWT

    @classmethod
    def authenticate_user(cls, db: Session, email: str, password: str) -> User:
        """Authenticate a user by email and password"""
        user = cls.get_user_by_email(db, email)
        if not user or not cls.verify_password(password, user.password_hash):
            return None
        return user

    @classmethod
    def update_user(cls, db: Session, user_id: int, user_update) -> User:
        """Update user information with validation"""
        user = cls.get_user_by_id(db, user_id)
        if not user:
            return None

        if user_update.email:
            is_valid, error_msg = SecurityValidator.validate_email(user_update.email)
            if not is_valid:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_msg)
            user.email = user_update.email.lower().strip()

        if user_update.username:
            is_valid, error_msg = SecurityValidator.validate_username(user_update.username)
            if not is_valid:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_msg)
            user.username = user_update.username.strip()

        db.add(user)
        db.commit()
        db.refresh(user)
        return user
