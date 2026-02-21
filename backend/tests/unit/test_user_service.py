import pytest
from unittest.mock import Mock, MagicMock
from sqlalchemy.orm import Session
from src.services.user_service import UserService
from src.models.user import User, UserCreate, UserUpdate


class TestUserService:
    """Unit tests for UserService"""

    def test_create_user_success(self):
        """Test successful user creation"""
        # Arrange
        mock_db = Mock(spec=Session)
        user_data = UserCreate(
            email="test@example.com",
            username="testuser",
            password="SecurePass123!"
        )

        # Mock the database operations
        mock_db.add = Mock()
        mock_db.commit = Mock()
        mock_db.refresh = Mock()

        # Act
        result = UserService.create_user(mock_db, user_data)

        # Assert
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()
        assert result.email == "test@example.com"
        assert result.username == "testuser"

    def test_get_user_by_id_found(self):
        """Test retrieving an existing user by ID"""
        # Arrange
        mock_db = Mock(spec=Session)
        user_id = 1

        mock_user = User(
            id=user_id,
            email="test@example.com",
            username="testuser",
            password_hash="hashed_password",
            is_active=True
        )

        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value.first.return_value = mock_user

        # Act
        result = UserService.get_user_by_id(mock_db, user_id)

        # Assert
        assert result is not None
        assert result.id == user_id
        assert result.email == "test@example.com"

    def test_get_user_by_id_not_found(self):
        """Test retrieving a non-existent user by ID"""
        # Arrange
        mock_db = Mock(spec=Session)
        user_id = 999

        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value.first.return_value = None

        # Act
        result = UserService.get_user_by_id(mock_db, user_id)

        # Assert
        assert result is None

    def test_get_user_by_email_found(self):
        """Test retrieving an existing user by email"""
        # Arrange
        mock_db = Mock(spec=Session)
        email = "test@example.com"

        mock_user = User(
            id=1,
            email=email,
            username="testuser",
            password_hash="hashed_password",
            is_active=True
        )

        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value.first.return_value = mock_user

        # Act
        result = UserService.get_user_by_email(mock_db, email)

        # Assert
        assert result is not None
        assert result.email == email

    def test_get_user_by_email_not_found(self):
        """Test retrieving a non-existent user by email"""
        # Arrange
        mock_db = Mock(spec=Session)
        email = "nonexistent@example.com"

        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value.first.return_value = None

        # Act
        result = UserService.get_user_by_email(mock_db, email)

        # Assert
        assert result is None

    def test_get_user_by_username_found(self):
        """Test retrieving an existing user by username"""
        # Arrange
        mock_db = Mock(spec=Session)
        username = "testuser"

        mock_user = User(
            id=1,
            email="test@example.com",
            username=username,
            password_hash="hashed_password",
            is_active=True
        )

        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value.first.return_value = mock_user

        # Act
        result = UserService.get_user_by_username(mock_db, username)

        # Assert
        assert result is not None
        assert result.username == username

    def test_get_user_by_username_not_found(self):
        """Test retrieving a non-existent user by username"""
        # Arrange
        mock_db = Mock(spec=Session)
        username = "nonexistent"

        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value.first.return_value = None

        # Act
        result = UserService.get_user_by_username(mock_db, username)

        # Assert
        assert result is None

    def test_authenticate_user_success(self):
        """Test successful user authentication"""
        # Arrange
        mock_db = Mock(spec=Session)
        email = "test@example.com"
        password = "SecurePass123!"

        # Mock user with hashed password
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        hashed_password = pwd_context.hash(password)

        mock_user = User(
            id=1,
            email=email,
            username="testuser",
            password_hash=hashed_password,
            is_active=True
        )

        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value.first.return_value = mock_user

        # Act
        result = UserService.authenticate_user(mock_db, email, password)

        # Assert
        assert result is not None
        assert result.email == email

    def test_authenticate_user_wrong_password(self):
        """Test authentication with wrong password"""
        # Arrange
        mock_db = Mock(spec=Session)
        email = "test@example.com"
        correct_password = "SecurePass123!"
        wrong_password = "WrongPassword"

        # Mock user with hashed password
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        hashed_password = pwd_context.hash(correct_password)

        mock_user = User(
            id=1,
            email=email,
            username="testuser",
            password_hash=hashed_password,
            is_active=True
        )

        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value.first.return_value = mock_user

        # Act
        result = UserService.authenticate_user(mock_db, email, wrong_password)

        # Assert
        assert result is None

    def test_authenticate_user_not_found(self):
        """Test authentication with non-existent user"""
        # Arrange
        mock_db = Mock(spec=Session)
        email = "nonexistent@example.com"
        password = "SecurePass123!"

        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value.first.return_value = None

        # Act
        result = UserService.authenticate_user(mock_db, email, password)

        # Assert
        assert result is None

    def test_update_user_success(self):
        """Test successful user update"""
        # Arrange
        mock_db = Mock(spec=Session)
        user_id = 1

        mock_user = User(
            id=user_id,
            email="old@example.com",
            username="oldusername",
            password_hash="hashed_password",
            is_active=True
        )

        user_update = UserUpdate(
            email="new@example.com",
            username="newusername"
        )

        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value.first.return_value = mock_user
        mock_db.commit = Mock()
        mock_db.refresh = Mock()

        # Act
        result = UserService.update_user(mock_db, user_id, user_update)

        # Assert
        assert result is not None
        assert result.email == "new@example.com"
        assert result.username == "newusername"
        mock_db.commit.assert_called_once()

    def test_update_user_not_found(self):
        """Test updating a non-existent user"""
        # Arrange
        mock_db = Mock(spec=Session)
        user_id = 999
        user_update = UserUpdate(email="new@example.com")

        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value.first.return_value = None

        # Act
        result = UserService.update_user(mock_db, user_id, user_update)

        # Assert
        assert result is None
