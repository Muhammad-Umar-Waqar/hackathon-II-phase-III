from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from slowapi import Limiter
from slowapi.util import get_remote_address
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from ..database import get_db
from ..models.user import UserCreate, UserResponse
from ..services.user_service import UserService
from ..utils.logger import logger, log_error, log_request, log_security_event

load_dotenv()

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET", "your-super-secret-jwt-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

router = APIRouter()
security = HTTPBearer()
limiter = Limiter(key_func=get_remote_address)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a new access token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    """
    Verify and decode a JWT token from Better Auth
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")  # Better Auth uses string IDs
        if user_id is None:
            log_security_event("Invalid token - missing user_id")
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        return user_id  # Return as string
    except JWTError as e:
        log_security_event("JWT verification failed", {"error": str(e)})
        raise HTTPException(status_code=401, detail="Could not validate credentials")

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
def register(request: Request, user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user
    """
    try:
        log_request("POST", "/auth/register")
        logger.info(f"Registration attempt for email: {user.email}")

        # Check if user already exists
        existing_user = UserService.get_user_by_email(db, user.email)
        if existing_user:
            log_security_event("Registration failed - email already exists", {"email": user.email})
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )

        existing_username = UserService.get_user_by_username(db, user.username)
        if existing_username:
            log_security_event("Registration failed - username already taken", {"username": user.username})
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already taken"
            )

        # Create new user
        db_user = UserService.create_user(db, user)
        logger.info(f"User registered successfully: user_id={db_user.id}, email={user.email}")
        return db_user
    except HTTPException:
        raise
    except Exception as e:
        log_error(e, "register")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to register user"
        )

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
@limiter.limit("10/minute")
def login(request: Request, login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT token
    """
    try:
        log_request("POST", "/auth/login")
        logger.info(f"Login attempt for email: {login_data.email}")

        user = UserService.authenticate_user(db, login_data.email, login_data.password)
        logger.info(f"Authentication result: {user is not None}")

        if not user:
            log_security_event("Failed login attempt", {"email": login_data.email})
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        logger.info(f"Creating access token for user_id={user.id}")
        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )
        logger.info(f"Access token created successfully")

        logger.info(f"User logged in successfully: user_id={user.id}, email={login_data.email}")
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user.id,
            "username": user.username
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login exception: {type(e).__name__}: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        log_error(e, "login")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to authenticate user"
        )

@router.get("/me", response_model=UserResponse)
@limiter.limit("60/minute")
def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Get current authenticated user
    """
    try:
        user_id = verify_token(credentials.credentials)
        log_request("GET", "/auth/me", user_id)

        user = UserService.get_user_by_id(db, user_id)
        if not user:
            logger.warning(f"User not found: user_id={user_id}")
            raise HTTPException(status_code=404, detail="User not found")

        logger.info(f"Retrieved current user: user_id={user_id}")
        return user
    except HTTPException:
        raise
    except Exception as e:
        log_error(e, "get_current_user")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user information"
        )