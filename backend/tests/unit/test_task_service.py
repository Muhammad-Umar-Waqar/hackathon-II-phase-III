import pytest
from unittest.mock import Mock, MagicMock
from sqlalchemy.orm import Session
from src.services.task_service import TaskService
from src.models.task import Task, TaskCreate, TaskUpdate


class TestTaskService:
    """Unit tests for TaskService"""

    def test_create_task_success(self):
        """Test successful task creation"""
        # Arrange
        mock_db = Mock(spec=Session)
        task_data = TaskCreate(
            title="Test Task",
            description="Test Description",
            status="pending"
        )
        user_id = 1

        # Mock the database operations
        mock_db.add = Mock()
        mock_db.commit = Mock()
        mock_db.refresh = Mock()

        # Act
        result = TaskService.create_task(mock_db, task_data, user_id)

        # Assert
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()
        assert result.title == "Test Task"
        assert result.user_id == user_id

    def test_create_task_integrity_error(self):
        """Test task creation with integrity constraint violation"""
        # Arrange
        from sqlalchemy.exc import IntegrityError
        mock_db = Mock(spec=Session)
        task_data = TaskCreate(
            title="Test Task",
            description="Test Description",
            status="pending"
        )
        user_id = 1

        # Mock database to raise IntegrityError
        mock_db.add = Mock()
        mock_db.commit = Mock(side_effect=IntegrityError("", "", ""))
        mock_db.rollback = Mock()

        # Act & Assert
        with pytest.raises(ValueError, match="Failed to create task"):
            TaskService.create_task(mock_db, task_data, user_id)

        mock_db.rollback.assert_called_once()

    def test_get_task_by_id_found(self):
        """Test retrieving an existing task"""
        # Arrange
        mock_db = Mock(spec=Session)
        task_id = 1
        user_id = 1

        mock_task = Task(
            id=task_id,
            title="Test Task",
            description="Test Description",
            status="pending",
            user_id=user_id
        )

        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value.first.return_value = mock_task

        # Act
        result = TaskService.get_task_by_id(mock_db, task_id, user_id)

        # Assert
        assert result is not None
        assert result.id == task_id
        assert result.user_id == user_id

    def test_get_task_by_id_not_found(self):
        """Test retrieving a non-existent task"""
        # Arrange
        mock_db = Mock(spec=Session)
        task_id = 999
        user_id = 1

        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value.first.return_value = None

        # Act
        result = TaskService.get_task_by_id(mock_db, task_id, user_id)

        # Assert
        assert result is None

    def test_get_tasks_for_user(self):
        """Test retrieving all tasks for a user"""
        # Arrange
        mock_db = Mock(spec=Session)
        user_id = 1

        mock_tasks = [
            Task(id=1, title="Task 1", status="pending", user_id=user_id),
            Task(id=2, title="Task 2", status="completed", user_id=user_id)
        ]

        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value.offset.return_value.limit.return_value.all.return_value = mock_tasks

        # Act
        result = TaskService.get_tasks_for_user(mock_db, user_id)

        # Assert
        assert len(result) == 2
        assert all(task.user_id == user_id for task in result)

    def test_update_task_success(self):
        """Test successful task update"""
        # Arrange
        mock_db = Mock(spec=Session)
        task_id = 1
        user_id = 1

        mock_task = Task(
            id=task_id,
            title="Old Title",
            description="Old Description",
            status="pending",
            user_id=user_id
        )

        task_update = TaskUpdate(
            title="New Title",
            status="completed"
        )

        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value.first.return_value = mock_task
        mock_db.commit = Mock()
        mock_db.refresh = Mock()

        # Act
        result = TaskService.update_task(mock_db, task_id, task_update, user_id)

        # Assert
        assert result is not None
        assert result.title == "New Title"
        assert result.status == "completed"
        mock_db.commit.assert_called_once()

    def test_update_task_not_found(self):
        """Test updating a non-existent task"""
        # Arrange
        mock_db = Mock(spec=Session)
        task_id = 999
        user_id = 1
        task_update = TaskUpdate(title="New Title")

        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value.first.return_value = None

        # Act
        result = TaskService.update_task(mock_db, task_id, task_update, user_id)

        # Assert
        assert result is None

    def test_delete_task_success(self):
        """Test successful task deletion"""
        # Arrange
        mock_db = Mock(spec=Session)
        task_id = 1
        user_id = 1

        mock_task = Task(
            id=task_id,
            title="Test Task",
            status="pending",
            user_id=user_id
        )

        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value.first.return_value = mock_task
        mock_db.delete = Mock()
        mock_db.commit = Mock()

        # Act
        result = TaskService.delete_task(mock_db, task_id, user_id)

        # Assert
        assert result is True
        mock_db.delete.assert_called_once_with(mock_task)
        mock_db.commit.assert_called_once()

    def test_delete_task_not_found(self):
        """Test deleting a non-existent task"""
        # Arrange
        mock_db = Mock(spec=Session)
        task_id = 999
        user_id = 1

        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value.first.return_value = None

        # Act
        result = TaskService.delete_task(mock_db, task_id, user_id)

        # Assert
        assert result is False

    def test_get_tasks_by_status(self):
        """Test retrieving tasks filtered by status"""
        # Arrange
        mock_db = Mock(spec=Session)
        user_id = 1
        status = "completed"

        mock_tasks = [
            Task(id=1, title="Task 1", status="completed", user_id=user_id),
            Task(id=2, title="Task 2", status="completed", user_id=user_id)
        ]

        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value.all.return_value = mock_tasks

        # Act
        result = TaskService.get_tasks_by_status(mock_db, user_id, status)

        # Assert
        assert len(result) == 2
        assert all(task.status == status for task in result)
