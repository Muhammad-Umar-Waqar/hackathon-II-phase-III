from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Optional
from slowapi import Limiter
from slowapi.util import get_remote_address
from jose import JWTError, jwt
import os
from dotenv import load_dotenv

from ..database import get_db
from ..models.task import TaskCreate, TaskUpdate, TaskResponse
from ..models.user import UserResponse
from ..services.task_service import TaskService
from ..services.user_service import UserService
from ..utils.logger import logger, log_error, log_request

load_dotenv()

# JWT Configuration (same as auth_router)
SECRET_KEY = os.getenv("JWT_SECRET", "your-super-secret-jwt-key-change-in-production")
ALGORITHM = "HS256"

router = APIRouter()
security = HTTPBearer()
limiter = Limiter(key_func=get_remote_address)

def verify_token(token: str) -> str:
    """
    Verify and decode a JWT token
    Returns user_id as string
    """
    try:
        logger.info(f"Verifying token: {token[:20]}...")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        logger.info(f"Token decoded successfully, user_id: {user_id}")
        if user_id is None:
            logger.error("Token payload missing 'sub' field")
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        return user_id
    except JWTError as e:
        logger.error(f"JWT verification failed: {str(e)}")
        raise HTTPException(status_code=401, detail="Could not validate credentials")

@router.get("/", response_model=List[TaskResponse])
@limiter.limit("60/minute")
def get_tasks(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Get all tasks for the authenticated user (JWT)
    """
    try:
        logger.info(f"GET /tasks - Headers: {dict(request.headers)}")
        logger.info(f"GET /tasks - Credentials: {credentials}")

        user_id = verify_token(credentials.credentials)
        log_request("GET", "/tasks", user_id)

        tasks = TaskService.get_tasks_for_user(db, user_id, skip=skip, limit=limit)
        logger.info(f"Retrieved {len(tasks)} tasks for user_id={user_id}")
        return tasks
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_tasks: {str(e)}")
        log_error(e, "get_tasks")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve tasks"
        )

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("30/minute")
def create_task(
    request: Request,
    task: TaskCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Create a new task for the authenticated user (JWT)
    """
    try:
        user_id = verify_token(credentials.credentials)
        log_request("POST", "/tasks", user_id)

        # Validate status field
        if task.status not in ["pending", "in-progress", "completed"]:
            logger.warning(f"Invalid status provided: {task.status}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Status must be one of: pending, in-progress, completed"
            )

        created_task = TaskService.create_task(db, task, user_id)
        logger.info(f"Task created: task_id={created_task.id}, user_id={user_id}")
        return created_task
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Validation error in create_task: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        log_error(e, "create_task")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create task"
        )

@router.get("/{task_id}", response_model=TaskResponse)
@limiter.limit("60/minute")
def get_task(
    request: Request,
    task_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Get a specific task by ID for the authenticated user (JWT)
    """
    try:
        user_id = verify_token(credentials.credentials)
        log_request("GET", f"/tasks/{task_id}", user_id)

        task = TaskService.get_task_by_id(db, task_id, user_id)
        if not task:
            logger.warning(f"Task not found or unauthorized: task_id={task_id}, user_id={user_id}")
            raise HTTPException(status_code=404, detail="Task not found")

        logger.info(f"Retrieved task: task_id={task_id}, user_id={user_id}")
        return task
    except HTTPException:
        raise
    except Exception as e:
        log_error(e, "get_task")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve task"
        )

@router.put("/{task_id}", response_model=TaskResponse)
@limiter.limit("30/minute")
def update_task(
    request: Request,
    task_id: int,
    task_update: TaskUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Update a specific task for the authenticated user (JWT)
    """
    try:
        user_id = verify_token(credentials.credentials)
        log_request("PUT", f"/tasks/{task_id}", user_id)

        # Validate status field if provided
        if task_update.status and task_update.status not in ["pending", "in-progress", "completed"]:
            logger.warning(f"Invalid status provided: {task_update.status}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Status must be one of: pending, in-progress, completed"
            )

        updated_task = TaskService.update_task(db, task_id, task_update, user_id)
        if not updated_task:
            logger.warning(f"Task not found or unauthorized: task_id={task_id}, user_id={user_id}")
            raise HTTPException(status_code=404, detail="Task not found")

        logger.info(f"Task updated: task_id={task_id}, user_id={user_id}")
        return updated_task
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Validation error in update_task: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        log_error(e, "update_task")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update task"
        )

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("30/minute")
def delete_task(
    request: Request,
    task_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Delete a specific task for the authenticated user (JWT)
    """
    try:
        user_id = verify_token(credentials.credentials)
        log_request("DELETE", f"/tasks/{task_id}", user_id)

        success = TaskService.delete_task(db, task_id, user_id)
        if not success:
            logger.warning(f"Task not found or unauthorized: task_id={task_id}, user_id={user_id}")
            raise HTTPException(status_code=404, detail="Task not found")

        logger.info(f"Task deleted: task_id={task_id}, user_id={user_id}")
        return {"message": "Task deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        log_error(e, "delete_task")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete task"
        )