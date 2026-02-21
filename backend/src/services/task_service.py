from sqlmodel import Session, select
from ..models.task import Task, TaskCreate, TaskUpdate
from typing import List, Optional

class TaskService:
    """Service class for task-related operations"""

    @classmethod
    def create_task(cls, db: Session, task: TaskCreate, user_id: str) -> Task:
        """Create a new task for a specific user"""
        db_task = Task(**task.model_dump(), user_id=user_id)
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task

    @classmethod
    def get_task_by_id(cls, db: Session, task_id: int, user_id: str) -> Task:
        """Retrieve a specific task by ID for a specific user"""
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        return db.exec(statement).first()

    @classmethod
    def get_tasks_for_user(cls, db: Session, user_id: str, skip: int = 0, limit: int = 100) -> List[Task]:
        """Retrieve all tasks for a specific user with pagination"""
        statement = select(Task).where(Task.user_id == user_id).offset(skip).limit(limit)
        return db.exec(statement).all()

    @classmethod
    def update_task(cls, db: Session, task_id: int, task_update: TaskUpdate, user_id: str) -> Optional[Task]:
        """Update a specific task for a specific user"""
        db_task = cls.get_task_by_id(db, task_id, user_id)
        if not db_task:
            return None

        update_data = task_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_task, field, value)

        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task

    @classmethod
    def delete_task(cls, db: Session, task_id: int, user_id: str) -> bool:
        """Delete a specific task for a specific user"""
        db_task = cls.get_task_by_id(db, task_id, user_id)
        if not db_task:
            return False

        db.delete(db_task)
        db.commit()
        return True

    @classmethod
    def get_tasks_by_status(cls, db: Session, user_id: str, status: str) -> List[Task]:
        """Retrieve tasks for a user filtered by status"""
        statement = select(Task).where(Task.user_id == user_id, Task.status == status)
        return db.exec(statement).all()
